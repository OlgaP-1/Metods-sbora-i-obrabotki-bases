# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.item import Item
import scrapy
import re
from pymongo import MongoClient

MONGO_URL = 'localhost:27017'

class LeruamerlenImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for photo_url in item['photos']:
                try:
                    yield scrapy.Request(photo_url)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [i[1] for i in results]
        # print()
        return item

class LeruamerlenPipeline:
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client['Leruamerlen']
        # по коду ниже под '#' парсинг не работает по не понятной причине
    	# def join_price(value):
    	# return float(''.join(value))
        
    def process_item(self, item, spider):
        item['price'] = ','.join(item['price'])
        item['price_square'] = ''.join(item['price_square'])
        item['dic'] = dict(zip(item['features_keys'], [re.sub(r'\s+', '', i.replace('\n', '')) for i in item['features']]))
        del [item['features']]
        del [item['features_keys']]
        
        collection = self.db[spider.name]
        collection.update_one({item['href']: 'href'}, {'$set': item}, upsert=True)
        return item
