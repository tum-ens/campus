# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 18:27:54 2018

@author: aelshaha
"""


NO_SITE     = 'NO_SITE'
NO_YEAR     = 'NO_YEAR'
NO_TS       = 'NO_TS'
TS_LEN      = 'TS_LEN'
NO_COMM     = 'NO_COMM'
NO_PROC     = 'NO_PROC'
NO_SCENARIO = 'NO_SC'


ERRORS = {
    NO_SITE     : 'Please define at least one site!',
    NO_YEAR     : 'Please define at least one year!',
    NO_SCENARIO : 'Please select at least one scenario!',
    NO_COMM     : 'No commodities defined for the site: %s',
    NO_TS       : 'Time Series is not defined for (site, commodity, year): (%s, %s, %s)',
    TS_LEN      : 'Time Series should be exactly %s (not %s) entries, for (site, commodity, year): (%s, %s, %s)',
    NO_PROC     : 'No processes defined for the site: %s'
}