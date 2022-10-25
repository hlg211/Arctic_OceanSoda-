# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 14:34:59 2021

@author: hlg211
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
from scipy import stats
import os, glob;
from os import path;
path1="/data/datasets/Projects/OceanSODA/Arctic_OceanSoda/output";
os.chdir(path1) #changes current working directory 
#/data/datasets/Projects/OceanSODA/Arctic_OceanSoda/output/7_4_22algo_metrics/combination9__SST-ESACCI_SSS-ISAS/AT/AiS/matchup_appended_Nondal2009a_at.csv
df = pd.read_csv("/data/datasets/Projects/OceanSODA//Arctic_OceanSoda//output/chap330/combination9__SST-ESACCI_SSS-ISAS/AT/AiS/matchup_appended_Nondal2009_at.csv")
df.head()
a=df['AT']
b= df['AT_pred']

from sklearn.linear_model import LinearRegression
X = a.values.reshape(-1, 1)  # iloc[:, 1] is the column of X
Y = b.values.reshape(-1, 1)  # df.iloc[:, 4] is the column of Y
linear_regressor = LinearRegression()
linear_regressor.fit(X, Y)
Y_pred = linear_regressor.predict(X)

# r value
stat=slope, intercept, r_value, _, _ = stats.linregress(a, b)
print("slope:", slope, "\nintercept:", intercept,"\nr squared:", r_value**2)

RMSD= 20.7337503623923
plt.figure()
c=df['AT_reference_output_uncertainty'] 
d=df['AT_pred_combined_output_uncertainty']

plt.plot(X, Y_pred, color='black', linewidth=2, )# label= "SST-ESACCI_SSS-ISAS Nondal et al 2009"
xpoints = ypoints = plt.xlim()
plt.plot(xpoints, ypoints, linestyle='--', color='k', lw=3, scalex=False, scaley=False)
inter= intercept
plt.text(2320,2200,
        'Slope:{:.2g}\nR²:{:.2g}\nintercept:{:.2g} \nRMSD:{:.2g}'.format(float(slope),float(r_value**2),float(inter), float (RMSD)),#TODO not sure why its printing wrong intercept value 
        fontsize=10,ha='center')
plt.xlabel("In situ Total Alkalinity (µmol/kg)")
plt.ylabel("Predicted Total Alkalinity   (µmol/kg)")
# plt.xlim([1700, 2350])
# plt.ylim([1800, 2350])
#plt.title("Best TA AiS")
#plt.legend(loc=3)
plt.scatter(X, Y, linewidth=2, zorder=1, color='red')#zorder lets you but plots infront of error bars
plt.errorbar(X, Y, xerr=c, yerr= d,color='b', linestyle="None", elinewidth=1, capsize=2, zorder=0, marker=None)
plt.savefig('aisTA.svg', format='svg', dpi=1200)
plt.show()

##########################################################################################

df = pd.read_csv("/data/datasets/Projects/OceanSODA//Arctic_OceanSoda//output/chap330/combination9__SST-ESACCI_SSS-ISAS/DIC/AiS/matchup_appended_Nondal2009_dic.csv")
df.head()
a=df['DIC']
b= df['DIC_pred']


from sklearn.linear_model import LinearRegression
X = a.values.reshape(-1, 1)  # iloc[:, 1] is the column of X
Y = b.values.reshape(-1, 1)  # df.iloc[:, 4] is the column of Y
linear_regressor = LinearRegression()
linear_regressor.fit(X, Y)
Y_pred = linear_regressor.predict(X)
# r value
stat=slope, intercept, r_value, _, _ = stats.linregress(a, b)
print("slope:", slope, "\nintercept:", intercept,"\nr squared:", r_value**2)

RMSD= 24.3971507560704

plt.figure()
c=df['DIC_reference_output_uncertainty'] 
d=df['DIC_pred_combined_output_uncertainty']

plt.plot(X, Y_pred, color='black', linewidth=2)
xpoints = ypoints = plt.xlim()
plt.plot(xpoints, ypoints, linestyle='--', color='k', lw=3, scalex=False, scaley=False)
inter= intercept
#plt.legend(loc=4)
plt.scatter(X, Y, linewidth=2, zorder=1, color='red')#zorder lets you but plots infront of error bars
plt.errorbar(X, Y, xerr=c, yerr= d,color='b', linestyle="None", elinewidth=1, capsize=2, zorder=0, marker=None)
plt.text(1950,2130,
        'Slope:{:.2g}\nR²:{:.2g}\nintercept:{:.2g} \nRMSD:{:.2g}'.format(float(slope),float(r_value**2),float(inter), float (RMSD)), 
        fontsize=10,ha='center')

