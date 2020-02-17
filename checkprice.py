import requests
import lxml
from lxml import html
import json


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
        root = self.my_requests('GET', url, None, 'html')
        script = root.xpath("/html/head/script[5]")[0].text
        print(script)


check_price = CheckPrice()
check_price.get_data_item_from_ssg("https://tiki.vn/smart-tivi-samsung-55-inch-4k-uhd-ua55nu7090kxxv-hang-chinh-hang-p3665301.html")