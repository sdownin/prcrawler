# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from prcrawler.spiders.base import BaseSpider


class PfizerSpider(BaseSpider):
    name = 'pfizer'
    allowed_domains = ['pfizer.com/news/press-release']
    start_urls = [
        'https://www.pfizer.com/news/press-release/press-releases-archive'
    ]
    rules = [
        ## Extract links and follow them (no callback means follow=True)
        Rule(LinkExtractor(allow=allowed_domains), 
        	follow=True, callback='parse')
    ]

    def parse(self, response):
        """ parse response from page request
        """
        # Links from the page
        links = LinkExtractor(allow=self.allowed_domains, unique=True).extract_links(response)
        #
        for link in links:
            # Check whether the domain of the URL of the link is allowed; so whether it is in one of the allowed domains
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True
            if is_allowed:
                item = super().parse(response)
                item['spider'] = self.name
                item['url_to'] = link.url
                yield item        