plt.xlabel("In situ Dissolved Inorganic Carbon (µmol/kg)")
plt.ylabel("Predicted Dissolved Inorganic Carbon (µmol/kg)")
#plt.title("Best DIC AiS")
plt.savefig('aisDIC.svg', format='svg', dpi=1200)

plt.show()


###########################################################################################
df = pd.read_csv("/data/datasets/Projects/OceanSODA/Arctic_OceanSoda/output/chap3n0/combination1__SST-CORA_SSS-ESACCI/AT/AiS/matchup_appended_Nondal2009_at.csv")
df.head()
a=df['AT']
b= df['AT_pred']

from sklearn.linear_model import LinearRegression
X = a.values.reshape(-1, 1)  # iloc[:, 1] is the column of X
Y = b.values.reshape(-1, 1)  # df.iloc[:, 4] is the column of Y
linear_regressor = LinearRegression()
linear_regressor.fit(X, Y)
Y_pred = linear_regressor.predict(X)

# r value
stat=slope, intercept, r_value, _, _ = stats.linregress(a, b)
print("slope:", slope, "\nintercept:", intercept,"\nr squared:", r_value**2)

RMSD=19.8455145205891
plt.figure()
c=df['AT_reference_output_uncertainty'] 
d=df['AT_pred_combined_output_uncertainty']

plt.plot(X, Y_pred, color='black', linewidth=2, )# label= "SST-ESACCI_SSS-ISAS Nondal et al 2009"
xpoints = ypoints = plt.xlim()
plt.plot(xpoints, ypoints, linestyle='--', color='k', lw=3, scalex=False, scaley=False)
inter= intercept
plt.text(2275,2315,
        'Slope:{:.2g}\nR²:{:.2g}\nintercept:{:.2g} \nRMSD:{:.2g}'.format(float(slope),float(r_value**2),float(inter), float (RMSD)),#TODO not sure why its printing wrong intercept value 
        fontsize=10,ha='center')
plt.xlabel("In situ Total Alkalinity (µmol/kg)")
plt.ylabel("Predicted Total Alkalinity   (µmol/kg)")
# plt.xlim([1700, 2350])
# plt.ylim([1800, 2350])
#plt.title("Best TA AiS")
#plt.legend(loc=3)
plt.scatter(X, Y, linewidth=2, zorder=1, color='red')#zorder lets you but plots infront of error bars
plt.errorbar(X, Y, xerr=c, yerr= d,color='b', linestyle="None", elinewidth=1, capsize=2, zorder=0, marker=None)
plt.savefig('smosaisTA.svg', format='svg', dpi=1200)
plt.show()

##########################################################################################

df = pd.read_csv("/data/datasets/Projects/OceanSODA/Arctic_OceanSoda/output/chap3n0/combination7__SST-CORA_SSS-RSS-SMAP/DIC/AiS/matchup_appended_Nondal2009_dic.csv")
df.head()
a=df['DIC']
b= df['DIC_pred']


from sklearn.linear_model import LinearRegression
X = a.values.reshape(-1, 1)  # iloc[:, 1] is the column of X
Y = b.values.reshape(-1, 1)  # df.iloc[:, 4] is the column of Y
linear_regressor = LinearRegression()
linear_regressor.fit(X, Y)
Y_pred = linear_regressor.predict(X)
# r value
stat=slope, intercept, r_value, _, _ = stats.linregress(a, b)
print("slope:", slope, "\nintercept:", intercept,"\nr squared:", r_value**2)

RMSD= 33.7645617893349


plt.figure()
c=df['DIC_reference_output_uncertainty'] 
d=df['DIC_pred_combined_output_uncertainty']

plt.plot(X, Y_pred, color='black', linewidth=2)
xpoints = ypoints = plt.xlim()
plt.plot(xpoints, ypoints, linestyle='--', color='k', lw=3, scalex=False, scaley=False)
inter= intercept
#plt.legend(loc=4)
plt.scatter(X, Y, linewidth=2, zorder=1, color='red')#zorder lets you but plots infront of error bars
plt.errorbar(X, Y, xerr=c, yerr= d,color='b', linestyle="None", elinewidth=1, capsize=2, zorder=0, marker=None)
plt.text(2100,2130,
        'Slope:{:.2g}\nR²:{:.2g}\nintercept:{:.2g} \nRMSD:{:.2g}'.format(float(slope),float(r_value**2),float(inter), float (RMSD)), 
        fontsize=10,ha='center')

