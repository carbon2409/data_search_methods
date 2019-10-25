import requests
from lxml import html
import pandas as pd
main_link = 'https://lenta.ru'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
req = requests.get('https://lenta.ru/', headers=headers).text
root = html.fromstring(req)
names_list = root.xpath('//div[contains(@class, "span4")]/div[@class="item"]/a/text()|//div[@class="first-item"]/h2/a/text()')
links = root.xpath('//div[contains(@class, "span4")]/div[@class="item"]/a/@href|//div[@class="first-item"]/h2/a/@href')
links_list=[]
for link in links:
    link = main_link + link
    links_list.append(link)
date_list = root.xpath('//div[contains(@class, "span4")]/div[@class="item"]/a/time/@datetime|//div[@class="first-item"]/h2/a/time/@datetime')
#Создадим список словарей
final_list = []
cycle = 0
lenta_data = {}
for n in range(len(names_list)):
    lenta_data['name'] = names_list[cycle]
    lenta_data['link'] = links_list[cycle]
    lenta_data['date'] = date_list[cycle]
    lenta_data['source'] = main_link
    final_list.append(lenta_data)
    lenta_data = {}
    cycle += 1
#Пишем код для Mail.ru
import datetime
now = str(datetime.datetime.now())
main_link_mail = 'https://mail.ru'
req_mail = requests.get('https://mail.ru/', headers=headers).text
root_mail = html.fromstring(req_mail)
names_list_mail = root_mail.xpath('//div[@class="news-item o-media news-item_media news-item_main"]/..//div/div/a[last()]/text()')
links_list_mail = root_mail.xpath('//div[@class="news-item o-media news-item_media news-item_main"]/..//div/div/a[last()]/@href')
date_list_mail = []
for n in range(len(names_list_mail)):
    date_list_mail.append(now)
#Добавляем в список словарей

mail_data = {}
cycle_mail = 0
for n in range(len(names_list_mail)):
    mail_data['name'] = names_list_mail[cycle_mail]
    mail_data['link'] = links_list_mail[cycle_mail]
    mail_data['date'] = date_list_mail[cycle_mail]
    mail_data['source'] = main_link_mail
    mail_data = {}
    cycle_mail += 1
    final_list.append(mail_data)
print(final_list)



