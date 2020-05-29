# -*- coding: utf-8 -*-
"""
Authors: Bich Tran
         IHE Delft 2019
Contact: b.tran@un-ihe.org
Repository: https://github.com/wateraccounting/watools
Module: Collect/WaPOR

Description:
This script collects WaPOR data from the WaPOR API. 
The data is available between 2009-01-01 till present.

Example:
from watools.Collect import WaPOR
WaPOR.PCP_monthly(Dir='C:/Temp/', Startdate='2009-02-24', Enddate='2009-03-09',
                     latlim=[50,54], lonlim=[3,7])
WaPOR.AETI_monthly(Dir='C:/Temp/', Startdate='2009-02-24', Enddate='2009-03-09',
                     latlim=[50,54], lonlim=[3,7])
"""

from .AET_dekadal import main as AET_dekadal
from .NPP_dekadal import main as NPP_dekadal
from .LCC_yearly import main as LCC_yearly
from .WaporAPI import __WaPOR_API_class

__all__ = ['AET_dekadal','NPP_dekadal','LCC_yearly']
__doc__ = """module for FAO WAPOR API"""
__version__ = '0.1'

# initiate class for .his-files
API = __WaPOR_API_class()
API.Token=input('Insert WAPOR API Token: ')
