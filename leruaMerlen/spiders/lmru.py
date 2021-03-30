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
        # На стартовой странице ищем блок с ссылками, за которые можно зацепиться
        links = response.xpath('//a[contains(@class, "plp-item__info__title")]/@href').extract()
        # обрабатываем все ссылки
        for link in links:
            yield response.follow(link, callback=self.parse_item)
        print(links)
        # Ищем ссылки на следующие страницы
    # def next_page(self, response: HtmlResponse):
    #     # paginator = response.xpath('//div[contains(@class, "next-paginator-button-wrapper")]/a/@href')
    #     # for page_url in paginator: # переходим по этим ссылкам, получая страницы с товаром
    #     #     yield response.follow(page_url, callback=self.next_page)
    #     # # Ищем ссылки на товар в открывшейся странице
    #     href = response.xpath('//uc-product-list/product-card//a[contains(@class, "plp-item__info__title")]/@href').extract()
    #     for link in href:
    #         yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response: HtmlResponse): #обрабатываем каждый товар
        loader = ItemLoader(item=LeruamerlenItem(), response=response)
        loader.add_xpath('photos', '//img[contains(@alt, "product image")]/@src')
        loader.add_xpath('name', '//h1[@itemprop="name"]/text()')
        loader.add_xpath('price', f'//uc-pdp-price-view[contains(@class, "primary-price")]//span[@slot="price"]/text() | .//uc-pdp-price-view[contains(@class, "primary-price")]//span[@slot="fract"]/text()')
        loader.add_xpath('price_square', '//uc-pdp-price-view[contains(@class, "second-price")]//span[@slot="price"]/text()')
        loader.add_xpath('href', '//uc-regions-overlay-item/a[contains(@class, "region-link highlighted new")]/@href')
        loader.add_xpath('features_keys', '//dt[contains(@class, "def-list__term")]/text()')
        loader.add_xpath('features', '//dd[contains(@class, "def-list__definition")]/text()')
        yield loader.load_item()
        # item = LeruamerlenItem()
        # item['name'] = response.xpath('//h1[@itemprop="name"]/text()').extract()
        # item['photos'] = response.xpath('//img[contains(@alt, "product image")]/@src').extract()
        # print()
        # yield item
