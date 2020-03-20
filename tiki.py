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


data_header = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}


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


def save_to_db(data, check_error_item):
    url = "http://mgghot.com/wp-admin/admin-ajax.php?action=api_v1_lazada_set_db"
    url = "http://localhost/analysis-center/wp-admin/admin-ajax.php?action=api_v1_lazada_set_db"

    datas = {
        'id_product': data['item_id'],
        'name_product': data['name'],
        'link_product': data['link'],
        'image_product': data['image'],
        'original_price': data['original_price'],
        'price': data['price'],
        'percent': data['discount'],
        'name_category': data['cat_id'],
        'is_error_price': int(check_error_item),
        'id_web': 3
    }

    req = requests.get(url, params=datas)


def get_total_page(url, data_header):
    req = requests.get(url, headers=data_header)
    data = json.loads(req.content)
    pages = data['paging']

    return pages['total']


def handle_detail(data):
    url = data['url']
    cat_id = data['cat_id']
    percent = 80
    req = requests.get(url, headers=data_header)
    data = json.loads(req.content)

    if 'data' not in data:
        return

    items = data['data']

    if len(items) == 0:
        return

    for item in items:
        discount = item['discount_rate']

        if int(discount) >= percent:
            id_product = item['id']
            price = item['price']
            link_product = 'https://tiki.vn/' + item['url_key'] + '.html'
            seller_product_id = item['seller_product_id']
            info = get_info(item, discount, cat_id)

            check_price = CheckPrice()
            # url_check = link_product + "?spid=" + str(seller_product_id)
            url_check = "3__" + str(id_product) + "__" + str(seller_product_id)
            check_error_item = check_price.check_item_is_error(url_check, price)

            if check_error_item:
                print("------------")
                print(info)
                print("------------")

            # save_to_db(info, check_error_item)


def handle(cat_id):
    limit_page = 40
    limit = 48

    if "/" not in cat_id:
        return

    temp1, temp2 = cat_id.split("/")

    id = temp2.replace("c", "")
    url = 'https://tiki.vn/api/v2/landingpage/products?category_id=' + str(
            id) + '&limit=' + str(limit) + '&sort=discount_percent,desc&page=1'

    total_page = get_total_page(url, data_header)
    total_page = int(total_page/limit)

    list_handel = []

    for i in range(total_page):
        if i >= limit_page:
            break

        url = 'https://tiki.vn/api/v2/landingpage/products?category_id=' + str(
            id) + '&limit=' + str(limit) + '&sort=discount_percent,desc&page=' + str(i + 1)
        list_handel.append({
            'url': url,
            'cat_id': cat_id
        })

    multi_handle(10, handle_detail, list_handel)


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
    while True:
        first_time = datetime.datetime.now()
        category = get_category_id()
        ts = time.time()

        for item in category:
            handle(item)

        logging.info('Took %s', time.time() - ts)

        time.sleep(500)
# check_price = CheckPrice()
# check = check_price.check_item_is_error("https://tiki.vn/smart-tivi-samsung-55-inch-4k-uhd-ua55nu7090kxxv-hang-chinh-hang-p3665301.html", 123)
# print(check)
