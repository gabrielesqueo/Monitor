import datetime
import json
import time
import randomheaders
import requests
import urllib3
import discord
from bs4 import BeautifulSoup


INSTOCK = []
WEBHOOK = 'https://discord.com/api/webhooks/932678139954475049/uGfr_H1cFQcHYGTiDHFwz5NinD2hh6TNP1ThT64kL66AiIu2vjh5i7NhqkxX1naZtzgY'
tempowait = 1
tempoprecedente = 0
resettime = 86400
"""NON MANDA GLI AVVISI SU DISCORD"""
def test_webhook():
    data = {
        "username": 'ZalandoMonitor',
        "avatar_url": 'https://www.pngitem.com/pimgs/m/122-1223088_one-bot-discord-avatar-hd-png-download.png',
        "embeds": [{
            "title": "Testing Webhook",
            "description": "This is just a quick test to ensure the webhook works. Thanks again for using these monitors!",
            "color": int('15258703'),
            "footer": {'text': 'Zalando Monitor'},
            "timestamp": str(datetime.datetime.now())
        }]
    }
    res= requests.post(WEBHOOK, data=json.dumps(data), headers={'Content-Type':'application/json'})

def monitor():
    global INSTOCK
    headers = randomheaders.LoadHeader()
    try:
        res = requests.get(url='https://www.zalando.it/sneakers-basse-uomo/__taglia-40.40~5.41.42.42~5.43.44~5.45.45~5.46/?q=air+force+1', headers=headers, verify=False)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'lxml')
            products = soup.find_all('div', attrs={'class': 'kpgVnb w8MdNG cYylcv QylWsg _75qWlu iOzucJ JT3_zV DvypSJ'})
            for product in products:
                try:
                    article = product.find('article')
                    item = [
                        article.find('h3').text,  # name
                        article.find('a')['href'],  # url
                        article.find('span', attrs={'class':'u-6V88 ka2E9k uMhVZi FxZV-M Kq1JPK pVrzNP ZkIJC- r9BRio qXofat EKabf7 nBq1-s _2MyPg2'}).text,# brand
                        article.find('span', attrs={'class':'u-6V88 ka2E9k uMhVZi FxZV-M _6yVObe pVrzNP cMfkVL'}).text,  # price
                        article.find('img')['src']  # image
                    ]
                    trovato = False
                    for items in INSTOCK:
                        if item[0] == items[0]:
                            trovato = True
                    if trovato == False:
                        discord.discord_webhook(item)
                        INSTOCK.append(item)
                except Exception as e:
                    pass
        else:
            monitor()
    except Exception as e:
        pass

def main():
    global tempoprecedente, INSTOCK
    counter = 0
    while True:
        counter += 1
        time.sleep(tempowait)
        urllib3.disable_warnings()
        monitor()
        if counter > resettime:
            INSTOCK = []


test_webhook()
main()
