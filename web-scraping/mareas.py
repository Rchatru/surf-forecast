#! /usr/bin/python3
"""
Created on Sun Mar 28 15:39:43 2021

@author: rrcht
"""

import pandas as pd
import time as tm
import requests
from bs4 import BeautifulSoup



################################################################################
                    ## Telegram Bot Alerts ##

def telegram_bot_sendtext(bot_message,disable_page_preview=True):
    
    bot_chatID = 'bot_chatID'
    bot_token = 'bot_token'


    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=MarkdownV2&text=' + bot_message + '&disable_web_page_preview=' + str(disable_page_preview)

    response = requests.get(send_text)

    return response.json()

################################################################################
my_header = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36", "X-Requested-With": "XMLHttpRequest" }
url = 'https://tablademareas.com/es/islas-canarias/los-cristianos-tenerife#_mareas'
page = requests.get(url,headers=my_header)
soup = BeautifulSoup(page.content,'html.parser')

job_elems = soup.find_all('div',class_='brujula_mareas_texto_pc grafico_estado_actual_texto2')

texto = job_elems[0].text.lower()
inicio = texto.find(' la')
fin = texto.find('mar')
primera = texto[inicio+4:fin+3].capitalize()

inicio = texto.find(' horas')
if inicio == -1:
    inicio = texto.find(' minutos')
    segunda = texto[inicio-2:inicio+8]
else:
    horas = texto[inicio-1:inicio+6]
    minut = texto.find(' minutos')
    if minut == -1:
        minutos=''
        segunda = horas        
    else:      
        minutos = texto[minut-2:minut+8]
        segunda = horas + ' y ' + minutos

mensaje2 = '_' + primera + ' en ' + segunda + '_'
   



html_page_text = requests.get('https://es.tideschart.com/Spain/Canary-Islands/Provincia-de-Santa-Cruz-de-Tenerife/Las-Galletas/',headers=my_header)
dfTables = pd.read_html(html_page_text.text,header=1,index_col=0)

mareas = dfTables[0]

mareas.drop(columns=['Unnamed: 6','Unnamed: 5'],inplace=True)
mareas = mareas.stack().str.replace('.',',').unstack()
mareas = mareas.stack().str.replace('▼',' ▼').unstack()
mareas = mareas.stack().str.replace('▲',' ▲').unstack()
mareas = mareas.stack().str.replace('-','\\-').unstack()

now = tm.localtime(tm.time())
dia = now.tm_mday


telegram_msg = telegram_bot_sendtext(""'''*Mareas Para Hoy*\n*1ºa:*  '''"" + str(mareas.iloc[0,0]) + ""''' \n*2ºa:*  '''"" + str(mareas.iloc[0,1]) + ""''' \n*3ºa:*  '''"" + str(mareas.iloc[0,2]) + ""''' \n*4ºa:*  '''"" + str(mareas.iloc[0,3]) + """\n""" + mensaje2 + """\n_[Fuente](https://es.tideschart.com/Spain/Canary-Islands/Provincia-de-Santa-Cruz-de-Tenerife/Las-Galletas/)_""")
print(telegram_msg)
