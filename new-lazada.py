import requests
import json
import time

custom_headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7",
    "cache-control": "no-cache",
    "cookie": "miidlaz=miid5h33d91dobe19ie3c4f; lzd_cid=9f220e55-b285-44c1-9a26-38569ba405f7; t_uid=9f220e55-b285-44c1-9a26-38569ba405f7; t_fv=1572341853568; cna=XfY+ForxxjYCAbym5QPD1yuN; _ga=GA1.2.1709111452.1572341857; _fbp=fb.1.1572341856752.4950898; cto_lwid=9811733c-0bde-423d-b516-e8aab9e00379; pdp_sfo=1; Hm_lvt_7cd4710f721b473263eed1f0840391b4=1574333090,1575261383; ab.storage.deviceId.7f5273fc-4f97-4a9a-9f19-e816c0d197be=%7B%22g%22%3A%2244dd1c37-4a79-b203-c43d-e595cbcfe08b%22%2C%22c%22%3A1578017760010%2C%22l%22%3A1578017760010%7D; ab.storage.sessionId.7f5273fc-4f97-4a9a-9f19-e816c0d197be=%7B%22g%22%3A%2283974c63-3bf5-4b05-502c-9fd00f7d2ac9%22%2C%22e%22%3A1578019560017%2C%22c%22%3A1578017760006%2C%22l%22%3A1578017760017%7D; _fbc=fb.1.1585281683785.IwAR3-9GVVQYGu8IvIbjp9sqh2ntAFqG4mKkru0l0gsjlndAqZ0Sji_Fjx03o; hng=VN|vi|VND|704; userLanguageML=vi; _bl_uid=Lnk3k9d6jqFba1btyiqtykthCm1k; lzd_click_id=clk5hinju1e7mkjf86rhgk; _gac_UA-30172376-1=1.1589530206.Cj0KCQjw-_j1BRDkARIsAJcfmTHNKR2YUTlWNlQut0POY2sQOVGKxFUxOnFTltk7k1GplVKctnISKxEaAn3WEALw_wcB; lzd_sid=16788cd42428ea4a868ef8bb2c8da850; _tb_token_=e555830b33b78; _gid=GA1.2.1166866456.1590378362; XSRF-TOKEN=6087d651-3246-4379-b8b0-e3a25f2ef8b2; _m_h5_tk=4c4fb6ed1caa24a385b125e8ff4dc846_1590391120133; _m_h5_tk_enc=01602a9b07bc62c03c03d10029e0c579; t_sid=rz1Bzg9TJASt4pDVVjcP3FgANke6kXyd; utm_channel=NA; x5sec=7b22617365727665722d6c617a6164613b32223a223737663031333763353337643134396331393138316237613939656330396164434a626872665946454b37377a4e722f6d4a484355773d3d227d; JSESSIONID=38D3FF9865D890D362194FB8F9865F97; _gat_UA-30172376-1=1; _uetsid=12a35eda-f930-65fa-deea-42e761f80505; l=eBO308aIq3ErQVOXBOfZnurza77TtIRfguPzaNbMiOCPOBC1yWhcWZAGSc8BCnMNns5DJ3kIwoduBSTzry4ohmysxGYkJDU_3dTh.; isg=BDY2W28GdEqMrANd2NEkaEdxh2U4V3qRrILhQaAfa5nO49d9CeJ0oI3V-6ePy3Kp",
    "pragma": "no-cache",
    "referer": "https://www.lazada.vn/lenovo-official-flagship-store/?from=wangpu&langFlag=vi&page=2&pageTypeId=2&q=All-Products",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "x-csrf-token": "e555830b33b78",
    "x-requested-with": "XMLHttpRequest",
    "x-ua": "123#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",
    "x-umidtoken": "T9AF02FD544C0D6B6D8FF8E467EA26B8B1A89B35B5766875C6533E12E71",
}


def requests_find(shop_name):
    global custom_headers

    total_page = 2
    max_discount = 80

    for i in range(total_page):
        page = i + 1
        url = "https://www.lazada.vn/" + str(shop_name) + "/?ajax=true&from=wangpu&langFlag=vi&page=" + str(page) + "&pageTypeId=2&q=All-Products&sort=priceasc"

        req = requests.get(url, headers=custom_headers)

        time.sleep(1)

        result = json.loads(req.content)

        if 'listItems' not in result['mods']:
            continue

        data = result['mods']['listItems']

        for item in data:
            price = int(item['price'].replace(".00", ""))
            discount = 0

            if 'discount' in item:
                discount = item['discount']
                discount = discount.replace("%", "")
                discount = int(discount)*-1

            if discount >= max_discount:
                print(price)
                print(item['productUrl'])

arr = ['thuc-pham-megadeli', 'shop-lata', 'maibenben-official-store', 'banh-vang-pain-dore', 'senka-official-store', 'logitech-official-store', 'zanzea-official-store', 'innisfree-vietnam', 'super-matche-digital-store', 'nang-kho', '4tech-official-store', 'acerglobalstore', 'tam-duc-thien-official', 'hp-flagship-store', 'lenovo-accessories', 'la-roche-posay-official-store', 'asus-official-store', 'foodmap-flagship-store', 'vichy-official-store', 'asus-official-flagship-store', 'tra-xanh-bao-loc-vu-gia', 'supersports', 'microsoft-official-store', 'vifon', 'midea-viet-nam', 'fd-flagship-store', 'ipp-flagship-store', 'lancome', 'victsingofficialstore', 'nestle-viet-nam', 'dk-harvest', 'laneige-official-store', 'fantech-flagship-store', 'rau-qua-hiep-nong-flagship-store', 'kiehls-official-store', 'machenikeofficialstore', 'covami', 'rohto-mentholatum-vietnam', 'ntech-electronic', 'glorystar-official-store', 'nivea-certified-store', 'tp-link-official-store', 'shondo', 'paulas-choice', 'aula-official-store', 'delux-official-store', 'fuller', 'heviefood', 'tada-foods', 'bee-gee-shop', 'light-coffee', 'lotus-rice']

for shop_name in arr:
    requests_find(shop_name)
    # time.sleep(1)