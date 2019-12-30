import requests
import json
import os
import datetime
import time
from requests.exceptions import ConnectionError


def get_category_id():
    results = []
    url = "https://shopee.vn/api/v2/brand_lists/get"

    req = requests.get(url)

    category = json.loads(req.content)
    data = category['data']

    for item in data:
        shop_id = data[item]['shopid']

        results.append(shop_id)

    temp = []
    print(len(results))
    for item in results:
        if item not in temp:
            temp.append(item)

    return temp


def get_info(item, discount, cat_id):
    name = item['name']
    item_id = str(item['itemid'])
    shop_id = str(item['shopid'])
    temp_name = name.replace(' ', '-')

    link = "https://shopee.vn/" + temp_name + "-i." + shop_id + "." + item_id

    url = "https://shopee.vn/api/v2/item/get?itemid=" + str(item_id) + "&shopid=" + str(shop_id)

    req = requests.get(url)

    contents = json.loads(req.content)
    items = contents['item']
    original_price = str(items['price_before_discount'])
    original_price = original_price.replace("00000", "")
    price = str(items['price'])
    price = price.replace("00000", "")
    image = "https://cf.shopee.vn/file/" + items['image']

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
        'id_web': 2
    }

    req = requests.get(url, params=datas)

    # print(datas)


def handle(cat_id):
    percent = 80
    data_header = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }

    i = 0
    check_availble = True

    while check_availble:
        url = "https://shopee.vn/api/v2/search_items/?by=price&limit=50&match_id=" + str(cat_id) + "&newest=" + str(i) +\
              "&order=asc&page_type=shop&version=2"

        req = requests.get(url, headers=data_header)

        contents = json.loads(req.content)

        items = contents['items']

        if items is None or len(items) == 0:
            return

        # try:
        for item in items:
            discount = item['discount']
            discount = str(discount).replace('%', '')

            if discount != 'None' and int(discount) >= percent:
                info = get_info(item, discount, cat_id)
                print(info)
                save_to_db(info)
        # except TypeError:
        #     print(i)
        #     return

        i = i + 50


if __name__=='__main__':
    first_time = datetime.datetime.now()
    category = get_category_id()
    print(len(category))
    while True:
        for item in category:
            try:
                # print(category.index(item))
                time_cat = datetime.datetime.now()
                handle(item)

                # print(datetime.datetime.now() - time_cat)
            except (ValueError, ConnectionError) as e:
                print ("Connect error!")

        # print(datetime.datetime.now() - first_time)

        time.sleep(2000)