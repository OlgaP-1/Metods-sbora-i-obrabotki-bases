# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class InstagramParserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_id = scrapy.Field()
    name = scrapy.Field()
    photo = scrapy.Field()
    login = scrapy.Field()
    his_subscriptions = scrapy.Field()
    subscribers = scrapy.Field()
    user_to_srapy = scrapy.Field()

