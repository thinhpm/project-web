from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time


def generate_cookie(string_cookie):
    if string_cookie == '':
        return {}

    string_cookie = string_cookie.replace(" ", "")
    arr = string_cookie.split(";")
    results = []

    for i in range(len(arr)):
        result = {}
        key, value = arr[i].split("=")

        result["name"] = key
        result["value"] = value

        results.append(result)

    return results


def first():
    cookie = "lzd_cid=6452f4c1-f8b6-4aa7-9760-c4010c2a8048; t_uid=6452f4c1-f8b6-4aa7-9760-c4010c2a8048; hng=VN|en|VND|704; userLanguageML=en; t_fv=1574331551287; isg=BAIC8Q6f6wZJF_fXGCsU68FXUAFu0wTi4byE6EwbUHUun6MZNGEa_GOXS0NG1H6F; l=dBSiKJ67qW39j4ZEBOCwCZZzUC_OMIObYuWbadjMi_5a818hXWbOkd4wdeJ6cOWcG-YB40FhhAytoFGQ8zlli9vJUWN6INrDBef..; cna=nVVdFphZL20CAYu0w1l2JPTi; _bl_uid=w6k7v39n83nkLRcmIytLa637yXvC; _ga=GA1.2.1597665392.1574331570; cto_lwid=a0fc21db-7f3c-4bdb-9ddd-e3423b65d248; cto_idcpy=ebe1ee59-95b1-4de7-87d2-63976b3cec65; Hm_lvt_7cd4710f721b473263eed1f0840391b4=1574386982,1574674477; _gid=GA1.2.815261684.1574665055; _tb_token_=fe9e5337bde85; Hm_lpvt_7cd4710f721b473263eed1f0840391b4=1574674477; _m_h5_tk=3a01bb8b4802b4a5ef331f513725c02a_1574683309814; _m_h5_tk_enc=ce61177892bd8a9453ed8718aad9e66c; t_sid=oMRfzwrWNFAZekR5cs2lJEbudOvGWJCr; utm_channel=NA; _fbp=fb.1.1574331570385.1181107822"
    cookies = generate_cookie(cookie)

    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/google-chrome-unstable"
    # options.add_argument("headless")
    options.add_argument("--no-sandbox")
    options.add_argument('window-size=1400x600')
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")

    driver = webdriver.Chrome(chrome_options=options)


    driver.get("https://www.lazada.vn/products/nuoc-hoa-co-dac-xbeauty-xpo3-cho-nam-nu-30ml-co-10-mui-nuoc-hoa-thom-lau-ca-ngay-dung-dich-nuoc-hoa-nhap-khau-tu-phap-i287718050-s527708690.html?spm=a2o4n.home.flashSale.3.1905e182UEqVt9&search=1&mp=1&c=fs&clickTrackInfo=%7B%22rs%22%3A%220.8656760072480152%22%2C%22prior_score%22%3A%220%22%2C%22submission_discount%22%3A%2278%25%22%2C%22rmc%22%3A%2292%22%2C%22type%22%3A%22entrance%22%2C%22prior_type%22%3A%22%22%2C%22isw%22%3A%220.3%22%2C%22userid%22%3A%22%22%2C%22sca%22%3A%2270%22%2C%22hourtonow%22%3A%224%22%2C%22abid%22%3A%22142638%22%2C%22itemid%22%3A%22287718050_1_leaf_0.5035999999999999_0.8656760072480152%22%2C%22pvid%22%3A%2200a2c3f9-4117-40e0-a319-0ad3edcbc39c%22%2C%22pos%22%3A%221%22%2C%22ccw%22%3A%220.1%22%2C%22rms%22%3A%221.0%22%2C%22c2i%22%3A%221.0%22%2C%22scm%22%3A%221007.17760.142638.%22%2C%22rmw%22%3A%220.06666820991226649%22%2C%22isrw%22%3A%220.1%22%2C%22rkw%22%3A%220.4%22%2C%22ss%22%3A%220.5035999999999999%22%2C%22ms%22%3A%220.5035999999999999%22%2C%22itr%22%3A%220.8133333333333334%22%2C%22mt%22%3A%22leaf%22%2C%22its%22%3A%22375%22%2C%22promotion_price%22%3A%2299000%22%2C%22anonid%22%3A%226452f4c1-f8b6-4aa7-9760-c4010c2a8048%22%2C%22ppw%22%3A%220.0%22%2C%22isc%22%3A%22305%22%2C%22iss2%22%3A%220.7529148800080513%22%2C%22iss1%22%3A%220.1525%22%2C%22config%22%3A%22%22%7D&scm=1007.17760.142638.0")
    for cookie in cookies:
        driver.add_cookie(cookie)


    print(driver.title)
    # driver.implicitly_wait(2000)
    # driver.get_screenshot_as_file('main-page.png')
    # driver.quit()

    time.sleep(50)

if __name__=="__main__":
    first()