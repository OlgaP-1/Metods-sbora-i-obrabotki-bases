import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        links = response.css('a.icMQ_._6AfZ9._2JivQ._1UJAN::attr(href)').extract()
        vacancy_links = links
        for link in vacancy_links:
            yield response.follow(link, callback=self.parse_vacancies)
        next_page = response.xpath('//a[contains(@class, "-button-dalshe")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        pass

    def parse_vacancies(self, response: HtmlResponse):
        title = response.xpath('//h1/text()').get()
        salary = response.xpath('//div[contains(@class, "_3MVeX")]/span//text()').getall()
        href = response.xpath('//a[contains(@class, "_2JivQ _1UJAN")]/@href').get()
        link = 'https://www.superjob.ru'
        yield JobparserItem(title=title, salary=salary, href='https://superjob.ru'+href, link=link)