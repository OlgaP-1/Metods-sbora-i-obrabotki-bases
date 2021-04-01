# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pprint import pprint
import re
from pymongo import MongoClient

MONGO_URL = 'localhost:27017'

class JobparserPipeline:
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client['vacancy']

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        collection.update_one({item['href']: 'href'}, {'$set': item}, upsert=True)
        if spider.name == 'hhru':
            self.process_item_hh(item, spider.name)
        if spider.name == 'sjru':
            self.process_item_sj(item, spider.name)
        return item

    def process_item_hh(self, item, collection_name):
        vacancy = {
            'name': item['title'],
            'salary_min': self.get_hh_salary_min(item),
            'salary_max': self.get_hh_salary_max(item),
            'currency': self.get_hh_valuta(item),
            'href': f"https://hh.ru{item['href']}",
            'link': item['link']
            }
        return item, vacancy

    def get_hh_salary_min(self, item):
        if 'salary' not in item:
            return None
        salary = item['salary']
        if len(salary) < 2:
            return None
        if 'от ' in salary:
            return int(salary[1].replace(' ', '').replace('\xa0', ''))

    def get_hh_salary_max(self, item):
        if 'salary' not in item:
            return None
        salary = item['salary']
        try:
            if len(salary) < 2:
                return None
            if 'до ' or 'до' or 'до' or ' - ' or '-' in salary:
                return int(salary[1].replace(' ', '').replace('\xa0', ''))
        except ValueError:
            return int(salary[2].replace(' ', '').replace('\xa0', ''))

    def get_hh_valuta(self, item):
        if 'salary' not in item:
            return None
        salary = item['salary']
        if len(salary) < 2:
            return None
        if 'от ' in salary[0] and ' до ' in salary[2]:
            return salary[5].replace(' ', '').replace('\xa0', '')
        if 'от ' in salary[0]:
            return salary[3].replace(' ', '')

    def process_item_sj(self, item, collection):
        vacancy = {
            'name': item['title'],
            'salary_min': self.get_salary_sj_min(item),
            'salary_max': self.get_salary_sj_max(item),
            'currency': self.get_valuta_sj(item),
            'link': item['link'],
            'href': f"https://superjob.ru{item['href']}"
        }
        return item, vacancy

    def get_salary_sj_min(self, item):
        if 'salary' not in item:
            return None
        salary = item['salary']
        if len(salary) < 2:
            return None
        if 'от' or 'от ' in salary:
            return int(re.sub('[^\d]', '', salary[2]))
        if len(salary) > 8:
            if salary[0] != 'от' or salary[0] != 'от ':
                return int(re.sub('[^\d]', '', salary[0]))
            if salary[0] == 'от' or salary[0] == 'от ':
                return salary[1]
        return int(re.sub('[^\d]', '', salary[0]))

    def get_salary_sj_max(self, item):
        if 'salary' not in item:
            return None
        salary = item['salary']
        if len(salary) < 2:
            return None
        if 'до' or ' до ' or ' до' not in salary:
            return int(re.sub('[^\d]', '', salary[2]))
        if len(salary) > 8:
            if salary[0] != 'от' or salary[0] != 'от ' or salary[0] != 'до' or salary[0] != 'до ' or salary[2] != '-':
                return int(re.sub('[^\d]', '', salary[0]))
            if salary[2] == 'до' or salary[2] == ' до ' or salary[2] == ' - ' or salary[2] == '-':
                return salary[4]

    def get_valuta_sj(self, item):
        if 'salary' not in item:
            return None
        salary = item['salary']
        if len(salary) < 2:
            return None
        if 'от' in salary:
            return re.sub('[\d\xa0\s]', '', salary[2])
        if 'до' not in salary:
            return re.sub('[\d\xa0\s]', '', salary[3])
        if len(salary) > 8:
            if salary[0] != 'от' or salary[0] != 'от ' or salary[0] != 'до' or salary[0] != 'до ' or salary[2] != '-':
                return int(re.sub('[^\d]', '', salary[2]))
            if salary[2] == 'до' or salary[2] == ' до ' or salary[2] == ' - ' or salary[2] == '-':
                return salary[6]
