import requests


proxy = {
    "http": "181.3.17.8:7071",
    "https": "181.3.17.8:7071"
}

# session = requests.Session()
#
# session.proxies = proxy

url = "http://api.myip.com"

req = requests.get(url, proxies=proxy)

print(req.content)