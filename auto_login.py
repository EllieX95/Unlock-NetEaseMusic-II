# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "000BEB56A821F462657164315228A61C9BDC79499C9BBD13958E2B7E11A890B6F986FA44474FBBA45349759354F7B15AEB75FEA9DD242513D3AFB7934FA453063139DA9E6EC3E3E6EBE20725845C8A6496BA85797BFC66906CE6E217273CE47947E3AF2F170D9C09DEB54F32E4BDEB482EB85C144256D9E105EA3FFDB63EDA8A0BB4FC27EED9EC3C40551A597FF0D4C3D7B2D292177EC397DE398DDB26F8AE704ABABA2E8FA53B92A9A16B10F536A19E19F5B076BB5C1858639CC024AA675BF29203B6D854561B318926029EDE4265B3763AD17E68EC3CC691332C41C9FCE05960918126D9775A729FA6BDE81E9CCDD63D2524B4473B4C9D36D1507CABB1C5BDB1225BDA185851772535D97756DF8C16CA5E002B57A8A05A0CE6896F92B87C98E75D97A1AC3DC2BEBD97471B937C73B2804F5BAA2690DEC6D71B28BA6C5781073ADEE1A40805E3314851A031A4AC30900FBDF8D939BD69F56A3EF0BE7F946FE272"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
