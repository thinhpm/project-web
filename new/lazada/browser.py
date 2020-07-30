from selenium.webdriver import Firefox
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import requests
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Browser:
    def __init__(self):
        self.driver = None


class FirefoxBrowser(Browser):
    def __init__(self, profile=""):
        super().__init__()
        self.profile = profile
        self.init_driver()

    def init_driver(self):
        options = Options()
        # options.add_argument("--headless")
        # profile = "C:\\Users\\noname\\Documents\\file\\firefox-profile\\j7nj8gnr.user1"

        self.driver = Firefox(executable_path="C:\\Users\\noname\\Documents\\file\\geckodriver.exe", firefox_options=options)

    def get_driver(self):
        return self.driver

    def stop(self):
        self.driver.close()
        self.driver.quit()


def un_verify(driver):
    time.sleep(1)
    driver.execute_script("document.getElementById('nc_2_n1z').style.left='500px'")
    time.sleep(2)
    action = ActionChains(driver)
    source_element = driver.find_element_by_id('nc_2_n1z')
    source_element2 = driver.find_element_by_id('nc_2__scale_text')
    action.drag_and_drop(source_element, source_element2)
    action.perform()
    time.sleep(1)


import requests

ff = FirefoxBrowser()
driver = ff.get_driver()
url = "https://www.lazada.vn/glorystar-official-store"
url2 = "https://www.lazada.vn/glorystar-official-store/?ajax=true&from=wangpu&langFlag=vi&page=2&pageTypeId=2&q=All-Products"
driver.get(url)
cookies = driver.get_cookies()

req = requests.Session()

for cookie in cookies:
    if len(cookie) == 0:
        continue

    req.cookies.set(cookie['name'], cookie['value'])
    req.cookies.set('domain', cookie['domain'])


import time
from selenium.webdriver.common.action_chains import ActionChains



max_discount = 80

