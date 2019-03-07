# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from prcrawler.spiders.base import BaseSpider


class PfizerSpider(BaseSpider):
	##-----SET FIRM PARAMS-----------
    name = 'pfizer'
    allowed_domains = ['pfizer.com']
    allow_regex = 'press-release'
    start_urls = [
        'https://www.pfizer.com/news/press-release/press-releases-archive'
    ]
    ##-------------------------------

    rules = [
        ## Extract links and follow them (no callback means follow=True)
        Rule(LinkExtractor(allow=allow_regex, unique=True), 
        	follow=True, callback='parse_items')
    ]

    def parse_items(self, response):
        """ parse items in response from page request
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
                args = {'spider':self.name, 'url_to':link.url}
                item = self.parse_item(response, args)  
                return item   