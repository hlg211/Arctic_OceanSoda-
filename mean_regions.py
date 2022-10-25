# -*- coding: utf-8 -*-
"""
CreSSSed on Mon Mar 21 14:53:01 2022

@author: hlg211
"""
from pandas import DataFrame
from string import Template
from os import path, makedirs
from netCDF4 import Dataset
import pandas as pd
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

import datetime
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

import matplotlib as mpl
# Handle date time conversions between pandas and matplotlib
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import numpy as np

#path1 = "/data/datasets/Projects/OceanSODA/Arctic_OceanSoda"
path1='/data/datasets/Projects/OceanSODA/Arctic_OceanSoda'
os.chdir(path1)  # changes current working directory
all_files_in_home_dir = os.listdir()
print(all_files_in_home_dir)

#matchup= Dataset('/data/datasets/Projects/OceanSODA/Arctic_OceanSoda/matchup_database/OCEANSODA-MMDB-2015-fv01.nc', 'r')
#projectRoot = "/data/datasets/Projects/OceanSODA/Arctic_OceanSoda"
projectRoot ='/data/datasets/Projects/OceanSODA/Arctic_OceanSoda'
from os_algorithms.utilities import convert_time_to_date
from osoda_global_settings import get_default_settings
from osoda_global_settings import DatasetInfo
import os_algorithms.utilities as utilities
import datetime as dt
settings = get_default_settings()
# importing in region mask already defined in setting file
settings['regions'] = ['AiS']

