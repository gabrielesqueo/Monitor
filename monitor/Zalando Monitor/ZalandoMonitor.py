import datetime
import json
import time
import randomheaders
import requests
import urllib3
import discord
from bs4 import BeautifulSoup


INSTOCK = []
WEBHOOK = 'https://discord.com/api/webhooks/932667971514531941/-x3X9nQKTXEPNvrCxVwezsbQO5rjzwRy7Kkh3ld830M04CSdHJO1s6R38Oui7VPlYYUc'
tempowait = 1
resettime = 86400

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
        res = requests.get(url='https://www.zalando.it/uomo/__taglia-M.S.XS/?q=tuta+tech+nike', headers=headers, verify=False)
        if res.status_code == 200:
            print (res.status_code)
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
                        article.find('img')['src'] , # image
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
            print (res.status_code)
            monitor()
    except Exception as e:
        pass

def main():
    global  INSTOCK
    counter = 0
    while True:
        counter += 1
        time.sleep(tempowait)
        urllib3.disable_warnings()
        monitor()
        if counter > resettime:
            INSTOCK = []


#test_webhook()
main()
