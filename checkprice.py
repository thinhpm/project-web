import requests
import lxml
from lxml import html
import json
import re


class CheckPrice:
    custom_headers = {
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'"
    }

    def __init__(self):
        pass

    def my_requests(self, method='GET', url='', params=None, type_response='text'):
        if params is None or params == '':
            params = {}

        if method == 'GET':
            req = requests.get(url, data=params)
        else:
            req = requests.post(url, data=params, headers=self.custom_headers)

        if type_response == 'json':
            return json.loads(req.content)

        if type_response == 'html':
            return html.fromstring(req.content)

        return req.content

    def get_url_from_ssg(self, url_item):
        url = "https://www.sosanhgia.com/apiv2/embed"
        params = {"urlList": [url_item]}

        content = self.my_requests('POST', url, json.dumps(params), 'json')

        return content['url']

    def get_data_item_from_ssg(self, url_item):
        url = self.get_url_from_ssg(url_item)

        string_script = self.my_requests('GET', url, None, 'text')
        # string_script = root.xpath("/html/head/script[5]")[0].text

        data = re.findall(r'"data":\[\[(.*?)]],', str(string_script))

        if len(data) == 0:
            return []

        data = data[0]

        data = '[[' + data + ']]'
        data = json.loads(data)
        length_data = len(data)

        # arr = [data[length_data - 1][1], data[length_data - 2][1], data[length_data - 3][1], data[length_data - 4][1]]
        arr = []

        for i in range(len(data)):
            arr.append(data[i][1])

        return arr

    def check_item_is_error(self, url_item, price_current):
        arr_price = self.get_data_item_from_ssg(url_item)

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

        return True
