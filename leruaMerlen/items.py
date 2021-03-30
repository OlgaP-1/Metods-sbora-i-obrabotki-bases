# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

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
    
    # код ниже под '#' не работает по не понятной причине
    # price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(price_params))
    # price_square = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(price_params))
    # dic = scrapy.Field(input_processor=Compose(feature_params))

