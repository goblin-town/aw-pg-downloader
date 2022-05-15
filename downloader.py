import os
from os.path import exists
import pickle
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import NoSuchElementException
import logging
import enlighten

PROFILE_NUMBER = input("AW Profile Number: ")
PROFILE_URL = f"https://www.adultwork.com/ViewProfile.asp?UserID={PROFILE_NUMBER}"
PRIVATE_GALLERY_URL = f"https://www.adultwork.com/XXXGallery.asp?UserID={PROFILE_NUMBER}"

# Xpaths
PROFILE_NAME = "/html/body/table/tbody/tr/td/div[2]/center/table[1]/tbody/tr/td/table/tbody/tr[1]/td[1]/span"
LOGINOUT_SELECTOR = "/html/body/div[1]/div[3]/ul/li[2]/a"
ADULT_WARNING_SELECTOR = "/html/body/div[5]/div/div/div/center/table/tbody/tr[6]/td[1]/a"
PRIVATE_GALLERY_BUTTON = "/html/body/div[4]/div/ul/li[3]/a"
FIRST_IMAGE = "/html/body/table/tbody/tr/td/div/center/table/tbody/tr[2]/td/div/div/center/form/table/tbody/tr[2]/td[1]/table/tbody/tr[1]/td/table/tbody/tr/td/a/img"
FULL_SIZE = "/html/body/form/table[1]/tbody/tr/td[2]/nobr/input[1]"
PIC_TITLE = "/html/body/form/p[1]/b"
PIC_TOTAL = "/html/body/table/tbody/tr/td/div/center/table/tbody/tr[2]/td/div/div/center/form/table/tbody/tr[1]/td/table/tbody/tr/td[2]"
LARGE_PIC_TOTAL = "/html/body/table/tbody/tr/td/div[2]/center/table[2]/tbody/tr[2]/td/div[2]/center/form/div/center/table/tbody/tr[2]/td/div[1]/table/tbody/tr[1]/td"

logging.basicConfig(level=logging.INFO)
file_exists = exists('cookies.pkl')
driver = webdriver.Firefox()
if (file_exists):
    logging.info("cookie file found")
    cookies = pickle.load(open("cookies.pkl", "rb"))
    driver.get("https://www.adultwork.com/Home.asp")
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://www.adultwork.com/Home.asp")
if (len(driver.find_elements(By.XPATH, LOGINOUT_SELECTOR)) == 0 or driver.find_element(By.XPATH, LOGINOUT_SELECTOR).text != "Logout"):
    logging.info("cookies have expired or do not exist, please login")
    driver.get("https://www.adultwork.com/Login.asp")
    adult_warning = WebDriverWait(driver, 120).until(
        EC.element_to_be_clickable((By.XPATH, ADULT_WARNING_SELECTOR))
    )
    adult_warning.click()
    try:
        element = WebDriverWait(driver, 120).until(
            EC.text_to_be_present_in_element((By.XPATH, LOGINOUT_SELECTOR), "Logout")
        )
    finally:
        logging.info("login successful")
        pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
        driver.quit()
else:
    logging.info("login successful")
    driver.quit()

cookies = pickle.load(open("cookies.pkl", "rb"))
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get("https://www.adultwork.com/Home.asp")
for cookie in cookies:
    driver.add_cookie(cookie)



driver.get(PROFILE_URL)
profile_name = driver.find_element(By.XPATH, PROFILE_NAME).text
driver.get(PRIVATE_GALLERY_URL)
num_pics = driver.find_element(By.XPATH, PIC_TOTAL).text.split(" pictures")[0]
main_window = driver.current_window_handle
if(len(driver.find_elements(By.XPATH, FIRST_IMAGE)) == 0):
    logging.info("private gallery images not found. Is your subscription expired?")
    driver.quit()
    exit()

driver.find_element(By.XPATH, FIRST_IMAGE).click()
for handle in driver.window_handles: 
    if handle != main_window: 
        popup = handle
        driver.switch_to.window(popup)

folder_name = f'downloads/{profile_name}'
if (os.path.isdir(folder_name) == False):
    logging.info(f"creating new folder {folder_name}")
    os.mkdir(folder_name)

manager = enlighten.get_manager()
pbar = manager.counter(total=int(num_pics), desc='Progress', unit='pics')

full_size = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, FULL_SIZE)))
full_size.click()
while True == True:
    file_name = "".join([c for c in driver.find_element(By.XPATH, PIC_TITLE).text if re.match(r'\w', c)])
    if (exists(f"{folder_name}/{file_name}.png") == True):
        logging.info(f'Already exists {folder_name}/{file_name}.png')
        pbar.update()
        driver.find_element(By.NAME, 'btnNext').click()
        continue
    with open(f"{folder_name}/{file_name}.png", 'wb') as file:
        logging.info(f"Writing {folder_name}/{file_name}.png")
        file.write(driver.find_element(By.NAME, 'TheImage').screenshot_as_png)
        pbar.update()
    if(len(driver.find_elements(By.NAME, 'btnNext')) == 0):
        break
    driver.find_element(By.NAME, 'btnNext').click()
manager.stop()
print()
driver.quit()
