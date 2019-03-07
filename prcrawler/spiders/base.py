# -*- coding: utf-8 -*-
import scrapy
import json
from uuid import uuid4
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from prcrawler.items import PrcrawlerItem
from prcrawler.helpers import timestamp, datestring

class BaseCrawlSpider(CrawlSpider): 
    ## Properties to be set in spiders that
    ## extend BaseCrawlSpider
    name = ''
    allowed_domains = []
    allow_regex = ''
    start_urls = []
    rules = []

    def parse_item(self, response, args={}):
        """ parse one scrapy item to be saved 
            as a record in the database or outpute file
        """
        # self.logger.info('parsed item page %s\n' % response.url)
        item = PrcrawlerItem()
        item['id'] = str(uuid4())
        item['timestamp'] = timestamp()
        item['date'] = datestring()
        item['spider'] = self.name
        item['status'] = response.status
        item['headers'] = str(response.headers)
        item['flags'] = response.flags
        item['html'] = response.text
        item['url_from'] = response.url
        for key in args.keys():
            item[key] = args[key]
        return item

    def parse_items(self, response):
        """ Main LinkExtractor callback for spiders that extend BaseCrawlSpider;
            parse items from all links in page request
        """
        # Links from the page
        links = LinkExtractor(allow=self.allow_regex, unique=True).extract_links(response)
        # loop over links on page
        for link in links:
            # Check whether the domain of the URL of the link is allowed; so whether it is in one of the allowed domains
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True
            if is_allowed:
                yield self.parse_item(response, {'url_to':link.url})  