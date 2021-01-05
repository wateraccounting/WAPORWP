[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3980715.svg)](https://doi.org/10.5281/zenodo.3980715)

# <font color='#ff009a'> Standardized protocol for land and water productivity analyses using WaPOR</font> 
### Version 1.1
**Water Productivity Improvement in Practice (Water-PIP)** 
<br/>**Prepared by IHE Delft**
<br/>**October 2020**

![title](ReadmeIMG/Figmd_1.png)

**Authors:** 
* Abebe Chukalla (a.chukalla@un-ihe.org),  
* Marloes Mul, 
* Poolad Karimi

With contributions from: Bich Tran, Quan Pan, Solomon Seyoum


# 1	Introduction 
Productivity is defined as a measure of gains per unit of resource use (Zwart and Bastiaanssen, 2004). For agriculture purposes, the most important indicators are biophysical, economic or social gains compared to the amount of land and water used. The most commonly used productivity indicator in agriculture is yield which defines the biophysical gain per unit of land (also called land productivity). With increasing concerns about the available water resources, water productivity has gained interest. 

## 1.1	Importance 
The combined increasing gains per unit of water and land would benefit the farmer and scheme manager as well as being beneficial at basin level.
Farmers aim to optimise the benefit generated per unit of land, as this is their main constraint. While the top priority of the river basin authority is to allocate water resources in equitable, efficient and sustainable manner between different water uses/ users. Thus, at river basin level, the interest is to optimise productivity at river basin level while maintaining equity and sustainability as core values. Policy makers are often interested to increase production and thus national income as well as increase employment. 

## 1.2	WaPOR data
FAO’s portal to monitor Water Productivity through Open-access of Remotely sensed derived (WaPOR) was “created to provide relevant and specific information on water and biomass status to develop solutions to sustainably increase agricultural land and water productivity” . WaPOR is the first comprehensive dataset that combines water use (actual evaporation, transpiration and interception), production (net primary production), land use (land cover classification), phenology, climate (precipitation and reference evapotranspiration) and water productivity layers covering sub-Saharan Africa and the Near East and North African regions. The data is available at decadal time steps and in near real-time for the period between 2009 to present day. WaPOR datasets are available at continental scale (Level 1 at 250 m), country and river basin (Level 2 at 100 m) and project level (Level 3 at 30 m). The latest WaPOR portal (WaPOR v2.1), was improved from WaPOR v1.0 following the independent quality assessment by IHE Delft and ITC (FAO and IHE, 2019). The methodology used for compiling the WaPOR database is provided in FAO (2020a). 

## 1.3	Ground data
Ground data such as boundary of the farm (to download WaPOR data and filter non cropped area), moisture content of fresh biomass (to convert dry matter to biomass), above ground over total biomass (to estimate the above ground biomass), start and end of seasons (to aggregate water and climate data per crop season), harvest index (to derive crop yield from above ground biomass) and crop coefficient (to estimate potential evapotranspiration from reference evapotranspiration) are required.
 
## 1.4	Protocol: objectives, scope and target audience
The protocol is aimed at guiding users to understand the different layers contained in the FAO Water Productivity Open-access portal (WaPOR) which can be used for land and water productivity analyses. It provides python scripts which can be used to calculate land and water productivity and other performance indicators such as water consumption, beneficial fraction, equity, adequacy, reliability as well as estimating productivity gaps. For each step, the protocol provides information about the assumptions used and provides links to reference materials.  
<br/>**Scope:** The protocol is tailored to biophysical water productivity with respect to consumed water use and land productivity at an areas (fields, and schemes) in similar agro-climatic zones. The protocol can be applied to crop production regardless of the water sources (e.g. from exclusively rainfall (rainfed), or irrigation (augmented through surface water and/or groundwater, or flood /spate)). The protocol is developed for agricultural areas with a single crop and same cropping season, which can vary between years. Implementing the protocol beyond fields/ scheme level such as at river basin and country levels, which could fall in different agro-climatic zones, require normalization for climate variation – which is outside the scope of the protocol.   
<br/>**Target**: The protocol is developed for project leads, irrigation managers and researchers who have a basic understanding of python and agricultural practices.  

# 2	Installation requirements
The scripts to download and process the WaPOR data for land and water productivity assessment are developed in the python programming language. The scripts can be downloaded from the wateraccounting repository on GitHub  and run in Jupyter Notebook. Beginners of python programming are advised to follow the OCW of IHE Delft on python scripting before starting with implementing the provided scripts . A beginning programmer should be able to run the scripts, it is advised to run them using Jupyter notebook. The following sections describe the installation requirements. 
## 2.1	Running from Jupyter notebook
### The requirement of the python and libraries used in the protocol
* python 3.7.3
* numpy 1.16.4
* pandas 0.24.2 
* GDAL 2.3.3
* pyshp 2.1.0 

## 2.1	Install python, Jupyter notebook and libraries (packages)
#### i) Install python and jupyter notebook using the Anaconda distribution: https://www.anaconda.com/products/individual
Use the anaconda installer, which is tailored to different operating system: window (64-Bit and 32-Bit), MacOS (64-Bit) or Linux system.
>Read more on Jupyter notebook: https://jupyter.org/, https://packaging.python.org/overview/

#### ii) Install packages: 
##### Packages such as GDAL, pyshp can be installed using pip or conda. 
>a) **pip** installs python **packages** in any environment. **Install a pip package in the current Jupyter kernel**
Pip is the Python Packaging Authority’s recommended tool for installing packages from the Python Package Index (PyPI), which is a repository of software for the Python programming language (https://pypi.org/). Pip installs python packages in any environment. Type the following codes to Install a pip package in the current Jupyter kernel: 
> <br/> <font color='#0d00ff'>import sys </font>
> <br/> <font color='#0d00ff'>!{sys.executable} -m pip install 'package' </font>

>b) **conda** installs any package in **conda environments**. **Install a conda package in the current Jupyter kernel**
 Conda is a cross platform package and environment manager that installs and manages conda packages from the Anaconda repository (https://repo.anaconda.com/) and the Anaconda Cloud (https://anaconda.org/). Conda installs any package in conda environments. Type the following codes to Install a conda package in the current Jupyter kernel:
> <br/> <font color='#0d00ff'>import sys </font>
> <br/> <font color='#0d00ff'>!conda install --yes --prefix {sys.prefix} 'package' </font>
More tutorials on conda commands: https://docs.conda.io/projects/conda/en/latest/user-guide/index.html

![title](ReadmeIMG/Figmd_2.png)

# 3	Structure of the protocol 
The protocol has six modules, which are described in detail in the following sections. For each of the modules a Jupyter notebook was developed, containing the scripts. Module 0 focusses on downloading WaPOR data on actual water consumption (ET), actual transpiration, reference evapotranspiration and net primary production. In Module 1, the pre-processing of the data to match the spatial resolution and remove non-crop pixels are conducted. In Module 2, the seasonal water consumption (transpiration, actual evapotranspiration, reference evapotranspiration and potential evapotranspiration) and seasonal net primary production are computed. In Module 3, different performance indicators are calculated. In Module 4, land and water productivity are computed. And finally in Module 5, bright spots and productivity gaps are calculated. 

![title](ReadmeIMG/Figmd_3.png)

## 3.1	Download WaPOR data (Module 0)
##### Step 0a Import modules/libraries
##### Step 0b Read geographical extent of the study area
##### Step 0c Bulk-download WaPOR data for the study area extent

## 3.2	Pre-processing WaPOR data (Module 1) 
##### Step 1a Import modules/libraries 
##### Step 1b Resample raster data 
##### Step 1c Filter non-cropped area using land cover map and project boundary 

## 3.3	Computing Seasonal Water Consumption & Net Primary Production (Module 2) 
##### Step 2a Set up: Import modules/libraries 
##### Step 2b Defining function and crop season
##### Step 2b Calculate seasonal T, ET, RET, ETp, NPP 

## 3.4	Calculate performance indicators (Module 3)
##### Step 3a Set up 
##### Step 3b Calculate Uniformity
Uniformity measures the evenness of the water supply in various portion of a field. Equity is the measure of spatial uniformity of water use among users, which can be water users at a tertiary unit or among tertiary units under a particular secondary canal. In the absence of plot or tertiary boundaries, the spatial uniformity of water use on a per unit area (pixel) bases can be used to measure uniformity or equity. It is calculated as the coefficients of variation (CV) of seasonal ETa in the area of interest. A CV of 0 to 10 % is defined as good uniformity, CV of 10 to 25 % as fair uniformity and CV > 25 % as poor uniformity (Bastiaanssen et al., 1996; Molden and Gates, 1990; Karimi et al., 2019).

##### Step 3c Calculate Efficiency (Beneficial fraction)
Beneficial fraction (BF) is measures the efficiency of on farm water and agronomic practices in converting water for crop growth. It is the percentage of the water that is consumed as transpiration compared to overall field water consumption (ETa). 

##### Step 3d Calculate Adequacy
Adequacy (A) is the measure of the degree of agreement between available water and crop water requirements in an irrigation system (Bastiaanssen and Bos, 1999; Clemmens and Molden, 2007). It is calculated as the relative evapotranspiration, which is the ratio of actual evapotranspiration over potential evaporation (Equation 3) (Kharrou et al., 2013; Karimi et al., 2019). 

##### Step 3e Calculate Relative Water Deficit
Relative Water Deficit (RWD) provides an indication on the level of water shortage found in the irrigation system. It is applied for a mono crop system, where the actual ET is compared to the maximum ET.

## 3.5	Land and water productivity (Module 4)
##### Step 4a Set up 
##### Step 4b Calculate land productivity: i) biomass and ii) crop yield
Land productivity is defined as the above-ground biomass production or yield in ton/ha/season.

##### Step 4c Calculate i) biomass water productivity and ii) crop water productivity
Biomass and crop Water productivity is estimated as the ratio of above-ground biomass or yield over actual evapotranspiration.

## 3.6	Productivity gaps and production projection (Module 5)
##### Step 5a Set up 
##### Step 5b Calculate the target productivity
The target productivity is a target for land and water productivity which is attainable under the local climatic conditions. This step of the script describes how the target is set and how bright spots are identified and how the productivity gap (related to the target) is estimated.
The target can be set for individual years to incorporate specific wet or dry conditions during that particular year. In our case we set the target at the 95 percentile of the land or water productivity for each year (Figure 2), this can be changed in the script. The corresponding ETa is also defined as the target ETa.

##### Step 5c Identify bright spots 
The bright spots are fields that have both land and water productivity equal or greater than the targets. The location of the bright spots are then mapped for the individual targets (biomass or yield and water productivity as well as areas where both targets are exceeded
##### Step 5d Calculate productivity gaps¶
Productivity gap is defined as the difference between the productivity at plot level and the target productivity. The production gap is defined as the sum of the land productivity gaps of a particular crop over area. The potential increase in biomass/ yield production of a particular crop in an area of interest is calculated by adding the productivity gap across the area. 

# 4	Example, Protocol applied at Xinavane irrigation scheme
### 4.1	Data
Case: crop = sugarcane, country = Mozambique, project = Xinavane
WaPOR and local data of Table 5 are used to implement the protocol. The Level 2 data used in this study include actual evapotranspiration and interception and net primary production at a decadal timescale and annual land cover classification. In addition, decadal precipitation at 5 km resolution, decadal reference evapotranspiration at 25 km resolution. The precipitation and reference evapotranspiration datasets were downscaled to 100 m resolution.
![title](ReadmeIMG/Figmd_4.png)

### 4.2	WaPOR data consistency 
It is recommended that consistency check and validation of WapOR data are done.  

### 4.3.2	Results
![title](ReadmeIMG/Figmd_5.png) 
![title](ReadmeIMG/Figmd_6.png) 


# 5	References
Allen, R. G., Pereira, L. S., Raes, D., and Smith, M.: Crop evapotranspiration-Guidelines for computing crop water requirements-FAO Irrigation and drainage paper 56, Fao, Rome, 300, D05109, 1998.
<br/>Bastiaanssen, W. G., Van der Wal, T., and Visser, T.: Diagnosis of regional evaporation by remote sensing to support irrigation performance assessment, Irrigation and Drainage Systems, 10, 1-23, 1996.
<br/>Doorenbos, J., and Kassam, A.: FAO irrigation and drainage paper No. 33 “Yield response to water”, FAO–Food and Agriculture Organization of the United Nations, Rome, 1979.
<br/>Karimi, P., Bongani, B., Blatchford, M., and de Fraiture, C.: Global satellite-based ET products for the local level irrigation management: An application of irrigation performance assessment in the sugarbelt of Swaziland, Remote Sensing, 11, 705, 2019.
<br/>Kharrou, M. H., Le Page, M., Chehbouni, A., Simonneaux, V., Er-Raki, S., Jarlan, L., Ouzine, L., Khabba, S., and Chehbouni, G.: Assessment of equity and adequacy of water delivery in irrigation systems using remote sensing-based indicators in semi-arid region, Morocco, Water resources management, 27, 4697-4714, 2013.
<br/>Smith, D., Inman-Bamber, N., and Thorburn, P.: Growth and function of the sugarcane root system, Field Crops Research, 92, 169-183, 2005.
<br/>Villalobos, F. J., and Fereres, E.: Principles of agronomy for sustainable agriculture, Springer, 2016.
<br/>WaPOR: The FAO portal to monitor Water Productivity through Open access of Remotely sensed derived data, 23 October, FAO, Rome, Italy, 2019.
<br/>Yilma, W. A., Opstal, J. V., Karimi, P., and Bastiaanssen, W.: Computation and spatial observation of water productivity in Awash River Basin, UNESCO-IHE, Delft, 2017.
<br/>Zwart, S. J., and Bastiaanssen, W. G.: Review of measured crop water productivity values for irrigated wheat, rice, cotton and maize, Agricultural water management, 69, 115-133, 2004.


```python

```
