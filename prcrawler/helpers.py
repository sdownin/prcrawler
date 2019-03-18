# -*- coding: utf-8 -*-

#
# Define helper functions here
#

import datetime as dt #import arrow as ar
from datetime import timezone


def timestamp(dt0=None, tz=timezone.utc):
    """ get UTC unix epoch timestamp (ex: 1445212800)
    """
    if isinstance(dt0, dt.datetime):
        return dt0.replace(tzinfo=tz).timestamp()
    else:
        return dt.datetime.now().replace(tzinfo=tz).timestamp()

def datestring(dt0=None, tz=timezone.utc):
    """ get UTC datetime string of format 'YYYY-MM-DD HH:MM:SS'
    """
    if isinstance(dt0, dt.datetime):
        return dt0.replace(tzinfo=tz).strftime('%Y-%m-%d %H:%M:%S')
    else:
        return dt.datetime.now().replace(tzinfo=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

def get_month_number_from_name(monthString):
    """ Get month number from the name of month
    """
    monthDict = dict(january=1, jan=1, february=2, feb=2, march=3, mar=3, april=4, apr=4, may=5, june=6, jun=6, july=7, jul=7, august=8, aug=8, september=9, sep=9, sept=9, october=10, oct=10, november=11, nov=11, december=12, dec=12)
    monthStringLower = monthString.lower()
    if monthStringLower in monthDict:
        return monthDict[monthStringLower]
    else:
        raise ValueError('invalid month name "%s"' % monthStringLower)

def convert_date(dateText, replacements=['\n','reviewed',',']):
    """Convert Date from USA date format string with extraneous words to YYYY-MM-DD string
    """
    if dateText is None or dateText == '':
        return None
    string = dateText.lower()
    for r in replacements:
        string = string.replace(r,'')
    
    parts = string.strip().split(' ')
    year  = [i for i in parts if i.isdigit() and float(i) > 1990 ][0]
    day   = [i for i in parts if i.isdigit() and float(i) < 1900 ][0]
    month = [i for i in parts if i not in [year, day ]           ][0]
    month_number = get_month_number_from_name(month)

    return dt.datetime(int(year),int(month_number),int(day), 1, 1, 1)

def url_domain(url):
    """ Returns the domain from a URL
        @see https://stackoverflow.com/questions/9626535/get-protocol-host-name-from-url
        
        Parameters
        ----------
        
        url : str 
            A URL to parse its domain
        
        
        Returns
        ----------
        
        domain : str
            The domain parsed from the URL 
    """
    return url.split("//")[-1].split("/")[0].split('?')[0]