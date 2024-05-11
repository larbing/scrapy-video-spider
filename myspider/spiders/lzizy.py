
import re
import scrapy
from hashlib import md5
from scrapy.selector import Selector
from myspider.items import VideoItem


from myspider.utils import md5_hash,idGenerator

class MySpider(scrapy.Spider):
    name = "lzizy"

    allowed_domains = ["lzizy.net"]

    base_url = "http://lzizy.net"

    def start_requests(self):
        # Loop through pages from 1 to 2
        # for page in range(1, 1000):
        #     # Generate URL for each page
        #     url = f"http://lzizy.net/index.php/index/index/page/{page}.html"
        #     # Send a request to the URL and parse the response
        #     yield scrapy.Request(url, self.parse)
        for page in range(1,200):
            url = f"http://lzizy.net/index.php/vod/type/id/1/page/{page}.html"
            yield scrapy.Request(url, self.parse)

        for page in range(1,200):
            url = f"http://lzizy.net/index.php/vod/type/id/2/page/{page}.html"
            yield scrapy.Request(url, self.parse)

        for page in range(1,50):
            url = f"http://lzizy.net/index.php/vod/type/id/3/page/{page}.html"
            yield scrapy.Request(url, self.parse)

        for page in range(1,100):
            url = f"http://lzizy.net/index.php/vod/type/id/4/page/{page}.html"
            yield scrapy.Request(url, self.parse)


        #yield scrapy.Request("http://lzizy.net/index.php/vod/detail/id/84384.html",self.parse1)

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
            # item['rating'] = selector.xpath('//a[@class="address"]/text()').get()
            item['id'] = md5_hash(item['url'])
            item['vid'] = str(idGenerator.get_id())
            item['site_name'] = "量子"

            yield item
            yield scrapy.Request(item['url'], self.parse1)
            # yield item
            
    def parse1(self,response):
        item = VideoItem()
        item['id'] = md5_hash(response.url)
        item['image_url'] = response.xpath('//div[@class="people"]/div[@class="left"]/img/@src').get()
        item['plot'] = response.xpath('//div[@class="vod_content"]/p/text()').get()
        self._parse_context_node(response,item)
        self._parse_links_node(response,item)
    
        yield item


    def _parse_context_node(self,response,item: VideoItem):
        pattern_dict = {
            "name" : "<p>片名：(.*)</p>" ,
            "rating" : "<p>豆瓣：(.*) 分</p>",
            "director" : "<p>导演：(.*)</p>",
            "cast" : "<p>演员：(.*)</p>",
            "release_date"  :  "<p>年代：(.*)</p>",
            "region" : "<p>地区：(.*)</p>" ,
            "language" : "<p>语言：(.*)</p>",
            "status" : "<p>状态：(.*)</p>",
            "updated" : "<p>更新时间：(.*)</p>"
        } 

        context = response.xpath('//div[@class="people"]/div[@class="right"]').get()
        for key in pattern_dict.keys():
            output = re.search(pattern_dict[key],context)
            item[key]  = output.groups()[0] if output else "Null"
    

    def _parse_links_node(self,response,item):
        item['links'] = []
        nodes = response.xpath('//div[@class="playlist wbox liangzi"]/li')
        for node in nodes:
            selector = Selector(text=node.get())
            output = selector.xpath('//input[@type="checkbox"]/@value').get()
            if output:
                item['links'].append(output)

        item['m3u8_links'] = []
        nodes = response.xpath('//div[@class="playlist wbox lzm3u8"]/li')
        for node in nodes:
            selector = Selector(text=node.get())
            output = selector.xpath('//input[@type="checkbox"]/@value').get()
            if output:
                item['m3u8_links'].append(output)


class DailyCrawler(MySpider):
    name = 'lzizy_daily'
    def start_requests(self):
        for t in range(1, 4):
            for page in range(1,10):
                url = f"http://lzizy.net/index.php/vod/type/id/{t}/page/{page}.html"
                yield scrapy.Request(url, self.parse)
