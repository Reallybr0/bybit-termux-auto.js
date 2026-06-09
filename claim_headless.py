#!/usr/bin/env python3
import json, time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

GECKODRIVER_PATH = "/data/data/com.termux/files/usr/bin/geckodriver"
COOKIE_FILE = "bybit_cookies.json"
REWARDS_URL = "https://www.bybit.com/rewards-hub"

def create_driver():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.set_preference("security.sandbox.content.level", 0)
    options.set_preference("browser.tabs.remote.autostart", False)
    options.binary_location = "/data/data/com.termux/files/usr/bin/firefox"
    return webdriver.Firefox(service=Service(GECKODRIVER_PATH), options=options)

def load_cookies(driver):
    with open(COOKIE_FILE) as f:
        cookies = json.load(f)
    for c in cookies:
        driver.add_cookie(c)
    print(f"✅ Loaded {len(cookies)} cookies")

def click_claim(driver):
    selectors = [
        (By.XPATH, "//button[contains(text(), 'Claim')]"),
        (By.XPATH, "//*[contains(text(), 'Claim Reward')]"),
        (By.XPATH, "//*[contains(@id, 'claim') or contains(@class, 'claim')]")
    ]
    for by_type, sel in selectors:
        try:
            btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by_type, sel)))
            btn.click()
            print("🎉 Claim button clicked!")
            return True
        except:
            continue
    print("❌ No claim button found")
    return False

def main():
    driver = create_driver()
    driver.get(REWARDS_URL)
    load_cookies(driver)
    driver.refresh()
    time.sleep(5)
    click_claim(driver)
    time.sleep(3)
    driver.quit()

if __name__ == "__main__":
    main()
