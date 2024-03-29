import datetime
import json
import time
import randomheaders
import requests
import urllib3
import discord
from bs4 import BeautifulSoup
import logging
import telebot

logging.basicConfig(filename='ZalandoMonitor.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.DEBUG)
INSTOCK = []
tempowait = 2
resettime = 86400
session = requests.session()
counter = 0
bot = telebot.TeleBot("5040856399:AAHgRISs2zYBdewTCAnfuC3RaZTvYSXTcQU")

def monitor():
    global INSTOCK, res, counter
    while True:
        time.sleep(tempowait)
        counter += 1
        try:
            headers = randomheaders.LoadHeader()
            try:
                logging.info('pre-request')
                res = session.get(url='https://www.zalando.it/sneakers-uomo/__taglia-38.38~5.39.40.40~5.41.42.42~5.43.44/?q=air+force+1', headers=headers, verify=False, timeout=15)
                logging.info('post-request')
            except Exception as e:
                logging.error(e)
            if res.status_code == 200:
                logging.debug ('%s', res.status_code)
                products = []
                try:
                    logging.info('pre-soup')
                    soup = BeautifulSoup(res.text, 'lxml')
                    logging.info('post-soup')
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
                            msg = f'{item[0]}\nFastLink= {item[1]}'
                            bot.send_message(chat_id='@testZalando', text=msg)
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