matchupDatasetTemplate = Template(path.join(projectRoot, "matchup_database", "OCEANSODA-MMDB-${YYYY}-fv01.nc"))  # Location of the matchup dataset
datasetInfoMap = {"date": DatasetInfo(commonName="date", datasetName="time", matchupVariableName="time", matchupDatabaseTemplate=settings["matchupDatasetTemplate"]),
                                  #"dayofyear": DatasetInfo(commonName="dayofyear", datasetName="time", matchupVariableName="time", matchupDatabaseTemplate=settings["matchupDatasetTemplate"]),
                                  "lon": DatasetInfo(commonName="lon", datasetName="lon", matchupVariableName="lon", matchupDatabaseTemplate=settings["matchupDatasetTemplate"]),
                                   "lat": DatasetInfo(commonName="lat", datasetName="lat", matchupVariableName="lat", matchupDatabaseTemplate=settings["matchupDatasetTemplate"]),
                                   "SST": [#DatasetInfo(commonName="SST", datasetName="SST-ESACCI", matchupVariableName="cci_sst_mean", matchupDatabaseError="cci_sst_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"], predictionDatasetTemplate=Template(path.join(projectRoot,"data", "prediction_datasets/ESACCI_SST/processed/ESACCI-SST-OSTIA-LT-v02.0-fv01.1_${YYYY}_${MM}_processed.nc")), predictionDatasetVariable="sst", predictionDatasetError="sst_err"),
                                           # DatasetInfo(commonName="SST", datasetName="SST-CORA", matchupVariableName="cora_temperature_mean", matchupDatabaseError="cora_temperature_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"], predictionDatasetTemplate=Template(path.join(projectRoot, "data", "prediction_datasets/CORA_SSS_SST/${YYYY}/OA_CORA5.2_${YYYY}_${MM}_processed.nc")), predictionDatasetVariable="TEMP", predictionDatasetError="TEMP_err"),
                                           # DatasetInfo(commonName="SST", datasetName="SST-OISST", matchupVariableName="noaa_sst_mean", matchupDatabaseError="noaa_sst_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"], predictionDatasetTemplate=Template(path.join(projectRoot, "data", "prediction_datasets/OISST_SST/processed/processed/${YYYY}/${YYYY}${MM}01_OCF-SST-GLO-1M-100-REYNOLDS_1.0x1.0.nc")), predictionDatasetVariable="sst_mean", predictionDatasetError="sst_stddev"),
                                           
                                           DatasetInfo(commonName="SST", datasetName="region_sst_mean", matchupVariableName="insitu_sst_mean:", matchupDatabaseError="insitu_sst_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"]),
                                            ],
                                   "SSS": [#DatasetInfo(commonName="SSS", datasetName="SSS-ESACCI", matchupVariableName="cci_sss_mean", matchupDatabaseError="cci_sss_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"], predictionDatasetTemplate=Template(path.join(projectRoot, "data", "prediction_datasets/ESACCI_SSS/processed/${YYYY}/ESACCI-SEASURFACESALINITY-L4-CENTRED15Day_${YYYY}_${MM}_processed.nc")), predictionDatasetVariable="sss", predictionDatasetError="sss_err"),
                                           DatasetInfo(commonName="SSS", datasetName="SSS-CORA", matchupVariableName="cora_salinity_mean", matchupDatabaseError="cora_salinity_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"], predictionDatasetTemplate=Template(path.join(projectRoot, "data", "prediction_datasets/CORA_SSS_SST/${YYYY}/OA_CORA5.2_${YYYY}_${MM}_processed.nc")), predictionDatasetVariable="PSAL", predictionDatasetError="PSAL_err"),
                                           #DatasetInfo(commonName="SSS", datasetName="SSS-RSS-SMAP", matchupVariableName="remss_smap_sss_mean", matchupDatabaseError="remss_smap_sss_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"], predictionDatasetTemplate=Template(path.join(projectRoot, "data", "prediction_datasets/RSS_SMAP_SSS/RSS_smap_SSS_L3_monthly_${YYYY}_${MM}_FNL_v04.0_processed.nc")), predictionDatasetVariable="sss", predictionDatasetError="sss_err"),
                                           ##DatasetInfo(commonName="SSS", datasetName="SSS-ISAS", matchupVariableName="isas15_salinity_mean", matchupDatabaseError="isas15_salinity_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"], predictionDatasetTemplate=Template(path.join(projectRoot, "data", "prediction_datasets/ISAS_SSS_SST/${YYYY}/ISAS15_DM_${YYYY}_${MM}_processed.nc")), predictionDatasetVariable="PSAL", predictionDatasetError="PSAL_err"),
                                           DatasetInfo(commonName="SSS", datasetName="SSS-BEC-Arctic", matchupVariableName="arctic_sss_mean", matchupDatabaseError="arctic_sss_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"]), #predictionDatasetTemplate=Template(path.join(projectRoot, "data", "prediction_datasets/")), predictionDatasetVariable="PSAL", predictionDatasetError="PSAL_err")) 
                                           #DatasetInfo(commonName="SSS", datasetName="region_sss_mean", matchupVariableName="insitu_sss_mean", matchupDatabaseError="insitu_sss_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"]),
                                            ],                                                                                                                                                                                            
                                   "Chla": DatasetInfo(commonName="chla", datasetName="OC-ESACCI", matchupVariableName="cci_oc_chloro-a_mean", matchupDatabaseError="cci_oc_chloro-a_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"], predictionDatasetTemplate=Template(path.join(projectRoot, "data", "old_prediction_datasets/ESA_CCI_V5/chlor_a/${YYYY}/ESACCI-OC-L3S-CHLOR_A-MERGED-1D_DAILY_4km_GEO_PML_OCx-${YYYY}${MM}${DD}-fv5.0.nc")), predictionDatasetVariable="chlor_a", predictionDatasetError="chlor_a_log10_rmsd"),
                                   "DO": DatasetInfo(commonName="DO", datasetName="DO-WOA", matchupVariableName="woa18_oxygen_mean", matchupDatabaseError="woa18_oxygen_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"], predictionDatasetTemplate=Template(path.join(projectRoot, "data", "prediction_datasets/WOA_dissolved_oxygen/woa18_all_o${MM}_processed.nc")), predictionDatasetVariable="o_an", predictionDatasetError="o_uncertainty"),
                                     "NO3": DatasetInfo(commonName="NO3", datasetName="NO3-WOA", matchupVariableName="woa18_nitrate_mean", matchupDatabaseError="woa18_nitrate_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"], predictionDatasetTemplate=Template(path.join(projectRoot, "data", "prediction_datasets/WOA_nitrate/woa18_all_n${MM}_processed.nc")), predictionDatasetVariable="n_an", predictionDatasetError="n_uncertainty"),
                                     "PO4": DatasetInfo(commonName="PO4", datasetName="PO4-WOA", matchupVariableName="woa18_phosphate_mean", matchupDatabaseError="woa18_phosphate_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"], predictionDatasetTemplate=Template(path.join(projectRoot, "data", "prediction_datasets/WOA_phosphate/woa18_all_p${MM}_processed.nc")), predictionDatasetVariable="p_an", predictionDatasetError="p_uncertainty"),
                                    "SiO4":DatasetInfo(commonName="SiO4", datasetName="SiO4-WOA", matchupVariableName="woa18_silicate_mean", matchupDatabaseError="woa18_silicate_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"], predictionDatasetTemplate=Template(path.join(projectRoot, "data", "prediction_datasets/WOA_silicate/woa18_all_i${MM}_processed.nc")), predictionDatasetVariable="i_an", predictionDatasetError="i_uncertainty"),
                                     "DIC": DatasetInfo(commonName="DIC", datasetName="DIC-matchup", matchupVariableName="insitu_dic_mean", matchupDatabaseError="insitu_dic_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"]),                
                                    "AT": DatasetInfo(commonName="AT", datasetName="AT-matchup", matchupVariableName="insitu_ta_mean", matchupDatabaseError="insitu_ta_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"]),
                                   
                                     #"depth": DatasetInfo(commonName="depth", datasetName="depth-matchup", matchupVariableName="depth_mean", matchupDatabaseError="depth_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"]),
                                    "distance": DatasetInfo(commonName="distance", datasetName="distance-matchup", matchupVariableName="insitu_dist2coast_mean", matchupDatabaseError="insitu_dist2coast_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"]),
                                    "region_pH_mean": DatasetInfo(commonName="pH", datasetName="pH-matchup", matchupVariableName="insitu_ph_mean", matchupDatabaseError="insitu_ph_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"]),
                                   "region_pco2w_mean": DatasetInfo(commonName="pco2", datasetName="pCO2-matchup", matchupVariableName="insitu_pco2w_mean", matchupDatabaseError="insitu_pco2w_stddev", matchupDatabaseTemplate=settings["matchupDatasetTemplate"]),
                                    'region_id': DatasetInfo(commonName="region_id", datasetName="region_id", matchupVariableName="region_id", matchupDatabaseError="region_id", matchupDatabaseTemplate=settings["matchupDatasetTemplate"])
                                   };

