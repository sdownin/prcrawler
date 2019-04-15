# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from prcrawler.spiders.base import BaseCrawlSpider
from prcrawler.helpers import url_domain
from prcrawler.browser import WebpageClient
# from scrapy_splash import SplashRequest

class PRSpider(BaseCrawlSpider): 
    
    def __init__(self, params={}):
        ## Check press release webpage has <article> elements and
        ## set has_dom_article attribute 
#        self.links = self.dynamic_links(params)
#        print('dynamic links parsed:')
#        print(self.links)
#        self.has_dom_article = 0 if len(self.links) else 1
        
        print('----------PRSpider::__init__---------')
        
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
                # process_request=self.dynamic_request,
            	follow=True, callback=self.parse_items)
        ]

    # def dynamic_request(self, request):
    #     print('--------PRSpider::dynamic_request----------------')
    #     page = WebpageClient(request.url)   
    #     request.replace(body=page.html)
    #     print('request')
    #     print(request)
    #     bsoup = BeautifulSoup(page.html, 'html.parser')
    #     jslist = bsoup.select('a[aria-label="Download"]')
    #     if jslist:
    #         return [x.attrs['href'] for x in jslist]
    #     # request.encoding = 'utf-8'
    #     return request   

