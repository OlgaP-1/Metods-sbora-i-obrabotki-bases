# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

# def get_big_img_url(url):
#     return url.replace('/m/', '/b/').replace('/s/', '/b/')


class LeruamerlenItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    # (input_processor=MapCompose(get_big_img_url())
    _id = scrapy.Field()
    price = scrapy.Field()
    price_square = scrapy.Field()
    href = scrapy.Field(output_processor=TakeFirst())
    features = scrapy.Field()
    features_keys = scrapy.Field()
    dic = scrapy.Field()

