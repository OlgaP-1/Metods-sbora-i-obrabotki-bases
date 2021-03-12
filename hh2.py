# !/usr/bin/python
# -*- coding: utf-8 -*-

import time
import pickle
from random import random
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# class HHparser:
#     def __init__(self, start_url, retry_number, sleep):
#         self.start_url = start_url
#         self.retry_number = retry_number
#         self.sleep = sleep
#         # TODO
#         self.headers = {}
#         pass
#
#     @staticmethod
#     def _get(self, *args, **kwargs):
#         for i in range(self.retry_number):
#             try:
#                 response = requests.get(*args, **kwargs)
#                 if response.status_code != 200:
#                     raise Exception("Status code != 200")
#                 return response
#             except:
#                 time.sleep(self.sleep)
#         return None
#
#     def run(self):
#         r = self._get(self.start_url, headers=self.headers)
#         pass
#
#     def save_pickle(o, path):
#         with open(path, 'wb') as f:
#             pickle.dump(o, f)
#
#     def load_pickle(path):
#         with open(path, 'rb') as f:
#             return pickle.load(f)
#
#     def get(url, headers, params, proxies):
#         r = requests.get(url, headers=headers, params=params, proxies=proxies)
#         return r
#
#     def bacspace_no(path):
#         for i in path:
#             l = ['&', 'n', 'b', 's', ' ']
#             if i == l:
#                 path = path.remove(i)
#             else:
#                 pass
#         return path
#
#     def next_url(page):
#         page = soup.find(attrs={'class': 'HH-Pager-Controls-Next'}).get('href')
#         while page == False or page == None or page == 0:
#             p_1 = 'https://hh.ru'
#             url = p_1 + page
#             time.sleep(0.5 + random.random(1, 15))
#
#     def parse(self):
#         pass
#
#     def save(self):
#         pass
#
#
# if __name__ == "__main__":
#     # TODO
#     start_url = ""
#     parser = KinopoiskParser(start_url, 5, 1)
#


def save_pickle(o, path):
    with open(path, 'wb') as f:
        pickle.dump(o, f)


def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


def get(url, headers, params, proxies):
    r = requests.get(url, headers=headers, params=params, proxies=proxies)
    return r


def bacspace_no(path):
    for i in path:
        l = ['&', 'n', 'b', 's', ' ']
        if i == l:
            path = path.remove(i)
        else:
            pass
    return path


# def next_url(page):
#     page = soup.find(attrs={'class': 'HH-Pager-Controls-Next'}).get('href')
#     while page == False or page == None or page == 0:
#         p_1 = 'https://hh.ru'
#         url_n = p_1 + page
#         time.sleep(0.5 + random.random(1, 15))
#     return url_n

url = 'https://hh.ru/search/vacancy'
us_vacancy = input('Введите должность для поиска вакансий: ')

params = {
    'area': 1,
    'fromSearchLine': 'true',
    'st': 'searchVacancy',
    'text': us_vacancy
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45'
}
proxies = {
    'http': 'http://79.164.27.240',
    # 'http': 'http://198.199.86.11',
    # 'https': 'https://165.227.223.19:3128',
}
r = get(url, headers, params, proxies)

path = "hh_2.csv"
save_pickle(r, path)
r = load_pickle(path)
soup = bs(r.text, 'html.parser')
vacancy_info = soup.find_all(attrs={'class': 'vacancy-serp-item'})

# d = soup.find_all(attrs={'class': 'vacancy-serp-item'})


# dd = soup.find(attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
# # dd = 'от 80 000 до 90 000 руб.'
#
# print(dd)
# min_sal = d.find('от')


vacancy = []

