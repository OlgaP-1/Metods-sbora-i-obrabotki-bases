# import csv
# import json
# import pandas as pd
# import sys, getopt, pprint
# from pymongo import MongoClient
# from pprint import pprint
# # vacancy.json
# with open("D://Обучение//Базы//hh_4.csv", encoding='utf-8') as f:
#     # Создаем объект reader, указываем символ-разделитель ","
#     file_reader = csv.reader(f, delimiter=",")
#     # Счетчик для подсчета количества строк и вывода заголовков столбцов
#     count = 0
#     # Считывание данных из файла
#     for row in file_reader:
#         if count == 0:
#             # Вывод строки, содержащей заголовки для столбцов
#             pprint(f'Файл содержит: {", ".join(row)}')
#         else:
#             # Вывод строк
#             pprint(f'    {row[0]} - {row[1]} и он родился в {row[2]} году.')
#         count += 1
#     pprint(f'Всего в файле {count} строк.')


''' в csv должно быть то же самое, но там совсем что-то левое'''
# path = "D://Обучение//Базы//hh_4.csv"
# with open(path, 'rb') as f:
#   contents = f.read()
#
# pprint(contents)

import pymongo
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re
from datetime import datetime

client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')
db = client['HH']
collection_vacancy = db['vacancy']


main_link = "https://hh.ru/search/vacancy"
wanted_work = "Data Scientist"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45'
headers = {
    'User-Agent': user_agent
}
# функция выдергивания зарплаты из объявления
def find_salary(some_str):
    return_salary = {
        'salary min': None,
        'salary max': None,
        'currency': None
    }
    if some_str[0] == 'о':
        salary_min = re.findall(r"\d", some_str)
        currency = re.findall(r"\w*\S$", some_str)
        return_salary['salary min'] = int(''.join(salary_min))
        return_salary['currency'] = currency[0]
        return return_salary
    elif some_str[0] == 'д':
        salary_max = re.findall(r"\d", some_str)
        currency = re.findall(r"\w*\S$", some_str)
        return_salary['salary max'] = int(''.join(salary_max))
        return_salary['currency'] = currency[0]
        return return_salary
    else:
        try:
            index_tire = some_str.index('-')
            first_path = some_str[0:index_tire]
            second_path = some_str[index_tire:len(some_str)]
            salary_min = re.findall(r"\d", first_path)
            return_salary['salary min'] = int(''.join(salary_min))
            salary_max = re.findall(r"\d", second_path)
            return_salary['salary max'] = int(''.join(salary_max))
            currency = re.findall(r"\w*\S$", second_path)
            return_salary['currency'] = currency[0]
        except ValueError:
            return_salary = {
                'salary min': None,
                'salary max': None,
                'currency': None
            }
            return return_salary

        return return_salary
page = 0
i = True
matched = 0
modified = 0
upserted = 0
# устанавливаем дату обновления
date_now = datetime.now()
while i == True:
    params = {
        "clusters": "true",
        "enable_snippets": "true",
        "salary": "",
        "st": "searchVacancy",
        "text": wanted_work,
        "fromSearch": "true",
        "page": page
    }
    response = requests.get(main_link, params=params, headers=headers)
    soup = bs(response.text, 'lxml')
    vacancy_list = soup.find_all('div', {'class': 'vacancy-serp-item'})
    try:
        page_link = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})['href']
    except TypeError:
        i = False
    else:
        page = page_link[len(page_link)-1]
    for work in vacancy_list:
        vacansy = {
        'site': None,
        'link':None,
        'vacancy_name':None,
        'salary': {
            'salary min': None,
            'salary max': None,
            'currency': None
        }
    }
        site = re.findall(r"https:\/\/\S*\.\S{2,3}",main_link)
        vacansy['site'] = site[0]
        vacansy['link'] = work.find(attrs={'data-qa': "vacancy-serp__vacancy-title"}).get('href')
        vacansy['vacancy_name'] = work.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
        salary = work.find('div', {'class':'vacancy-serp-item__sidebar'}).text
        if len(salary) != 0:
            vacansy['salary'] = find_salary(salary)
        # обновляем вакансии, если такой нету то добавляем
        result = collection_vacancy.update_one(vacansy, {'$set':{
            'site': vacansy['site'],
            'link': vacansy['link'],
            'vacancy_name':vacansy['vacancy_name'],
            'salary': {
                'salary min': vacansy['salary']['salary min'],
                'salary max': vacansy['salary']['salary max'],
                'currency': vacansy['salary']['currency']
            },
            'date': date_now
        }}, upsert=True)
        if result.matched_count != 0:
            matched +=1
        if result.modified_count != 0:
            modified +=1
        if result.upserted_id != None:
            upserted +=1

print(f'Finded: {matched} documents')
print(f'Modified: {modified} documents')
print(f'Added: {upserted} documents')
# удаляем те вакансии которых нет на сайте
result = db.collection_vacancy.delete_many({"date": {"$lte": date_now}})
print(f'Удаленных вакансий: {result.deleted_count}')