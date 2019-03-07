# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PrcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    timestamp = scrapy.Field()
    date = scrapy.Field()
    spider = scrapy.Field()
    url = scrapy.Field()
    url_from = scrapy.Field()
    url_to = scrapy.Field()
    status = scrapy.Field()
    headers = scrapy.Field()
    flags = scrapy.Field()
    html = scrapy.Field()
