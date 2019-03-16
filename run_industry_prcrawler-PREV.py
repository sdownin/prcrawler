# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

#
# Run multiple spiders for crawling press releases from
# all firms listed for a given industry
#

import os, scrapy
import pandas as pd
from scrapy.crawler import CrawlerRunner
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from argparse import ArgumentParser
from scrapy.settings import Settings, default_settings
from prcrawler.spiders import pfizer

##------------------------------------
## list industry spider modules here
##------------------------------------
INDUSTRY_SPIDER_NAMES = {
    'pharma':[
        'pfizer'
    ],
    'automotive':[
    ]
}

def run():
    """ Main run function
    """
    # sldr = SpiderLoader(Settings())
    # print('|'.join(sldr.list()))
    configure_logging()
    par = ArgumentParser(description="Run Industry Press Release Crawler")
    par.add_argument('industry', type=str, default='pharma', help="The industry to crawl [pharma,automotive,...]") 
    args = par.parse_args()

    if args.industry not in INDUSTRY_SPIDER_NAMES.keys():
        raise ValueError("Industry name `%s` not available" % args.industry)

    # ##----------TEMPORARY HACK -------------
    # workaround since scrapy API not loading settings config for parallel spider runs
    for spider_name in INDUSTRY_SPIDER_NAMES[args.industry]:
        os.system('scrapy crawl %s' % spider_name)
    # ##----------TODO: DEBUG -------------
    # ## add industry spiders to runner in parallel
    # runner = CrawlerRunner(Settings())
    # for spider in INDUSTRY_SPIDERS[args.industry]:
    #     runner.crawl(spider)
    #     d = runner.join()
    #     d.addBoth(lambda _: reactor.stop())
    #
    # # after running, the script will block here until all crawling jobs are finished
    # reactor.run() 


if __name__ == '__main__':
    run()


# INDUSTRY_SPIDERS = {
#     'pharma':[
#         pfizer.PfizerSpider
#     ],
#     'automotive':[
#     ]
# }
