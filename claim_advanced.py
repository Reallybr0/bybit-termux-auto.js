#!/usr/bin/env python3
import json
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===== CONFIG =====
GECKO = "/data/data/com.termux/files/usr/bin/geckodriver"
COOKIE_FILE = "bybit_cookies.json"
URL = "https://www.bybit.com/en/task-center/my_rewards"
# =================

def create_driver():
    opt = webdriver.FirefoxOptions()
    opt.add_argument("--headless")
    opt.set_preference("security.sandbox.content.level", 0)
    opt.set_preference("browser.tabs.remote.autostart", False)
    opt.binary_location = "/data/data/com.termux/files/usr/bin/firefox"
    return webdriver.Firefox(service=Service(GECKO), options=opt)

def load_cookies(driver):
    try:
        with open(COOKIE_FILE) as f:
            cookies = json.load(f)
        # remove duplicate names
        unique = {c['name']: c for c in cookies}
        for c in unique.values():
            driver.add_cookie(c)
        print(f"✅ Loaded {len(unique)} cookies")
        return True
    except Exception as e:
        print(f"❌ Cookie error: {e}")
        return False

def click_with_retry(driver, xpath, description):
    try:
        btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        btn.click()
        print(f"✅ {description} clicked!")
        return True
    except Exception as e:
        print(f"❌ {description} not found or not clickable: {e}")
        return False

def main():
    driver = create_driver()
    print("🌐 Loading My Rewards page...")
    driver.get(URL)

    if not load_cookies(driver):
        driver.quit()
        return

    driver.refresh()
    print("🔄 Page refreshed. Waiting for content...")
    time.sleep(5)  # allow JavaScript to render

    # ----- 1. Check for "Pending collection" first -----
    pending_xpath = "//*[contains(text(), 'Pending collection')]"
    pending_elements = driver.find_elements(By.XPATH, pending_xpath)
    if pending_elements:
        print("🔍 'Pending collection' found.")
        # Try to find the parent button
        try:
            btn = pending_elements[0].find_element(By.XPATH, "./ancestor::button")
            btn.click()
            print("🎉 Claimed via Pending collection!")
        except:
            pending_elements[0].click()
            print("🎉 Clicked on Pending collection element directly.")
        time.sleep(2)
        driver.quit()
        return

    # ----- 2. Look for "Claim All" button -----
    if click_with_retry(driver, "//button[contains(text(), 'Claim All')]", "Claim All"):
        time.sleep(2)
        driver.quit()
        return

    # ----- 3. Look for individual "Claim" buttons -----
    claim_btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'Claim')]")
    if claim_btns:
        print(f"🔍 Found {len(claim_btns)} individual Claim buttons.")
        for i, btn in enumerate(claim_btns):
            try:
                btn.click()
                print(f"🎁 Claimed reward {i+1}")
                time.sleep(1)
            except:
                print(f"⚠️ Could not click reward {i+1}")
        driver.quit()
        return

    # ----- 4. Nothing found -----
    print("❌ No claimable rewards at this moment.")
    print("   - Maybe you already claimed everything.")
    print("   - Or cookies expired (re-export from PC browser).")
    print("   - Or page structure changed (need to update selectors).")

    # Optional: save screenshot for debugging
    driver.save_screenshot("debug_my_rewards.png")
    print("📸 Saved screenshot as debug_my_rewards.png")
    driver.quit()

if __name__ == "__main__":
    main()
