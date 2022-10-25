# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 15:09:55 2020

@author: hlg211
"""
import pandas as pd;
import numpy as np;

from os_algorithms.base_algorithm import BaseAlgorithm;
from .utilities import subset_from_mask;


verb= False
filehandle=open("arctic_dic.txt","a")

# arrigo relationships spring
#DICpacspring=a0pacspring + (a1pacspring * sst) + (a2pacspring* chla) + (a3pacspring* sss) temp degrees c
class Arrigo2010pis_dic(BaseAlgorithm):
    #String representation of the algorithm
    def __str__(self):
        return "Arrigo2010pis_dic: Arr(dic)";

    #common names of input and output variables (see global_settings for definitions of these)
    @staticmethod
    def input_names():
        return  ["SST", "Chla", "SSS"];
    @staticmethod
    def output_name():
        return "DIC";
    
    def __init__(self, settings):
        #super().__init__(settings); #Call the parent class's initator
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        
                
        self.northernSummer =np.array([ 6, 7, 8]); #May-august
        self.northernWinter= np.array([3, 4, 5]); #March-may
        
#valid in pis
    def _equation1(self, data):
                               
        #Calculate indices of summer data
        seasonalIndices =  (data["date"].dt.month.isin(self.northernSummer))
        if (data['date'].dt.month < 1).any(): raise ValueError()
        
        dataToUse = data[seasonalIndices];
                              
        coefs =[278.9011,-16.4536,-2.3763, 56.3991] 
        r =(np.sqrt(0.92)); 
        rmsd =   61.6;
        SST = dataToUse["SST"];
        SSS = dataToUse["SSS"]
        Chla= dataToUse["Chla"]
        
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + coefs[1]*SST +coefs[2]*Chla + coefs[3]*SSS
                      
        
        #Calculate each uncertainty term serparately, for simplicity
        uterm1 = coefs[1] * dataToUse["SST_err"];#
        uterm2 = coefs[2] * dataToUse["Chla_err"];
        uterm3 = coefs[3] * dataToUse["SSS_err"]; 
        outputUncertaintyDueToInputUncertainty = np.sqrt( uterm1**2 + uterm2**2 + uterm3**2);
        
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    
    
    
    #This is zone 3 equation 10 eastern north Atlantic for SST < 20 C (summer)
    def _equation2(self, data):
        #dataToUse= data 
        coefs = [473.01,-44.319,-13.505, 49.646];
        rmsd = 17.3
        r =(np.sqrt(0.9)); 
        
        #Calculate indices of season data
        seasonalIndices = (data["date"].dt.month.isin(self.northernWinter));
        if (data['date'].dt.month < 1).any(): raise ValueError()
        dataToUse = data[seasonalIndices]
                              

  
        SST = dataToUse["SST"];
        SSS = dataToUse["SSS"]
        Chla= dataToUse["Chla"]
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + coefs[1]*SST +coefs[2]*Chla + coefs[3]*SSS
                      
        
        #Calculate each uncertainty term serparately, for simplicity
        uterm1 = coefs[1] * dataToUse["SST_err"];#
        uterm2 = coefs[2] * dataToUse["Chla_err"];
        uterm3 = coefs[3] * dataToUse["SSS_err"]; 
        outputUncertaintyDueToInputUncertainty = np.sqrt( uterm1**2 + uterm2**2 + uterm3**2);
        
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    

    
        #The main calculation is performed here, returns the model output
    def _kernal(self, dataToUse):
        #Innernal function used to run, check and assign values for each equation/zone
        def run_single_zone(function, data, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds):
            zoneData, zoneUncertainty, zoneRmsd = function(data);
            modelOutput[zoneData.index] = zoneData;
            outputUncertaintyDueToInputUncertainty[zoneData.index] = zoneUncertainty;
            rmsds[zoneData.index] = zoneRmsd;
       

        #Create empty output array
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        outputUncertaintyDueToInputUncertainty = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        rmsds = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        
        #Perform calculations for each zone
        
        run_single_zone(self._equation2, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);
        run_single_zone(self._equation1, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);
         
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertainty;
       
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsds;
    
    


    
 #atlantic arrigo   
#DICatl= a0atl + (a1atl * sst) + (a2atl* chla) + (a3atl* sss)
        
class Arrigo2010c_dic(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "Arrigo2010c_dic: Arrc(dic)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SST", "Chla", "SSS"];
    @staticmethod
    def output_name():
        return "DIC";
    
    #Set algorithm specific variables
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        self.coefs = [-4.8762,-5.139,-4.0197,64.7901]; #intersept,sst,chla, sss
        self.coefsUncertainty = [None, None, None, None]; #Uncertainty reported for the coefficients
        self.rmsd = 33.4; #See section 2
        self.r = (np.sqrt(0.62)) #table 1
           
        #Specify rectangular regions which the algorithm is valid for. Defaults to global when empty.
        #See fig 2, 3 for extents used by authors
        self.includedRegionsLons = [ 
                                ];
        self.includedRegionsLats = [
                                    ];
        
        #Algorithm will only be applied to values inside these ranges
        self.restrictRanges = { 
                               };
        
        #If the matchup dataset contains values outside of these ranges they will be flagged to the user
        self.flagRanges = {
                           }; 
        #The main calculation is performed here, returns the model output
    def _kernal(self, dataToUse):
        SST = dataToUse["SST"];
        modelOutput = self.coefs[0] + self.coefs[1]*SST + self.coefs[2]*dataToUse["Chla"]+ self.coefs[3]*dataToUse["SSS"]; 
        outputUncertaintyDueToInputUncertainty = np.sqrt( (self.coefs[3]*dataToUse["SSS_err"])**2 + \
                                          (self.coefs[1]*dataToUse["SST_err"])**2 + \
                                          (self.coefs[2]*dataToUse["Chla_err"])**2); 
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;
       
   
class Nondal2009_dic(BaseAlgorithm):
    #String representation of the algorithm
    def __str__(self):
        return "Nondal2009_dic: Non(dic)";

    #common names of input and output variables (see global_settings for definitions of these)
    @staticmethod
    def input_names():
        return ["SST", "SSS", "NO3"]
    @staticmethod
    def output_name():
        return "DIC";
    
    def __init__(self, settings):
        #super().__init__(settings); #Call the parent class's initator
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        
                
        self.northernSummer =  np.array([ 4, 5, 6, 7, 8, 9]); #April- sept 
        self.northernWinter= np.array([  1, 2, 3,10, 11, 12]); #oct- march 

    def _equation1(self, data):
                               
        #Calculate indices of summer data
        seasonalIndices =  (data["date"].dt.month.isin(self.northernSummer))
        if (data['date'].dt.month < 1).any(): raise ValueError()
        
        dataToUse = data[seasonalIndices];
                              
        coefs = [1176.52,-4.32,26.55,4.25]; 
        r =(np.sqrt(0.83)); 
        rmsd =  16.6;
        SST = dataToUse["SST"];
        SSS = dataToUse["SSS"]
        NO3= dataToUse["NO3"]
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + coefs[1]*SST +coefs[2]*SSS  + coefs[3]*NO3
                      
        
        #Calculate each uncertainty term serparately, for simplicity
        uterm1 = coefs[1] * dataToUse["SST_err"];#
        uterm2 = coefs[2] * dataToUse["SSS_err"]; 
        uterm3 = coefs[3] * dataToUse["NO3_err"];
        outputUncertaintyDueToInputUncertainty = np.sqrt( uterm1**2 + uterm2**2 + uterm3**2);
        
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    
    
    
    def _equation2(self, data):
        #dataToUse= data 
        coefs = [-293.63,-7.17,69.58,1.28]
        rmsd = 8.1
        r =(np.sqrt(0.94)); 
        
        #Calculate indices of season data
        seasonalIndices = (data["date"].dt.month.isin(self.northernWinter));
        
        dataToUse = data[seasonalIndices]
                              
        SST = dataToUse["SST"]
        SSS = dataToUse["SSS"]
        NO3= dataToUse["NO3"]
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + coefs[1]*SST +coefs[2]*SSS  + coefs[3]*NO3
                      
        
        #Calculate each uncertainty term serparately, for simplicity
        uterm1 = coefs[1] * dataToUse["SST_err"]; #
        uterm2 = coefs[2] * dataToUse["SSS_err"];
        uterm3 = coefs[3] * dataToUse["NO3_err"];
        outputUncertaintyDueToInputUncertainty = np.sqrt( uterm1**2 + uterm2**2 + uterm3**2);
        
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    

    
        #The main calculation is performed here, returns the model output
    def _kernal(self, dataToUse):
        #Innernal function used to run, check and assign values for each equation/zone
        def run_single_zone(function, data, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds):
            zoneData, zoneUncertainty, zoneRmsd = function(data);
            modelOutput[zoneData.index] = zoneData;
            outputUncertaintyDueToInputUncertainty[zoneData.index] = zoneUncertainty;
            rmsds[zoneData.index] = zoneRmsd;
        
        #Create empty output array
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        outputUncertaintyDueToInputUncertainty = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        rmsds = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        
        #Perform calculations for each zone
        
        run_single_zone(self._equation2, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);
        run_single_zone(self._equation1, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);
        if np.isnan(modelOutput).any():raise ValueError(np.isnan(modelOutput).sum()) 
        if np.isnan(outputUncertaintyDueToInputUncertainty).any():raise ValueError(np.isnan(outputUncertaintyDueToInputUncertainty).sum())
        if np.isnan(rmsds).any():raise ValueError(np.isnan(rmsds).sum())
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertainty;
    
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsds;
 #nondal2009 summer april-sept dic=1176.52-(4.32 SST)+_(26.55 SSS)+(4.25 NO3-)


    
   #Lee, K., Wanninkhof, R., Feely, R.A., Millero, F.J. and Peng, T.H., 2000. Global relationships of total inorganic carbon with temperature and nitrate in surface seawater. Global Biogeochemical Cycles, 14(3), pp.979-994.
class Lee2000_dic(BaseAlgorithm):
    #String representation of the algorithm
    def __str__(self):
        return "Lee2000_dic: L00(dic)";

    #common names of input and output variables (see global_settings for definitions of these)
    @staticmethod
    def input_names():
        return ["SST", "SSS", "NO3"];
    @staticmethod
    def output_name():
        return "DIC";
    
    def __init__(self, settings):
        #super().__init__(settings); #Call the parent class's initator
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        
        from netCDF4 import Dataset;
        self.regionMasks = Dataset(settings["algorithmSpecificDataPaths"][type(self).__name__], 'r');
        
        self.northernSummer = np.array([5, 6, 7, 8, 9]); #May-Sept
        self.northernWinter = np.array([10, 11, 12, 1, 2, 3, 4]); #Oct - April
        
#This is zone 3 equation western north Atlantic  western north Atlantic  for SST < 20 C (summer)
    def _equation9s(self, data):
        coefs = [2010.0, -8.633, -0.036, -0.279]; #intersept, SST, SST^2, NO3, Table 5
        rmsd = 6.9; #See table 5
        
        #Subset data to only rows valid for this zone. See Table 6
        dataToUse = subset_from_mask(data, self.regionMasks, "zone3_equation9_mask");
        
        #Calculate indices of summer data
        seasonalIndices = (dataToUse["lat"] >= 0) & (dataToUse["date"].dt.month.isin(self.northernSummer));
        
        dataToUse = dataToUse[(dataToUse["SST"] < 20) &
                              (seasonalIndices)
                              ];
        
        SST = dataToUse["SST"]-20;
        
        #Equation from table 5
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + \
                      coefs[1]*SST + \
                      coefs[2]*(SST**2) + \
                      coefs[3]*dataToUse["NO3"];
        
        #Calculate each uncertainty term serparately, for simplicity
        uterm1 = coefs[1] * dataToUse["SST_err"]; #B*SST
        uterm2 = coefs[2] * 2.0*dataToUse["SST_err"]*SST; #B*SST^2: Rearranged form of Taylor eq. 3.10: if x=q^n, then dx = n*u*q^(n-1), where u is uncertainty on q
        uterm3 = coefs[3] * dataToUse["NO3_err"]; #B*NO3
        outputUncertaintyDueToInputUncertainty = np.sqrt( uterm1**2 + uterm2**2 + uterm3**2 );
        
        #Normalised DIC (N_DIC) is N_DIC = DIC*(35/SSS), so DIC = N_DIC/(35/SSS)
        #Convert to non-normalised DIC
        outputUncertaintyDueToInputUncertaintyRatio = (outputUncertaintyDueToInputUncertainty/modelOutput) + (dataToUse["SSS_err"]/dataToUse["SSS"]); #Propagate uncertainty through normalisation
        modelOutput = modelOutput / (35.0/dataToUse["SSS"]);
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertaintyRatio*modelOutput; #two steps to avoid duplicate calculation
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    
    #This is zone 3 equation 9 western north Atlantic for SST < 20 C (winter)
    def _equation9w(self, data):
        coefs = [1980.0, -14.680, -0.297, -1.152]; #intersept, SST, SST^2, NO3, Table 5
        rmsd = 7.5; #See table 5
        
        
        #Subset data to only rows valid for this zone. See Table 5
        dataToUse = subset_from_mask(data, self.regionMasks, "zone3_equation9_mask");
        
        #Calculate indices of summer data
        seasonalIndices = (dataToUse["lat"] >= 0) & (dataToUse["date"].dt.month.isin(self.northernWinter));
       
        
        dataToUse = dataToUse[(dataToUse["SST"] < 20) &
                              (seasonalIndices)
                              ];
        
        SST = dataToUse["SST"]-20;
        
        #Equation from table 5
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + \
                      coefs[1]*SST + \
                      coefs[2]*(SST**2) + \
                      coefs[3]*dataToUse["NO3"];
        
        #Calculate each uncertainty term serparately, for simplicity
        uterm1 = coefs[1] * dataToUse["SST_err"]; #B*SST
        uterm2 = coefs[2] * 2.0*dataToUse["SST_err"]*SST; #B*SST^2: Rearranged form of Taylor eq. 3.10: if x=q^n, then dx = n*u*q^(n-1), where u is uncertainty on q
        uterm3 = coefs[3] * dataToUse["NO3_err"]; #B*NO3
        outputUncertaintyDueToInputUncertainty = np.sqrt( uterm1**2 + uterm2**2 + uterm3**2 );
        
        #Normalised DIC (N_DIC) is N_DIC = DIC*(35/SSS), so DIC = N_DIC/(35/SSS)
        #Convert to non-normalised DIC
        outputUncertaintyDueToInputUncertaintyRatio = (outputUncertaintyDueToInputUncertainty/modelOutput) + (dataToUse["SSS_err"]/dataToUse["SSS"]); #Propagate uncertainty through normalisation
        modelOutput = modelOutput / (35.0/dataToUse["SSS"]);
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertaintyRatio*modelOutput; #two steps to avoid duplicate calculation
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    
    #This is zone 3 equation 10 eastern north Atlantic for SST < 20 C (summer)
    def _equation10s(self, data):
        coefs = [2010, -4.262, -0.013, 5.054]; #intersept, SST, SST^2, NO3, Table 5
        rmsd = 5.9; #See table 5
        
        
        #Subset data to only rows valid for this zone. See Table 6
        dataToUse = subset_from_mask(data, self.regionMasks, "zone3_equation10_mask");
        
        #Calculate indices of summer data
        seasonalIndices = (dataToUse["lat"] >= 0) & (dataToUse["date"].dt.month.isin(self.northernSummer));
        
        
        dataToUse = dataToUse[(dataToUse["SST"] < 20) &
                              (seasonalIndices)
                              ];
        
        SST = dataToUse["SST"]-20;
        
        #Equation from table 5
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + \
                      coefs[1]*SST + \
                      coefs[2]*(SST**2) + \
                      coefs[3]*dataToUse["NO3"];
        
        #Calculate each uncertainty term serparately, for simplicity
        uterm1 = coefs[1] * dataToUse["SST_err"]; #B*SST
        uterm2 = coefs[2] * 2.0*dataToUse["SST_err"]*SST; #B*SST^2: Rearranged form of Taylor eq. 3.10: if x=q^n, then dx = n*u*q^(n-1), where u is uncertainty on q
        uterm3 = coefs[3] * dataToUse["NO3_err"]; #B*NO3
        outputUncertaintyDueToInputUncertainty = np.sqrt( uterm1**2 + uterm2**2 + uterm3**2 );
        
        #Normalised DIC (N_DIC) is N_DIC = DIC*(35/SSS), so DIC = N_DIC/(35/SSS)
        #Convert to non-normalised DIC
        outputUncertaintyDueToInputUncertaintyRatio = (outputUncertaintyDueToInputUncertainty/modelOutput) + (dataToUse["SSS_err"]/dataToUse["SSS"]); #Propagate uncertainty through normalisation
        modelOutput = modelOutput / (35.0/dataToUse["SSS"]);
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertaintyRatio*modelOutput; #two steps to avoid duplicate calculation
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    
    #This is zone 3 equation 10 eastern north Atlantic for SST < 20 C (winter)
    def _equation10w(self, data):
        coefs = [1980.0, -10.864, -0.311, 4.235]; #intersept, SST, SST^2, NO3, Table 5
        rmsd = 6.7; #See table 5
        
        
        #Subset data to only rows valid for this zone. See Table 5
        dataToUse = subset_from_mask(data, self.regionMasks, "zone3_equation10_mask");
        
        #Calculate indices of summer data
        seasonalIndices = (dataToUse["lat"] >= 0) & (dataToUse["date"].dt.month.isin(self.northernWinter));
        
        dataToUse = dataToUse[(dataToUse["SST"] < 20) &
                              (seasonalIndices)
                              ];
        
        SST = dataToUse["SST"]-20;
        
        #Equation from table 5
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + \
                      coefs[1]*SST + \
                      coefs[2]*(SST**2) + \
                      coefs[3]*dataToUse["NO3"];
        
        #Calculate each uncertainty term serparately, for simplicity
        uterm1 = coefs[1] * dataToUse["SST_err"]; #B*SST
        uterm2 = coefs[2] * 2.0*dataToUse["SST_err"]*SST; #B*SST^2: Rearranged form of Taylor eq. 3.10: if x=q^n, then dx = n*u*q^(n-1), where u is uncertainty on q
        uterm3 = coefs[3] * dataToUse["NO3_err"]; #B*NO3
        outputUncertaintyDueToInputUncertainty = np.sqrt( uterm1**2 + uterm2**2 + uterm3**2 );
        
        #Normalised DIC (N_DIC) is N_DIC = DIC*(35/SSS), so DIC = N_DIC/(35/SSS)
        #Convert to non-normalised DIC
        outputUncertaintyDueToInputUncertaintyRatio = (outputUncertaintyDueToInputUncertainty/modelOutput) + (dataToUse["SSS_err"]/dataToUse["SSS"]); #Propagate uncertainty through normalisation
        modelOutput = modelOutput / (35.0/dataToUse["SSS"]);
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertaintyRatio*modelOutput; #two steps to avoid duplicate calculation
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    
    #This is zone 4 equation 11 north pacific for SST < 20 C (summer)
    def _equation11s(self, data):
        coefs = [2010, -7.805, 0.069, 3.891]; #intersept, SST, SST^2, NO3, Table 5
        rmsd = 7.8; #See table 5
        
        
        #Subset data to only rows valid for this zone. See Table 6
        dataToUse = subset_from_mask(data, self.regionMasks, "zone4_equation11_mask");
        
        #Calculate indices of summer data
        seasonalIndices = (dataToUse["lat"] >= 0) & (dataToUse["date"].dt.month.isin(self.northernSummer));
        
        
        dataToUse = dataToUse[(dataToUse["SST"] < 20) &
                              (seasonalIndices)
                              ];
        
        SST = dataToUse["SST"]-20;
        
        #Equation from table 5
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + \
                      coefs[1]*SST + \
                      coefs[2]*(SST**2) + \
                      coefs[3]*dataToUse["NO3"];
        
        #Calculate each uncertainty term serparately, for simplicity
        uterm1 = coefs[1] * dataToUse["SST_err"]; #B*SST
        uterm2 = coefs[2] * 2.0*dataToUse["SST_err"]*SST; #B*SST^2: Rearranged form of Taylor eq. 3.10: if x=q^n, then dx = n*u*q^(n-1), where u is uncertainty on q
        uterm3 = coefs[3] * dataToUse["NO3_err"]; #B*NO3
        outputUncertaintyDueToInputUncertainty = np.sqrt( uterm1**2 + uterm2**2 + uterm3**2 );
        
        #Normalised DIC (N_DIC) is N_DIC = DIC*(35/SSS), so DIC = N_DIC/(35/SSS)
        #Convert to non-normalised DIC
        outputUncertaintyDueToInputUncertaintyRatio = (outputUncertaintyDueToInputUncertainty/modelOutput) + (dataToUse["SSS_err"]/dataToUse["SSS"]); #Propagate uncertainty through normalisation
        modelOutput = modelOutput / (35.0/dataToUse["SSS"]);
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertaintyRatio*modelOutput; #two steps to avoid duplicate calculation
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    
    #This is zone 4 equation 11 north pacific for SST < 20 C (winter)
    def _equation11w(self, data):
        coefs = [1980, -13.199, -0.172, 3.983]; #intersept, SST, SST^2, NO3, Table 5
        rmsd = 6.7; #See table 5
        
        
        #Subset data to only rows valid for this zone. See Table 5
        dataToUse = subset_from_mask(data, self.regionMasks, "zone4_equation11_mask");
        
        #Calculate indices of summer data
        seasonalIndices = (dataToUse["lat"] >= 0) & (dataToUse["date"].dt.month.isin(self.northernWinter));
        
        
        dataToUse = dataToUse[(dataToUse["SST"] < 20) &
                              (seasonalIndices)
                              ];
        
        SST = dataToUse["SST"]-20;
        
        #Equation from table 5
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + \
                      coefs[1]*SST + \
                      coefs[2]*(SST**2) + \
                      coefs[3]*dataToUse["NO3"];
        
        #Calculate each uncertainty term serparately, for simplicity
        uterm1 = coefs[1] * dataToUse["SST_err"]; #B*SST
        uterm2 = coefs[2] * 2.0*dataToUse["SST_err"]*SST; #B*SST^2: Rearranged form of Taylor eq. 3.10: if x=q^n, then dx = n*u*q^(n-1), where u is uncertainty on q
        uterm3 = coefs[3] * dataToUse["NO3_err"]; #B*NO3
        outputUncertaintyDueToInputUncertainty = np.sqrt( uterm1**2 + uterm2**2 + uterm3**2 );
        
        #Normalised DIC (N_DIC) is N_DIC = DIC*(35/SSS), so DIC = N_DIC/(35/SSS)
        #Convert to non-normalised DIC
        outputUncertaintyDueToInputUncertaintyRatio = (outputUncertaintyDueToInputUncertainty/modelOutput) + (dataToUse["SSS_err"]/dataToUse["SSS"]); #Propagate uncertainty through normalisation
        modelOutput = modelOutput / (35.0/dataToUse["SSS"]);
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertaintyRatio*modelOutput; #two steps to avoid duplicate calculation
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    
        
    def _kernal(self, dataToUse):
        #Innernal function used to run, check and assign values for each equation/zone
        def run_single_zone(function, data, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds):
            zoneData, zoneUncertainty, zoneRmsd = function(data);
            if np.any(np.isfinite(modelOutput[zoneData.index])==True): #Sanity check for overlaps
                raise RuntimeError("Overlapping zones in Lee00_dic. Something has done wrong!");
            modelOutput[zoneData.index] = zoneData;
            outputUncertaintyDueToInputUncertainty[zoneUncertainty.index] = zoneUncertainty;
            rmsds[zoneData.index] = zoneRmsd;
        
        
        #Create empty output array
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        outputUncertaintyDueToInputUncertainty = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        rmsds = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        
        #Perform calculations for each zone
                
        run_single_zone(self._equation9s, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);
        run_single_zone(self._equation9w, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);
        run_single_zone(self._equation10s, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);
        run_single_zone(self._equation10w, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);
        run_single_zone(self._equation11s, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);
        run_single_zone(self._equation11w, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);
        
        
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertainty;
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsds;     
#Brewer, P.G., Glover, D.M., Goyet, C. and Shafer, D.K., 1995. The pH of the North Atlantic Ocean: Improvements to the global model for sound absorption in seawater. Journal of Geophysical Research: Oceans, 100(C5), pp.8761-8776.
#Implementation of equation 10 (<250m depth)
class Brewer1995_dic(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "Brewer1995_dic: B95(dic)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS", "SST", "DO", "PO4", "NO3"];

    @staticmethod
    def output_name():
        return "DIC";
    
    #Set algorithm specific variables
    def __init__(self, settings):
        self.settings = settings;

        self.coefs = [944.0, 35.584, -7.099, -0.464, 138.0, -4.62]; #intersept, SSS, SST (as potential temperature), DO, PHO4, NO3 see equation 10
        self.coefsUncertainty = [None, None, None, None, None, None]; #Uncertainty reported for the coefficients, see fig 11
        self.rmsd = None;
        self.r = 0.940**0.5; #equation 10
        
        #Specify rectangular regions which the algorithm is valid for. Defaults to global when empty.
        self.includedRegionsLons = [(-100, 30)]; #See fig 1a
        self.includedRegionsLats = [(0, 80)]; #See fig 1a
        
        
        #Algorithm will only be applied to values inside these ranges
        self.restrictRanges = {"SSS": (31, 37.5), #See fig 4
                               "SST": (-2, 28), #See fig 5
                               "PO4": (0, 2.2), #See fig 5 (continued, second page)
                               "NO3": (0, 34), #See fig 5 (continues, 3rd page)
                               "DO": (100, 420), #See fig 5...
                               };
        
        #If the matchup dataset contains values outside of these ranges they will be flagged to the user
        self.flagRanges = {
                           };

    
    #The main calculation is performed here, returns the model output
    def _kernal(self, dataToUse):
        #equation 10
        modelOutput = self.coefs[0] + \
                      self.coefs[1]*dataToUse["SSS"] + \
                      self.coefs[2]*(dataToUse["SST"]) + \
                      self.coefs[3]*dataToUse["DO"] + \
                      self.coefs[4]*dataToUse["PO4"] + \
                      self.coefs[5]*dataToUse["NO3"];
        
        #equation 10
        outputUncertaintyDueToInputUncertainty = np.sqrt( (self.coefs[1]*dataToUse["SSS_err"])**2 + \
                                          (self.coefs[2]*dataToUse["SST_err"])**2 + \
                                          (self.coefs[3]*dataToUse["DO_err"])**2 + \
                                          (self.coefs[4]*dataToUse["PO4_err"])**2 + \
                                          (self.coefs[5]*dataToUse["NO3_err"])**2
                                         );
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;
# wong et a 2002 Seasonal cycles of nutrients and dissolved inorganic carbon at high and mid latitudes in the North Pacific Ocean during the Skaugran cruises: Determination of new production and nutrient uptake ratios
#BER relationship fig 5
class wong2002a_dic(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "wong2002a_dic: wong02a(dic)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["NO3", "SSS"];
    @staticmethod
    def output_name():
        return "DIC";
    
    #Set algorithm specific variables
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        self.coefs = [2082, 6.23]; #intersept,sst,chla, sss
        self.coefsUncertainty = [None, None, None, None]; #Uncertainty reported for the coefficients
        self.rmsd = None; #See section 2
        self.r = None #table 1
           
        #Specify rectangular regions which the algorithm is valid for. Defaults to global when empty.
        #See fig 2, 3 for extents used by authors
        self.includedRegionsLons = [ 
                                ];
        self.includedRegionsLats = [
                                    ];
        
        #Algorithm will only be applied to values inside these ranges
        self.restrictRanges = { 
                               };
        
        #If the matchup dataset contains values outside of these ranges they will be flagged to the user
        self.flagRanges = {
                           }; 
        #The main calculation is performed here, returns the model output
    def _kernal(self, dataToUse):
        
        modelOutput = self.coefs[0] + self.coefs[1]*dataToUse["NO3"]  
        outputUncertaintyDueToInputUncertainty = self.coefs[1]*dataToUse["NO3_err"];
          
        
   #Convert from  sss normalised dic by sss- to dic
        #This algorithm gives dic normalised to 35 salinity. Reverse normalisation:
        
        outputUncertaintyDueToInputUncertaintyRatio = (outputUncertaintyDueToInputUncertainty/modelOutput) + (dataToUse["SSS_err"]/dataToUse["SSS"]); #Propagate uncertainty through normalisation
        modelOutput = modelOutput / (35.0/dataToUse["SSS"]);
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertaintyRatio*modelOutput; #two steps to avoid duplicate calculation
        
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertainty;
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;    
#wong et al 2002 Seasonal cycles of nutrients and dissolved inorganic carbon at high and mid latitudes in the North Pacific Ocean during the Skaugran cruises: Determination of new production and nutrient uptake ratios
# SEBER relationship fig 5
class wong2002b_dic(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "wong2002a_dic: wong02a(dic)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["NO3", "SSS"];
    @staticmethod
    def output_name():
        return "DIC";
    
    #Set algorithm specific variables
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        self.coefs = [2102, 6.13]; #intersept,sst,chla, sss
        self.coefsUncertainty = [None, None, None, None]; #Uncertainty reported for the coefficients
        self.rmsd = None; #See section 2
        self.r = None #table 1
           
        #Specify rectangular regions which the algorithm is valid for. Defaults to global when empty.
        #See fig 2, 3 for extents used by authors
        self.includedRegionsLons = [ 
                                ];
        self.includedRegionsLats = [
                                    ];
        
        #Algorithm will only be applied to values inside these ranges
        self.restrictRanges = { 
                               };
        
        #If the matchup dataset contains values outside of these ranges they will be flagged to the user
        self.flagRanges = {
                           }; 
        #The main calculation is performed here, returns the model output
    def _kernal(self, dataToUse):
        
        modelOutput = self.coefs[0] + self.coefs[1]*dataToUse["NO3"]  
        outputUncertaintyDueToInputUncertainty = self.coefs[1]*dataToUse["NO3_err"];
          
        
   #Convert from  sss normalised dic by sss- to dic
        #This algorithm gives dic normalised tosalinity. Reverse normalisation:
        
        outputUncertaintyDueToInputUncertaintyRatio = (outputUncertaintyDueToInputUncertainty/modelOutput) + (dataToUse["SSS_err"]/dataToUse["SSS"]); #Propagate uncertainty through normalisation
        modelOutput = modelOutput / (35.0/dataToUse["SSS"]);
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertaintyRatio*modelOutput; #two steps to avoid duplicate calculation
        
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertainty;
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;         
    
    
    
    
    
    
    
    
