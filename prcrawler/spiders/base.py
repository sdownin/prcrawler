# -*- coding: utf-8 -*-
import re
import datetime as dt
from uuid import uuid4
from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from prcrawler.items import PrcrawlerItem
from bs4 import BeautifulSoup
from prcrawler.helpers import timestamp, datestring
from dateparser import parse
from time import sleep
from numpy.random import exponential

## default allow_regex terms
PR_KEYWORDS = [
    'news','press','media','story','stories','detail','archive'
]

MEDIA_EXTS = [
    '.pdf','.jpg','.jpeg','.png','.gif','.tiff','.bmp','.exif'
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
        print('-------BaseCrawlSpider::parse_item--------')
        print('response')
        print(response)
        print('args')
        print(args)
        # self.logger.info('parsed item page %s\n' % response.url)
        bsoup = BeautifulSoup(response.body, 'html.parser') ## 'lxml'
        item = PrcrawlerItem()
        item['id'] = str(uuid4())
        item['spider'] = self.name
        item['crawl_timestamp'] = timestamp()
        item['crawl_date'] = datestring()
        item['status'] = response.status
        item['headers'] = str(response.headers)
        item['flags'] = response.flags
        item['text'] = bsoup.find('body').text.replace('\r',' ').replace('\n',' ')
        item['url_from'] = response.url
        for key in args.keys():
            item[key] = args[key]
        item['date'] = self.parse_date(bsoup, response)  
        if isinstance(item['date'], dt.datetime):
            item['timestamp'] = timestamp(item['date'])
        item['title'] = self.parse_title(bsoup, response)
        item['article'] = self.parse_article(bsoup, response)
        item['location'] = self.parse_location(bsoup, response)
        item['source'] = self.parse_source(bsoup, response) ## TODO: add source
        item['tags'] = self.parse_tags(bsoup, response)  ## TODO: add tags
        return item
    
    def parse_pdf(self, response):
        """
        """
        return

    def parse_items(self, response):
        """ Main LinkExtractor callback for spiders that extend BaseCrawlSpider;
            parse items from all links in page request
        """
        # Links from the page
        print("----------BaseCrawlSpider::parse_items ---------")
        links = LinkExtractor(allow=self.allow_regex, unique=True).extract_links(response)
        print([l.url for l in links])
        # loop over links on page
        for link in links:
            # Check whether the domain of the URL of the link is allowed; so whether it is in one of the allowed domains
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True
            for ext in MEDIA_EXTS:
                if ext in link.url:
                    is_allowed = False
            if is_allowed:
                yield self.parse_item(response, {
                    'url_to': link.url, 
                    'industry': self.industry,
                    'firm': self.name, 
                    'has_dom_article': self.has_dom_article
#                    ,
#                    'image_urls': image_urls,
#                    'pdf_urls': pdf_urls
                })  



    def parse_date(self, bsoup, response):
        """ Return datetime.datetime from arbitrary numberic|text date formats
        """
        ## regex partial match
        chron = bsoup.find('chron')
        if chron is not None and isinstance(chron.text, str):
            dt0 = parse(chron.text)
            if dt0 is not None:
                return dt0
        spans = bsoup.find_all(['span','div'], attrs={'class':re.compile('.*date.*')})
        while len(spans):
            dt0 = parse(spans.pop(0).text)
            if dt0 is not None:
                return dt0

    def parse_timezone(self, bsoup, response):
        """ Return datetime.datetime from arbitrary numberic|text date formats
        """
        pass

    def parse_title(self, bsoup, response):
        """ Parse the press release or news article title
        """
        els = bsoup.find_all('h1')
        if len(els) == 1:
            return els.pop(0).text.replace('\n',' ')
        elif len(els) > 1:
            els = bsoup.select('h1[id*=title]')
            if len(els) == 1:
                return els.pop(0).text.replace('\n',' ')
            els = bsoup.select('h1[class*=title]')
            if len(els) == 1:
                return els.pop(0).text.replace('\n',' ')
        ## TODO: robust logic for checking for page title outside of <h1>
        ## fallback: just return end of url path
        return response.url.split('/')[-1]
           
    def parse_article(self, bsoup, response):
        """ Parse the body text of the press release or news article 
        """
        article = bsoup.find('article')
        if article is not None and isinstance(article.text, str):
            return article.text.replace('\n',' ').replace('\r',' ')

    def parse_location(self, bsoup, request):
        """ Return the location of article  
        """
        ## regex partial match
        loc = bsoup.find('location')
        if loc is not None and isinstance(loc.text, str):
           return loc.text.capitalize()

    def parse_source(self, bsoup, response):
        """
        """
        pass

    def parse_tags(self, bsoup, response):
        """
        """
        return []

    def parse_images(self, bsoup, response):
        """
        """
        return []

    def parse_pdfs(self, bsoup, response):
        """
        """
        return []
    
#        pdfs = [x['href'] for x in bsoup.select('a[href]') ]
#        for i,pdf in enumerate(pdfs):
#            pdfs[i] = '%s/%s' % (response.url.rstrip('/'), pdf.lstrip('/'))
#        return pdfs
    
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



