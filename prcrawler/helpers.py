# -*- coding: utf-8 -*-

#
# Define helper functions here
#

import datetime as dt #import arrow as ar
from datetime import timezone


def timestamp():
	""" get UTC unix epoch timestamp (ex: 1445212800)
	"""
	return dt.datetime.now().replace(tzinfo=timezone.utc).timestamp()

def datestring():
	""" get UTC datetime string of format 'YYYY-MM-DD HH:MM:SS'
	"""
	return dt.datetime.now().replace(tzinfo=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')