import requests
import json
import time

result = []


def test():
    global result

    url = "https://www.lazada.vn/lenovo-official-flagship-store/?ajax=true&from=wangpu&langFlag=vi&page=2&pageTypeId=2&q=All-Products"
    url = "https://acs-m.lazada.vn/h5/mtop.lazada.mobile.lazmall.storelist.get/1.0/?jsv=2.4.11&appKey=24677475&t=1590380890829&sign=a0ea526de3060aacb7877a6e7b9aa8c8&api=mtop.lazada.mobile.lazmall.storelist.get&v=1.0&timeout=8000&x-i18n-language=vi&x-i18n-regionID=VN&dataType=json&type=originaljson&data=%7B%22language%22%3A%22vi%22%2C%22regionID%22%3A%22VN%22%2C%22deviceID%22%3A%22%22%2C%22platform%22%3A%22pc%22%2C%22pageSize%22%3A10%2C%22columnId%22%3A%221001%22%2C%22pageNo%22%3A0%2C%22isbackup%22%3Atrue%2C%22backupParams%22%3A%22language%2CregionID%2Cplatform%2CpageSize%2CcolumnId%2CpageNo%22%2C%22appId%22%3A%2220180501004%22%2C%22_pvuuid%22%3A1590380890668%2C%22terminalType%22%3A1%2C%22campBasicId%22%3A%22%22%7D"

    custom_headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7",
        "cache-control": "no-cache",
        "cookie": "miidlaz=miid5h33d91dobe19ie3c4f; lzd_cid=9f220e55-b285-44c1-9a26-38569ba405f7; t_uid=9f220e55-b285-44c1-9a26-38569ba405f7; t_fv=1572341853568; cna=XfY+ForxxjYCAbym5QPD1yuN; _ga=GA1.2.1709111452.1572341857; _fbp=fb.1.1572341856752.4950898; cto_lwid=9811733c-0bde-423d-b516-e8aab9e00379; pdp_sfo=1; Hm_lvt_7cd4710f721b473263eed1f0840391b4=1574333090,1575261383; ab.storage.deviceId.7f5273fc-4f97-4a9a-9f19-e816c0d197be=%7B%22g%22%3A%2244dd1c37-4a79-b203-c43d-e595cbcfe08b%22%2C%22c%22%3A1578017760010%2C%22l%22%3A1578017760010%7D; ab.storage.sessionId.7f5273fc-4f97-4a9a-9f19-e816c0d197be=%7B%22g%22%3A%2283974c63-3bf5-4b05-502c-9fd00f7d2ac9%22%2C%22e%22%3A1578019560017%2C%22c%22%3A1578017760006%2C%22l%22%3A1578017760017%7D; _fbc=fb.1.1585281683785.IwAR3-9GVVQYGu8IvIbjp9sqh2ntAFqG4mKkru0l0gsjlndAqZ0Sji_Fjx03o; hng=VN|vi|VND|704; userLanguageML=vi; _bl_uid=Lnk3k9d6jqFba1btyiqtykthCm1k; lzd_click_id=clk5hinju1e7mkjf86rhgk; _gac_UA-30172376-1=1.1589530206.Cj0KCQjw-_j1BRDkARIsAJcfmTHNKR2YUTlWNlQut0POY2sQOVGKxFUxOnFTltk7k1GplVKctnISKxEaAn3WEALw_wcB; lzd_sid=16788cd42428ea4a868ef8bb2c8da850; _m_h5_tk=644004107a58a6438290bc6487baf8b4_1590386994114; _m_h5_tk_enc=a707276ca1ad13fde2ba0f3285db602a; t_sid=JPUHIzfHays3LUZIaMzEjkqE5tLvujTN; utm_channel=NA; _tb_token_=e555830b33b78; _gid=GA1.2.1166866456.1590378362; _uetsid=12a35eda-f930-65fa-deea-42e761f80505; x5sec=7b22617365727665722d6c617a6164613b32223a226133393839666435613638313064323462396264303763336535336262626539434c66337250594645494c6679717a433364336865413d3d227d; JSESSIONID=C3CD83EA7D2463148A4A9AF82B5C6416; l=eBO308aIq3ErQvIwBO5Cnurza77TyIRb8sPzaNbMiInca18PT9IQENQDs1lp7dtjQt5cgetrdbEvZRFBz5ULyxZMCbhhYyCoNZJ68e1..; isg=BMHBOdxRe9uOk5Scm5hbmTSY0ATb7jXgP3uWQCMWAUj2CuDcazv3sEFM7GZMAs0Y",
        "pragma": "no-cache",
        "referer": "https://www.lazada.vn/lenovo-official-flagship-store/?from=wangpu&langFlag=vi&page=2&pageTypeId=2&q=All-Products",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "x-csrf-token": "e555830b33b78",
        "x-requested-with": "XMLHttpRequest",
        "x-ua": "123#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",
        "x-umidtoken": "TAA643D1E5AB4D486E8B3C01E9B657A020E56D9479C0688FBCA73C00E72",
    }

    session = requests.Session()

    req = session.get(url, headers=custom_headers, timeout=5)
    session.close()
    data = json.loads(req.content)

    datas = data['data']['resultValue']['20180501004']['data']

    for item in datas:
        shop_url = item['shopUrl']

        arr = shop_url.split("?")
        l1 = arr[0].split('/')

        name = l1[-1]
        if len(name) == 0:
            name = l1[-2]
        if name not in result:
            result.append(name)

# while True:
#     test()
#     print(result)


# result = ['thuc-pham-megadeli', 'shop-lata', 'maibenben-official-store', 'banh-vang-pain-dore', 'senka-official-store', 'logitech-official-store', 'zanzea-official-store', 'innisfree-vietnam', 'super-matche-digital-store', 'nang-kho', '4tech-official-store', 'acerglobalstore', 'tam-duc-thien-official', 'hp-flagship-store', 'lenovo-accessories', 'la-roche-posay-official-store', 'asus-official-store', 'foodmap-flagship-store', 'vichy-official-store', 'asus-official-flagship-store', 'tra-xanh-bao-loc-vu-gia', 'supersports', 'microsoft-official-store', 'vifon', 'midea-viet-nam', 'fd-flagship-store', 'ipp-flagship-store', 'lancome', 'victsingofficialstore', 'nestle-viet-nam', 'dk-harvest', 'laneige-official-store', 'fantech-flagship-store', 'rau-qua-hiep-nong-flagship-store', 'kiehls-official-store', 'machenikeofficialstore', 'covami', 'rohto-mentholatum-vietnam', 'ntech-electronic', 'glorystar-official-store', 'nivea-certified-store', 'tp-link-official-store', 'shondo', 'paulas-choice', 'aula-official-store', 'delux-official-store', 'fuller', 'heviefood', 'tada-foods', 'bee-gee-shop', 'light-coffee', 'lotus-rice']
#
# print(len(result))

#
# req = requests.get(url)
#
# print(json.loads(req.content))
test()