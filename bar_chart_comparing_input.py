# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 11:53:23 2021

@author: hlg211
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#sns.set() # gives the chart a odd gridded background 



#This next line makes our charts show up in the notebook
#%matplotlib inline

data = pd.read_csv("/data/datasets/Projects/OceanSODA/Arctic_OceanSoda/output/chap3n0/barsummary_best_algos.csv")
data.head()


###ta plot
sns.set_palette("colorblind")
sns.barplot(x='region', y='AT_wRMSD', hue = 'SSS_input', errcolor='.26', linewidth=2.5, errwidth=1, ci="sd", capsize=.1,  data=data)
plt.xlabel("Region")
plt.ylabel("Total alkalinity RMSD (µmol/kg)")
plt.savefig('TARMSD.svg', format='svg', dpi=1200)
plt.show()
##### dic split ais plot
sns.set_palette("colorblind")
f, (ax1, ax2) = plt.subplots(ncols=1, nrows=2, sharex=True, gridspec_kw={'hspace':0.05})
ax=sns.barplot(x='region', y='DIC_wRMSD(umol/kg)', hue = 'SSS_input', errcolor='.26', linewidth=2.5, errwidth=1, ci="sd", capsize=.1,  data=data, ax=ax1)
ax=sns.barplot(x='region', y='DIC_wRMSD(umol/kg)', hue = 'SSS_input', errcolor='.26', linewidth=2.5, errwidth=1, ci="sd", capsize=.1,  data=data, ax=ax2)
ax1.set_ylim(150, 900)
ax1.set(ylabel=None)
ax2.set(ylabel=None)
d = .01  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax1.transAxes, color="k", clip_on=False)
ax1.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

plt.ylabel("                                  Dissolved inorganic carbon RMSD (µmol/kg)")
ax2.set_ylim(0, 90)
ax2.legend_.remove()
sns.despine(ax=ax2)
sns.despine(ax=ax1, bottom=True)
#ax1.ylabel("Dissolved inorganic carbon wRMSD (µmol/kg)")
plt.xlabel("Region")
#remove one of the legend

plt.savefig('DICRMSD.svg', format='svg', dpi=1200)




#######################################################################################################


