import requests
import json
import os
import datetime
import time
from requests.exceptions import ConnectionError

def get_category_id():
    results = []
    url = "https://www.sendo.vn/m/wap_v2/category/sitemap"

    req = requests.get(url)

    category = json.loads(req.content)
    list_category = category['result']['data']


    for item in list_category:
        for child in item['child']:
            results.append(child['id'])

    return results


def get_info(item, discount, cat_id):
    name = item['name']
    item_id = str(item['product_id'])
    link = "https://sendo.vn/" + item['cat_path']

    original_price = str(item['price'])
    price = str(item['final_price'])
    image = item['image']

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
        'id_web': 4
    }

    req = requests.get(url, params=datas)

    # print(datas)


def handle(cat_id):
    pages = 25
    percent = 60
    data_header = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }

    for i in range(1, pages):
        url = "https://www.sendo.vn/m/wap_v2/category/product?category_id=" + str(cat_id) + "&listing_algo=algo6&p=" + \
              str(i) + "&s=60&sortType=price_asc"

        req = requests.get(url, headers=data_header)
        try:
            contents = json.loads(req.content)
            contents = contents['result']['data']

            for item in contents:
                discount = item['promotion_percent']
                discount = str(discount).replace('%', '')

                if int(discount) >= percent:
                    info = get_info(item, discount, cat_id)
                    save_to_db(info)
        except ValueError:
            print("decode error!")


if __name__=='__main__':
    category = get_category_id()

    while True:
        first_time = datetime.datetime.now()
        for item in category:
            try:
                print(category.index(item))
                time_cat = datetime.datetime.now()

                handle(item)

                print(datetime.datetime.now() - time_cat)
            except (ValueError, ConnectionError) as e:
                print ("Connect error!")

        print(datetime.datetime.now() - first_time)

        time.sleep(2000)