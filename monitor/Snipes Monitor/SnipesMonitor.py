import datetime
import json
import time
import randomheaders
import requests
import urllib3
import discord
from bs4 import BeautifulSoup

INSTOCK = []
WEBHOOK = 'https://discord.com/api/webhooks/932919093105917952/667uWD0eipNzB1TWjj11tGDj25SejJCdQVvGlHDMPh5h3e0FufHvzDLALYJ3N0Js7G1p'
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
        res = requests.get('https://www.snipes.it/c/shoes/sneaker/jordan%7Cnike?prefn1=size&prefv1=40%7C40.5%7C41%7C42%7C42.5%7C43%7C44%7C44.5%7C45%7C45.5%7C46&srule=Standard&openCategory=true&sz=48', headers=headers)
        #tutto da testare da qui
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'lxml')
            products = soup.find_all('div', attrs={'class': 'b-product-grid-tile js-tile-container'})
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
    global INSTOCK
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