plt.xlabel("In situ Dissolved Inorganic Carbon (µmol/kg)")
plt.ylabel("Predicted Dissolved Inorganic Carbon (µmol/kg)")
#plt.title("Best DIC AiS")
plt.savefig('smapaisDIC.svg', format='svg', dpi=1200)

plt.show()


###########################################################################################
df = pd.read_csv("/output/n=0algo_metrics/combination9__SST-ESACCI_SSS-ISAS/AT/OFS/matchup_appended_Tynan2016c_at.csv")
df.head()
a=df['AT']
b= df['AT_pred']



from sklearn.linear_model import LinearRegression
X = a.values.reshape(-1, 1)  # iloc[:, 1] is the column of X
Y = b.values.reshape(-1, 1)  # df.iloc[:, 4] is the column of Y
linear_regressor = LinearRegression()
linear_regressor.fit(X, Y)
Y_pred = linear_regressor.predict(X)

# r value
slope, intercept, r_value, _, _ = stats.linregress(a, b)
print("slope:", slope, "\nintercept:", intercept,"\nr squared:", r_value**2)
plt.figure()
RMSD= 43.087321467854

plt.figure()
c=df['AT_reference_output_uncertainty'] 
d=df['AT_pred_combined_output_uncertainty']

plt.plot(X, Y_pred, color='black', linewidth=2, )
xpoints = ypoints = plt.xlim()
plt.plot(xpoints, ypoints, linestyle='--', color='k', lw=3, scalex=False, scaley=False)
inter= intercept
#plt.legend(loc=4)
plt.scatter(X, Y, linewidth=2, zorder=1, color='red')#zorder lets you but plots infront of error bars
plt.errorbar(X, Y, xerr=c, yerr= d,color='b', linestyle="None", elinewidth=1, capsize=2, zorder=0, marker=None)
plt.text(2300,2060,
        'Slope:{:.2g}\nR²:{:.2g}\nintercept:{:.2g} \nRMSD:{:.2g}'.format(float(slope),float(r_value**2),float(inter), float (RMSD)), 
        fontsize=10,ha='center')



plt.xlabel("In situ Total Alkalinity (µmol/kg)")
plt.ylabel("Predicted Total Alkalinity   (µmol/kg)")
#plt.title("Best TA OFS")
#plt.legend(loc=4)
plt.savefig('ofsta.svg', format='svg', dpi=1200)
plt.show()

##########################################################################################

df = pd.read_csv("/data/datasets/Projects/OceanSODA//Arctic_OceanSoda//output/chap330/combination3__SST-ESACCI_SSS-CORA/DIC/OFS/matchup_appended_Nondal2009_dic.csv")
df.head()
a=df['DIC']
b= df['DIC_pred']


from sklearn.linear_model import LinearRegression
X = a.values.reshape(-1, 1)  # iloc[:, 1] is the column of X
Y = b.values.reshape(-1, 1)  # df.iloc[:, 4] is the column of Y
linear_regressor = LinearRegression()
linear_regressor.fit(X, Y)
Y_pred = linear_regressor.predict(X)
c=df['DIC_reference_output_uncertainty'] 
d=df['DIC_pred_combined_output_uncertainty']
RMSD= 48.622630915647


# r value
slope, intercept, r_value, _, _ = stats.linregress(a, b)
print("slope:", slope, "\nintercept:", intercept,"\nr squared:", r_value**2)
plt.figure()

plt.plot(X, Y_pred, color='black', linewidth=2,)
xpoints = ypoints = plt.xlim()
plt.plot(xpoints, ypoints, linestyle='--', color='k', lw=3, scalex=False, scaley=False)
inter= intercept
#plt.legend(loc=4)
plt.scatter(X, Y, linewidth=2, zorder=1, color='red')#zorder lets you but plots infront of error bars
plt.errorbar(X, Y, xerr=c, yerr= d,color='b', linestyle="None", elinewidth=1, capsize=2, zorder=0, marker=None)
plt.text(1700,2100,
        'Slope:{:.2g}\nR²:{:.2g}\nintercept:{:.2g} \nRMSD:{:.2g}'.format(float(slope),float(r_value**2),float(inter), float (RMSD)), 
        fontsize=10,ha='center')


