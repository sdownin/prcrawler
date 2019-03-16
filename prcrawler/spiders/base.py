# -*- coding: utf-8 -*-
import scrapy, json, re
import datetime as dt
from uuid import uuid4
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from prcrawler.items import PrcrawlerItem
from bs4 import BeautifulSoup
from prcrawler.helpers import timestamp, datestring
from time import sleep
from numpy import random
from dateparser import parse

## default allow_regex terms
PR_KEYWORDS = [
    'news','press','media','story','stories','detail','archive'
]


class BaseCrawlSpider(CrawlSpider): 
    ## Properties to be set in spiders that
    ## extend BaseCrawlSpider
    name = ''
    allowed_domains = []
    allow_regex = PR_KEYWORDS
    start_urls = []
    _rules = []

    def parse_item(self, response, args={}):
        """ parse one scrapy item to be saved 
            as a record in the database or outpute file
        """
        # self.logger.info('parsed item page %s\n' % response.url)
        item = PrcrawlerItem()
        item['id'] = str(uuid4())
        item['spider'] = self.name
        item['crawl_timestamp'] = timestamp()
        item['crawl_date'] = datestring()
        item['status'] = response.status
        item['headers'] = str(response.headers)
        item['flags'] = response.flags
        item['html'] = response.text
        item['url_from'] = response.url
        for key in args.keys():
            item[key] = args[key]
        # ##------TODO: parsed article items--------
        bsoup = BeautifulSoup.parse(response.body, 'html.parser') ## 'lxml'
        item['crawl_date'] = self.parse_date(bsoup, request)  ##TODO: datetime parse
        if isinstance(item['crawl_date'], dt.datetime):
            item['crawl_timestamp'] = timestamp(item['crawl_date'])
        item['title'] = self.parse_title(bsoup, request)
        item['article'] = self.parse_article(bsoup, request)
        # item['source'] = self.parse_source(bsoup, request)
        # item['location'] = self.parse_source(bsoup, request)
        return item

    def parse_items(self, response, request):
        """ Main LinkExtractor callback for spiders that extend BaseCrawlSpider;
            parse items from all links in page request
        """
        sleep(random.exponential(scale=1.5))
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


    def parse_date(self, bsoup, request):
        """ Return datetime.datetime from arbitrary numberic|text date formats
        """
        ## regex partial match
        chron = bsoup.find('chron')
        if len(chron) and isinstance(chron.text, str):
           dt0 = parse(chron.text)
           if dt0 is not None:
              return dt0
        spans = bsoup.find_all(['span','div'], attrs={'class':re.compile('.*date.*')})
        while len(spans):
           dt0 = parse(spans.pop(0).text)
           if dt0 is not None:
              return dt0

    def parse_timezone(self, bsoup, request):
        """ Return datetime.datetime from arbitrary numberic|text date formats
        """
        pass

    def parse_location(self, bsoup, request):
        """ Return the location of the press release 
        """
        ## regex partial match
        loc = bsoup.find('location')
        if len(loc) and isinstance(loc.text, str):
           return loc.text.capitalize()

    def parse_title(self, bsoup, request):
        """
        """
        els = bsoup.find_all('h1')
        if len(els) == 1:
            return els.pop(0).text.replace('\n','')
        elif len(els) > 1:
            els = bsoup.select('h1[id*=title]')
            if len(els) == 1:
               return els.pop(0).text.replace('\n','')
            els = bsoup.select('h1[class*=title]')
            if len(els) == 1:
               return els.pop(0).text.replace('\n','')
        ## TODO: robust logic for checking for page title outside of <h1>
        ## fallback just return end of url path
        return request.url.split('/')[-1]
           

    def parse_article(self, bsoup, request):
        """ Parse the text of the news article from the web request 
        """
        article = bsoup.find('article')
        text = article.pop(0).text
        if len(article):
            return text.replace('\n','').replace('\r','')
        

    def parse_news_source(self, bsoup, request):
        """
        """
        pass
     
      
#    def testing(self):
#        url = 'https://www.pfizer.com/news/press-release/press-release-detail/u_s_fda_approves_pfizer_s_oncology_biosimilar_trazimera_trastuzumab_qyyp_a_biosimilar_to_herceptin_1'
#        r = requests.get(url)
#        soup = BeautifulSoup(r.text, 'html.parser')
#        ## exact match of one class
#        soup.find_all('span', attrs={'class':'date-display-single'})
#        ## regex partial match
#        spans = soup.find_all('span', attrs={'class':re.compile('.*date.*')})
##        soup.select('div[class*="date"]')
#        dt0 = dateparser.parse(spans[0].contents[0])
#        timestamp()



