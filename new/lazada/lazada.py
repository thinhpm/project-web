import requests
import time
import json


custom_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "referer": "https://www.lazada.vn/shop/glorystar-official-store?path=product.htm&hideHeadFoot=true&hybrid=1"
}


def test():
    global custom_headers
    url = "https://www.lazada.vn/glorystar-official-store/?ajax=true&from=wangpu&langFlag=vi&page=2&pageTypeId=2&q=All-Products"

    header = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7",
        "cookie": "t_fv=1590202392478; t_uid=Zw6rQixXjFDUTvq8USm4igZ7YyRc1Nrc; t_sid=iCAfT1Okt3noCd8SrG8ktAwXtaZZqMlK; utm_channel=NA; cna=FbNOFyVZVUYCAavwhELf4LPb; lzd_sid=1feb97095f6b1dbc6edec48ab7224a49; _tb_token_=ed5eb6457071e; lzd_cid=fa5e771f-abdf-4391-8dab-1e2df22bb238; hng=VN|vi|VND|704; userLanguageML=vi; _fbp=fb.1.1590202405609.228283958; _bl_uid=88k1gavkjw51Utg7gdbe40e1Up9s; _m_h5_tk=694d9f0367f485f502436d0e8904359b_1590209965031; _m_h5_tk_enc=61088dadd90089dc8d14aeca56f55397; _ga=GA1.2.1500165588.1590202406; _gid=GA1.2.78327788.1590202406; x5sec=7b22617365727665722d6c617a6164613b32223a223834623137376633326233663861646338363033616163663339613364663132434c6d756f765946454f7279722f792f3376547249673d3d227d; _gat_UA-30172376-1=1; JSESSIONID=9F19CE59AF15D7E18E82284F553F03F9; _uetsid=6bda74fe-f3e6-5272-b3cc-8d579440f242; l=eBa2A58cQ3eUmwrUBO5alurza77T1QObzsPzaNbMiInca6ZlTeAEnNQD6-Zk7dtjQt5fAetzEdARfRFXzo438x6IwIYApi6IYfveRe1..; isg=BFJSDLA8WCUhPaSm9hqBqi8Woxg0Y1b9ouv5pxyoFoXUL_ApBPYYDF0Jn5MTX86V",
        "referer": "https://www.lazada.vn/glorystar-official-store/?from=wangpu&langFlag=vi&page=2&pageTypeId=2&q=All-Products",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "x-csrf-token": "587af1ef5331e",
        "x-requested-with": "XMLHttpRequest",
        "x-ua": "123#OdJDbdqZCaQu+6bxlDl28ldEzQXHO1A9926XiGEXJz/HzaHKD/HbkbLYsAZjca13Y6jKCWBA/0s5my+ozO4vurg+qWv+okHh++Rl9MHbPrZnNIHwaiyJTZ3/QTUkdCFuUHjnFfV9eWP5ZsBbERxFq6YQDNNCSAFfLXK807imQTA/9wuQy0nq94n6QuM334f9svpq7zE1WTkRpM9ZqvoHGDydj27vVxuH7Kc7JfJEx+GNv7kTJjxJvc5MnuwT870HT+XGIk+H7pCFcVlEsGjWvEOeuQDqIG3fBaiBD2iGDiFU0ib+ZuPDyedZ5Jbv3B6Fe/YlSpQPZ3SSrRUzjih/nHI2ULnV1Pbjta6H4CVveTohZ8t1hsOVDHRjghE7+mnE/Cw4+w4zZj1JWNrYkQmRoTj7zJ2ivpVJcK/0whXPubnyK7csZLl/TupnEtfH9Uf457fWwnis08PMpWtXjeJ29j9uLKwnr+eTMuQil1LZgA4JWfViDI5zT9C7zCOVFFxZUgO1jNqlmJFt5QCEY/QWxtfSPYBsm3CLAG+kshLTB8inO4Wf6E40henhbMaliivE2IRiBq9nuO7oBcg6lWUD+zPL4HBb0+Z9RZMeiVxkrCesiULjw08xfXzRajMLQ6Wy8E7lUsvTfO/cm2PqUaHXVNbB27NCHcnI9praz0gk2vSEDbP3NMeZ5CebXFXWvoFa/OynLA1lVVMz/4U/ysKegHI00uh/GgtebQtdz/608MgXvory8OUgHi2ac5p8O6dLBrtpRu7TSGObaDFlZIAtl1StRYK43HYqrKuhuAJR58nI0caXxy/sxPWc4u0s+cTK+PCmbXr4DCmEpXt=",
        "x-umidtoken": "TBBD4648EBAFBDF6C3974C8F7F791F222CBB2EBE71A4FF16261F86B3819"
    }


    req = requests.get(url, headers=header)
    req.close()
    result = json.loads(req.content)

    print(result)