plt.xlabel("In situ Dissolved Inorganic Carbon (µmol/kg)")
plt.ylabel("Predicted Dissolved Inorganic Carbon (µmol/kg)")
#plt.title("Best DIC OFS")
#plt.legend(loc=4)
plt.savefig('ofsdic.svg', format='svg', dpi=1200)
plt.show()

##########################################################################################

df = pd.read_csv("/data/datasets/Projects/OceanSODA//Arctic_OceanSoda//output/chap330//combination12__SST-ESACCI_SSS-BEC-Arctic/AT/PiS/matchup_appended_kaltin2005_at.csv")
df.head()
a=df['AT']
b= df['AT_pred']


from sklearn.linear_model import LinearRegression
X = a.values.reshape(-1, 1)  # iloc[:, 1] is the column of X
Y = b.values.reshape(-1, 1)  # df.iloc[:, 4] is the column of Y
linear_regressor = LinearRegression()
linear_regressor.fit(X, Y)
Y_pred = linear_regressor.predict(X)
RMSD=80.5782257813379

# r value
slope, intercept, r_value, _, _ = stats.linregress(a, b)
print("slope:", slope, "\nintercept:", intercept,"\nr squared:", r_value**2)
plt.figure()
c=df['AT_reference_output_uncertainty'] 
d=df['AT_pred_combined_output_uncertainty']


plt.plot(X, Y_pred, color='black', linewidth=2)
xpoints = ypoints = plt.xlim()
plt.plot(xpoints, ypoints, linestyle='--', color='k', lw=3, scalex=False, scaley=False)
inter= intercept
#plt.legend(loc=4)
plt.scatter(X, Y, linewidth=2, zorder=1, color='red')#zorder lets you but plots infront of error bars
plt.errorbar(X, Y, xerr=c, yerr= d,color='b', linestyle="None", elinewidth=1, capsize=2, zorder=0, marker=None)
plt.text(1720,2100,
        'Slope:{:.2g}\nR²:{:.2g}\nintercept:{:.2g} \nRMSD:{:.2g}'.format(float(slope),float(r_value**2),float(inter), float (RMSD)), 
        fontsize=10,ha='center')

plt.xlabel("In situ Total Alkalinity (µmol/kg)")
plt.ylabel("Predicted Total Alkalinity (µmol/kg)")
#plt.title("Best TA PiS")
#plt.legend(loc=4)
plt.savefig('pisat.svg', format='svg', dpi=1200)
plt.show()


##########################################################################################

df = pd.read_csv("/data/datasets/Projects/OceanSODA//Arctic_OceanSoda//output/chap330/combination10__SST-CORA_SSS-ISAS/AT/CA/matchup_appended_Arrigo2010_at.csv")
df.head()
a=df['AT']
b= df['AT_pred']


from sklearn.linear_model import LinearRegression
X = a.values.reshape(-1, 1)  # iloc[:, 1] is the column of X
Y = b.values.reshape(-1, 1)  # df.iloc[:, 4] is the column of Y
linear_regressor = LinearRegression()
linear_regressor.fit(X, Y)
Y_pred = linear_regressor.predict(X)
RMSD=79.5984102616111

# r value
slope, intercept, r_value, _, _ = stats.linregress(a, b)
print("slope:", slope, "\nintercept:", intercept,"\nr squared:", r_value**2)
plt.figure()
c=df['AT_reference_output_uncertainty'] 
d=df['AT_pred_combined_output_uncertainty']


plt.plot(X, Y_pred, color='black', linewidth=2, )
xpoints = ypoints = plt.xlim()
plt.plot(xpoints, ypoints, linestyle='--', color='k', lw=3, scalex=False, scaley=False)
inter= intercept
#plt.legend(loc=4)
plt.scatter(X, Y, linewidth=2, zorder=1, color='red')#zorder lets you but plots infront of error bars
plt.errorbar(X, Y, xerr=c, yerr= d,color='b', linestyle="None", elinewidth=1, capsize=2, zorder=0, marker=None)
plt.text(1820,2200,
        'Slope:{:.2g}\nR²:{:.2g}\nintercept:{:.2g} \nRMSD:{:.2g}'.format(float(slope),float(r_value**2),float(inter), float (RMSD)), 
        fontsize=10,ha='center')

