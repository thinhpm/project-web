
import re
import requests
import time
import lxml
from lxml import html
from bs4 import BeautifulSoup

PERCENTDISCOUNT = 70


def check_exist_chapt(id_series, id_chapt_new):
    name_file = "save-data.txt"

    fo = open(name_file, "r")

    lines = fo.readlines()
    # format series:chapt,chapt\n
    for line in lines:
        arr_split = line.split(':')
        if (len(arr_split) > 1):
            series_current = arr_split[0]
            list_chapt_current = arr_split[1].replace('\n', '').split(',')

            if (str(series_current) == str(id_series)):
                if str(id_chapt_new) in list_chapt_current:
                    return False
    fo.close()
    return True


def save_to_file(id_series, id_chapt_new):
    name_file = "save-data.txt"

    fo = open(name_file, "r")
    lines = fo.readlines()
    check = True
    i = 0
    len_lines = len(lines)
    n = '\n'
    # format series:chapt,chapt\n
    for line in lines:
        arr_split = line.split(':')
        if (len(arr_split) > 1):
            series_current = arr_split[0]
            list_chapt_current = arr_split[1].replace('\n', '')

            if (i == len_lines - 1):
                n = ''
            if (str(series_current) == str(id_series)):
                list_chapt_current = str(id_series) + ':' + str(list_chapt_current) + ',' + str(id_chapt_new) + n
                lines[i] = list_chapt_current
                check = False
        i = i + 1
    if (check):
        if (len(lines) > 0):
            lines[len(lines) - 1] = lines[len(lines) - 1] + '\n'
        lines.append(str(id_series) + ':' + id_chapt_new)
    fo.close()

    fo = open(name_file, "w")
    fo.writelines(lines)
    fo.close()
    return True


def get_data_file(file_name):
    path_file = file_name
    fo = open(path_file, "r")
    lines = fo.readlines()
    fo.close()
    stt_video = ''

    if len(lines) > 0:
        stt_video = lines[0]

    return stt_video


def getProxy():
    url = "https://free-proxy-list.net"
    req = requests.get(url)

    root = html.fromstring(req.content)
    list_item = root.xpath('//*[@id="proxylisttable"]/tbody/tr')

    for item in list_item:
        ip = item.xpath("td[1]/text()")[0]
        port = item.xpath("td[2]/text()")[0]
        type_proxy = item.xpath("td[5]/text()")[0]

        if type_proxy == 'transparent' and check_exist_chapt('proxy', ip):
            save_to_file('proxy', ip)

            return str(ip) + ':' + str(port)


def getValueOf(stringText, name):
    index1 = stringText.find("\"" + name + "\":\"")
    stringText = stringText[index1 + len("\"" + name + "\":\""):]
    index2 = stringText.find('"')

    return stringText[:index2]


def save_to_db(data):
    url = "http://mgghot.com/wp-admin/admin-ajax.php?action=api_v1_lazada_set_db"

    datas = {
        'id_product': data['item_id'],
        'name_product': data['name'],
        'link_product': data['link'],
        'image_product': data['image'],
        'original_price': data['original_price'],
        'price': data['price'],
        'percent': data['discount'],
        'name_category': data['cat_id'],
        'id_web': 1
    }

    req = requests.get(url, params=datas)


def getNameProduct(link):
    index = link.rfind('/')
    link = link[index + 1:]
    index = link.rfind('i')
    link = link[:index]
    name = link.replace('-', " ")

    return name


def generate_cookie(string_cookie):
    if string_cookie == '':
        return {}

    string_cookie = string_cookie.replace(" ", "")
    arr = string_cookie.split(";")
    result = {}

    for i in range(len(arr)):
        key, value = arr[i].split("=")

        result[key] = value

    return result


def main(string_link):
    need_new_proxy = False
    arr_link = string_link.split(",")
    stt = 0
    cookie = "client_type=desktop; lzd_cid=6452f4c1-f8b6-4aa7-9760-c4010c2a8048; t_uid=6452f4c1-f8b6-4aa7-9760-c4010c2a8048; hng=VN|en|VND|704; userLanguageML=en; t_fv=1574331551287; cna=nVVdFphZL20CAYu0w1l2JPTi; _bl_uid=w6k7v39n83nkLRcmIytLa637yXvC; cto_lwid=a0fc21db-7f3c-4bdb-9ddd-e3423b65d248; cto_idcpy=ebe1ee59-95b1-4de7-87d2-63976b3cec65; Hm_lvt_7cd4710f721b473263eed1f0840391b4=1574386982,1574674477; _m_h5_tk=93e3674f1b1e599f82e4f845d058426b_1575025678628; _m_h5_tk_enc=a6b5b4c3007b3d39adff7c147ccd70ef; _tb_token_=7edebe536a75a; t_sid=JaOpOHNiPLhdDuNKD5SL6ihaS2RH7TuV; utm_channel=NA; _ga=GA1.2.1597665392.1574331570; _gid=GA1.2.182739780.1575015610; _gat_UA-30172376-1=1; _fbp=fb.1.1574331570385.1181107822; l=dBSiKJ67qW39jerzBOCwdZZzUC_OsIO4YuWbadjMi_5Ik1L6DkQOkn3-lep6cOWcGVLB40FhhAJToEM8-zvfi9vJUJ2emVMDBef..; isg=BEJCPmA7q_38O7eX2GvUKwEXkEGuE0QioXxEqIxbY7Vg3-BZdKWaPLodjwMGlL7F"
    proxies = {
        'http': 'http://36.89.190.131:36588',
        'https': 'http://36.89.190.131:36588'
    }



    while True:
        link = arr_link[stt]
        print(link)
        for i in range(25):
            index = link.rfind("/")
            nameCategory = link[index + 1:]
            cat_id = nameCategory
            url = link + '/?page=' + str(i) + '&sort=priceasc'

            if ('http' not in link):
                url = 'https://' + url

            # req = requests.get(url, proxies=proxies)
            req = requests.get(url, cookies=generate_cookie(cookie))
            result = handle(req, cat_id)

            if result is False:
                break

            time.sleep(1)

            # if need_new_proxy is True:
            #     proxy = getProxy()
            #     proxies = {
            #         'http': 'http://' + proxy,
            #         'https': 'http://' + proxy
            #     }
            # time.sleep(1)

        stt = stt + 1

        if stt >= len(arr_link):
            stt = 0


