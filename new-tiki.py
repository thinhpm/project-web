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
import asyncio
import aiohttp
from aiosocksy import Socks5Auth
from aiosocksy.connector import ProxyConnector, ProxyClientRequest

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()


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

    if 'paging' not in data:
        return 0

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

    if total_page == 0:
        return

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


async def fetch(method="POST", url="", data=(), session=None, proxy="", proxy_auth=""):
    if method == "GET":
        async with session.get(url, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
            return await response.read()
    else:
        async with session.put(url, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
            return await response.read()


async def async_request_aio_http(arr_handle):
    timeout = aiohttp.ClientTimeout(total=10)
    auth = Socks5Auth(login='', password='')
    connector = ProxyConnector(verify_ssl=False)

    socks_api = ""
    auth = ""

    async with aiohttp.ClientSession(connector=connector, request_class=ProxyClientRequest, timeout=timeout) as session:
        tasks = []

        for item in arr_handle:

            url = item['url']
            data_post = {}

            task = asyncio.ensure_future(fetch("GET", url, data_post, session, socks_api, auth))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

        await session.close()

    return responses


def get_list_cat_id(category):
    results = []

    for item in category:
        if "/" not in item:
            continue

        temp1, temp2 = item.split("/")

        cat_id = temp2.replace("c", "")
        results.append(cat_id)

    return results


def get_list_total_page(list_cat_id):
    limit = 48
    list_url = []
    result = {}

    for cat_id in list_cat_id:
        url = 'https://tiki.vn/api/v2/landingpage/products?category_id=' + str(cat_id) + '&limit=' + str(limit) + '&sort=discount_percent,desc&page=1'
        list_url.append({
            'url': url
        })

    list_data = loop.run_until_complete(async_request_aio_http(list_url))

    for item in list_data:
        item = json.loads(item)
        total_paging = item['paging']['total']
        aggregations = item['aggregations']
        cat_parent_id = aggregations['category']['values'][0]['parent_id']

        result[str(cat_parent_id)] = total_paging

    return result


def get_all_url(list_cat_id, list_total_page):
    limit = 48
    results = []
    result = {}
    max_page = 200

    for cat_id in list_cat_id:
        paging = list_total_page[cat_id]
        total_page = int(paging / limit)

        for i in range(total_page):
            if i > max_page:
                break

            url = "https://tiki.vn/api/v2/landingpage/products?category_id=" + str(cat_id) + \
                  "&limit=48&sort=discount_percent,desc&page=" + str(i+1)

            result = {
                'url': url
            }

            results.append(result)

    return results


def handle_data(datas):
    results = []
    result = []
    arr_price = {}

    percent = 80

    for data in datas:
        data = json.loads(data)

        if 'data' not in data:
            continue

        items = data['data']

        if 'aggregations' not in data:
            continue

        cat_id = data['aggregations']['category']['values'][0]['parent_id']

        if len(items) == 0:
            continue

        for item in items:
            discount = item['discount_rate']

            if int(discount) >= percent:

                id_product = item['id']
                price = item['price']

                seller_product_id = item['seller_product_id']
                info = get_info(item, discount, cat_id)

                url_check = "3__" + str(id_product) + "__" + str(seller_product_id)

                result.append({
                    'url': "https://apiv2.beecost.com/ecom/product/history?product_base_id=" + url_check,
                    'data_info': info
                })

                arr_price[str(id_product)] = price

    return [results, arr_price]


def check_item_is_error(data, price_current):
    data = json.loads(data)
    arr = []

    if 'data' not in data or data['data'] is None:
        arr = []

    if 'item_history' not in data['data']:
        arr = []

    data = data['data']['item_history']['price']

    for item in data:
        arr.append(int(item))

    if len(arr) == 0:
        return False

    arr_price = arr

    if len(arr_price) == 0:
        return False

    time_repeat = arr_price.count(price_current)

    if time_repeat > 1:
        return False

    min_price = min(arr_price)

    if price_current > min_price:
        return False

    max_price = max(arr_price)

    if max_price < price_current + 100000:
        return False

    if int(price_current / max_price)*100 > 20:
        return False

    if price_current in arr_price:
        arr_price.remove(price_current)

    arr_price = sorted(arr_price)

    if arr_price[0] - price_current < 200000:
        return False

    return True


def main_func():
    category = get_category_id()
    list_cat_id = get_list_cat_id(category)
    list_total_page = get_list_total_page(list_cat_id)
    list_all_link = get_all_url(list_cat_id, list_total_page)

    data = loop.run_until_complete(async_request_aio_http(list_all_link[:1000]))
    time.sleep(1)

    data_handle = handle_data(data)
    list_price = data_handle[0]
    arr_list_price_item = data_handle[1]

    data_check_price_error = loop.run_until_complete(async_request_aio_http(list_price[:1000]))

    print(data_check_price_error[0])

    return
    # for item in category:
    #     handle(item)

    arr_handle = list(range(10))

    loop.run_until_complete(async_request_aio_http(arr_handle))


if __name__ == '__main__':
    ts = time.time()
    main_func()
    logging.info('Took %s', time.time() - ts)
    # while True:
    #     first_time = datetime.datetime.now()
    #     category = get_category_id()
    #     ts = time.time()
    #
    #     for item in category:
    #         handle(item)
    #
    #     logging.info('Took %s', time.time() - ts)
    #
    #     time.sleep(500)