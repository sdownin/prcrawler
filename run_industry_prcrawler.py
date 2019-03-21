# -*- coding: utf-8 -*-

#
# Run multiple spiders for crawling press releases from
# all firms listed for a given industry
#

import os, logging
import pandas as pd
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from argparse import ArgumentParser
from prcrawler.spiders.prspider import PRSpider
from scrapy.utils.project import get_project_settings
from prcrawler.helpers import timestamp

##------------------------------------
## Load Firm (& industry) items for
##   spiders to run
##------------------------------------
#pd.set_option('max_columns',10)

def run():
    """ Main web crawler run function
    """
    work_dir = os.getcwd()
    data_dir = os.path.join(work_dir,'data')
    log_dir = os.path.join(work_dir,'logs')

    ## add logs directory
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    ## logging
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename=os.path.join(log_dir,'log_%s.txt' % round(timestamp())),
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )
    
    ## parse arguments
    par = ArgumentParser(description="Run Industry Press Release Crawler")
    par.add_argument('-f','--files', type=str, help="The data files to process") 
    args = par.parse_args()
    files = args.files.split(',') if args.files is not None else []
    
    ## if no files specified, run all files in data dir
    if not files:
        files = os.listdir(data_dir)
    print('files to crawl:')
    print(files)
    
    ## run crawlers for each data file
    for file in files:
        
        ## check data file
        if file not in os.listdir(data_dir):
            print('skipping missing file %s' % file)
            next
        else:
            print('processing file: %s' % file)
        
        ## load data
        df = pd.read_csv(os.path.join(data_dir, file), na_values=[""])
        
        ## init runner for multiple spiders
        runner = CrawlerRunner(get_project_settings())
    
        ## run web crawlers per domain in data file
        for index, row in df.iterrows():
            runner.crawl(PRSpider, params=row.to_dict())
            d = runner.join()
            d.addBoth(lambda _: reactor.stop())
            
        # after running, the script will block here until all crawling jobs are finished
        reactor.run() 


if __name__ == '__main__':
    run()


