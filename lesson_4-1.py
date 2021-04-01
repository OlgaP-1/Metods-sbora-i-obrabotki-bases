# Нельзя использовать BeautifulSoup!
# Используйте lxml, requests, pymongo
# 1) Написать приложение, которое собирает основные новости с сайтов news.mail.ru,
# lenta.ru, yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать:
# - название источника,
# - наименование новости,
# - ссылку на новость,
# - дата публикации
#
# 2) Сложить все новости в БД(MongoDB)
from lxml import html
import requests
from pprint import pprint
import datetime
from pymongo import MongoClient


def get_value(elem):
    if len(elem) > 0:
        return elem[0]
    return elem

def mail():
    url_mail = 'https://news.mail.ru/'
    x_string = ['//li[contains(@class, "list__item")]', '//div[contains(@class, "daynews")]//a',
                '//div[contains(@class, "cols__column")]//a[contains(@class, "newsitem__title")]']
    r = requests.get(url_mail, headers)
    s = r.text
    doc = html.fromstring(s)
    elem1 = doc.xpath(x_string[0])
    elem2 = doc.xpath(x_string[1])
    elem3 = doc.xpath(x_string[2])
    for i, el in enumerate(elem1):
        info = {}
        info['source'] = url_mail
        info['name'] = get_value(el.xpath('.//text()')).replace('\xa0', ' ')
        info['link'] = get_value(el.xpath('.//@href'))
        info['date'] = str(datetime.datetime.now())
        news.append(info)
    for i, el in enumerate(elem2):
        info = {}
        info['source'] = url_mail
        info['name'] = get_value(el.xpath('./span//text()')).replace('\xa0', ' ')
        info['link'] = get_value(el.xpath('.//@href'))
        info['date'] = str(datetime.datetime.now())
        news.append(info)
    for i, el in enumerate(elem3):
        info = {}
        info['source'] = url_mail
        info['name'] = get_value(el.xpath('.//text()')).replace('\xa0', ' ')
        info['link'] = get_value(el.xpath('.//@href'))
        info['date'] = str(datetime.datetime.now())
        news.append(info)
    return news

def lenta():
    url_lenta = 'https://lenta.ru'
    x_string = '//div[contains(@class, "item")]//h3'
    r = requests.get(url_lenta, headers)
    s = r.text
    doc = html.fromstring(s)
    elem = doc.xpath(x_string)
    for i, el in enumerate(elem):
        info = {}
        info['source'] = url_lenta
        info['name'] = get_value(el.xpath('.//text()')).replace('\xa0', ' ')
        info['link'] = url_lenta + get_value(el.xpath('.//a/@href'))
        info['date'] = str(datetime.datetime.now())
        news.append(info)
    return news

def yandex():
    url_yandex = 'https://yandex.ru/news'
    x_string = '//div[contains(@class, "mg-card__text")]//a'
    r = requests.get(url_yandex, headers)
    s = r.text
    doc = html.fromstring(s)
    elem = doc.xpath(x_string)
    for i, el in enumerate(elem):
        info = {}
        info['source'] = url_yandex
        info['name'] = get_value(el.xpath('.//text()')).replace('\xa0', ' ')
        info['link'] = get_value(el.xpath('.//@href'))
        info['date'] = str(datetime.datetime.now())
        news.append(info)

    return news

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45'
headers = {
    'User-Agent': user_agent}
news = []

mail = mail()
lenta = lenta()
yandex = yandex()

client = MongoClient('mongodb://localhost:27017/')
db = client['news']
news_gb = db.news_gb
news_gb.insert_many(news)
for new in news_gb.find({}):
    pprint(new)
