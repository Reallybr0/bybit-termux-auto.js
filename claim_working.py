#!/usr/bin/env python3
import json, time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

COOKIE_FILE = "bybit_cookies.json"
URL = "https://www.bybit.com/en/task-center/my_rewards"
GECKO = "/data/data/com.termux/files/usr/bin/geckodriver"

def start_driver():
    opt = webdriver.FirefoxOptions()
    opt.add_argument("--headless")
    opt.set_preference("security.sandbox.content.level", 0)
    opt.binary_location = "/data/data/com.termux/files/usr/bin/firefox"
    return webdriver.Firefox(service=Service(GECKO), options=opt)

def main():
    driver = start_driver()
    driver.get(URL)
    with open(COOKIE_FILE) as f:
        for c in json.load(f):
            try:
                driver.add_cookie(c)
            except: pass
    driver.refresh()
    time.sleep(5)
    
    # Try Claim All
    try:
        btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Claim All')]")
        btn.click()
        print("✅ Claim All clicked!")
    except:
        print("❌ No Claim All button")
    
    # Try each claim button
    for btn in driver.find_elements(By.XPATH, "//button[contains(text(), 'Claim')]"):
        btn.click()
        print("🎁 Claimed one reward")
        time.sleep(1)
    
    time.sleep(2)
    driver.quit()

if __name__ == "__main__":
    main()