for d in vacancy_info:

    info = {}
    name = d.find(attrs={'class': 'HH-VacancyActivityAnalytics-Vacancy'}).text
    salary = d.find(attrs={'class': 'vacancy-serp-item__sidebar'}).text
    salary_min = None
    salary_max = None
    if salary.startswith('от'):
        salary_min = salary[3:-1]
        bacspace_no(salary_min)

    elif salary.startswith('до'):
        salary_max = salary[3:-1]
        bacspace_no(salary_max)

    else:
        s = salary.split('-')
        salary_min = s[0]
        salary_max = s[-1]
        bacspace_no(salary_max)
        bacspace_no(salary_min)

    employer = d.find(attrs={'class': 'bloko-link_secondary'}).text
    href = d.find(attrs={'data-qa': "vacancy-serp__vacancy-title"}).get('href')
    ''' ссылку достала, но почему-то она отражается не корректно только - /, поэтому решила 
     пойти другим путем и взяла за основу href'''
    # website = soup.find(attrs={'class': 'supernova-logo-wrapper'}).get('href')
    website = href[0:13]
    info['name'] = name
    info['employer'] = employer
    info['min_salary'] = salary_min
    info['max_salary'] = salary_max
    info['href'] = href
    info['website'] = website

    vacancy.append(info)

page = soup.find(attrs={'class': 'HH-Pager-Controls-Next'}).get('href')
p_1 = 'https://hh.ru'

# if page == None or page == 0:
#     pass
# else:
#     next_url = p_1 + page
b = []
# while page is not None or page == False or page == 0:
#     page = soup.find(attrs={'class': 'HH-Pager-Controls-Next'}).get('href')
#     b.append(page)
# else:
#     pass
# while page is None or page == False or page == 0:
if page is not None:
    r = get(url, headers, params, proxies)
    save_pickle(r, path)
    r = load_pickle(path)
    soup = bs(r.text, 'html.parser')
    vacancy_info = soup.find_all(attrs={'class': 'vacancy-serp-item'})
    page = soup.find(attrs={'class': 'HH-Pager-Controls-Next'}).get('href')
    next_url = p_1 + page
    url = next_url
    l = []
    for i in range(1, 40):
        l.append(i)
    k = 1
    p = l[0:k]
    new_params = {
        'L_is_autosearch': 'false',
        'area': 1,
        'clusters': 'true',
        'enable_snippets': 'true',
        'text': us_vacancy,
        'page': p
    }
    params = new_params
    r = get(url, headers, params, proxies)
    save_pickle(r, path)
    r = load_pickle(path)
    soup = bs(r.text, 'html.parser')
    vacancy_info = soup.find_all(attrs={'class': 'vacancy-serp-item'})
    for d in vacancy_info:

        info = {}
        name = d.find(attrs={'class': 'HH-VacancyActivityAnalytics-Vacancy'}).text
        salary = d.find(attrs={'class': 'vacancy-serp-item__sidebar'}).text
        salary_min = None
        salary_max = None
        if salary.startswith('от'):
            salary_min = salary[3:-1]
            bacspace_no(salary_min)

        elif salary.startswith('до'):
            salary_max = salary[3:-1]
            bacspace_no(salary_max)

        else:
            s = salary.split('-')
            salary_min = s[0]
            salary_max = s[-1]
            bacspace_no(salary_max)
            bacspace_no(salary_min)

        employer = d.find(attrs={'class': 'bloko-link_secondary'}).text
        href = d.find(attrs={'data-qa': "vacancy-serp__vacancy-title"}).get('href')
        ''' ссылку достала, но почему-то она отражается не корректно только - /, поэтому решила 
         пойти другим путем и взяла за основу href'''
        # website = soup.find(attrs={'class': 'supernova-logo-wrapper'}).get('href')
        website = href[0:13]
        info['name'] = name
        info['employer'] = employer
        info['min_salary'] = salary_min
        info['max_salary'] = salary_max
        info['href'] = href
        info['website'] = website

        vacancy.append(info)
        k = k + 1
    else:
        pass

    # r = requests.get(url, headers=headers, params=params, proxies=proxies)
    # time.sleep(0.5 + random.random(1, 15))

import json

with open('hh_vacancy_2.json', "w", encoding='utf8') as f:
    json.dump(vacancy, f, indent=2, ensure_ascii=False)
import sys

# print(sys.getrefcount('hh_vacancy_2.json'), len('hh_vacancy_2.json'))
with open('hh_vacancy_2.json', "r", encoding='utf8') as read_f:
    d = json.load(read_f)

print(len(d))
print(r)
df=pd.read_csv('hh_2.csv', sep=',')
df.head()