import requests
import json
import os
import datetime
from bs4 import BeautifulSoup
import lxml
import time
from requests.exceptions import ConnectionError
import logging
from queue import Queue
from multi_threading import MyWorker
from checkprice import CheckPrice


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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
    id_product = item['id']
    name = item['name']
    link_product = 'https://tiki.vn/' + item['url_key'] + '.html'
    image_product = item['thumbnail_url']
    original_price = item['list_price']
    price = item['price']

    return {
        'item_id': id_product,
        'name': name,
        'original_price': original_price,
        'price': price,
        'image': image_product,
        'link': link_product,
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
        if "/" not in cat_id:
            break

        temp1, temp2 = cat_id.split("/")

        id = temp2.replace("c", "")
        url = 'https://tiki.vn/api/v2/landingpage/products?category_id=' + str(id) + '&limit=48&sort=discount_percent,desc&page=' + str(i)

        req = requests.get(url, headers=data_header)
        data = json.loads(req.content)
        items = data['data']

        if len(items) == 0:
            break

        for item in items:
            discount = item['discount_rate']

            if int(discount) >= percent:
                price = item['price']
                link_product = 'https://tiki.vn/' + item['url_key'] + '.html'
                seller_product_id = item['seller_product_id']
                info = get_info(item, discount, cat_id)

                check_price = CheckPrice()
                check_error_item = check_price.check_item_is_error(link_product + "?spid=" + str(seller_product_id), price)
                # print(info)
                if check_error_item:
                    print("------------")
                    print(info)
                    print("------------")
                # save_to_db(info)


def multi_handle(total_worker, func_run, list_handle):
    queue = Queue()

    for i in range(total_worker):
        worker = MyWorker(queue, func_run)
        worker.daemon = True
        worker.start()

    for i in range(len(list_handle)):
        # logger.info('Queue ' + str(i))
        # print("-" + str(j))
        queue.put(list_handle[i])

    queue.join()


if __name__ == '__main__':
    first_time = datetime.datetime.now()
    category = get_category_id()
    ts = time.time()
    multi_handle(10, handle, category)
    # for item in category:
    #     try:
    #         handle(item)
    #
    #     except ConnectionError as e:
    #         print ("Connect error!")

    logging.info('Took %s', time.time() - ts)
# check_price = CheckPrice()
# check = check_price.check_item_is_error("https://tiki.vn/smart-tivi-samsung-55-inch-4k-uhd-ua55nu7090kxxv-hang-chinh-hang-p3665301.html", 123)
# print(check)