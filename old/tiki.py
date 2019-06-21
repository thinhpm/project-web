import requests
import json
import os
import datetime
from bs4 import BeautifulSoup
import lxml
import time
from requests.exceptions import ConnectionError


def get_category_id():
    result = []
    url = "http://mgghot.com/wp-admin/admin-ajax.php?action=api_v1_get_category"
    data = {
        'id_web': 3
    }

    req = requests.get(url, params=data)
    contents = req.content

    arr = str(contents).split(',')

    for item in arr:
        item = item.replace('"', '').replace("\\", "")

        result.append(item)

    return result


def get_info(item, discount, cat_id):
    name = item.get('data-title')
    item_id = item.get('data-id')

    link = item.a.get('href')

    original_price = item.find(class_='price-regular').string
    original_price = original_price[:-1].replace(".", "")
    original_price = original_price.strip()

    price = item.get('data-price').strip()
    image = item.img.get('src')

    return {
        'item_id': item_id,
        'name': name,
        'original_price': original_price,
        'price': price,
        'image': image,
        'link': link,
        'discount': discount,
        'cat_id': cat_id
    }


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
        'id_web': 3
    }

    req = requests.get(url, params=datas)

    # print(datas)


def handle(cat_id):
    pages = 50
    percent = 80
    data_header = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }

    for i in range(1, pages):
        url = 'https://tiki.vn/' + str(cat_id) + '?src=mega-menu&order=price%2Casc&page=' + str(i)
        req = requests.get(url, headers=data_header)

        contents = BeautifulSoup(req.content, 'lxml')

        items = contents.find_all(class_="product-item")

        for item in items:
            discount = item.find(class_="sale-tag sale-tag-square").string
            discount = str(discount).replace('%', '').replace('-', '')

            if discount != 'None' and int(discount) >= percent:
                info = get_info(item, discount, cat_id)
                save_to_db(info)


if __name__=='__main__':
    first_time = datetime.datetime.now()
    category = get_category_id()

    while True:
        for item in category:
            try:
                print(category.index(item))
                time_cat = datetime.datetime.now()

                handle(item)

                print(datetime.datetime.now() - time_cat)
            except ConnectionError as e:
                print ("Connect error!")
        print(datetime.datetime.now() - first_time)

        time.sleep(2000)