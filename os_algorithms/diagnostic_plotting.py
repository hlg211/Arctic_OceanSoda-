#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 13:49:57 2020

@author: tom holding
"""

from os import path;
import pandas as pd;
import matplotlib.pyplot as plt;

#imports the module operating system
import os, glob

# this gets your current working directory

# path1="D:\data\OceanSODA-master";
# os.chdir(path1) #changes current working directory 
# glob.glob ('*.NC') # RETURNS A LIST OF ALL THE .NC FILES in current working directory
# [os.path.realpath(f) for f in glob.glob ('*NC')]

# all_files_in_home_dir=os.listdir()

# print(all_files_in_home_dir)

def prediction_accuracy_plot(insituOutput, modelOutput, title, outputVariable, savePath=None):
    guidelineX1 = min(insituOutput.min(), modelOutput.min())#*0.9;
    guidelineX2 = max(insituOutput.max(), modelOutput.max())#*1.1;
    
    plt.figure();
    plt.plot([guidelineX1, guidelineX2], [guidelineX1, guidelineX2]);
    plt.scatter(insituOutput, modelOutput);
    plt.xlabel("in situ %s (umol/kg)" % outputVariable);
    plt.ylabel("predicted %s (umol/kg)" % outputVariable);
    plt.title(title);
    
    if savePath is not None:
        plt.savefig(savePath);
        plt.close();


if __name__ == "__main__":
######tmp scratchpad
    import osoda_global_settings;
    
    
    settings = osoda_global_settings.get_default_settings();
    tmp = osoda_global_settings.get_arctic_dic_algorithms_list();
    
    algoNames = [algo.__name__ for algo in settings["arctic_at_algorithms"]];
    algoNames = ["Arrigo2010_at"];
    
    for algoName in algoNames:
        #read algo data
        readPath = path.join(settings["outputPath"], "global", "matchup_appended_"+algoName+".csv");
        try:
            df = pd.read_csv(readPath, sep=",", index_col=0);
        except FileNotFoundError:
            continue;
        
        prediction_accuracy_plot(df["DIC"], df["DIC_pred"], algoName, "DIC");
    