plt.xlabel("In situ Total Alkalinity (µmol/kg)")
plt.ylabel("Predicted Total Alkalinity   (µmol/kg)")
#plt.title("Best TA CA")
#plt.legend(loc=4)
plt.savefig('caat.svg', format='svg', dpi=1200)
plt.show()
##########################################################################################

df = pd.read_csv("/data/datasets/Projects/OceanSODA//Arctic_OceanSoda//output/chap330//combination5__SST-OISST_SSS-CORA/DIC/PiS/matchup_appended_Lee2000_dic.csv")
df.head()
a=df['DIC']
b= df['DIC_pred']


from sklearn.linear_model import LinearRegression
X = a.values.reshape(-1, 1)  # iloc[:, 1] is the column of X
Y = b.values.reshape(-1, 1)  # df.iloc[:, 4] is the column of Y
linear_regressor = LinearRegression()
linear_regressor.fit(X, Y)
Y_pred = linear_regressor.predict(X)
c=df['DIC_reference_output_uncertainty'] 
d=df['DIC_pred_combined_output_uncertainty']
RMSD=74.2561383206634

# r value
slope, intercept, r_value, _, _ = stats.linregress(a, b)
print("slope:", slope, "\nintercept:", intercept,"\nr squared:", r_value**2)
plt.figure()

plt.plot(X, Y_pred, color='black', linewidth=2, )
xpoints = ypoints = plt.xlim()
plt.plot(xpoints, ypoints, linestyle='--', color='k', lw=3, scalex=False, scaley=False)
inter= intercept
#plt.legend(loc=4)
plt.scatter(X, Y, linewidth=2, zorder=1, color='red')#zorder lets you but plots infront of error bars
plt.errorbar(X, Y, xerr=c, yerr= d,color='b', linestyle="None", elinewidth=1, capsize=2, zorder=0, marker=None)
plt.text(1800,2000,
        'Slope:{:.2g}\nR²:{:.2g}\nintercept:{:.2g} \nRMSD:{:.2g}'.format(float(slope),float(r_value**2),float(inter), float (RMSD)), 
        fontsize=10,ha='center')


plt.xlabel("In situ Dissolved Inorganic Carbon (µmol/kg)")
plt.ylabel("Predicted Dissolved Inorganic Carbon (µmol/kg)")
#plt.title("Best DIC PiS")
#plt.legend(loc=4)
plt.savefig('pisdic.svg', format='svg', dpi=1200)
plt.show()

##############################################

df = pd.read_csv("/data/datasets/Projects/OceanSODA/Arctic_OceanSoda/output/chap3n0/combination5__SST-OISST_SSS-CORA/DIC/RiS_1/matchup_appended_Lee2000_dic.csv")
df.head()
a=df['DIC']
b= df['DIC_pred']


from sklearn.linear_model import LinearRegression
X = a.values.reshape(-1, 1)  # iloc[:, 1] is the column of X
Y = b.values.reshape(-1, 1)  # df.iloc[:, 4] is the column of Y
linear_regressor = LinearRegression()
linear_regressor.fit(X, Y)
Y_pred = linear_regressor.predict(X)
RMSD=236.815744472597

# r value
slope, intercept, r_value, _, _ = stats.linregress(a, b)
print("slope:", slope, "\nintercept:", intercept,"\nr squared:", r_value**2)
plt.figure()
c=df['DIC_reference_output_uncertainty'] 
d=df['DIC_pred_combined_output_uncertainty']


plt.plot(X, Y_pred, color='black', linewidth=2, label= "SST-OISST_SSS-CORA Lee et al 2000")
xpoints = ypoints = plt.xlim()
plt.plot(xpoints, ypoints, linestyle='--', color='k', lw=3, scalex=False, scaley=False)
inter= intercept
plt.legend(loc=4)
plt.scatter(X, Y, linewidth=2, zorder=1, color='red')#zorder lets you but plots infront of error bars
plt.errorbar(X, Y, xerr=c, yerr= d,color='b', linestyle="None", elinewidth=1, capsize=2, zorder=0, marker=None)
plt.text(900,1200,
        'Slope:{:.2g}\nR²:{:.2g}\nintercept:{:.2g} \nRMSD:{:.2g}'.format(float(slope),float(r_value**2),float(inter), float (RMSD)), 
        fontsize=10,ha='center')

plt.xlabel("In situ Dissolved Inorganic Carbon (µmol/kg)")
plt.ylabel("Predicted Dissolved Inorganic Carbon  (µmol/kg)")
plt.title("Best DIC RiS 1")
plt.legend(loc=4)
plt.savefig('Ris1dic.svg', format='svg', dpi=1200)
plt.show()

