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
from .WaporAPI import __WaPOR_API_class
from .download_dekadal import main as download_dekadal
from .download_monthly import main as download_monthly
from .download_yearly import main as download_yearly
from .download_daily import main as download_daily
from .download_seasonal import main as download_seasonal

__all__ = ['download_dekadal','download_monthly','download_yearly','download_daily']
__doc__ = """module for FAO WAPOR API"""
__version__ = '0.1'

# initiate class for .his-files

api_token_pickle=os.path.join(os.path.dirname(__file__),
                              'wapor_api_token.pickle')

if not os.path.exists(api_token_pickle):
    wapor_api_token=input('Insert WAPOR API Token: ')
    with open(api_token_pickle, 'wb') as handle:
        pickle.dump(wapor_api_token, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("Saved API Token")    
else:
    with open(api_token_pickle, 'rb') as handle:
        wapor_api_token=pickle.load(handle)
        print("Obtained saved API Token")
print("Your WaPOR API Token is saved into: {0}. \n If you wish to change your API Token, please delete this file".format(api_token_pickle))       
APIToken=wapor_api_token
API = __WaPOR_API_class(APIToken)

# load catalog
#API.getCatalog()