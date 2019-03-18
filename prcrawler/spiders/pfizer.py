# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from prcrawler.spiders.base import BaseCrawlSpider


class PfizerSpider(BaseCrawlSpider):
    ##------FIRM-SPECIFIC PARAMS-----------
    name = 'pfizer'
    allowed_domains = ['pfizer.com']
    allow_regex = 'press-release'
    start_urls = [
        'https://www.pfizer.com/news/press-release/press-releases-archive'
    ]

    ##-------DEFAULT RULES LIST------------
    rules = [
        ## Extract links and follow them (no callback means follow=True)
        Rule(LinkExtractor(allow=allow_regex, unique=True), 
        	follow=True, callback='parse_items')
    ]

    # def parse_items(self, response):
    #     """ uncomment to overwrite callback from BaseCrawlSpider
    #     """
	#     pass 
