# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from prcrawler.spiders.base import BaseCrawlSpider
from pandas import isna



class PRSpider(BaseCrawlSpider): 
    
    def __init__(self, params=None):
        #------FIRM-SPECIFIC PARAMS-----------
        keys = params.keys() if params is not None else []
#        print("BERFORE INIT VALS: ")
#        print(self.name)
#        print(self.allowed_domains)
#        print(self.allow_regex)
#        print(self.start_urls)
#        print("AFTER INIT, keys:")
#        print(params)
        if 'firm' in keys:
            self.name = params['firm']
#            print("SET self.name %s" % self.name)
            
        if 'allowed_domain' in keys:
            self.allowed_domains = [params['allowed_domain']]
#            print("SET self.allowed_domains %s" % self.allowed_domains)
            
        if 'allow_regex' in keys and not isna(params['allow_regex']):
            self.allow_regex += [params['allow_regex']]  ## extend base array of PR keywords
#            print("SET self.allow_regex %s" % self.allow_regex)
            
        if 'start_url' in keys: 
            self.start_urls = [params['start_url']]
#            print("SET self.start_urls %s" % self.start_urls)
   
        #-------DEFAULT RULES LIST------------
        self._rules = [
            ## Extract links and follow them (no callback means follow=True)
            Rule(LinkExtractor(allow=self.allow_regex, unique=True), 
            	follow=True, callback=self.parse_items)
        ]
        
#        print("after init:")
#        print("(%s)(%s)" % (self.name, self._name))
#        print("(%s)(%s)" % (self.allowed_domains, self._allowed_domains))
#        print("(%s)(%s)" % (self.start_urls, self._start_urls))
#        print("(%s)(%s)" % (self.allow_regex, self._allow_regex))
    

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