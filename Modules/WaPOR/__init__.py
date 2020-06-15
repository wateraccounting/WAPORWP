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
WaPOR.PCP_dekadal(Dir='C:/Temp/', Startdate='2009-02-24', Enddate='2009-03-09',
                     latlim=[50,54], lonlim=[3,7])
WaPOR.AETI_dekadal(Dir='C:/Temp/', Startdate='2009-02-24', Enddate='2009-03-09',
                     latlim=[50,54], lonlim=[3,7])
"""
import pickle
import os
from .AET_dekadal import main as AET_dekadal
from .NPP_dekadal import main as NPP_dekadal
from .LCC_yearly import main as LCC_yearly
from .T_dekadal import main as T_dekadal
from .RET_dekadal import main as RET_dekadal
from .PCP_dekadal import main as PCP_dekadal
from .WaporAPI import __WaPOR_API_class


__all__ = ['AET_dekadal','NPP_dekadal','LCC_yearly',
           'T_dekadal','RET_dekadal','PCP_dekadal']
__doc__ = """module for FAO WAPOR API"""
__version__ = '0.1'

# initiate class for .his-files
API = __WaPOR_API_class()
api_token_pickle=os.path.join(os.path.dirname(__file__),
                              'wapor_api_token.pickle')

if not os.path.exists(api_token_pickle):
    wapor_api_token=input('Insert WAPOR API Token: ')
    with open(api_token_pickle, 'wb') as handle:
        pickle.dump(wapor_api_token, handle, protocol=pickle.HIGHEST_PROTOCOL)
else:
    with open(api_token_pickle, 'rb') as handle:
        wapor_api_token=pickle.load(handle)
        
API.Token=wapor_api_token

# load catalog
API.getCatalog()