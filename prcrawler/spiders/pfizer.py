# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from prcrawler.spiders.base import BaseSpider
# from reviewscrawler.pipelines import MongoPipeline


class PfizerSpider(BaseSpider):
    name = 'pfizer'
    allowed_domains = ['pfizer.com']
    start_urls = ['https://www.pfizer.com/news/press-release/press-releases-archive']
    rules = (
        ## Extract links and follow them (no callback means follow=True)
        Rule(LinkExtractor(allow=(r'/press-releases-archive/',)), 
        	follow=True),
        ## Extract links and parse them with parse() callback
        Rule(LinkExtractor(allow=(r'/press-releases-archive/',)), 
        	callback='parse')
    )

    def parse(self, response):
        """ call parent method; then add this spider name
        """
        item = super().parse(response)
        item['spider'] = self.name
        yield item
        