arr_data = ['jettingbuy', 'lotte-mart', 'jvgood', 'uncle-bills', 'cheerfulhigh', 'bermoon', 'kapuko', 'leacat-store', 'oria', 'da-quy-thu-ngoc', 'monsa-official', 'mars-petcare', 'genyo', 'ganador-vietnam', 'minino-vietnam', 'navarch-petcare-store', 'sitto-viet-nam', 'hoang-khiem-cham-soc-thu-cung-cua-ban', 'nha-sach-fahasa', 'ielgy-official-store', 'midoctor-oficial', 'blesiya', 'reakids', 'teen-spirit', 'bbt-global-official', 'amalife-viet-nam', 'lego-shop-1', 'popo-collection', 'baoblade', 'tukeofficialstore', 'colormate1', 'baby-plaza-shop', 'drbike-official-store', 'diabrand-mall', 'wenno', 'vinatoy-nhua-cho-lon', 'boardgame-vn', 'orzbow-official-store', 'the-gioi-ti-hon-store', 'do-choi-go-benrikids', 'ohmnix-store', 'bitex-official-store', 'chicco-flagship-store', 'shop-minh-long-book', 'sunshine-distribution', 'dreamtok', 'hellokimi', 'kagonk-store', 'goodwayofficialstore', 'gau-bong-pipobun', 'do-choi-giao-duc-tedu', 'goldcat-vietnam-official-store', 'hinata-vietnam-official', 'hi-pencil-store', 'winfun-viet-nam', 'tinistore-1564371230', 'hay-yan-global', 'cua-hang-giay-patin-van-truot-scooter1582029215', 's-kids-viet-nam', 'polesie-viet-nam', 'light-coffee', 'unilever-cham-soc-gia-dinh-nang-tam-cuoc-song', 'dao-hai-san-flagship-store', 'nang-kho', 'julyhouse', 'thien-huong-foods', 'tam-duc-thien-official', 'thuc-pham-megadeli', 'vica-official', 'bot-cacao-chocolate-figo', 'orifood-vi-ngon-chuan-nha-hang', 'dk-harvest', 'no-brand-store-emart', 'hai-san-hasasa-flagship-store', 'the-kaffeine-coffee-green-food', 'thit-heo-thao-moc', 'mfood-viet-nam', 'vifon', 'covami', 'farmers-market-flagship-store', 'mk-farm', 'beauty-republic-store', 'toro-fresh-official-store', 'co-cu', 'trai-cay-dtpro-flagship-store', 'yummydeli', 'lothamilk-flagship-store', 'vietcoco', 'nam-an-market', 'nong-trai-sao-be', 'nosafood-official-store', 'king-car-viet-nam', 'phan-phoi-van-an', 'richy-food-store', 'gkitchen', 'heinz-vietnam', 'an-thai-viet-nam', 'hat-a-cafe', 'avn-viet-nam', 'vi-mall', 'foodmap-flagship-store', 'hai-san-va-thuc-pham-sach-soi-bien', 'smile-puzzle', 'oishi-viet-nam', 'kentary-official', 'mat-ong-phuc-khang', 'lotus-rice', 'dongtrunghathaodrtrung', 'hkfoods-official', 'ecolife-shop', 'banh-vang-pain-dore', 'ipp-flagship-store', 'heviefood', 'perfetti-van-melle-vietnam', 'langfarm-flagship-store', 'huong-que-tra-bong', 'king-coffee-viet-nam', 'idocean', 'want-want-flagship-store', 'yen-sao-winsnest', 'bibica-corporation', 'dakmark-foods', 'vinut', 'yen-sao-tien-thinh-phat', 'honee-coffee', 'viettin-mart-1593072786', 'happy-trade-shop', 'namsachricaflagshipstore', 'tan-tan1', 'trung-nguyen-legend', 'bidrico-official-store', 'ancofamilyfood', 'lai-phu-beverage', 'honeyboy', 'o-mai-van-huong-huong-vi-ha-thanh', 'shop-lock-lock', 'sweejar-official-store', 'kebeteme-official-store', 'oneisall-official-store', 'tam-house1', 'lidaco-bedding', 'deli-vietnam-official-store', 'sen-voi-thiet-bi-phong-tam-nha-bep-eurolife', 'ckeyin-store', 'flexoffice-thien-long-group', 'camdaglassco-1525339434', 'beautifulhome', 'beyours', 'tefal-flagship-store', 'metagio', 'myjae-official-experience-store', 'macaland-natural-cosmetic1586254059', 'woim-world-of-instrumental-music', 'banfang', 'dien-quang-lamp-store', 'oshima-vietnam', 'nagakawa-chinh-hang', 'homenhome-official-store', 'cat-thai', 'vioba-shop', 'yozo-official-store', 'do-da-thanh-long-tlg', 'kj', 'tomcityvn-1585112964', 'metermallofficialstore', 'noi-that-ngoc-thinh-68', 'amorus-digital-store', 'miniso-vietnam', 'vinahc-group-official', 'fivestar-store', 'alphabooks', 'kiotool', 'sofirnlight', 'comet-official-store', 'hobbyhomedecor', 'kokko-official-store', 'jomoo-flagship-store', 'migecon-official-store', 'vinabook-shop', 'zuiaich', 'dragonpad-official-store', 'zoqi-official-store', 'van-phong-pham-hong-ha-official', 'perfect-usa1', 'younik', 'erginioofficialstore', 'babyhop-official-store', 'yieryi-official-store', 'as-trading', 'thang-loi1', 'givasolar', 'goldsun1', '3m-flagship-store', 'shop-happy-cook', 'lioa-flagship-store', 'kkmoonofficialstore', 'suntek-official', 'myjae-vietnam', 'everso-homewater-store', 'inqmega', 'jysk-vietnam', 'milvusofficial', 'adidas-vietnam', 'supersports', 'ylong-shopping-mall', 'camel-international', 'cameljeansofficialstore', 'bg-vn-trading-coltd', 'highfly365', 'lining-flagship-store', 'benpai', 'rockbros-store1', 'sougayilang', 'pinkjoysofficialstore', 'zuucee', 'lyseacia-official-store', 'jointrip', 'loldeal-official-store', 'jayer', 'pinsv-official-store', 'inbikeflagshipstore', 'grand-sport-viet-nam', 'yoomee', 'fornix', 'west-biking', 'yonid', 'naimo', 'tourshofficialstore', 'victorinox-vietnam', 'one-step-one-footprint', 'qnt-vietnam', 'yozoh-official-store', 'cofoeofficialstore', 'ban-mai-official-store', 'pbh-outdoor', 'protec-helmet', 'pax-bikes', 'arr-fitness', 'mounchain', 'mung-leu-metta-official-store', 'johnson-johnson', 'bearleader', 'moc-dong-office-store', 'unilever-international', 'htlkid', 'wipro-unza-store', 'chiaus-official-store', 'hipp-store', 'purevess', 'pigeon-vietnam-official', '27kids-official-store', 'moony-vietnam', 'lozi-fashion', 'tin-an', 'toro-farm', 'patpat-flagship-store', 'diligo-shop', 'mamicare-viet-nam', 'kobi-flagship-store', 'hello-bb', 'philips-avent', 'max-cool', 'ienens', 'merries-store', 'tommee-tippee-vn', 'la-pomme-flagship-store', 'tokyolife', 'thivi-shop', 'mothercare-vietnam', 'mamamy-shop', 'babyupp', 'medela-viet-nam', 'kiddiezoomofficialstore', 'dorabe', 'likado-viet-nam', 'lovekids-viet-nam', 'diimuu', 'kokofit', 'dambauemum', 'babybean-official-store', 'vitadairy-official-store', 'kidloveofficialstore', 'pikatu-1580355789', 'az-mom-baby', 'v-baby-care', 'aoberst-viet-nam', 'nomad-pure', 'bellamys-organic', 'zcarevn', 'bambo-nature', 'duoc-pham-pharvina', 'muoi-giam-dau-co-truyen-bao-nhien', 'cham-soc-me-va-be-wonmom', 'mustela-vietnam-official', 'tuong-thanh-viet', 'ecostore-chinh-hang', 'baa-baby-official-store', 'mamypoko-vietnam', 'babycute-ta-vai-hien-dai', 'organicfood-flagship-store', 'baby-tattoo-gold', 'noi-tu-dong-cao-cap-autoru', 'sebamed-viet-nam', 'nutri-plus', 'beesmart1', 'dg-smartmom-vietnam', 'vietmat', 'myrica-official', 'lansinoh-official-store', 'as-goods-vietnam', 'gumac', 'shop-lata', 'fine-too', 'bee-gee-shop', 'rohto-mentholatum-vietnam', 'zanzea-official-store', 'isummerfashion', 'maybi-shop', 'hara-shop', 'skmei-flagship-store', 'ichoix-store', 'pigovietnam', 'kemstone-jewelry', 'levis-vn', 'laza-shopvn', 'louiswill', 'bitis', 'praza', 'skute-official-store', 'sezo', 'sunnies-studios', 'vincy-official-store', 'pixie-shop', 'chau-hoang-bach', 'maden-style', 'kojibavn', 'cindydrella123', 'sunpolo', 'sodrovjewelry', 'epi-jewelry', 'missky-official-store', 'azago-mall', 'hit-upon', 'ammin-official-store', 'dongzhu', '4u-official-store', 'vingo-vietnam', 'shondo', 'ariza-fashion', 'zocen', 'rozalo', 'anta-flagship-store', 'shop-ibasic', 'vanoca-1523533200', 'speranza', 'doreal-official-store', 'hoang-phuc-international-store', 'hapas-official', 'luxqloofficialstore', 'miley-lingerie', 'sabina', 'jojos-adventure', 'thoi-trang-eden', 'giordano-vietnam', 'inwpllr-official-store', 'h-h-p', '92wear-store', 'callia-fashion', 'fancystyle', 'sablanca-official-store', 'laneige-official-store', 'maccosmetics-flagship-store', 'loreal-paris-official-store', 'shu-uemura', 'senka-official-store', 'anessa-official-store', 'kiehls-official-store', 'maybelline-new-york-official-store', 'unilever-cham-soc-ve-dep', 'paulas-choice', 'estee-lauder-flagship-store', 'loreal-professionnel', 'la-roche-posay-official-store', 'innisfree-vietnam', 'mybeautymall', 'vichy-official-store', 'watsons-vietnam-official-store', 'xbeauty-official', 'saniye-office-store', 'lancome', 'bbia-official-store', 'bobbi-brown-flagship-store', 'maange-official-store', 'shiseido', 'rtopr-beauty-mall', 'sulwhasoo-flagship-store', 'unicharm-official-store', 'clinique-flagship-store', 'enchanteur-store', 'black-rouge-vietnam-official-store', 'olay-viet-nam', 'meiyanqiong', 'ckeyin-beauty-store', 'beauty-buffet-vietnam-1523440789', 'cham-soc-toc-pg', 'truesky-official-store', 'ofelia-viet-nam', 'tsubaki-official-store', 'revlon1', 'cetaphil-official-store', 'vedette-chinh-hang', 'eucerin', 'd-program', 'merzy-official-store', 'minimeli', 'tra-xanh-bao-loc-vu-gia', 'eglips', 'bioderma', 'lemonade', 'evoluderm1', 'thefaceshop1', 'dhc-viet-nam', 'ahc', 'essance-flagship-store', 'the-body-shop-viet-nam', 'venus-perfume-house', 'missha-official-store', 'choetech-flagship-store', 'ugreen-shop', 'swayofficialstore', 'hoco-store-viet-nam', 'duxducisofficialstore', 'goviz', 'glorystar-official-store', 'fengzhi-viet-nam', 'anker', 'ntech-electronic', 'baseusofficialstore', 'asanzo-vietnam', 'robot-official-store', 'ilepovn', 'supcase-official', 'fantech-flagship-store', 'viet-star-quoc-te-vn', 'imou-viet-nam', 'zeallion-official-store', 'pxn-official-store', 'pulierde-official-store', 'ezviz-official-store', 'ekleva-official-store', '4tech-official-store', 'puluzofficialstore', 'nillkin-flagship-store', 'viuioofficialstore', 'logitech-official-store', 'yongnuo-official-store', 'lenuo-official-store-1524534199', 'magicsee-official-store', 'svbony-official-store', 'essagerofficialstore', 'vp-canh-phong', 'hamrol-official-store', 'tp-link-official-store', 'heinler-viet-nam', 'daytech-1524533308', 'aula-official-store', 'joway', 'zuzgofficialstore', 'hp-flagship-store', 'tenda-official-store', 'aurum', 'escam-store', 'baseus-3c-boutique-store', 'depshock-official', 'apc-by-schneider-electric-flagship-store', 'selens-official-store', 'joyroom-global-store', 'hukey-official-store', 'asus-flagship-store', 'acasisofficialstore', 'delux-official-store', 'afesar-official-store', 'super-matche-digital-store', 'fdofficialstore', 'raxfly-3c-store', 'magegee-store', 'zg-flagship-store', 'akaso-official-store', 'kingston-vietnam', 'benq-viet-nam', 'victsingofficialstore', 'microlab-vn', 'zhiyun-official-store', 'sjcam-oficial-store', 'actto-official', 'wavlink-official-store', 'totolink-vietnam', 'blitzwolf-official-store', 'machenikeofficialstore', 'llano', 'vinetteam', 'selected-life', 'thinkpad-global-store', 'vention-viet-nam-1580524409', 'fd-flagship-store', 'ulanzi-official-store', 'acerglobalstore', 'fuhlen-vietnam', 'acehe', 'xiaomi-official', 'gutek-sieu-thi-dien-tu', 'colgate', 'panasonic-official-store', 'midea-viet-nam', 'green-cook-store', 'autobotflagshipstore', 'bluestone-vietnam', 'may-loc-nuoc-unilever-pureit', 'the-gioi-gaming', 'masuto-online-store', 'sunhouse-shop-online', 'karcher-vietnam', 'bunbea', 'hakawa', 'jisulife', 'venado-official', 'toshiba', 'yoobao-flagship-store', 'soocas-official-store', 'ad-official-store', 'gree-official-store', 'braun-shop-1559551969', 'mike-solove', 'deliya-official', 'haeger-official', 'may-cao-rau-flyco', 'deerma-official', 'kemei-viet-nam', 'kangaroo-shop', 'eufy', 'ubeator', 'ktg', 'sportsman-vn', 'dong-duong-sai-gon', 'robot-hut-bui-ecovacs', 'cty-tnhh-ca-phe-volcano', 'delonghiperfetto', 'flyco-viet-nam', 'arieteofficialstore', 'rang-dong-official', 'la-gourmet-official-store', 'aolon-official-store', 'elmich-flagship-store', 'kahchan', 'kagemaflagshipstore', 'cuckoo-store', 'arco-viet-nam', 'benks-official-store', 'bep-blue-star', 'supor-flagship-store', 'tiger-official-store', 'duxton-store', 'mosumflagshipstore', 'kachi-brand-shop', 'nam-thanh-viet-nam', 'aiomao-flagship-store', 'tamthienchico', 'the-gioi-do-choi-xe-may-anh-em-gia-nghiep', 'brt-viet-nam-official', 'caparies-retail-store', 'hetie-store', 'meguiars-viet-nam', 'bktec-akazu', 'giayhuyhoang', 'davis-shop', 'non-son1', 'dolphins-elife', 'galaxystore', 'retekess-flagship-store', 'shop-vietmap', 'jfg-racing', 'ridingtribestore', 'kocomo-dai-nhiet-giam-mo', 'tiencongfashions', 'focar-official', 'mai-lee-official-store', 'odomy-autoparts-store', 'non-bao-hiem-chita', 'nhot-thai-lan-nhap-khau', 'car365-viet-nam', 'iremax-vn', 'bluechem-bms', 'non-bao-hiem-srt', 'speed-way', 'caroline-viet-nam', 'wurth-vietnam', 'ptxm-yoko', 'bjmoto-racing-components', 'tavana', 'crazycarcity', 'vpc-petrochemical', 'atomiumvn', 'cong-ty-ntp', 'car-dvr-store', 'xethom', 'topdiagofficialstore', 'nasda', 'dau-nhot-npoil-1591666913', 'umidigi-official-store', 'wikomobile-viet-nam', 'huawei-official-store', 'cong-nghe-sao-viet', 'oukitelflagshipstore', 'realme-retail-store', 'vsmart-retail-store', 'apple-store', 'xiaomi-retail-store', 'electrical-official-mall', 'vivo-retail-store', 'samsung-official-store', 'oppo-retail-store', 'netcam', 'teclast-official-store', 'avita-official-store', 'chuwi-official-store', 'acer-flagship-store', 'wacom-store-1573195495', 'besder-official-store', 'spender-vn', 'camera-an-ninh-nhap-khau', 'loosafe-official-store', 'bakeey-official-store', 'kings-deal', 'wowholiday', 'du-lich-sai-gon-vip-tour', 'cattour', 'goldsport-millennium', 'red-river-tours', 'nha-hang-am-thuc-que-nha-1581392201', 'du-lich-dat-viet-1582185129', 'bamboo-airways', '7-ga', 'clip-tv-truyen-hinh-internet1585115545', 'elsa-speak-phat-am-tieng-anh-chuan-ban-xu', 'quy-hy-vong', 'life-fitness-yoga']

for item_data in arr_data:
    i = 0
    print(item_data)

    while True:
        time.sleep(1)
        if i > 12:
            break
        url2 = "https://www.lazada.vn/" + item_data + "/?ajax=true&from=wangpu&langFlag=vi&page=" + str(i+1) + "&pageTypeId=2&q=All-Products&sort=priceasc"
        print(url2)
        content = req.get(url2)
        html = content.text
        if 'nc_2_n1z' in html or 'rgv587_flag' in html or '/verify/' in html:
            print(html)
            driver.get(url)
            time.sleep(1)
            un_verify(driver)

            cookies = driver.get_cookies()

            req = requests.Session()

            for cookie in cookies:
                if len(cookie) == 0:
                    continue

                req.cookies.set(cookie['name'], cookie['value'])
                req.cookies.set('domain', cookie['domain'])
            time.sleep(2)

        data = json.loads(html)

        if 'mods' not in data or 'listItems' not in data['mods']:
            break

        list_item = data['mods']['listItems']

        for item in list_item:
            discount = 0

            if 'discount' in item:
                discount = item['discount']
                discount = discount.replace("%", "")
                discount = discount.replace("-", "")
                discount = int(discount)

            if discount >= max_discount:
                print(item)

        i += 1