##############################################

df = pd.read_csv("/data/datasets/Projects/OceanSODA//Arctic_OceanSoda//output/chap330//combination12__SST-ESACCI_SSS-BEC-Arctic/AT/RiS_2/matchup_appended_DeGrandpre2019_at.csv")
df.head()
a=df['AT']
b= df['AT_pred']


from sklearn.linear_model import LinearRegression
X = a.values.reshape(-1, 1)  # iloc[:, 1] is the column of X
Y = b.values.reshape(-1, 1)  # df.iloc[:, 4] is the column of Y
linear_regressor = LinearRegression()
linear_regressor.fit(X, Y)
Y_pred = linear_regressor.predict(X)
RMSD=73.8194647436306

# r value
slope, intercept, r_value, _, _ = stats.linregress(a, b)
print("slope:", slope, "\nintercept:", intercept,"\nr squared:", r_value**2)
plt.figure()
c=df['AT_reference_output_uncertainty'] 
d=df['AT_pred_combined_output_uncertainty']


plt.plot(X, Y_pred, color='black', linewidth=2, )
xpoints = ypoints = plt.xlim()
plt.plot(xpoints, ypoints, linestyle='--', color='k', lw=3, scalex=False, scaley=False)
inter= intercept
#plt.legend(loc=4)
plt.scatter(X, Y, linewidth=2, zorder=1, color='red')#zorder lets you but plots infront of error bars
plt.errorbar(X, Y, xerr=c, yerr= d,color='b', linestyle="None", elinewidth=1, capsize=2, zorder=0, marker=None)
plt.text(1780,2100,
        'Slope:{:.2g}\nR²:{:.2g}\nintercept:{:.2g} \nRMSD:{:.2g}'.format(float(slope),float(r_value**2),float(inter), float (RMSD)), 
        fontsize=10,ha='center')

plt.xlabel("In situ Total Alkalinity (µmol/kg)")
plt.ylabel("Predicted Total Alkalinity   (µmol/kg)")
#plt.title("Best TA RiS2")
#plt.legend(loc=4)
plt.savefig('Ris2ta.svg', format='svg', dpi=1200)
plt.show()

##########################################################################################

df = pd.read_csv("/data/datasets/Projects/OceanSODA//Arctic_OceanSoda//output/chap330//combination5__SST-OISST_SSS-CORA/DIC/RiS_2/matchup_appended_Arrigo2010pis_dic.csv")
df.head()
a=df['DIC']
b= df['DIC_pred']


from sklearn.linear_model import LinearRegression
X = a.values.reshape(-1, 1)  # iloc[:, 1] is the column of X
Y = b.values.reshape(-1, 1)  # df.iloc[:, 4] is the column of Y
linear_regressor = LinearRegression()
linear_regressor.fit(X, Y)
Y_pred = linear_regressor.predict(X)
c=df['DIC_reference_output_uncertainty'] 
d=df['DIC_pred_combined_output_uncertainty']
RMSD= 335.931441079274


# r value
slope, intercept, r_value, _, _ = stats.linregress(a, b)
print("slope:", slope, "\nintercept:", intercept,"\nr squared:", r_value**2)
plt.figure()

plt.plot(X, Y_pred, color='black', linewidth=2, )
xpoints = ypoints = plt.xlim()
plt.plot(xpoints, ypoints, linestyle='--', color='k', lw=3, scalex=False, scaley=False)
inter= intercept
#plt.legend(loc=4)
plt.scatter(X, Y, linewidth=2, zorder=1, color='red')#zorder lets you but plots infront of error bars
plt.errorbar(X, Y, xerr=c, yerr= d,color='b', linestyle="None", elinewidth=1, capsize=2, zorder=0, marker=None)
plt.text(1500,2400,
        'Slope:{:.2g}\nR²:{:.2g}\nintercept:{:.2g} \nRMSDe:{:.2g}'.format(float(slope),float(r_value**2),float(inter), float (RMSD)), 
        fontsize=10,ha='center')


plt.xlabel("In situ Dissolved Inorganic Carbon (µmol/kg)")
plt.ylabel("Predicted Dissolved Inorganic Carbon (µmol/kg)")
#plt.title("Best DIC RiS_2")
#plt.legend(loc=4)
plt.savefig('Ris2dic.svg', format='svg', dpi=1200)

plt.show()
