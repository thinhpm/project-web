from selenium.webdriver import Firefox
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import requests
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Browser:
    def __init__(self):
        self.driver = None


class FirefoxBrowser(Browser):
    def __init__(self, profile=""):
        super().__init__()
        self.profile = profile
        self.init_driver()

    def init_driver(self):
        options = Options()
        # options.add_argument("--headless")
        # profile = "C:\\Users\\noname\\Documents\\file\\firefox-profile\\j7nj8gnr.user1"

        self.driver = Firefox(executable_path="C:\\Users\\noname\\Documents\\file\\geckodriver.exe", firefox_options=options)

    def get_driver(self):
        return self.driver

    def stop(self):
        self.driver.close()
        self.driver.quit()


def un_verify(driver):
    time.sleep(1)
    driver.execute_script("document.getElementById('nc_2_n1z').style.left='500px'")
    time.sleep(2)
    action = ActionChains(driver)
    source_element = driver.find_element_by_id('nc_2_n1z')
    source_element2 = driver.find_element_by_id('nc_2__scale_text')
    action.drag_and_drop(source_element, source_element2)
    action.perform()
    time.sleep(1)


import requests

ff = FirefoxBrowser()
driver = ff.get_driver()
url = "https://www.lazada.vn/glorystar-official-store"
url2 = "https://www.lazada.vn/glorystar-official-store/?ajax=true&from=wangpu&langFlag=vi&page=2&pageTypeId=2&q=All-Products"
driver.get(url)
cookies = driver.get_cookies()

req = requests.Session()

for cookie in cookies:
    if len(cookie) == 0:
        continue

    req.cookies.set(cookie['name'], cookie['value'])
    req.cookies.set('domain', cookie['domain'])


import time
from selenium.webdriver.common.action_chains import ActionChains



for i in range(10000):
    time.sleep(1)
    content = req.get(url2)
    html = content.text
    if 'nc_2_n1z' in html or 'rgv587_flag' in html or '/verify/' in html:
        print(html)

        un_verify(driver)

        cookies = driver.get_cookies()

        req = requests.Session()

        for cookie in cookies:
            if len(cookie) == 0:
                continue

            req.cookies.set(cookie['name'], cookie['value'])
            req.cookies.set('domain', cookie['domain'])
        time.sleep(2)

    print(html)