dfList = []
commonNames = datasetInfoMap.keys()
matchupVariableName = datasetInfoMap.keys()
years = settings["years"]

#indexc=0

for year in years:
    #if year is less than 1974 :
        
        
    matchupDatasetPath = matchupDatasetTemplate.safe_substitute(YYYY=year)
    nc = Dataset(matchupDatasetPath, 'r')

    # Create a pandas dataframe from the netCDF file

    df = pd.DataFrame()
    
    #variable check
    vars = nc.variables.keys()
    
    
    # calling up variables with the netcdf files
    df["lat"] = nc[datasetInfoMap["lat"].matchupVariableName][:]
    df["lon"] = nc[datasetInfoMap["lon"].matchupVariableName][:]
    df["region_id"] = nc[datasetInfoMap["region_id"].matchupVariableName][:]
    df["date"] = nc[datasetInfoMap["date"].matchupVariableName][:]
    #df["depth"] = nc[datasetInfoMap["depth"].matchupVariableName][:]
    df["distance"] = nc[datasetInfoMap["distance"].matchupVariableName][:]
    #df.length'dataframe length'.index to length of dataframe 
    #df['obs']= nc[datasetInfoMap["obs"].matchupVariableName][:]
    #df["SST"] = nc[datasetInfoMap["SST"].matchupVariableName][:]
    if 'cora_salinity_mean' in vars:
        df["SSS"] = nc[datasetInfoMap["SSS"].matchupVariableName][:]
    else:
        df["SSS"] = np.NaN 
    if "woa18_nitrate_n_an" in vars:
        df["NO3"] = nc[datasetInfoMap["NO3"].matchupVariableName][:]
    else:
        df["NO3"] = np.NaN 
    
   
    if "woa18_phosphate_p_an" in vars:
        df["PO4"] = nc[datasetInfoMap["PO4"].matchupVariableName][:]
    else:
        df["PO4"] = np.NaN 
        
    if "woa18_silicate_i_an" in vars:
        df["SiO4"] = nc[datasetInfoMap["SiO4"].matchupVariableName][:]
    else:
        df["SiO4"] = np.NaN
    if "woa18_oxygen_o_an" in vars:
        df["DO"] = nc[datasetInfoMap["DO"].matchupVariableName][:]
    else:
        df["DO"] = np.NaN
        
    if "region_at_mean" in vars:
        df["AT"] = nc[datasetInfoMap["AT"].matchupVariableName][:]
    else:    
        df["AT"]= np.NaN
    if "region_dic_mean" in vars:
        df["DIC"] = nc[datasetInfoMap["DIC"].matchupVariableName][:]
    else:    
        df["AT"]= np.NaN
    if "cci_oc_chloro-a_mean" in vars:
        df["chla"] = nc[datasetInfoMap["chla"].matchupVariableName][:]
    else:    
        df["chla"]= np.NaN
    if "region_pco2w_mean" in vars:
        df["pco2"] = nc[datasetInfoMap["pco2"].matchupVariableName][:]
    else:    
        df["pco2"]= np.NaN
    if "region_ph_mean" in vars:
        df["ph"] = nc[datasetInfoMap["ph"].matchupVariableName][:]
    else:    
        df["ph"]= np.NaN

    # Convert date from time in seconds since 1980-01-01 to a pd.datetime object
    df["date"] = convert_time_to_date(df["date"])
    # df["SSTinsitu"] = nc[datasetInfoMap["SSTinsitu"].matchupVariableName][:]; # gets rid of nan values

    df.index = pd.to_datetime(df["date"])  # index dataframe by date
    # df = df.drop(columns=["date"]) # drops the date column in rest of table
    df=df.replace( 1e+20, np.nan) 

    df = df.replace({"AT": 1,
                     "DIC": 1, }, np.nan)
   # df.dropna(subset=["SST"], inplace=True)  # gets rid of nan values
    df.dropna(subset=["SSS"], inplace=True)
    #df.dropna(subset=["DIC"], inplace=True)
    df.dropna(subset=["AT"], inplace=True)
    #matchupDataindex=
    #   #### mask file into dataframe,calling variables
   # maskNC = Dataset(
       # '/data/datasets/Projects/OceanSODA/Arctic_OceanSoda/aux_data/Arctic_mask_file2.nc', 'r')
    maskNC= Dataset ('/data/datasets/Projects/OceanSODA/Arctic_OceanSoda/aux_data/Arctic_mask_file2.nc', 'r')
    maskName =  "PiS"#,"OFS","RiS_1","RiS_2"]
    # for i in range(0,len(maskName)):
    maskValue = 1
    mask = maskNC.variables[maskName][:]

    # def subset_from_mask(data, maskNC, maskName, maskValue=1):
    # Read the mask and lon/lat dimension values
    mask = maskNC.variables[maskName][:]
    lats = maskNC.variables["lat"][:]
    lons = maskNC.variables["lon"][:]

    # find index of closest mask lats value to each row
    a, b = np.meshgrid(lats, df["lat"])  # df=match data base
    latIndices = np.abs(a-b).argmin(axis=1)
    # and again for longitudesname dateframe filename netcdf
    a, b = np.meshgrid(lons, df["lon"])
    lonIndices = np.abs(a-b).argmin(axis=1)

    df = df.iloc[mask[(latIndices, lonIndices)] == maskValue]

    dfList.append(df)
    del vars

matchupData = pd.concat(dfList, ignore_index=True)
matchupData.head()
#matchupData.index = pd.to_datetime(df["date"])
#get year and month column in dataframe 
matchupData['year'] = [d.year for d in matchupData.date]
matchupData['month'] = [d.strftime('%m') for d in matchupData.date]# %b to change it to month name 

matchupData['dayofyear'] = matchupData['date'].dt.dayofyear

#matchupData.index= matchupData["month"]
matchupData=matchupData.sort_index()

matchupData['date']=matchupData['date'].dt.date 
 
matchupData.mean()
matchupData.max()
matchupData.min()
matchupData.std()
matchupData.count()



































