# `prcrawler` Company Press Release Web Crawler

Python3 scrapy web crawler for collecting company press releases

## Getting Started 

Place CSV files listing firms to crawl in the `./data/` directory. 

Each data file should be formatted as follows:

industry | firm | pdf | start_url 
--- | --- | --- | ---
pharma | pfizer | 0 | https://www.pfizer.com/news/press-release/press-release-detail/augustus_demonstrates_favorable_safety_results_of_eliquis_versus_vitamin_k_antagonists_in_non_valvular_atrial_fibrillation_patients_with_acute_coronary_syndrome_and_or_undergoing_percutaneous_coronary_intervention 
pharma | sanofi | 1 | https://mediaroom.sanofi.com/en/press-releases/ 
... | ... | ... | ...

Required columns include: 

 - `industry`  [string] The firm's industry 
 - `firm`  [string] The firm name
 - `pdf`  [0,1] Flag indicating if press releases are formatted as PDFs, not HTML text (1=yes, 0=no)
 - `start_url`  [string] An example press release URL for the firm to start crawling links on that firm's domain. 

Column order is optional, and other columns (e.g., notes for reference) may be included in the data file but will not be processed.


## Collecting Press Releases 

Run a batch of simultaneous asynchronous `prcrawler`s by executing the `run_industry_crawler.py` script from the command line. 

Process *all files* in the `./data/` directory:

`$ python run_industry_crawler.py`

Process *specific files* in `./data/` with the optional files argument `-f` (or `--files`):

`$ python run_industry_crawler.py -f datafile1.csv datafile2.csv datafile3.csv`


## Logs and Debugging

Log files for each run are written in `./logs/`. 