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
    id = scrapy.Field()
    vid = scrapy.Field()
    links = scrapy.Field()
    m3u8_links = scrapy.Field()

    image_url = scrapy.Field()
    site_name = scrapy.Field()
    plot = scrapy.Field()
    rating = scrapy.Field()
    director = scrapy.Field()
    cast = scrapy.Field()
    release_date = scrapy.Field()
    language = scrapy.Field()
    status = scrapy.Field()
    updated = scrapy.Field()
    