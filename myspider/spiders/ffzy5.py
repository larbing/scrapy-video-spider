
import scrapy
from hashlib import md5
from scrapy.selector import Selector
from myspider.items import VideoItem


def md5_hash(string:str):
    return md5(string.encode('utf-8')).hexdigest()

class MySpider(scrapy.Spider):
    name = "ffzy5"
    allowed_domains = ["ffzy5.tv"]

    base_url = "http://ffzy5.tv"

    def start_requests(self):
        # Loop through pages from 1 to 2
        for page in range(1, 100):
            # Generate URL for each page
            url = f"http://ffzy5.tv/index.php/index/index/page/{page}.html"
            # Send a request to the URL and parse the response
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        nodes = response.xpath('//ul[@class="videoContent"]/li')
        for node in nodes:
            selector = Selector(text=node.get())
            item = VideoItem()
            item['name'] = selector.xpath('//a[@class="videoName"]/text()').get()
            item['url'] = self.base_url + selector.xpath('//a[@class="videoName"]/@href').get()
            item['update_context'] = selector.xpath('//a[@class="videoName"]/i/text()').get()
            item['region'] = selector.xpath('//span[@class="region"]/text()').get()
            item['category'] = selector.xpath('//span[@class="category type"]/text()').get()
            item['rating'] = selector.xpath('//a[@class="address"]/text()').get()
            item['id'] = md5_hash(item['url'])
            yield item
            
    
    def parse1(self,response):
        item = VideoItem()
        item['id'] = md5_hash(response.url)
        nodes = response.xpath('//div[@class="playlist wbox feifan"]/li')
        item['links'] = []
        for node in nodes:
             selector = Selector(text=node.get())
             item['links'].append(selector.xpath('//input[@type="checkbox"]/@value').get())
        
        yield item