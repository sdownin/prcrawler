# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PrcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    spider = scrapy.Field()
    firm = scrapy.Field()
    industry = scrapy.Field()
    crawl_date = scrapy.Field()
    crawl_timestamp = scrapy.Field()
    url_from = scrapy.Field()
    url_to = scrapy.Field()
    status = scrapy.Field()
    headers = scrapy.Field()
    flags = scrapy.Field()
    text = scrapy.Field()
    ## parsed item fields
    date = scrapy.Field()
    timestamp = scrapy.Field()
    has_dom_article = scrapy.Field()  ## 1=firm's press release pages have <article>; 0 otherwise
    title = scrapy.Field()
    article = scrapy.Field()
    source = scrapy.Field()
    location = scrapy.Field()
    tags = scrapy.Field()
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
    pdf_urls = scrapy.Field()
    pdf_paths = scrapy.Field()
