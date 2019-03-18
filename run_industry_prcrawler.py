# -*- coding: utf-8 -*-

#
# Run multiple spiders for crawling press releases from
# all firms listed for a given industry
#

import os, logging
import pandas as pd
from scrapy.crawler import CrawlerRunner
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from argparse import ArgumentParser
from prcrawler.spiders.prspider import PRSpider
from scrapy.utils.project import get_project_settings
#from scrapy.settings import Settings, default_settings
# from prcrawler import settings

##------------------------------------
## Load Firm (& industry) items for
##   spiders to run
##------------------------------------
#pd.set_option('max_columns',10)

def run():
    """ Main web crawler run function
    """
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )
    #par = ArgumentParser(description="Run Industry Press Release Crawler")
    #par.add_argument('industry', type=str, default='pharma', help="The industry to crawl [pharma,automotive,...]") 
    #args = par.parse_args()
    
    ## TODO: arguments to set multiple files in different paths
    data_file = os.path.join(os.getcwd()) + '/data/firms_test.csv'
    df = pd.read_csv(data_file, na_values=[""])

    ## init runner for multiple spiders
    runner = CrawlerRunner(get_project_settings())
    
    for index, row in df.iterrows():
        runner.crawl(PRSpider, params=row.to_dict())
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())

    # after running, the script will block here until all crawling jobs are finished
    reactor.run() 


if __name__ == '__main__':
    run()


