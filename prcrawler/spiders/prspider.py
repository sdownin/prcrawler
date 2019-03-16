# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from prcrawler.spiders.base import BaseCrawlSpider
from pandas import isna



class PRSpider(BaseCrawlSpider): 
    
    def __init__(self, params=None):
        #------FIRM-SPECIFIC PARAMS-----------
        keys = params.keys() if params is not None else []
        
        if 'name' in keys:
            self.name = params['name']
            
        if 'allowed_domain' in keys:
            self.allowed_domains = [params['allowed_domain']]
            
        if 'allow_regex' in keys and not isna(params['allow_regex']):
            self.allow_regex += [params['allow_regex']]  ## extend base array of PR keywords
            
        if 'start_url' in keys: 
            self.start_urls = [params['start_url']]
   
        #-------DEFAULT RULES LIST------------
        self._rules = [
            ## Extract links and follow them (no callback means follow=True)
            Rule(LinkExtractor(allow=self.allow_regex, unique=True), 
            	follow=True, callback=self.parse_items)
        ]
    
        # def parse_items(self, response):
        #     """ uncomment to overwrite callback from BaseCrawlSpider
        #     """
    	#     pass 



#    print('PRSpider:')
#    print(params)
#    name = 'prspider'
#    allowed_domains = ['pfizer.com']
#    allow_regex = 'press-release'
#    start_urls = [
#        'https://www.pfizer.com/news/press-release/press-releases-archive'
#    ]
#    rules = [
#    ## Extract links and follow them (no callback means follow=True)
#        Rule(LinkExtractor(allow=allow_regex, unique=True), 
#             follow=True, callback='parse_items')
#    ]