def handle(response, cat_id):
    need_new_proxy = False
    content = str(response.content)

    index1 = content.find('window.pageData={')
    string1 = content[index1:]
    index2 = string1.find(':{"footer')
    string2 = string1[:index2]

    regex = u"\"itemId\":\"(.+?),\"ratingScore\"+?"
    arr1 = re.findall(regex, string2)

    print(len(arr1))
    count_none = 0

    if len(arr1) == 0:
        return False

        content2 = BeautifulSoup(content, 'lxml')
        classes = content2.find(id="nc-verify-form")

        return classes is not None and len(classes) > 0

    for item in arr1:
        if ('discount' in item):
            textCheck = item[:-1]
            index = textCheck.rfind('"')
            disCount = textCheck[index + 1:].replace('-', '').replace('%', '')

            if (disCount == 0):
                count_none = count_none + 1

            if (int(disCount) > PERCENTDISCOUNT):
                index = item.find('"')
                idProduct = item[:index]
                originalPrice = getValueOf(item, 'originalPrice').replace('.00', '')
                price = getValueOf(item, 'price').replace('.00', '')
                disCount = getValueOf(item, 'discount').replace('-', '').replace('%', '')

                linkProduct = 'https:' + getValueOf(item, 'productUrl')
                imageProduct = getValueOf(item, 'image')
                nameProduct = getNameProduct(linkProduct)

                data = {
                    'item_id': idProduct,
                    'name': nameProduct,
                    'original_price': originalPrice,
                    'price': price,
                    'image': imageProduct,
                    'link': linkProduct,
                    'discount': disCount,
                    'cat_id': cat_id
                }
                print(data)
                save_to_db(data)

    if count_none >= len(arr1):
        return False

    return True


