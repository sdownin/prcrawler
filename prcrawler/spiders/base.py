# -*- coding: utf-8 -*-
import scrapy
import json
from uuid import uuid4
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from prcrawler.items import PrcrawlerItem
from prcrawler.helpers import timestamp, datestring

class BaseSpider(CrawlSpider): 
    name = ''
    allowed_domains = []
    start_urls = []
    rules = ()

    # def parse(self, response):
    #     pass

    def parse_item(self, response, args={}):
        """ parse one item
        """
        self.logger.info('parsed item page %s\n' % response.url)
        item = PrcrawlerItem()
        item['id'] = str(uuid4())
        item['timestamp'] = timestamp()
        item['date'] = datestring()
        item['url_from'] = response.url
        item['status'] = response.status
        item['headers'] = str(response.headers)
        item['flags'] = response.flags
        item['html'] = response.text
        for key in args.keys():
            item[key] = args[key]
        return item