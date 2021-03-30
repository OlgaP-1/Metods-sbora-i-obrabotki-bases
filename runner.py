from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from leruaMerlen import settings
from leruaMerlen.spiders.lmru import LmruSpider
from urllib.parse import quote_plus

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    # search = 'керамическая+плитка'
    search = quote_plus('керамическая плитка')  #.encode('cp1251'))
    print(search)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LmruSpider, search=search)

    process.start()