import requests
import datetime
import json
def discord_webhook(product):
    webhook='https://discord.com/api/webhooks/928028413904715837/VtcJhOlm7Uh9SelBgb_t_ZWJ9klxFIcAHUwoQdKUj-FFsTbVponOpzdS7O_JFK0TAIEo'
    data = {
        "username": 'ZalandoMonitor',
        "avatar_url": 'https://www.pngitem.com/pimgs/m/122-1223088_one-bot-discord-avatar-hd-png-download.png',
        "embeds": [{
            "title": product[0],
            "url": product[1],
            "thumbnail": {"url": product[4]},
            "color": int('15258703'),
            "footer": {"text": "Zalando Monitor"},
            "timestamp": str(datetime.datetime.now()),
            "fields": [
                {"name": "Brand", "value": str(product[2])},
                {"name": "Price", "value": str(product[3])}
            ]
        }]
    }

    result = requests.post(webhook,data=json.dumps(data), headers={"Content-Type": "application/json"})