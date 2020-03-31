import os
import requests
import time
import json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup as bs
from pprint import pprint as pp
from tqdm import tqdm
from multiprocessing import Pool
from dotenv import load_dotenv
load_dotenv()

# Create ~/.env file with this parameters
NDB_URL = os.environ.get("NDB_URL")
API_URL = os.environ.get("API_URL")
API_TOKEN = os.environ.get("API_TOKEN")
DRIVER_PATH = os.path.join(os.getcwd(), "driver", "chromedriver.exe")


def search_movies():
    driver = webdriver.Chrome(DRIVER_PATH)
    driver.get(NDB_URL)
    SCROLL_PAUSE_TIME = 0.5
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            time.sleep(5)
            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
        last_height = new_height
    print('Finished Scrolling')

    titles = []
    for t in tqdm(driver.find_elements_by_css_selector(
            ".videodiv >div:nth-child(4) > b:nth-child(1)")):
        titles.append(t.find_elements_by_tag_name(
            'span')[0].get_attribute('innerHTML'))
    driver.close()

    for title in tqdm(titles):
        body = {
            "title": title,
            "countries": "BR"
        }
        resp = requests.post(f"{ API_URL}/movie/", data=json.dumps(body),
                             headers={"Authorization": API_TOKEN, "Content-Type": "application/json"})


if __name__ == "__main__":
    search_movies()
