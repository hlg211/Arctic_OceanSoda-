#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 07:55:00 2020

Example driver script to run all parts of the OceanSODA algorithm comparison,
gridded carbonate system time series, Amazon DIC outflow case study, and 
the coral reef vulnerability case study.

@author: tom holding
"""

from string import Template;

from os import path; 
import pandas as pd;
pd.set_option("mode.chained_assignment", None);

import os
path1='/data/datasets/Projects/OceanSODA/Arctic_OceanSoda/Chapter3code'
os.chdir(path1)  # changes current working directory
all_files_in_home_dir = os.listdir()
print(all_files_in_home_dir)

import osoda_global_settings;

settings = osoda_global_settings.get_default_settings();
##########
# Compare algorithm performance using matchup data set
# Compute all metrics and determine the 'best' and 'long' optimal algorithm
#    for DIC and AT
import osoda_algorithm_comparison;

#settings['regions'] = ['OFS'] 
osoda_algorithm_comparison.main(settings);



########## 

# #Download all prediction data sets and calculate gridded time series predictions
# import osoda_calculate_gridded_predictions;
# years = settings["years"];
# regions = settings["regions"];
# regionMaskPath= settings["regionMasksPath"];

# # #Run for "Best algorithms allowing for reduced temporal overlap and validation matchups" - (aka weighted with no time or restriction on the number of matchups)
# optAlgoTableBest = "/data/datasets/Projects/OceanSODA/Arctic_OceanSoda/output/algo_metrics/overall_best_algos.csv";
# griddedTimeSeriesOutputPathBest = settings["bestGriddedTimeSeriesPathTemplate"];
# osoda_calculate_gridded_predictions.main(optAlgoTableBest, griddedTimeSeriesOutputPathBest, years, regions, regionMaskPath);

# # #Run for the 'optimal algorithms' (aka min 8 year time series and n=30 matchups) - this is main dataset run. 
# optAlgoTableLong = "output/algo_metrics/overall_best_algos_min_years=8.csv";
# griddedTimeSeriesOutputPathLong = settings["longGriddedTimeSeriesPathTemplate"];
# osoda_calculate_gridded_predictions.main(optAlgoTableLong, griddedTimeSeriesOutputPathLong, years, regions, regionMaskPath);

# # #Run for the 'Best  unweighted algorithms' note still with (min 8 year time series and n=30 matchups) -  
# optAlgoTableLongunweighted = "output/algo_metrics/overall_best_algos_unweighted_min_years=8.csv";
# griddedTimeSeriesOutputPathLongunweighted = settings["longunweightedGriddedTimeSeriesPathTemplate"];
# osoda_calculate_gridded_predictions.main(optAlgoTableLongunweighted, griddedTimeSeriesOutputPathLongunweighted, years, regions, regionMaskPath);

