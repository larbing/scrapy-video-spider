from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from myspider.spiders import lzizy

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(lzizy.MySpider)
    process.start()   