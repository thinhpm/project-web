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
    stringLink = 'https://www.lazada.vn/san-pham-tam-cham-soc-co-the,https://www.lazada.vn/thuc-pham-bo-sung,https://www.lazada.vn/thiet-bi-y-te,https://www.lazada.vn/cham-soc-ca-nhan,https://www.lazada.vn/cham-soc-tre-so-sinh-tre-nho,https://www.lazada.vn/do-dung-bu-sua-an-dam,https://www.lazada.vn/quan-ao-phu-kien-cho-be,https://www.lazada.vn/ta-dung-cu-ve-sinh,https://www.lazada.vn/dung-cu-cham-soc-co-the-tre-em,https://www.lazada.vn/xe-ghe-em-be,https://www.lazada.vn/do-choi-cho-tre-so-sinh-chap-chung,https://www.lazada.vn/do-choi-bo-suu-tap-nhan-vat,https://www.lazada.vn/the-thao-tro-choi-ngoai-troi,https://www.lazada.vn/xe-mo-hinh-tro-choi-dieu-khien-tu-xa,https://www.lazada.vn/do-an-sang,https://www.lazada.vn/do-hop-do-kho-thuc-pham-dong-goi,https://www.lazada.vn/cac-loai-do-uong,https://www.lazada.vn/thuc-uong-co-con,https://www.lazada.vn/giat-giu-cham-soc-nha-cua,https://www.lazada.vn/keo-socola,https://www.lazada.vn/nau-an-lam-banh,https://www.lazada.vn/phu-kien-hut-thuoc,https://www.lazada.vn/snack-do-an-vat,https://www.lazada.vn/cham-soc-thu-cung,https://www.lazada.vn/do-dung-bep-phong-an,https://www.lazada.vn/cac-loai-den,https://www.lazada.vn/do-dung-phong-ngu-gia-dinh,https://www.lazada.vn/do-dung-phu-kien-phong-tam,https://www.lazada.vn/san-pham-noi-that,https://www.lazada.vn/san-pham-trang-tri-nha-cua,https://www.lazada.vn/tan-trang-nha-cua,https://www.lazada.vn/van-phong-pham-va-nghe-thu-cong,https://www.lazada.vn/sach,https://www.lazada.vn/nhac-cu-moi,https://www.lazada.vn/trang-phuc-nu,https://www.lazada.vn/giay-nu-thoi-trang,https://www.lazada.vn/tui-cho-nu,https://www.lazada.vn/phu-kien-cho-nu,https://www.lazada.vn/do-ngu-noi-y,https://www.lazada.vn/trang-phuc-cua-be-gai,https://www.lazada.vn/thoi-trang-giay-danh-cho-be-gai,https://www.lazada.vn/phu-kien-danh-cho-be-gai,https://www.lazada.vn/tui-danh-cho-tre-em,https://www.lazada.vn/trang-phuc-nam,https://www.lazada.vn/do-lot-nam'
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

