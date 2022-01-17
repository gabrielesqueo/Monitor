import bs4
import randomheaders
import requests
import random
def callurl(url):
    url= str(url)
    trovato = False
    while trovato == False:
        session = requests.session()
        headers = randomheaders.LoadHeader()
        res = session.get(url=url, headers=headers, allow_redirects=False)
        if res.status_code == 200:
            page = bs4.BeautifulSoup(res.text, 'lxml')
            prezzo = page.find('div', attrs={'class':'_0xLoFW vSgP6A _7ckuOK'})
            prezzo = str(prezzo).replace('[<span class="uqkIZw ka2E9k uMhVZi dgII7d _6yVObe _88STHx cMfkVL">','').replace('</span>','').replace('>',' ')
            prezzo = prezzo.split()
            for prezzounico in prezzo:
                prezzounico = str(prezzounico)
                if prezzounico.find(',') == -1:
                    print ('')
                else:
                    prezzounico = prezzounico.replace(',','.')
                    prezzofinale = float(prezzounico) - (float(prezzounico)*27)/100
                    prezzofinale = round(prezzofinale, 2)
                    return prezzofinale
        else:
            print('')