if __name__ == '__main__':
    string_link = 'https://www.lazada.vn/laptop,https://www.lazada.vn/may-tinh-de-ban-va-phu-kien,https://www.lazada.vn/thiet-bi-am-thanh-di-dong,https://www.lazada.vn/thiet-bi-choi-game,https://www.lazada.vn/may-quay-phim,https://www.lazada.vn/camera-giam-sat-2,https://www.lazada.vn/may-anh-may-quay-phim,https://www.lazada.vn/thiet-bi-so,https://www.lazada.vn/phu-kien-dien-thoai-may-tinh-bang,https://www.lazada.vn/phu-kien-may-vi-tinh,https://www.lazada.vn/thiet-bi-mang,https://www.lazada.vn/linh-kien-may-tinh,https://www.lazada.vn/phu-kien-may-anh-may-quay-phim,https://www.lazada.vn/thiet-bi-deo-cong-nghe,https://www.lazada.vn/thiet-bi-luu-tru,https://www.lazada.vn/thiet-bi-choi-game,https://www.lazada.vn/may-in-phu-kien,https://www.lazada.vn/phu-kien-may-tinh-bang,https://www.lazada.vn/tivi,https://www.lazada.vn/phu-kien-cho-tv,https://www.lazada.vn/he-thong-giai-tri-cho-tai-gia,https://www.lazada.vn/gia-dung-nha-bep,https://www.lazada.vn/do-gia-dung-nha-bep,https://www.lazada.vn/quat-may-nong-lanh,https://www.lazada.vn/choi-cay-lau-san-nha,https://www.lazada.vn/thiet-bi-cham-soc-quan-ao,https://www.lazada.vn/cham-soc-ca-nhan,https://www.lazada.vn/thiet-bi-do-gia-dung,https://www.lazada.vn/trang-diem,https://www.lazada.vn/cham-soc-da-mat,https://www.lazada.vn/san-pham-cham-soc-toc,https://www.lazada.vn/dung-cu-cham-soc-sac-dep,https://www.lazada.vn/nuoc-hoa,https://www.lazada.vn/cham-soc-cho-nam-gioi,https://www.lazada.vn/san-pham-tam-cham-soc-co-the,https://www.lazada.vn/thuc-pham-bo-sung,https://www.lazada.vn/thiet-bi-y-te,https://www.lazada.vn/cham-soc-ca-nhan,https://www.lazada.vn/cham-soc-tre-so-sinh-tre-nho,https://www.lazada.vn/do-dung-bu-sua-an-dam,https://www.lazada.vn/quan-ao-phu-kien-cho-be,https://www.lazada.vn/ta-dung-cu-ve-sinh,https://www.lazada.vn/dung-cu-cham-soc-co-the-tre-em,https://www.lazada.vn/xe-ghe-em-be,https://www.lazada.vn/do-choi-cho-tre-so-sinh-chap-chung,https://www.lazada.vn/do-choi-bo-suu-tap-nhan-vat,https://www.lazada.vn/the-thao-tro-choi-ngoai-troi,https://www.lazada.vn/xe-mo-hinh-tro-choi-dieu-khien-tu-xa,https://www.lazada.vn/do-an-sang,https://www.lazada.vn/do-hop-do-kho-thuc-pham-dong-goi,https://www.lazada.vn/cac-loai-do-uong,https://www.lazada.vn/thuc-uong-co-con,https://www.lazada.vn/giat-giu-cham-soc-nha-cua,https://www.lazada.vn/keo-socola,https://www.lazada.vn/nau-an-lam-banh,https://www.lazada.vn/phu-kien-hut-thuoc,https://www.lazada.vn/snack-do-an-vat,https://www.lazada.vn/cham-soc-thu-cung,https://www.lazada.vn/do-dung-bep-phong-an,https://www.lazada.vn/cac-loai-den,https://www.lazada.vn/do-dung-phong-ngu-gia-dinh,https://www.lazada.vn/do-dung-phu-kien-phong-tam,https://www.lazada.vn/san-pham-noi-that,https://www.lazada.vn/san-pham-trang-tri-nha-cua,https://www.lazada.vn/tan-trang-nha-cua,https://www.lazada.vn/van-phong-pham-va-nghe-thu-cong,https://www.lazada.vn/sach,https://www.lazada.vn/nhac-cu-moi,https://www.lazada.vn/trang-phuc-nu,https://www.lazada.vn/giay-nu-thoi-trang,https://www.lazada.vn/tui-cho-nu,https://www.lazada.vn/phu-kien-cho-nu,https://www.lazada.vn/do-ngu-noi-y,https://www.lazada.vn/trang-phuc-cua-be-gai,https://www.lazada.vn/thoi-trang-giay-danh-cho-be-gai,https://www.lazada.vn/phu-kien-danh-cho-be-gai,https://www.lazada.vn/tui-danh-cho-tre-em,https://www.lazada.vn/trang-phuc-nam,https://www.lazada.vn/do-lot-nam,https://www.lazada.vn/giay-nam-thoi-trang,https://www.lazada.vn/tui-nam,https://www.lazada.vn/phu-kien-thoi-trang-nam,https://www.lazada.vn/trang-phuc-cua-be-trai,https://www.lazada.vn/thoi-trang-giay-cho-be-trai,https://www.lazada.vn/phu-kien-danh-cho-be-trai,https://www.lazada.vn/tui-danh-cho-tre-em,https://www.lazada.vn/dong-ho-nu-thoi-trang,https://www.lazada.vn/dong-ho-nam-gioi,https://www.lazada.vn/dong-ho-danh-cho-tre-em,https://www.lazada.vn/kinh-mat,https://www.lazada.vn/kinh-deo-mat,https://www.lazada.vn/san-pham-cham-soc-mat,https://www.lazada.vn/trang-suc-nu,https://www.lazada.vn/trang-suc-nam,https://www.lazada.vn/kinh-phu-kien,https://www.lazada.vn/vali-ba-lo-tui-du-lich-2,https://www.lazada.vn/dung-cu-de-tap-the-hinh,https://www.lazada.vn/hoat-dong-da-ngoai,https://www.lazada.vn/do-the-thao-nam,https://www.lazada.vn/do-the-thao-nu,https://www.lazada.vn/cac-mon-the-thao-vot,https://www.lazada.vn/cac-mon-tap-luyen-doi-khang,https://www.lazada.vn/dam-boc-vo-thuat-danh-mma,https://www.lazada.vn/cac-mon-the-thao-duoi-nuoc,https://www.lazada.vn/phu-kien-the-thao,https://www.lazada.vn/xe-may,https://www.lazada.vn/thiet-bi-phu-kien-o-to-xe-may,https://www.lazada.vn/dich-vu-lap-dat-xe,https://www.lazada.vn/do-bao-ho-mo-to,https://www.lazada.vn/dau-nhot-mo-to,https://www.lazada.vn/bo-phan-mo-to-phu-tung-thay-the-cho-mo-to,https://www.lazada.vn/cham-soc-ngoai-xe,https://www.lazada.vn/dau-nhot-o-to-xe-may,https://www.lazada.vn/phu-kien-ngoai-o-to-xe-may'
    main(string_link)