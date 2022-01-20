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
from utils import strip_name
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
    sleep(random.randint(2,4))

def split(list_a, chunk_size):
  for i in range(0, len(list_a), chunk_size):
    yield list_a[i:i + chunk_size]

root = tk.Tk()
root.withdraw()


TEMPLATE_TXT_FILE = filedialog.askopenfilename(title="Select a template script file", filetypes = [("Text files", "*.txt")])
TXT_FILE = filedialog.askopenfilename(title="Select a script for image file", filetypes = [("Text files", "*.txt")])
TEMPLATE_IMAGE_FILE = filedialog.askopenfilename(title="Select a template Image", filetypes = [("JPG files", "*.jpg"),
                                                                            ("PNG files", "*.png"),
                                                                            ("JPEG files", "*.jpeg")])
IMAGE_FILE = filedialog.askopenfilename(title="Select a Image for only image blasting", filetypes = [("JPG files", "*.jpg"),
                                                                            ("PNG files", "*.png"),
                                                                            ("JPEG files", "*.jpeg")])
DATA_FILE = filedialog.askopenfilename(title="Select a data", filetypes = [("Excel files", "*.xlsx"),
                                                                            ("CSV files", "*.csv")])

if DATA_FILE.endswith(".xlsx"):
    df = pd.read_excel(DATA_FILE)
else:
    df = pd.read_csv(DATA_FILE)


XPATH_BUTTON_SEND = "/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div"
XPATH_TEXT = '/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'


with open(TEMPLATE_TXT_FILE, "r", encoding='utf-8') as f:
    template_text = f.read()

with open(TXT_FILE, "r", encoding='utf-8') as f:
    image_text = f.read()

if platform == "win32":
    IMAGE_FILE = IMAGE_FILE.replace("/", "\\")
    TEMPLATE_IMAGE_FILE = TEMPLATE_IMAGE_FILE.replace("/", "\\")
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

index_data = 0
list_df = df.to_dict(orient="records")
list_df = list(split(list_df, 50))
df["is_success"] = False

for list_data in list_df:
    # initialize first launch
    if platform == "win32":
        driver = webdriver.Firefox(executable_path=GECKO_FILE, options=options)
    else:
        driver = webdriver.Firefox(options=options)
    driver.get(f"http://web.whatsapp.com/send?phone=628128154050")
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "_2Nr6U")))
    except TimeoutException:
        driver.get(f"http://web.whatsapp.com/send?phone=628128154050")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "_2Nr6U")))
    for data in list_data:
        try:
            driver.get(f"http://web.whatsapp.com/send?phone={data.get('phone', '')}")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, XPATH_TEXT)))
            # name = strip_name(data.get("name", ""))
            # Check wether send only image or full campaign
            if pd.isnull(data.get("only_image")):
                # Write message
                text = template_text.format(**data)
            else:  
                text = image_text.format(**data)   
            for line in text.split('\n'):
                ActionChains(driver).send_keys(line).perform()
                ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
            delay()
            driver.find_element('css selector', "span[data-icon='clip']").click()
            if pd.isnull(data.get("only_image")):
                driver.find_element('css selector', "input[type='file']").send_keys(TEMPLATE_IMAGE_FILE)
            else:
                driver.find_element('css selector', "input[type='file']").send_keys(IMAGE_FILE)
            delay()
            driver.find_element('xpath', XPATH_BUTTON_SEND).click()
            df.loc[index_data,"is_success"] = True
            sleep(random.randint(7,10))
        except Exception as e:
            if isinstance(e, TimeoutException):
                df.loc[index_data,"is_success"] = "WA not valid"
            print(e)
        index_data += 1
    df.to_csv("result.csv", index=False)
    driver.close()