arr1 = 'https://www.lazada.vn/laptop,https://www.lazada.vn/may-tinh-de-ban-va-phu-kien,https://www.lazada.vn/thiet-bi-am-thanh-di-dong,https://www.lazada.vn/thiet-bi-choi-game,https://www.lazada.vn/may-quay-phim,https://www.lazada.vn/camera-giam-sat-2,https://www.lazada.vn/may-anh-may-quay-phim,https://www.lazada.vn/thiet-bi-so,https://www.lazada.vn/phu-kien-dien-thoai-may-tinh-bang,https://www.lazada.vn/phu-kien-may-vi-tinh,https://www.lazada.vn/thiet-bi-mang,https://www.lazada.vn/linh-kien-may-tinh,https://www.lazada.vn/phu-kien-may-anh-may-quay-phim,https://www.lazada.vn/thiet-bi-deo-cong-nghe,https://www.lazada.vn/thiet-bi-luu-tru,https://www.lazada.vn/thiet-bi-choi-game,https://www.lazada.vn/may-in-phu-kien,https://www.lazada.vn/phu-kien-may-tinh-bang,https://www.lazada.vn/tivi,https://www.lazada.vn/phu-kien-cho-tv,https://www.lazada.vn/he-thong-giai-tri-cho-tai-gia,https://www.lazada.vn/gia-dung-nha-bep,https://www.lazada.vn/do-gia-dung-nha-bep,https://www.lazada.vn/quat-may-nong-lanh,https://www.lazada.vn/choi-cay-lau-san-nha,https://www.lazada.vn/thiet-bi-cham-soc-quan-ao,https://www.lazada.vn/cham-soc-ca-nhan,https://www.lazada.vn/thiet-bi-do-gia-dung,https://www.lazada.vn/trang-diem,https://www.lazada.vn/cham-soc-da-mat,https://www.lazada.vn/san-pham-cham-soc-toc,https://www.lazada.vn/dung-cu-cham-soc-sac-dep,https://www.lazada.vn/nuoc-hoa,https://www.lazada.vn/cham-soc-cho-nam-gioi'
arr2 = 'https://www.lazada.vn/san-pham-tam-cham-soc-co-the,https://www.lazada.vn/thuc-pham-bo-sung,https://www.lazada.vn/thiet-bi-y-te,https://www.lazada.vn/cham-soc-ca-nhan,https://www.lazada.vn/cham-soc-tre-so-sinh-tre-nho,https://www.lazada.vn/do-dung-bu-sua-an-dam,https://www.lazada.vn/quan-ao-phu-kien-cho-be,https://www.lazada.vn/ta-dung-cu-ve-sinh,https://www.lazada.vn/dung-cu-cham-soc-co-the-tre-em,https://www.lazada.vn/xe-ghe-em-be,https://www.lazada.vn/do-choi-cho-tre-so-sinh-chap-chung,https://www.lazada.vn/do-choi-bo-suu-tap-nhan-vat,https://www.lazada.vn/the-thao-tro-choi-ngoai-troi,https://www.lazada.vn/xe-mo-hinh-tro-choi-dieu-khien-tu-xa,https://www.lazada.vn/do-an-sang,https://www.lazada.vn/do-hop-do-kho-thuc-pham-dong-goi,https://www.lazada.vn/cac-loai-do-uong,https://www.lazada.vn/thuc-uong-co-con,https://www.lazada.vn/giat-giu-cham-soc-nha-cua,https://www.lazada.vn/keo-socola,https://www.lazada.vn/nau-an-lam-banh,https://www.lazada.vn/phu-kien-hut-thuoc,https://www.lazada.vn/snack-do-an-vat,https://www.lazada.vn/cham-soc-thu-cung,https://www.lazada.vn/do-dung-bep-phong-an,https://www.lazada.vn/cac-loai-den,https://www.lazada.vn/do-dung-phong-ngu-gia-dinh,https://www.lazada.vn/do-dung-phu-kien-phong-tam,https://www.lazada.vn/san-pham-noi-that,https://www.lazada.vn/san-pham-trang-tri-nha-cua,https://www.lazada.vn/tan-trang-nha-cua,https://www.lazada.vn/van-phong-pham-va-nghe-thu-cong,https://www.lazada.vn/sach,https://www.lazada.vn/nhac-cu-moi,https://www.lazada.vn/trang-phuc-nu,https://www.lazada.vn/giay-nu-thoi-trang,https://www.lazada.vn/tui-cho-nu,https://www.lazada.vn/phu-kien-cho-nu,https://www.lazada.vn/do-ngu-noi-y,https://www.lazada.vn/trang-phuc-cua-be-gai,https://www.lazada.vn/thoi-trang-giay-danh-cho-be-gai,https://www.lazada.vn/phu-kien-danh-cho-be-gai,https://www.lazada.vn/tui-danh-cho-tre-em,https://www.lazada.vn/trang-phuc-nam,https://www.lazada.vn/do-lot-nam'
arr3 = 'https://www.lazada.vn/giay-nam-thoi-trang,https://www.lazada.vn/tui-nam,https://www.lazada.vn/phu-kien-thoi-trang-nam,https://www.lazada.vn/trang-phuc-cua-be-trai,https://www.lazada.vn/thoi-trang-giay-cho-be-trai,https://www.lazada.vn/phu-kien-danh-cho-be-trai,https://www.lazada.vn/tui-danh-cho-tre-em,https://www.lazada.vn/dong-ho-nu-thoi-trang,https://www.lazada.vn/dong-ho-nam-gioi,https://www.lazada.vn/dong-ho-danh-cho-tre-em,https://www.lazada.vn/kinh-mat,https://www.lazada.vn/kinh-deo-mat,https://www.lazada.vn/san-pham-cham-soc-mat,https://www.lazada.vn/trang-suc-nu,https://www.lazada.vn/trang-suc-nam,https://www.lazada.vn/kinh-phu-kien,https://www.lazada.vn/vali-ba-lo-tui-du-lich-2,https://www.lazada.vn/dung-cu-de-tap-the-hinh,https://www.lazada.vn/hoat-dong-da-ngoai,https://www.lazada.vn/do-the-thao-nam,https://www.lazada.vn/do-the-thao-nu,https://www.lazada.vn/cac-mon-the-thao-vot,https://www.lazada.vn/cac-mon-tap-luyen-doi-khang,https://www.lazada.vn/dam-boc-vo-thuat-danh-mma,https://www.lazada.vn/cac-mon-the-thao-duoi-nuoc,https://www.lazada.vn/phu-kien-the-thao,https://www.lazada.vn/xe-may,https://www.lazada.vn/thiet-bi-phu-kien-o-to-xe-may,https://www.lazada.vn/dich-vu-lap-dat-xe,https://www.lazada.vn/do-bao-ho-mo-to,https://www.lazada.vn/dau-nhot-mo-to,https://www.lazada.vn/bo-phan-mo-to-phu-tung-thay-the-cho-mo-to,https://www.lazada.vn/cham-soc-ngoai-xe,https://www.lazada.vn/dau-nhot-o-to-xe-may,https://www.lazada.vn/phu-kien-ngoai-o-to-xe-may'
main()
# string = '//www.lazada.vn/laptop/,//www.lazada.vn/may-tinh-de-ban-va-phu-kien/,//www.lazada.vn/thiet-bi-am-thanh-di-dong/,//www.lazada.vn/thiet-bi-choi-game/,//www.lazada.vn/may-quay-phim/,//www.lazada.vn/camera-giam-sat-2/,//www.lazada.vn/may-anh-may-quay-phim/,//www.lazada.vn/thiet-bi-so/,//www.lazada.vn/phu-kien-dien-thoai-may-tinh-bang/,//www.lazada.vn/phu-kien-may-vi-tinh/,//www.lazada.vn/thiet-bi-mang/,//www.lazada.vn/linh-kien-may-tinh/,//www.lazada.vn/phu-kien-may-anh-may-quay-phim/,//www.lazada.vn/thiet-bi-deo-cong-nghe/,//www.lazada.vn/thiet-bi-luu-tru/,//www.lazada.vn/thiet-bi-choi-game/,//www.lazada.vn/may-in-phu-kien/,//www.lazada.vn/phu-kien-may-tinh-bang/,//www.lazada.vn/tivi/,//www.lazada.vn/phu-kien-cho-tv/,//www.lazada.vn/he-thong-giai-tri-cho-tai-gia/,//www.lazada.vn/gia-dung-nha-bep/,//www.lazada.vn/do-gia-dung-nha-bep/,//www.lazada.vn/quat-may-nong-lanh/,//www.lazada.vn/choi-cay-lau-san-nha/,//www.lazada.vn/thiet-bi-cham-soc-quan-ao/,//www.lazada.vn/cham-soc-ca-nhan/,//www.lazada.vn/thiet-bi-do-gia-dung/,//www.lazada.vn/trang-diem/,//www.lazada.vn/cham-soc-da-mat/,//www.lazada.vn/san-pham-cham-soc-toc/,//www.lazada.vn/dung-cu-cham-soc-sac-dep/,//www.lazada.vn/nuoc-hoa/,//www.lazada.vn/cham-soc-cho-nam-gioi/,//www.lazada.vn/san-pham-tam-cham-soc-co-the/,//www.lazada.vn/thuc-pham-bo-sung/,//www.lazada.vn/thiet-bi-y-te/,//www.lazada.vn/cham-soc-ca-nhan/,//www.lazada.vn/cham-soc-tre-so-sinh-tre-nho/,//www.lazada.vn/do-dung-bu-sua-an-dam/,//www.lazada.vn/quan-ao-phu-kien-cho-be/,//www.lazada.vn/ta-dung-cu-ve-sinh/,//www.lazada.vn/dung-cu-cham-soc-co-the-tre-em/,//www.lazada.vn/xe-ghe-em-be/,//www.lazada.vn/do-choi-cho-tre-so-sinh-chap-chung/,//www.lazada.vn/do-choi-bo-suu-tap-nhan-vat/,//www.lazada.vn/the-thao-tro-choi-ngoai-troi/,//www.lazada.vn/xe-mo-hinh-tro-choi-dieu-khien-tu-xa/,//www.lazada.vn/do-an-sang/,//www.lazada.vn/do-hop-do-kho-thuc-pham-dong-goi/,//www.lazada.vn/cac-loai-do-uong/,//www.lazada.vn/thuc-uong-co-con/,//www.lazada.vn/giat-giu-cham-soc-nha-cua/,//www.lazada.vn/keo-socola/,//www.lazada.vn/nau-an-lam-banh/,//www.lazada.vn/phu-kien-hut-thuoc/,//www.lazada.vn/snack-do-an-vat/,//www.lazada.vn/cham-soc-thu-cung/,//www.lazada.vn/do-dung-bep-phong-an/,//www.lazada.vn/cac-loai-den/,//www.lazada.vn/do-dung-phong-ngu-gia-dinh/,//www.lazada.vn/do-dung-phu-kien-phong-tam/,//www.lazada.vn/san-pham-noi-that/,//www.lazada.vn/san-pham-trang-tri-nha-cua/,//www.lazada.vn/tan-trang-nha-cua/,//www.lazada.vn/van-phong-pham-va-nghe-thu-cong/,//www.lazada.vn/sach/,//www.lazada.vn/nhac-cu-moi/,//www.lazada.vn/trang-phuc-nu/,//www.lazada.vn/giay-nu-thoi-trang/,//www.lazada.vn/tui-cho-nu/,//www.lazada.vn/phu-kien-cho-nu/,//www.lazada.vn/do-ngu-noi-y/,//www.lazada.vn/trang-phuc-cua-be-gai/,//www.lazada.vn/thoi-trang-giay-danh-cho-be-gai/,//www.lazada.vn/phu-kien-danh-cho-be-gai/,//www.lazada.vn/tui-danh-cho-tre-em/,//www.lazada.vn/trang-phuc-nam/,//www.lazada.vn/do-lot-nam/,//www.lazada.vn/giay-nam-thoi-trang/,//www.lazada.vn/tui-nam/,//www.lazada.vn/phu-kien-thoi-trang-nam/,//www.lazada.vn/trang-phuc-cua-be-trai/,//www.lazada.vn/thoi-trang-giay-cho-be-trai/,//www.lazada.vn/phu-kien-danh-cho-be-trai/,//www.lazada.vn/tui-danh-cho-tre-em/,//www.lazada.vn/dong-ho-nu-thoi-trang/,//www.lazada.vn/dong-ho-nam-gioi/,//www.lazada.vn/dong-ho-danh-cho-tre-em/,//www.lazada.vn/kinh-mat/,//www.lazada.vn/kinh-deo-mat/,//www.lazada.vn/san-pham-cham-soc-mat/,//www.lazada.vn/trang-suc-nu/,//www.lazada.vn/trang-suc-nam/,//www.lazada.vn/kinh-phu-kien/,//www.lazada.vn/vali-ba-lo-tui-du-lich-2/,//www.lazada.vn/dung-cu-de-tap-the-hinh/,//www.lazada.vn/hoat-dong-da-ngoai/,//www.lazada.vn/do-the-thao-nam/,//www.lazada.vn/do-the-thao-nu/,//www.lazada.vn/cac-mon-the-thao-vot/,//www.lazada.vn/cac-mon-tap-luyen-doi-khang/,//www.lazada.vn/dam-boc-vo-thuat-danh-mma/,//www.lazada.vn/cac-mon-the-thao-duoi-nuoc/,//www.lazada.vn/phu-kien-the-thao/,//www.lazada.vn/xe-may/,//www.lazada.vn/thiet-bi-phu-kien-o-to-xe-may/,//www.lazada.vn/dich-vu-lap-dat-xe/,//www.lazada.vn/do-bao-ho-mo-to/,//www.lazada.vn/dau-nhot-mo-to/,//www.lazada.vn/bo-phan-mo-to-phu-tung-thay-the-cho-mo-to/,//www.lazada.vn/cham-soc-ngoai-xe/,//www.lazada.vn/dau-nhot-o-to-xe-may/,//www.lazada.vn/phu-kien-ngoai-o-to-xe-may/'
# arr = string.split(',')
#
# arrResult = []
# stt = 1
# for link in arr:
#     link = link.replace('//', '')[:-1]
#     if('http' not in link):
#         link = 'https://' + link
#     if(stt >= 80):
#         arrResult.append(link)
#     stt = stt + 1
# print(','.join(arrResult))
# connection = pymysql.connect(host='localhost', user='root', password='', db='db-analysis-center', charset='utf8mb4',
#                                  cursorclass=pymysql.cursors.DictCursor)
# sql = "INSERT INTO `categories` (`id_category`, `name_category`, `id_web`) VALUES (%s, %s, %s)"
# for link in arrResult:
#     index = link.rfind("/")
#     idCategory = link[index + 1:]
#
#     html = webDriver(link)
#     # r = requests.get(link)
#     # content = r.text
#     soup = BeautifulSoup(html, 'lxml')
#
#     h1 = soup.h1.string
#
#     with connection.cursor() as cursor:
#         # Create a new record
#         cursor.execute(sql, (idCategory, h1, 1))
#     connection.commit()

