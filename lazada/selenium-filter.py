from selenium.webdriver import Firefox
import time
import requests
import json

class Browser:
    def __init__(self):
        self.driver = None


class FirefoxBrowser(Browser):
    def __init__(self):
        super().__init__()
        self.init_driver()

    def init_driver(self):
        self.driver = Firefox(executable_path="C:\\Users\\noname\\Documents\\file\\geckodriver.exe")

    def get_driver(self):
        return self.driver

    def stop(self):
        self.driver.close()
        self.driver.quit()


class Lazada:
    def __init__(self, driver):
        self.driver = driver

    def test(self):
        url = "https://www.lazada.vn/glorystar-official-store/"
        self.driver.get(url)
        cookies = self.driver.get_cookies()
        print(cookies)
        # for i in range(10):
        #     url = "https://www.lazada.vn/glorystar-official-store/?ajax=true&from=wangpu&langFlag=vi&page=2&pageTypeId=2&q=All-Products"
        #     # data = my_request(url)
        #     self.driver.get(url)
        #     print(self.driver.page_source)
        #     # print(data)
        #     time.sleep(1)



def my_request(url):
    req = requests.get(url)

    content = req.content
    return json.loads(content)


if __name__ == "__main__":
    browser = FirefoxBrowser()
    driver = browser.get_driver()
    lazada = Lazada(driver)
    lazada.test()
    time.sleep(40)
    driver.close()
    driver.quit()