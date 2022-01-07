import pandas as pd
from selenium import webdriver
import pandas as pd
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import random
from time import sleep
from sys import platform
import tkinter as tk
from tkinter import filedialog
import os
import argparse

if platform == "win32":
    parser = argparse.ArgumentParser(description='User Folder to open Firefox Profile')

    parser.add_argument('--user', dest='user', type=str, help='Name of folder user that store Firefox Profile')
    args = parser.parse_args()
    USER = args.user
else:
    import pwd
    def get_username():
        return pwd.getpwuid(os.getuid())[0]
    USER = get_username()

def delay():
    sleep(random.randint(3,5))

root = tk.Tk()
root.withdraw()


TXT_FILE = filedialog.askopenfilename(title="Select a text file", filetypes = [("Text files", "*.txt")])
IMAGE_FILE = filedialog.askopenfilename(title="Select a Image", filetypes = [("JPG files", "*.jpg"),
                                                                            ("PNG files", "*.png"),
                                                                            ("JPEG files", "*.jpeg")])
DATA_FILE = filedialog.askopenfilename(title="Select a data", filetypes = [("Excel files", "*.xlsx"),
                                                                            ("CSV files", "*.csv")])

if DATA_FILE.endswith(".xlsx"):
    data = pd.read_excel(DATA_FILE)
else:
    data = pd.read_csv(DATA_FILE)
phones = data.phone.values
names = data.name.values


XPATH_BUTTON_SEND = '/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span'
XPATH_TEXT = '/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'


with open(TXT_FILE, "r") as f:
    text = f.read()

if platform == "win32":
    PROFILES_PATH = f'C:\\Users\\{USER}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\'
else:
    PROFILES_PATH = f'/Users/{USER}/Library/Application Support/Firefox/Profiles/'

profile = [x for x in os.listdir(PROFILES_PATH) if "default-release" in x]
fp = os.path.join(PROFILES_PATH, profile[0])

options=Options()

options.add_argument("-profile")
options.add_argument(fp)

if platform == "win32":
    GECKO_FILE = filedialog.askopenfilename(title="Select geckodriver", filetypes = [("Geckodriver files", "*.exe")])
    driver = webdriver.Firefox(executable_path=GECKO_FILE, options=options)
else:
    driver = webdriver.Firefox(options=options)



# initialize first launch
driver.get(f"http://web.whatsapp.com/send?phone=628128154050")
try:
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "_2Nr6U")))
except TimeoutException:
    driver.get(f"http://web.whatsapp.com/send?phone=628128154050")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "_2Nr6U")))

for phone, name in zip(phones, names):
    driver.get(f"http://web.whatsapp.com/send?phone={phone}")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, XPATH_TEXT)))

    # Write message
    for line in text.split('\n'):
        ActionChains(driver).send_keys(line).perform()
        ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()

    driver.find_element('css selector', "span[data-icon='clip']").click()
    driver.find_element('css selector',"input[type='file']").send_keys(IMAGE_FILE)
    delay()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, XPATH_BUTTON_SEND)))
    element.click()
    sleep(random.randint(7,10))