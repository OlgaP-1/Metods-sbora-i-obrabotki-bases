import pymongo
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://localhost:27017/')
db = client['HH']
collection_vacancy = db['vacancy']

salary = int(input('Введите желаемый уровень зарплаты: '))
count = collection_vacancy.count_documents({"$or":[ {"salary.salary min": {"$gte": salary}}, {"salary.salary max": {"$gte": salary}}]})
print(f'Найдено {count} вакансий соответствующих условию поиска')
for work in collection_vacancy.find({"$or":[ {"salary.salary min": {"$gte": salary}}, {"salary.salary max": {"$gte": salary}}]}):
    pprint(work)