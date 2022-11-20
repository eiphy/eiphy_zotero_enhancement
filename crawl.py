import time

import pandas as pd
import requests
import selenium.webdriver.support.ui as ui
import yaml
from bs4 import BeautifulSoup
from naapc import NDict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def main():
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    with open("configs/cvpr.yaml", "r") as f:
        configs = NDict(yaml.safe_load(f))

    with webdriver.Edge(
        options=options, service=EdgeService(EdgeChromiumDriverManager(path=".").install())
    ) as driver:
        wait = WebDriverWait(driver, 10)
        driver.get(configs["configs;y2022;url;main"])

        # search
        driver.find_element(By.XPATH, "//form/input[@name='query']").send_keys("talking face")
        driver.find_element(By.XPATH, "//form/input[@type='submit']").click()

        for i in tqdm(range(len(driver.find_elements(By.CLASS_NAME, "ptitle")))):
            paper = driver.find_elements(By.CLASS_NAME, "ptitle")[i]
            paper.find_element(By.TAG_NAME, "a").click()
            title = driver.find_element(By.ID, "papertitle").text
            abstract = driver.find_element(By.ID, "abstract").text
            # print(title)
            # print(abstract)
            path = f"tmp/{title}.pdf"
            # print(path)
            pdf_url = driver.find_element(By.XPATH, "//*[text()='pdf']").get_attribute("href")
            r = requests.get(pdf_url, stream=True)
            with open(path, "wb") as f:
                f.write(r.content)
            driver.back()

        content = driver.page_source
        print(content)


if __name__ == "__main__":
    main()
