from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
import datetime
import pymysql.cursors

PERCENTDISCOUNT = 80
NUMPAGE = 999


def webDriver(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x20200')
    driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe', chrome_options=options)
    driver.get(url)
    # driver.implicitly_wait(60)

    html = driver.page_source
    driver.close()
    driver.quit()

    return html


def getDiscout(url):
    r = requests.get(url)

    if (r.status_code == 200):
        content = r.text
        soup = BeautifulSoup(content, 'lxml')
        classDiscout = soup.find(class_="pdp-product-price__discount")

        if (classDiscout != None):
            stringDiscout = classDiscout.string
            disCount = stringDiscout.replace('%', '').replace('-', '')

            return int(disCount)

    return 0


def hanldeDatabase(item, nameCategory, connection, sql, isUpdate):
    index = item.find('"')
    idProduct = item[:index]
    originalPrice = getValueOf(item, 'originalPrice').replace('.00', '')
    price = getValueOf(item, 'price').replace('.00', '')
    disCount = getValueOf(item, 'discount').replace('-', '').replace('%', '')

    if (isUpdate):
        with connection.cursor() as cursor:
            cursor.execute(sql, (originalPrice, price, disCount, idProduct))
            connection.commit()

            return

    nameProduct = getValueOf(item, 'name')
    linkProduct = 'https:' + getValueOf(item, 'productUrl')
    imageProduct = getValueOf(item, 'image')

    with connection.cursor() as cursor:
        # Create a new record
        cursor.execute(sql, (
            idProduct, nameProduct, linkProduct, imageProduct, originalPrice, price, disCount, nameCategory))

    connection.commit()


def hanleCategory(arrProducts, main_url, nameCategory, connection, sqlInsert, sqlUpdate):
    i = 1

    while (True):
        url = main_url + '/?page=' + str(i) + '&sort=priceasc'

        if ('http' not in main_url):
            url = 'https://' + url

        r = requests.get(url)

        if (r.status_code != 200 or i == NUMPAGE):
            break

        content = r.text
        index1 = content.find('window.pageData={')
        string1 = content[index1:]
        index2 = string1.find(':{"footer')
        string2 = string1[:index2]

        regex = u"\"itemId\":\"(.+?),\"ratingScore\"+?"
        arr1 = re.findall(regex, string2)

        for item in arr1:
            if ('discount' in item):
                textCheck = item[:-1]
                index = textCheck.rfind('"')
                disCount = textCheck[index + 1:].replace('-', '').replace('%', '')

                if (int(disCount) > PERCENTDISCOUNT):
                    index = item.find('"')
                    idProduct = item[:index]
                    isUpdate = idProduct in arrProducts
                    sql = sqlInsert

                    if(isUpdate):
                        sql = sqlUpdate

                    hanldeDatabase(item, nameCategory, connection, sql, isUpdate)

        i = i + 1

    return


def getValueOf(stringText, name):
    index1 = stringText.find("\"" + name + "\":\"")
    stringText = stringText[index1 + len("\"" + name + "\":\""):]
    index2 = stringText.find('"')

    return stringText[:index2]


def getAllProduct(connection):
    arrProducts = []

    with connection.cursor() as cursor:
        sql = "SELECT id_product FROM products"
        cursor.execute(sql)
        result = cursor.fetchall()

        for item in result:
            arrProducts.append(item['id_product'])

        return arrProducts


def checkExist(arrProduct, idProduct):
    return idProduct in arrProduct


def main():
    stringLink = 'https://www.lazada.vn/giay-nam-thoi-trang,https://www.lazada.vn/tui-nam,https://www.lazada.vn/phu-kien-thoi-trang-nam,https://www.lazada.vn/trang-phuc-cua-be-trai,https://www.lazada.vn/thoi-trang-giay-cho-be-trai,https://www.lazada.vn/phu-kien-danh-cho-be-trai,https://www.lazada.vn/tui-danh-cho-tre-em,https://www.lazada.vn/dong-ho-nu-thoi-trang,https://www.lazada.vn/dong-ho-nam-gioi,https://www.lazada.vn/dong-ho-danh-cho-tre-em,https://www.lazada.vn/kinh-mat,https://www.lazada.vn/kinh-deo-mat,https://www.lazada.vn/san-pham-cham-soc-mat,https://www.lazada.vn/trang-suc-nu,https://www.lazada.vn/trang-suc-nam,https://www.lazada.vn/kinh-phu-kien,https://www.lazada.vn/vali-ba-lo-tui-du-lich-2,https://www.lazada.vn/dung-cu-de-tap-the-hinh,https://www.lazada.vn/hoat-dong-da-ngoai,https://www.lazada.vn/do-the-thao-nam,https://www.lazada.vn/do-the-thao-nu,https://www.lazada.vn/cac-mon-the-thao-vot,https://www.lazada.vn/cac-mon-tap-luyen-doi-khang,https://www.lazada.vn/dam-boc-vo-thuat-danh-mma,https://www.lazada.vn/cac-mon-the-thao-duoi-nuoc,https://www.lazada.vn/phu-kien-the-thao,https://www.lazada.vn/xe-may,https://www.lazada.vn/thiet-bi-phu-kien-o-to-xe-may,https://www.lazada.vn/dich-vu-lap-dat-xe,https://www.lazada.vn/do-bao-ho-mo-to,https://www.lazada.vn/dau-nhot-mo-to,https://www.lazada.vn/bo-phan-mo-to-phu-tung-thay-the-cho-mo-to,https://www.lazada.vn/cham-soc-ngoai-xe,https://www.lazada.vn/dau-nhot-o-to-xe-may,https://www.lazada.vn/phu-kien-ngoai-o-to-xe-may'
    arrLink = stringLink.split(',')
    firstTime = datetime.datetime.now()

    connection = pymysql.connect(host='localhost', user='root', password='', db='db-analysis-center', charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    sqlInsert = "INSERT INTO `products` (`id_product`, `name_product`, `link_product`, `image_product`, `original_price`, `price`, `percent`, `name_category`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    sqlUpdate = "UPDATE `products` SET `original_price` = %s, `price` = %s, `percent` = %s WHERE `id_product` = %s"
    arrProducts = getAllProduct(connection)

    try:
        for link in arrLink:
            index = link.rfind("/")
            nameCategory = link[index + 1:]

            hanleCategory(arrProducts, link, nameCategory, connection, sqlInsert, sqlUpdate)

            # break
    finally:
        connection.close()

    print(datetime.datetime.now() - firstTime)

    # sorted_list = sorted(arrItemProduct, key=lambda x: x[4], reverse=True)


main()
