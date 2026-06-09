#!/usr/bin/env python3
import json
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===== CONFIGURATION =====
# Geckodriver path (this is correct)
GECKODRIVER_PATH = "/data/data/com.termux/files/usr/bin/geckodriver"
# Cookie file
COOKIE_FILE = "bybit_cookies.json"
# Rewards page URL
REWARDS_URL = "https://www.bybit.com/en/task-center/my_rewards"
# Firefox binary path (fix: remove quotes inside? No, keep as string)
FIREFOX_BINARY = "/data/data/com.termux/files/usr/bin/firefox"
# ========================

def create_driver():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.set_preference("security.sandbox.content.level", 0)
    options.set_preference("browser.tabs.remote.autostart", False)
    
    # IMPORTANT: Set binary location correctly
    options.binary_location = FIREFOX_BINARY
    
    service = Service(executable_path=GECKODRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=options)
    return driver

def load_cookies(driver):
    try:
        with open(COOKIE_FILE) as f:
            cookies = json.load(f)
        unique = {c['name']: c for c in cookies}
        for c in unique.values():
            # Remove 'domain' if it causes issues? No, keep as is
            driver.add_cookie(c)
        print(f"✅ Loaded {len(unique)} cookies")
        return True
    except Exception as e:
        print(f"❌ Cookie error: {e}")
        return False

def claim_rewards(driver):
    # Step 1: Look for "Pending collection"
    try:
        pending = driver.find_elements(By.XPATH, "//*[contains(text(), 'Pending collection')]")
        if pending:
            print("✅ 'Pending collection' found")
            # Find clickable button
            btn = pending[0].find_element(By.XPATH, "./ancestor::button")
            btn.click()
            print("🎉 Claimed via Pending collection")
            return True
    except:
        pass
    
    # Step 2: Look for standard "Claim" button
    print("Looking for 'Claim' button...")
    selectors = [
        "//button[contains(text(), 'Claim')]",
        "//span[contains(text(), 'Claim')]/parent::button",
        "//button[contains(@class, 'claim')]",
        "//*[@data-testid='claim-button']"
    ]
    
    for xp in selectors:
        try:
            btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xp)))
            btn.click()
            print(f"🎉 Claimed via '{xp}'")
            return True
        except:
            continue
    
    print("❌ No claim buttons found")
    return False

def main():
    print("🚀 Starting...")
    driver = create_driver()
    print("🌐 Loading page...")
    driver.get(REWARDS_URL)
    
    if not load_cookies(driver):
        driver.quit()
        return
    
    driver.refresh()
    print("🔄 Waiting for page to load...")
    time.sleep(5)
    
    claim_rewards(driver)
    
    print("✅ Done. Closing browser...")
    time.sleep(2)
    driver.quit()

if __name__ == "__main__":
    main()
