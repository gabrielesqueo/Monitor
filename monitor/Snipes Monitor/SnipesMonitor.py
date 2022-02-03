import datetime
import json
import time
import randomheaders
import requests
import urllib3
import discord
from bs4 import BeautifulSoup

INSTOCK = []
WEBHOOK = 'https://discord.com/api/webhooks/928028413904715837/VtcJhOlm7Uh9SelBgb_t_ZWJ9klxFIcAHUwoQdKUj-FFsTbVponOpzdS7O_JFK0TAIEo'
tempowait = 1
resettime = 86400

def test_webhook():
    data = {
        "username": 'SnipesMonitor',
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
        res = requests.get('https://www.snipes.it/c/shoes?srule=Standard&prefn1=brand&prefv1=jordan%7Cnike&prefn2=size&prefv2=43&openCategory=true&sz=48', timeout=50, headers=headers, verify=False)

        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'lxml')
            print (soup.find('title'))
            products = soup.find_all('div', attrs={'class': 'b-product-grid-tile js-tile-container'})
            for product in products:
                try:
                    articlestyle = None
                    articlestyle = product.find('div', attrs={"class":"b-product-tile-swatches b-carousel-slot js-plp-swatch-carousel"})
                    print (articlestyle)
                    if articlestyle != None:
                        item = [
                            product.find('span', attrs={'class':'b-product-tile-link js-product-tile-link'}).text,  # name
                            product.find('a')['href'],  # url
                            #Verificare i due qui sotto e capire come prendere l'articlestyle
                            #print(product.find('span', attrs={'class':'b-product-tile-brand b-product-tile-text js-product-tile-link'})['data-brand']),# brand
                            #print(product.find('span', attrs={'class':'b-product-tile-price-item'}).text),  # price
                            product.find('img')['src']  # image
                        ]
                        print (item)
                        trovato = False
                        for items in INSTOCK:
                            if item[0] == items[0]:
                                trovato = True
                        if trovato == False:
                            #Problema WebHook
                            discord.discord_webhook(item)
                            INSTOCK.append(item)
                            print (INSTOCK)
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

