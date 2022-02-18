import datetime
import json
import time
import randomheaders
import requests
import urllib3
import discord
from bs4 import BeautifulSoup
import logging

logging.basicConfig(filename='ZalandoTutaMonitor.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.DEBUG)
INSTOCK = []
WEBHOOK = 'https://www.zalando.it/uomo/__taglia-43/?q=air+force+1'
tempowait = 2
resettime = 86400
session = requests.session()
counter = 0

def monitor():
    global INSTOCK, res, counter
    while True:
        time.sleep(tempowait)
        counter += 1
        try:
            headers = randomheaders.LoadHeader()
            try:
                res = session.get(url='https://www.zalando.it/giacche-zip-uomo/__taglia-M.S.XS/?q=Nike+Sportswear+HOODIE+-+Felpa+con+zip', headers=headers, verify=False, timeout=15)
            except Exception as e:
                logging.error(e)
            if res.status_code == 200:
                logging.debug ('%s', res.status_code)
                products = []
                try:
                    soup = BeautifulSoup(res.text, 'lxml')
                    products = soup.find_all('div', attrs={'class': 'kpgVnb w8MdNG cYylcv QylWsg _75qWlu iOzucJ JT3_zV DvypSJ'})
                except Exception as e:
                    logging.error(e)
                for product in products:
                    try:
                        article = product.find('article')
                        item = [
                            article.find('h3').text,  # name
                            article.find('a')['href'],  # url
                            article.find('span', attrs={'class':'u-6V88 ka2E9k uMhVZi FxZV-M Kq1JPK pVrzNP ZkIJC- r9BRio qXofat EKabf7 nBq1-s _2MyPg2'}).text,# brand
                            article.find('span', attrs={'class':'u-6V88 ka2E9k uMhVZi FxZV-M _6yVObe pVrzNP cMfkVL'}).text,  # price
                            article.find('img')['src'] , # imagepy
                        ]
                        trovato = False
                        for items in INSTOCK:
                            if item[0] == items[0]:
                                trovato = True
                        if trovato == False:
                            discord.discord_webhook(item)
                            INSTOCK.append(item)
                            logging.info(INSTOCK)
                    except Exception as e:
                        logging.error('%s', e)
            else:
                logging.debug ('%s', res.status_code)
        except Exception as e:
            logging.error('%s', e)
        if counter > resettime:
            INSTOCK = []
            counter = 0

def main():
        urllib3.disable_warnings()
        monitor()


main()
