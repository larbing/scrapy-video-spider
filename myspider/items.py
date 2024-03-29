# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VideoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    update_context = scrapy.Field()
    region = scrapy.Field()
    category = scrapy.Field()
    rating = scrapy.Field()
    id = scrapy.Field()
    links = scrapy.Field()

