# импортируем библиотеку для входа на сайт через нажатие Enter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pprint import pprint
from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
import requests
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException

def bs_post():
    page = 0
    for d in posts_vk:
        info = {}
        try:
            try:
                text_post = d.find(attrs={'class': 'wall_post_text'}).text
            except AttributeError:
                text_post = None
            try:
                date = d.find('span', attrs={'class': 'rel_date'}).text.replace('\xa0', ' ')
            except AttributeError:
                date = None
            try:
                href = d.find(attrs={'class': "wall_post_text"}).get('href')
            except AttributeError:
                href = None
            try:
                link_post = d.find(attrs={'class': "post_link"}).get('href')
            except AttributeError:
                link_post = None
            try:
                like = d.find(attrs={'class': 'like_button_count'}).text
            except AttributeError:
                like = None
            try:
                share = d.find(attrs={'class': "like_btn share _share"}).text[1]
            except AttributeError:
                share = None
            try:
                views = d.find(attrs={'class': 'like_views _views'}).text
            except AttributeError:
                views = None
            info['text_post'] = text_post
            info['date'] = date
            info['href'] = href
            info['link_post'] = link_post
            info['like'] = like
            info['share'] = share
            info['views'] = views
            posts.append(info)
            page += 1
            print(page)
            print(info)
            time.sleep(30)
            search_2.send_keys(Keys.END)
        # в случае появления окна, всплывет ошибка, которую ликвидирую с помощью нажатия на кнопку "не сейчас"
        except ElementNotInteractableException:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "JoinForm__notNow")]'))).click()
            continue
    return posts

posts = []
# .env должен лежать рядом со скриптом и хранить в себе эти поля (Email, Password)
url = 'https://vk.com/tokyofashion'
# user_search = input("Введите запрос поиска: ")
user_search = 'синий'
DRIVER_PATH = './edgedriver_win64/msedgedriver'
driver = webdriver.Edge(DRIVER_PATH)
driver.get(url)
search = driver.find_element_by_id('wall_search')
search_2 = WebDriverWait(driver, 9).until(
    EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "ui_tab_plain ui_tab_search")]')))

proxies = {'http': 'http://81.177.73.17'}
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45'
headers = {
    'User-Agent': user_agent}
res = requests.get(url, headers=headers, proxies=proxies)
soup = bs(res.text, 'html.parser')
posts_vk = soup.find_all(attrs={'class': 'post_info'})
time.sleep(15)
search_2.send_keys(Keys.ENTER, user_search, Keys.RETURN, Keys.ENTER)

bs_post()

client = MongoClient('mongodb://localhost:27017/')
db = client['VK_tokyofashion_posts']
post_gb = db.post_gb
post_gb.insert_many(posts)
for new in post_gb.find({}):
    pprint(new)
