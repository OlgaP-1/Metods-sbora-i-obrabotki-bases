import scrapy
from scrapy.http import HtmlResponse
from leruaMerlen.items import LeruamerlenItem
from scrapy.loader import ItemLoader

class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[contains(@class, "plp-item__info__title")]/@href').extract()
        # находим ссылку на следующую страницу
        next_page = response.xpath('//a[@class= "paginator-button next-paginator-button"]/@href').extract_first()
        for link in links:
            yield response.follow(link, callback=self.parse_item)
        #переходим на следующую страницу и возвращаем метод parse для парсинга новой страницы
        yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response: HtmlResponse): #обрабатываем каждый товар
        loader = ItemLoader(item=LeruamerlenItem(), response=response)
        loader.add_xpath('photos', '//img[contains(@alt, "product image")]/@src')
        loader.add_xpath('name', '//h1[@itemprop="name"]/text()')
        loader.add_xpath('price', f'//uc-pdp-price-view[contains(@class, "primary-price")]//span[@slot="price"]/text() | .//uc-pdp-price-view[contains(@class, "primary-price")]//span[@slot="fract"]/text()')
        loader.add_xpath('price_square', '//uc-pdp-price-view[contains(@class, "second-price")]//span[@slot="price"]/text()')
        loader.add_xpath('href', '//uc-regions-overlay-item/a[contains(@class, "region-link highlighted new")]/@href')
        loader.add_xpath('features_keys', '//dt[contains(@class, "def-list__term")]/text()')
        loader.add_xpath('features', '//dd[contains(@class, "def-list__definition")]/text()')

        # по коду ниже под '#' парсинг не работает по не понятной причине
        # loader.add_xpath('dic', '//div[contains(@class, "def-list__group")]/text()')

        yield loader.load_item()
