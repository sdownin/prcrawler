# -*- coding: utf-8 -*-
import scrapy
import json
from uuid import uuid4
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from prcrawler.items import PrcrawlerItem
from prcrawler.helpers import timestamp, datestring

class BaseSpider(scrapy.Spider): 
    name = ''
    allowed_domains = []
    start_urls = []
    rules = ()

    def parse(self, response):
        self.logger.info('parsed item page %s\n' % response.url)
        item = PrcrawlerItem()
        item['id'] = str(uuid4())
        item['timestamp'] = timestamp()
        item['date'] = datestring()
        item['spider'] = ''
        item['url'] = response.url
        item['status'] = response.status
        item['headers'] = str(response.headers)
        item['flags'] = response.flags
        item['html'] = response.text
        return item