from scrapy import Spider, Request
import re
import requests
import time
import json
import datetime
from scrapy.crawler import CrawlerProcess


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


class TestDev(Spider):
    name = 'sendo-tool'
    pages = 50
    percent = 70
    clone_page_id = ''
    time = 1

    def start_requests(self):
        category = get_category_id()

        stt = 0

        while True:
            cat_id = category[stt]

            for i in range(1, self.pages):
                self.clone_page_id = cat_id

                url = "https://www.sendo.vn/m/wap_v2/category/product?category_id=" + str(
                    cat_id) + "&listing_algo=algo6&p=" + \
                      str(i) + "&s=60&sortType=price_asc"

                request = Request(url=url, callback=self.parse)

                yield request

            stt = stt + 1

            if stt >= len(category):
                self.time = self.time + 1
                print("success")
                print(self.time)

                stt = 0
                time.sleep(3600)



    def parse(self, response):
        contents = json.loads(response.body)
        contents = contents['result']['data']

        for item in contents:
            discount = item['promotion_percent']
            discount = str(discount).replace('%', '')

            if int(discount) >= self.percent:
                info = get_info(item, discount, self.clone_page_id)
                save_to_db(info)
        return
