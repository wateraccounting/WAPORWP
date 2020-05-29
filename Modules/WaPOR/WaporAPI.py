# -*- coding: utf-8 -*-
"""
Authors: Bich Tran
         IHE Delft 2019
Contact: b.tran@un-ihe.org


"""
import requests
import json
import pandas as pd
import datetime

class __WaPOR_API_class(object):
    def __init__(self):    
        self.time_start=datetime.datetime.now().timestamp()
        self.time_now=datetime.datetime.now().timestamp()
        self.path_catalog=r'https://io.apps.fao.org/gismgr/api/v1/catalog/workspaces/'
        self.path_sign_in=r'https://io.apps.fao.org/gismgr/api/v1/iam/sign-in/'
        self.path_refresh=r'https://io.apps.fao.org/gismgr/api/v1/iam/token'
        self.path_download=r'https://io.apps.fao.org/gismgr/api/v1/download/'
        self.path_query=r'https://io.apps.fao.org/gismgr/api/v1/query/'
        self.path_jobs=r'https://io.apps.fao.org/gismgr/api/v1/catalog/workspaces/WAPOR/jobs/'
        self.workspaces={1: 'WAPOR',2: 'WAPOR_2'}
        self.version=1
                
    def getCatalog(self,level=None,cubeInfo=True):
        '''
        Get catalog from workspace
        ''' 

        print('Loading WaPOR catalog...')
        
        try:
            df=self._query_catalog(level)
        except:
            print('ERROR: The data with specified level version is not available in this version')
        if cubeInfo:
            cubes_measure=[]
            cubes_dimension=[]
            for cube_code in df['code'].values:                
                cubes_measure.append(self._query_cubeMeasures(cube_code,
                                                                   version=self.version))
                cubes_dimension.append(self._query_cubeDimensions(cube_code,
                                                                   version=self.version))
            df['measure']=cubes_measure
            df['dimension']=cubes_dimension
        self.catalog=df
        return self.catalog            
            
    def _query_catalog(self,level):
        if level == None:
            request_url = r'{0}{1}/cubes?overview=false&paged=false'.format(self.path_catalog,self.workspaces[self.version])
        else:
            request_url = r'{0}{1}/cubes?overview=false&paged=false&tags=L{2}'.format(self.path_catalog,self.workspaces[self.version],level)
        resp = requests.get(request_url)
        meta_data_items = resp.json()
        
        try:
            response=meta_data_items['response']
            df = pd.DataFrame.from_dict(response, orient='columns')
            return df
        except:
            print('ERROR: No response')
                        
