import telebot
import callurl
TOKEN = "5040856399:AAHgRISs2zYBdewTCAnfuC3RaZTvYSXTcQU"


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 "Ciao, inserisci di seguito il link del prodotto Zalando che vuoi comprare.\nRiceverai uno sconto addizionale che varia dal 25% al 28%\nUtilizza il formato: \nhttp://url.com oppure https://url.com")


@bot.message_handler(func=lambda message: True)
def get_link(message):
    LINK = message.text.split()
    for links in LINK:
        if links.find('http') == -1:
            print('')
        else:
            prezzo = callurl.callurl(links)
            outputprezzo(message, prezzo)

def outputprezzo(message, prezzo):
    bot.reply_to(message, "Il prezzo scontato è: "+str(prezzo)+"€")




bot.polling()
