# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from prcrawler.spiders.base import BaseCrawlSpider
from prcrawler.helpers import url_domain


class PRSpider(BaseCrawlSpider): 
    
    def __init__(self, params=None):
        ## Check press release webpage has <article> elements and
        ## set has_dom_article attribute 
        r = requests.get(params['start_url'])
        bsoup = BeautifulSoup(r.text, 'html.parser')
        self.has_dom_article = 1 if bsoup.find('article') is not None else 0
        
        ## Set start_urls and allowed_domains
        url = params['start_url'].rstrip('/')
        domain = url_domain(url) 
        self.start_urls = [url]
        self.allowed_domains = [domain]
        
        ## Set allow_regex list
        path = url.split(domain)[-1] ## end of start_url
        subs = path.split('/')                       ## subdomain parts
        allow_subs = [x for x in subs[:-1] if x is not '']
        if not allow_subs:
            self.allow_regex = []  ## no press release subdomains in URL 
        else:
            self.allow_regex += allow_subs ## extend base array of PR keywords
#        print("SET start_url %s" % '|'.join(self.start_urls))
#        print("SET allowed_domain %s" % '|'.join(self.allowed_domains))
#        print("SET allow_regex %s" % '|'.join(self.allow_regex))

        ## Set name
        self.name = params['firm']
#        print("SET self.name %s" % self.name)
        
        ## Set industry
        self.industry = params['industry']
        
        ## Set rules
        self._rules = [
            ## Extract links and follow them (no callback means follow=True)
            Rule(LinkExtractor(allow=self.allow_regex, unique=True), 
            	follow=True, callback=self.parse_items)
        ]
  