#    def _query_cubeInfo(self,cube_code):
#        request_url = r'{0}{1}/cubes/{2}?overview=false'.format(self.path_catalog,
#        self.workspaces[self.version],cube_code)
#        resp = requests.get(request_url)        
#        try:
#            meta_data_items = resp.json()['response']
#            cube_info=meta_data_items #['additionalInfo']           
#        except:
#            cube_info=None
#        return cube_info
            
    def getCubeInfo(self,cube_code):
        '''
        Get cube info
        '''
        try: 
            catalog=self.catalog
            if 'measure' not in catalog.columns:
                catalog=self.getCatalog(cubeInfo=True)
        except:
            catalog=self.getCatalog(cubeInfo=True)         
        try:
            cube_info=catalog.loc[catalog['code']==cube_code].to_dict('records')[0]         
            return cube_info
        except:
            print('ERROR: Data for specified cube code and version is not available')
    
    def _query_cubeMeasures(self,cube_code,version=1):
        request_url = r'{0}{1}/cubes/{2}/measures?overview=false&paged=false'.format(self.path_catalog,
                        self.workspaces[self.version],cube_code)
        resp = requests.get(request_url)
        cube_measures = resp.json()['response'][0]    
        return cube_measures
    
    def _query_cubeDimensions(self,cube_code,version=1):
        request_url = r'{0}{1}/cubes/{2}/dimensions?overview=false&paged=false'.format(self.path_catalog,
                        self.workspaces[self.version],cube_code)
        resp = requests.get(request_url)
        cube_dimensions = resp.json()['response']
        return cube_dimensions
    
    def _query_accessToken(self,APIToken):
        resp_vp=requests.post(self.path_sign_in,headers={'X-GISMGR-API-KEY':APIToken})
        resp_vp = resp_vp.json()
        self.AccessToken=resp_vp['response']['accessToken']
        self.RefreshToken=resp_vp['response']['refreshToken']        
        self.time_expire=resp_vp['response']['expiresIn'] 
        return self.AccessToken
    
    def _query_refreshToken(self,RefreshToken):
        resp_vp=requests.post(self.path_refresh,params={'grandType':'refresh_token','refreshToken':RefreshToken})
        resp_vp = resp_vp.json()
        self.AccessToken=resp_vp['response']['accessToken']
        return self.AccessToken        

    def getAvailData(self,cube_code,time_range='2009-01-01,2018-12-31',
                     location=[],season=[],stage=[]):
        '''
        cube_code: str
            ex. 'L2_CTY_PHE_S'
        time_range: str
            ex. '2009-01-01,2018-12-31'
        location: list of strings
            default: empty list, return all available locations
            ex. ['ETH']
        season: list of strings
            default: empty list, return all available seasons
            ex. ['S1']
        stage: list of strings
            default: empty list, return all available stages
            ex. ['EOS','SOS']
        '''
        try:
            cube_info=self.getCubeInfo(cube_code)
            #get measures    
            measure_code=cube_info['measure']['code']
            #get dimension
            dimensions=cube_info['dimension']
        except:
            print('ERROR: Cannot get cube info')
            
        dims_ls=[]
        columns_codes=['MEASURES']
        rows_codes=[]
        try:
            for dims in dimensions:
                if dims['type']=='TIME': #get time dims
                    time_dims_code=dims['code']
                    df_time=self._query_dimensionsMembers(cube_code,time_dims_code)
                    time_dims= {
                        "code": time_dims_code,
                        "range": '[{0})'.format(time_range)
                        }
                    dims_ls.append(time_dims)
                    rows_codes.append(time_dims_code)
                if dims['type']=='WHAT':
                    dims_code=dims['code']
                    df_dims=self._query_dimensionsMembers(cube_code,dims_code) 
                    members_ls=[row['code'] for i,row in df_dims.iterrows()]
                    if (dims_code=='COUNTRY' or dims_code=='BASIN'):
                        if location:
                            members_ls=location
                    if (dims_code=='SEASON'):
                        if season:
                            members_ls=season
                    if (dims_code=='STAGE'):
                        if stage:
                            members_ls=stage    
                         
                    what_dims={
                            "code":dims['code'],
                            "values":members_ls
                            }
                    dims_ls.append(what_dims)
                    rows_codes.append(dims['code']) 
    
            df=self._query_availData(cube_code,measure_code,
                             dims_ls,columns_codes,rows_codes)
        except:
            print('ERROR:Cannot get list of available data')
            return None
        #sorted df
        keys=rows_codes+ ['raster_id','bbox','time_code']
        df_dict = { i : [] for i in keys }
        for irow,row in df.iterrows():
            for i in range(len(row)-1):
                if row[i]['type']=='ROW_HEADER':
                    key_info=row[i]['value']
                    df_dict[keys[i]].append(key_info)
                    if keys[i]==time_dims_code:
                        time_info=df_time.loc[df_time['caption']==key_info].to_dict(orient='records')
                        df_dict['time_code'].append(time_info[0]['code'])
                if row[i]['type']=='DATA_CELL':
                    raster_info=row[i]['metadata']['raster']
                    df_dict['raster_id'].append(raster_info['id'])
                    df_dict['bbox'].append(raster_info['bbox'])                    
        df_sorted=pd.DataFrame.from_dict(df_dict)
        return df_sorted            
    
    def _query_availData(self,cube_code,measure_code,
                         dims_ls,columns_codes,rows_codes):                
        query_load={
          "type": "MDAQuery_Table",              
          "params": {
            "properties": {                     
              "metadata": True,                     
              "paged": False,                   
            },
            "cube": {                            
              "workspaceCode": self.workspaces[self.version],            
              "code": cube_code,                       
              "language": "en"                      
            },
            "dimensions": dims_ls,
            "measures": [measure_code],
            "projection": {                      
              "columns": columns_codes,                               
              "rows": rows_codes
            }
          }
        }
            
        resp = requests.post(self.path_query, json=query_load)
        resp_vp = resp.json() 
        if resp_vp['message']=='OK':
            try:
                results=resp_vp['response']['items']
                return pd.DataFrame(results)  
            except:
                print('ERROR: Cannot get list of available data')
        else:
            print(resp_vp['message'])
                
    def _query_dimensionsMembers(self,cube_code,dims_code):
        base_url='{0}{1}/cubes/{2}/dimensions/{3}/members?overview=false&paged=false'       
        request_url=base_url.format(self.path_catalog,
                                    self.workspaces[self.version],
                                    cube_code,
                                    dims_code
                                    )
        resp = requests.get(request_url)
        resp_vp = resp.json()
        if resp_vp['message']=='OK':
            try:
                avail_items=resp_vp['response']
                df=pd.DataFrame.from_dict(avail_items, orient='columns')
                return df
            except:
                print('ERROR: Cannot get dimensions Members')
        else:
            print(resp_vp['message'])
        
    def getLocations(self,level=None):
        '''
        level: int
            2 or 3
        '''
        try:
            df_loc=self.locationsTable
        except:
            df_loc=self._query_locations()
            df_loc=self.locationsTable
        if level is not None:
            df_loc=df_loc.loc[df_loc["l{0}".format(level)]==True]        
        return df_loc
    
    def _query_locations(self):
        query_location={
               "type":"TableQuery_GetList_1",
               "params":{  
                  "table":{  
                     "workspaceCode":self.workspaces[self.version],
                     "code":"LOCATION"
                  },
                  "properties":{  
                     "paged":False
                  },              
                  "sort":[  
                     {  
                        "columnName":"name"
                     }
                  ]
               }        
            }                
        resp = requests.post(self.path_query, json=query_location)
        resp_vp = resp.json()  
        if resp_vp['message']=='OK':
            avail_items=resp_vp['response']
            df_loc = pd.DataFrame.from_dict(avail_items, orient='columns')
            self.locationsTable=df_loc
            df_CTY=df_loc.loc[(df_loc["l2"]==True)&(df_loc["type"]=='COUNTRY')]
            df_BAS=df_loc.loc[(df_loc["l2"]==True)&(df_loc["type"]=='BASIN')]
            self.list_countries=[rows['code'] for index, rows in df_CTY.iterrows()]
            self.list_basins=[rows['code'] for index, rows in df_BAS.iterrows()]
            return df_loc
        else:
            print(resp_vp['message'])
           
    
    def getRasterUrl(self,cube_code,rasterId,APIToken):
        #Get AccessToken
        self.time_now=datetime.datetime.now().timestamp()        
        try:
            AccessToken=self.AccessToken    
            if self.time_now-self.time_start > self.time_expire:
                AccessToken=self._query_refreshToken(self.RefreshToken)
                self.time_start=self.time_now
        except:
            AccessToken=self._query_accessToken(APIToken)
            
        download_url=self._query_rasterUrl(cube_code,rasterId,AccessToken)
        return download_url
        
    def _query_rasterUrl(self,cube_code,rasterId,AccessToken):
        base_url='{0}{1}'.format(self.path_download,
                  self.workspaces[self.version])
        
        headers_val={'Authorization': "Bearer " + AccessToken}
        params_val={'language':'en', 'requestType':'mapset_raster', 
                'cubeCode':cube_code, 'rasterId':rasterId}
        
        resp_vp=requests.get(base_url,headers=headers_val,
                             params=params_val)
        resp_vp = resp_vp.json()
        try:
            resp=resp_vp['response']
            expiry_date = datetime.datetime.now() + datetime.timedelta(seconds=int(resp['expiresIn']))
            download_url = {'url': resp['downloadUrl'],'expiry_datetime': expiry_date}
            return download_url
        except:
            print('Error: Cannot get Raster URL')
            
    
    def _query_jobOutput(self,job_url):
        '''
                 
                    
        '''
        contiue=True        
        while contiue:        
            resp = requests.get(job_url)
            resp=resp.json()
            jobType=resp['response']['type']            
            if resp['response']['status']=='COMPLETED':
                contiue=False
                if jobType == 'CROP RASTER':
                    output=resp['response']['output']['downloadUrl']                
                elif jobType == 'AREA STATS':
                    results=resp['response']['output']
                    output=pd.DataFrame(results['items'],columns=results['header'])
                else:
                    print('ERROR: Invalid jobType')                
                return output
            if resp['response']['status']=='COMPLETED WITH ERRORS':
                contiue=False
                print(resp['response']['log'])
                
                
    def getCropRasterURL(self,bbox,cube_code,
                          time_code,rasterId,APIToken,print_job=True):
        '''
        bbox: str
            latitude and longitude
            [xmin,ymin,xmax,ymax]
        '''
        #Get AccessToken
        self.time_now=datetime.datetime.now().timestamp()        
        try:
            AccessToken=self.AccessToken    
            if self.time_now-self.time_start > self.time_expire:
                AccessToken=self._query_refreshToken(self.RefreshToken)
                self.time_start=self.time_now
        except:
            AccessToken=self._query_accessToken(APIToken)
        #Create Polygon        
        xmin,ymin,xmax,ymax=bbox[0],bbox[1],bbox[2],bbox[3]
        Polygon=[
                  [xmin,ymin],
                  [xmin,ymax],
                  [xmax,ymax],
                  [xmax,ymin],
                  [xmin,ymin]
                ]
        #Get measure_code and dimension_code
        cube_info=self.getCubeInfo(cube_code)
        cube_measure_code=cube_info['measure']['code']
        cube_dimensions=cube_info['dimension']
        
        for cube_dimension in cube_dimensions:
            if cube_dimension['type']=='TIME':
                cube_dimension_code=cube_dimension['code']
        
        #Query payload
        query_crop_raster={
          "type": "CropRaster",
          "params": {
            "properties": {
              "outputFileName": "{0}.tif".format(rasterId),
              "cutline": True,
              "tiled": True,
              "compressed": True,
              "overviews": True
            },
            "cube": {
              "code": cube_code,
              "workspaceCode": self.workspaces[self.version],
              "language": "en"
            },
            "dimensions": [
                   {
                "code": cube_dimension_code,
                "values": [
                  time_code
                ]
              }
            ],
            "measures": [
              cube_measure_code
            ],
            "shape": {
              "type": "Polygon",
              "properties": {
                      "name": "epsg:4326" #latlon projection
                              },
              "coordinates": [
                Polygon
              ]
            }
          }
        }
        resp_vp=requests.post(self.path_query,
                              headers={'Authorization':'Bearer {0}'.format(AccessToken)},
                                                       json=query_crop_raster)
        resp_vp = resp_vp.json()
        try:
            job_url=resp_vp['response']['links'][0]['href']
            if print_job:
                print('Getting download url from: {0}'.format(job_url))
            download_url=self._query_jobOutput(job_url)
            return download_url     
        except:
            print('Error: Cannot get cropped raster URL')

    def getAreaTimeseries(self,shapefile_fh,cube_code,APIToken,
                          time_range="2009-01-01,2018-12-31"):
        '''
        shapefile_fh: str
                    "E:/Area.shp"
        time_range: str
                    "YYYY-MM-DD,YYYY-MM-DD"
        '''
        #Get AccessToken
        self.time_now=datetime.datetime.now().timestamp()        
        try:
            AccessToken=self.AccessToken    
            if self.time_now-self.time_start > self.time_expire:
                AccessToken=self._query_refreshToken(self.RefreshToken)
                self.time_start=self.time_now
        except:
            AccessToken=self._query_accessToken(APIToken)
        #get shapefile info
        import ogr
        dts=ogr.Open(shapefile_fh)
        layer=dts.GetLayer()
        epsg_code=layer.GetSpatialRef().GetAuthorityCode(None)
        shape=layer.GetFeature(0).ExportToJson(as_object=True)['geometry']
        shape["properties"]={"name": "EPSG:{0}".format(epsg_code)}
        
        #get cube info
        cube_info=self.getCubeInfo(cube_code)
        cube_measure_code=cube_info['measure']['code']
        for dims in cube_info['dimension']:
            if dims['type']=='TIME':
                cube_dimension_code=dims['code'] 
        
        #query load
        query_areatimeseries={
          "type": "AreaStatsTimeSeries",
          "params": {
            "cube": {
              "code": cube_code,
              "workspaceCode": self.workspaces[self.version],
              "language": "en"
            },
            "dimensions": [
              {
                "code": cube_dimension_code,
                "range": "[{0})".format(time_range)
              }
            ],
            "measures": [
              cube_measure_code
            ],
            "shape": shape
          }
        }
        
        resp_query=requests.post(self.path_query,
                                 headers={'Authorization':'Bearer {0}'.format(AccessToken)},
                                          json=query_areatimeseries)
        resp_query = resp_query.json()
        try:
            job_url=resp_query['response']['links'][0]['href'] 
        except:
            print('Error: Cannot get server response')
            return None
        try:
            print('Getting result from: {0}'.format(job_url))
            output=self._query_jobOutput(job_url)     
            return output
        except:
            print('Error: Cannot get job output')
            return None

            
    def getPixelTimeseries(self,pixelCoordinates,cube_code,
                           time_range="2009-01-01,2018-12-31"):
        '''
        pixelCoordinates: list
            [37.95883206252312, 7.89534]
        '''
        #get cube info
        cube_info=self.getCubeInfo(cube_code)
        cube_measure_code=cube_info['measure']['code']
        for dims in cube_info['dimension']:
            if dims['type']=='TIME':
                cube_dimension_code=dims['code'] 
        
        #query load
        query_pixeltimeseries={
              "type": "PixelTimeSeries",
              "params": {
                "cube": {
                  "code": cube_code,
                  "workspaceCode": self.workspaces[self.version],
                  "language": "en"
                },
                "dimensions": [
                  {
                    "code": cube_dimension_code,
                    "range": "[{0})".format(time_range)
                  }
                ],
                "measures": [
                  cube_measure_code
                ],
                "point": {
                  "crs": "EPSG:4326", #latlon projection              
                  "x":pixelCoordinates[0],
                    "y":pixelCoordinates[1]
                }
              }
            }
               
        #requests
        resp_query=requests.post(self.path_query,json=query_pixeltimeseries)
        resp_vp=resp_query.json()
        if resp_vp['message']=='OK':               
            try:
                results=resp_vp['response']
                df=pd.DataFrame(results['items'],columns=results['header'])
                return df
            except:
                print('Error: Server response is empty')
                return None
        else:
            print(resp_vp['message'])

                

        