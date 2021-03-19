#!/usr/bin/env python
# coding: utf-8

# In[27]:


from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pickle
import re
import time
from tqdm import tqdm
import pandas as pd


# In[28]:


def save_pickle(o, path):
    with open(path, 'wb') as f:
        pickle.dump(o, f)

def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def get_j(url, headers, params, proxies):
    r = requests.get(url, headers=headers, params=params_j, proxies=proxies)
    return r

def salarys(salary):
    salary_min = []
    salary_max = []
    valut = []
    if (salary[0:] == 'по договоренности') == True:
        salary = 'по договоренности'
    elif salary.split('до'):
        for i in salary[0]:
            if i.isnumeric():
                salary_min.append(i)
            salary_min = ''.join(salary_min)
        '''после до: '''
        for j in salary[1]:
            if j.isnumeric():
                salary_max.append(j)
            salary_max = ''.join(salary_max)
            if j.isnumeric == False:
                valut.append(j)
            valut = ''.join(valut[3:6])
    else:
        salary_min = None
        salary_max = None
        valut = None
    return salary_min, salary_max, valut

def superjob(vacancy_info_j):
    time_to_sleep_when_captcha = 5
    vacancy = []
    for d in vacancy_info_j:
        try:
            info = {}
            name = d.find(attrs={'class': 'icMQ_ _6AfZ9'})['text']
            salary = d.find(attrs={'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).text
            salarys(salary)
            
            href = d.find(attrs={'class': "icMQ_ _6AfZ9"}).get('href')
            website = 'https://www.superjob.ru'
            employer = d.find(attrs={'class': 'icMQ_ _205Zx'}).text
            info['name'] = name
            info['employer'] = employer
            info['min_salary'] = salarys[0]
            info['max_salary'] = salarys[1]
            info['valuta'] = salarys[2]
            info['href'] = href
            info['website'] = website

            vacancy.append(info)
        except:
            time.sleep(time_to_sleep_when_captcha)
            time_to_sleep_when_captcha += 1
    return vacancy

# us_vacancy = input('Введите должность для поиска вакансий: ')
us_vacancy = 'python'
url_j = 'https://www.superjob.ru/vacancy/search/'
params_j = {'keywords': us_vacancy}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45'}
proxies = {'http': 'http://79.164.27.240'}
r_j = get_j(url_j, headers, params_j, proxies)

path = "hh_5.csv"

save_pickle(r_j, path)
r_j = load_pickle(path)
soup_j = bs(r_j.text, 'html.parser')

vacancy = []
vacancy_info_j = soup_j.find_all(attrs={'class': 'Fo44F'})

superjob(vacancy_info_j)
page_list = []
page_bloc = soup.find('div', attrs={'data-qa': "pager-block"}).find(attrs={'class': 'bloko-button HH-Pager-Control'})['href']
page_list.append('https://hh.ru' + page_bloc)
page_ran = [i for i in range(0, 40)]


is_true_j = True
page_ran_j = 1
while is_true_j or page_ran_j == None:
    time_to_sleep_when_captcha = 5
    bas_url = 'https://www.superjob.ru/vacancy/search/'
    params = {'keywords': us_vacancy,
              'geo%5Bt%5D%5B0%5D': 4,
              'page': page_ran_j}
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45'
    }
    proxies = {'http': 'http://81.177.73.17'}
    
    res = requests.get(bas_url, params=params, headers=headers, proxies=proxies)
    path = "hh_5.csv"
    save_pickle(res, path)
    res = load_pickle(path)
    soup = bs(res.text, 'html.parser')
    vacancy_info_j = soup.find_all(attrs={'class': 'vacancy-serp-item'})
    page = soup.find('a', {'rel': "next"})
    superjob(vacancy_info_j)
    
    for d in vacancy_info_j:
        
        info = {}
        name = d.find(attrs={'class': 'icMQ_ _6AfZ9'}).text
        salary = d.find(attrs={'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).text
        salarys(salary)
            
        href = d.find(attrs={'class': "icMQ_ _6AfZ9"}).get('href')
        website = 'https://www.superjob.ru'
        employer = d.find(attrs={'class': 'icMQ_ _205Zx'}).text
        info['name'] = name
        info['employer'] = employer
        info['min_salary'] = salarys[0]
        info['max_salary'] = salarys[1]
        info['valuta'] = salarys[2]
        info['href'] = href
        info['website'] = website

        vacancy.append(info)
        
        time.sleep(time_to_sleep_when_captcha)
        time_to_sleep_when_captcha += 1

    if page:
        page_ran_j += 1
    else:
        is_true = False
        break
    if page_ran_j != None:
        is_true = True
    else: 
        is_true = False
    time.sleep(1)        



# In[29]:


print(len(vacancy))
print(vacancy_info_j)


# In[26]:



read_csv('hh_5.csv')


# In[ ]:




