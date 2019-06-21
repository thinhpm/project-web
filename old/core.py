from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
import datetime
import pymysql.cursors

PERCENTDISCOUNT = 1
NUMPAGE = 20


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
        print(content)
        return 2
        for item in arr1:
            print(content)
            return
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
    stringLink = 'https://www.lazada.vn/laptop,https://www.lazada.vn/may-tinh-de-ban-va-phu-kien,https://www.lazada.vn/thiet-bi-am-thanh-di-dong,https://www.lazada.vn/thiet-bi-choi-game,https://www.lazada.vn/may-quay-phim,https://www.lazada.vn/camera-giam-sat-2,https://www.lazada.vn/may-anh-may-quay-phim,https://www.lazada.vn/thiet-bi-so,https://www.lazada.vn/phu-kien-dien-thoai-may-tinh-bang,https://www.lazada.vn/phu-kien-may-vi-tinh,https://www.lazada.vn/thiet-bi-mang,https://www.lazada.vn/linh-kien-may-tinh,https://www.lazada.vn/phu-kien-may-anh-may-quay-phim,https://www.lazada.vn/thiet-bi-deo-cong-nghe,https://www.lazada.vn/thiet-bi-luu-tru,https://www.lazada.vn/thiet-bi-choi-game,https://www.lazada.vn/may-in-phu-kien,https://www.lazada.vn/phu-kien-may-tinh-bang,https://www.lazada.vn/tivi,https://www.lazada.vn/phu-kien-cho-tv,https://www.lazada.vn/he-thong-giai-tri-cho-tai-gia,https://www.lazada.vn/gia-dung-nha-bep,https://www.lazada.vn/do-gia-dung-nha-bep,https://www.lazada.vn/quat-may-nong-lanh,https://www.lazada.vn/choi-cay-lau-san-nha,https://www.lazada.vn/thiet-bi-cham-soc-quan-ao,https://www.lazada.vn/cham-soc-ca-nhan,https://www.lazada.vn/thiet-bi-do-gia-dung,https://www.lazada.vn/trang-diem,https://www.lazada.vn/cham-soc-da-mat,https://www.lazada.vn/san-pham-cham-soc-toc,https://www.lazada.vn/dung-cu-cham-soc-sac-dep,https://www.lazada.vn/nuoc-hoa,https://www.lazada.vn/cham-soc-cho-nam-gioi'
    arrLink = stringLink.split(',')
    firstTime = datetime.datetime.now()

    # connection = pymysql.connect(host='localhost', user='root', password='', db='db-analysis-center', charset='utf8mb4',
    #                              cursorclass=pymysql.cursors.DictCursor, port=2082)

    sqlInsert = "INSERT INTO `products` (`id_product`, `name_product`, `link_product`, `image_product`, `original_price`, `price`, `percent`, `name_category`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    sqlUpdate = "UPDATE `products` SET `original_price` = %s, `price` = %s, `percent` = %s WHERE `id_product` = %s"
    # arrProducts = getAllProduct(connection)
    connection = ''
    arrProducts = ()

    try:
        for link in arrLink:
            index = link.rfind("/")
            nameCategory = link[index + 1:]

            hanleCategory(arrProducts, link, nameCategory, connection, sqlInsert, sqlUpdate)

            break
    finally:
        print("1")
        # connection.close()

    print(datetime.datetime.now() - firstTime)

    # sorted_list = sorted(arrItemProduct, key=lambda x: x[4], reverse=True)


main()


# connection = pymysql.connect(host='sql212.byethost11.com',
#                              user='b11_22962409',
#                              password='iamduclan123',
#                              db='b11_22962409_db_analysis_center',
#                              charset='utf8mb4',
#                              port=3306,
#                              cursorclass=pymysql.cursors.DictCursor)
#
# print ("connect successful!!")
#
# try:
#     with connection.cursor(buffered=True) as cursor:
#
#         # SQL
#         sql = "SELECT * from products "
#
#         # Execute query.
#         cursor.execute(sql)
#
#         print ("cursor.description: ", cursor.description)
#
#         print()
#
#         for row in cursor:
#             print(row)
#
# finally:
#     # Close connection.
#     connection.close()