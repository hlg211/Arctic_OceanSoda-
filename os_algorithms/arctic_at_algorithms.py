
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:44:45 2020

@author: hlg211
"""
import numpy as np;
import pandas as pd;

from os_algorithms.base_algorithm import BaseAlgorithm;
from os_algorithms.utilities import subset_from_mask, subset_from_inclusive_coord_list;

import datetime as dt
verb= False

filehandle=open("arctic_at.txt","a")
#katlin2002a barents sea  south 74 degrees (AT normalised by no3) 
class kaltin2002_at(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "kaltin2002_at: kal02(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS", "NO3"]
    @staticmethod
    def output_name():
        return "AT";
    
    #Set algorithm specific variables
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
          
   


    def _equation1(self, data):
        coefs = [1130, 33.7]; #intersept, salinity slope, 
        rmsd = None;
        r = np.sqrt(0.62)
        dis= data['lat']<74
        dataToUse=data[dis]
        
     
        dataToUse=data 
        #dataToUse=data[dis] 
        SSS = dataToUse["SSS"]
        NO3= dataToUse["NO3"]
        
        modelOutput = coefs[0] + coefs[1]*SSS+ NO3
        
        outputUncertaintyDueToInputUncertainty = coefs[1]*dataToUse["SSS_err"]
               #Convert from normalised alkalinity by no3- to TA
        #normalised alkalinity = TA - NO3-, so calculate TA using:
       
        outputUncertaintyDueToInputUncertainty = np.sqrt( outputUncertaintyDueToInputUncertainty**2 + dataToUse["NO3_err"]**2);
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertainty;
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;
    def _equation2(self, data):
        coefs = [273, 58.1]; #intersept, salinity slope, 
        rmsd = None;
        r = np.sqrt(0.95)
        dis= data['lat']>=74
        dataToUse=data[dis]

        SSS = dataToUse["SSS"]
        NO3= dataToUse["NO3"]
       
        modelOutput = coefs[0] + coefs[1]*SSS + NO3
               #Convert from normalised alkalinity by no3- to TA
        outputUncertaintyDueToInputUncertainty = coefs[1]*dataToUse["SSS_err"]
        #normalised alkalinity = TA - NO3-, so calculate TA using:
        
        outputUncertaintyDueToInputUncertainty = np.sqrt( outputUncertaintyDueToInputUncertainty**2 + dataToUse["NO3_err"]**2);
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertainty;
    
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
  
        run_single_zone(self._equation1, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);
        
        run_single_zone(self._equation2, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);

        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertainty;

        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsds;

 
#katlin2005 pacific influenced 
class kaltin2005_at(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "kaltin2005_at: kal05(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS", "NO3"];
    @staticmethod
    def output_name():
        return "AT";
    
    #Set algorithm specific variables
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        self.coefs = [688.6, 47.2]; #intersept, salinity slope, 
        self.coefsUncertainty = [None, None]; 
        self.rmsd = 75; #arrigo equation 3 
        self.r = (np.sqrt(0.92)); #But see fig 2
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
   
        modelOutput = self.coefs[0] + self.coefs[1]*dataToUse["SSS"]; 
        outputUncertaintyDueToInputUncertainty = self.coefs[1]*dataToUse["SSS_err"];
          
        
   #Convert from normalised alkalinity by no3- to TA
        #normalised alkalinity = TA - NO3-, so calculate TA using:
        outputUncertaintyDueToInputUncertaintyRatio = (outputUncertaintyDueToInputUncertainty/modelOutput) + (dataToUse["NO3_err"]/dataToUse["NO3"]); #Propagate uncertainty through normalisation
        modelOutput = modelOutput + (dataToUse["NO3"]);
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertaintyRatio*modelOutput; #two steps to avoid duplicate calculation
        
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertainty;
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;       
         
    
 #arrigo2010 atlantic influenced 
class Arrigo2010_at(BaseAlgorithm):    
    #String representation of the algorithm temp degree C TA& DIC umolkg-1
    def __str__(self):
        return "Arrigo2010_at: Ar10(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SST", "SSS"];
    
    @staticmethod
    def output_name():
        return "AT";
    
    #Set algorithm specific variables
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        self.coefs = [200.13,4.42,63.06 ]; #intersept, sst, salinity, 
        self.coefsUncertainty = [None, None];                           
        self.rmsd = 26.9; #equation 1
        self.r =(np.sqrt(0.86)); #But see section 2.1
          
        #Specify rectangular regions which the algorithm is valid for. Defaults to global when empty.
        #See fig 2, 3 for extents used by authors
        self.includedRegionsLons = {} ;
        self.includedRegionsLats = {};
        
        #Algorithm will only be applied to values inside these ranges
        self.restrictRanges = { 
                               };
        
        #If the matchup dataset contains values outside of these ranges they will be flagged to the user
        self.flagRanges = {
                           }; 
        
 #The main calculation is performed here, returns the model output
    def _kernal(self, dataToUse):
        SST = dataToUse["SST"];
        modelOutput = self.coefs[0] + self.coefs[2]*dataToUse["SSS"]+ self.coefs[1]*SST; 
        
        outputUncertaintyDueToInputUncertainty = np.sqrt( (self.coefs[2]*dataToUse["SSS_err"])**2 + \
                                          (self.coefs[1]*dataToUse["SST_err"])**2 ); 
                       
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd; 

#Nondal et al 2009 North Atlantic relationship

#Atlantic-influence water and ice melt
#NonTAatl=49.35* sss +582 
class Nondal2009_at(BaseAlgorithm):
    #String representation of the algorithm
    def __str__(self):
        return "Nondal2009_at: Non09(at)";

    #common names of input and output variables (see global_settings for definitions of these)
    @staticmethod
    def input_names():
        return ["SSS"];
    @staticmethod
    def output_name():
        return "AT";
    
    def __init__(self, settings):
        #super().__init__(settings); #Call the parent class's initator
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        

    def _equation1(self, data):
                               
        #Calculate 
        sss=data["SSS"] >= 34.5
        
        dataToUse = data[sss];
                              
     
        coefs = [582,49.35];
        r =(np.sqrt(0.86)); 
        rmsd =9.7
     
        SSS = dataToUse["SSS"]
        
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + coefs[1]*SSS 
                      
        
        #Calculate each uncertainty term serparately, for simplicity
        uterm1 = coefs[1] * dataToUse["SSS_err"]; #
#
        outputUncertaintyDueToInputUncertainty = np.sqrt( uterm1**2);
        
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    
    
    
    #This is zone 3 equation 10 eastern north Atlantic for SST < 20 C (summer)
    def _equation2(self, data):
       #Calculate 
        sss=data["SSS"] < 34.5
        
        dataToUse = data[sss];
                              
     
        coefs = [1751.73, 15.29];
        r =(np.sqrt(0.63)); 
        rmsd =8.8
     
        SSS = dataToUse["SSS"]
        
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + coefs[1]*SSS 
                      
        
        #Calculate each uncertainty term serparately, for simplicity
        uterm1 = coefs[1] * dataToUse["SSS_err"]; #
#
        outputUncertaintyDueToInputUncertainty = np.sqrt( uterm1**2);
        
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    
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


#Tynan 2016 western side of fram strait outflow waters 
class Tynan2016a_at(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "Tynan2016a_at: Tyn16a(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS"];
    
    @staticmethod
    def output_name():
        return "AT";
    
    def __init__(self, settings):
        self.settings = settings;
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.coefs = [1230, 30.8]; #intersept, sss,figure 3
        self.coefsUncertainty = [None, None]; 
        self.rmsd = None
        self.r = (np.sqrt(0.96)); # equation 7
        
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
        modelOutput = self.coefs[0] + self.coefs[1]*dataToUse["SSS"]; 
        
        outputUncertaintyDueToInputUncertainty = self.coefs[1]*dataToUse["SSS_err"];
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd; 
    
#Tynan 2016 Nordic Seas, Barents Sea
class Tynan2016b_at(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "Tynan2016b_at: Tyn16b(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS"];
    
    @staticmethod
    def output_name():
        return "AT";
 
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        self.coefs = [403, 54.5]; #intersept, salinity slope, figure 3
        self.coefsUncertainty = [None, None]; 
        self.rmsd = None
        self.r = (np.sqrt(0.78)); # equation 7
        
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
        modelOutput = self.coefs[0] + self.coefs[1]*dataToUse["SSS"]; 
        outputUncertaintyDueToInputUncertainty = self.coefs[1]*dataToUse["SSS_err"];
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;
    
class Tynan2016c_at(BaseAlgorithm):     
    #String representation of the algorithm
    def __str__(self):
        return "Tynan2016c_at: Tyn16c(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS", "SST"];
    
    @staticmethod
    def output_name():
        return "AT";
 
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        self.coefs = [-801, 127.3, -1.08, -10.3, 1.27 ]; # temp degree C found in section 3.2.3. Carbonate system calculations
        self.coefsUncertainty = [None, None]; 
        self.rmsd = 10.2
        self.r = None; # 
          
      
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
        modelOutput = self.coefs[0] + self.coefs[1]*dataToUse["SSS"] + self.coefs[2]*((dataToUse["SSS"])**2) + self.coefs[3]*SST+ self.coefs[4]*(SST**2) 
        
        #Calculate each uncertainty term serparately, for simplicity
        uterm1 = self.coefs[3] * dataToUse["SST_err"];
        uterm4 =  self.coefs[4] * dataToUse["SST_err"];
        uterm2 =  self.coefs[2] * dataToUse["SSS_err"];
        uterm3 =  self.coefs[3] * dataToUse["SSS_err"]; 
        outputUncertaintyDueToInputUncertainty = np.sqrt( uterm1**2 + uterm2**2 + uterm3**2+ uterm4**2);
        
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;
  
#Fransson et al 2001 - The importance of shelf processes for the modification of chemical constituents in the waters of the eastern Arctic Ocean.  Cont. Shelf Res., 21 , 225-242, 2001

class Fransson2001_at(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "Fransson2001_at: Fran01(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS"];
    
    @staticmethod
    def output_name():
        return "AT";    
    
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        self.coefs = [1480, 22.67 ]; #intersept, salinity slope,
        self.coefsUncertainty = [None, None]; 
        self.rmsd = None
        self.r = (np.sqrt(0.79)); # fig 4
           
       
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
        modelOutput = self.coefs[0] + self.coefs[1]*dataToUse["SSS"]; 
        outputUncertaintyDueToInputUncertainty = self.coefs[1]*dataToUse["SSS_err"];
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;


         
#Fransson et al 2009 -New insights into the spatial variability of the surface water carbon dioxide in varying sea ice conditions in the Arctic Ocean
#North west passage 
class Fransson2009_at(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "Fransson2009_at: Fran09(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS"];
    
    @staticmethod
    def output_name():
        return "AT";
 
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        
        self.includedRegionsLons = [ 
                                ];
        self.includedRegionsLats = [
                                    ];
        
        #Algorithm will only be applied to values inside these ranges
        self.restrictRanges = { 
                               };
        
        #If the matchup dataset contains values outside of these ranges they will be flagged to the user
        self.flagRanges = {
                           }
    def _equation1(self, data):
        coefs = [ 69.3];
        rmsd = None
        r = (np.sqrt(0.78));
        dataToUse =data
        modelOutput = coefs[0]*dataToUse["SSS"]; 
        outputUncertaintyDueToInputUncertainty = coefs[0]*dataToUse["SSS_err"];
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    
    
    def _equation2(self, data):
        coefs = [1494, 21.74 ]
        r = (np.sqrt(0.81))
        rmsd = None
        dataToUse =data
        modelOutput = coefs[0] + coefs[1]*dataToUse["SSS"]; 
        outputUncertaintyDueToInputUncertainty = coefs[1]*dataToUse["SSS_err"];
        return modelOutput, outputUncertaintyDueToInputUncertainty,rmsd;
        
        
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
      
              
 # Chierici & Fransson 2009 Calcium carbonate saturation in the surface water of the Arctic Ocean: undersaturation in freshwater influenced shelves  

# bering sea

class Chierici2009_at(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "Chierici2009_at: Cher09(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS"];
    
    @staticmethod
    def output_name():
        return "AT";    
    
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        self.coefsUncertainty = [None, None]; 
        self.coefs = [303.99, 58.854]; #intersept, salinity slope,
        
        self.rmsd = 5
        self.r = (np.sqrt(0.974)); # fig 5 
                
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
        modelOutput = self.coefs[0] + self.coefs[1]*dataToUse["SSS"]; 
        outputUncertaintyDueToInputUncertainty = self.coefs[1]*dataToUse["SSS_err"];
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;

#Anderson et al 2011 East Siberian Sea, an Arctic region of very high biogeochemical activity           

class Anderson2011_at(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "Anderson2011_at: Ander11(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS"];
    
    @staticmethod
    def output_name():
        return "AT";    
    
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        self.coefs = [501, 52.48]; #intersept, salinity slope,
        self.coefsUncertainty = [None, None]; 
        self.rmsd = None
        self.r = (np.sqrt(0.9822)); # fig 6
        
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
        modelOutput = self.coefs[0] + self.coefs[1]*dataToUse["SSS"]; 
        outputUncertaintyDueToInputUncertainty = self.coefs[1]*dataToUse["SSS_err"];
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;

#Yamamoto- Kawai et al 2016 Seasonal variation of CaCO3 saturation state in bottom water of a biological hotspot in the Chukchi Sea, Arctic Ocean
#chukchi sea s>31 
class Yamamoto2016_at(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "Yamamoto2016_at: Yam16(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS"];
    
    @staticmethod
    def output_name():
        return "AT";    
    
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        self.coefs = [370.34, 59.23]; #intersept, salinity slope,
        self.coefsUncertainty = [None, None]; 
        self.rmsd = 14.03
        self.r = (np.sqrt(0.83)); # equation 2
    
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
    #Algorithm will only be applied to values inside these ranges
        self.restrictRanges = {"SSS": (31, 37.0), #Algorithm valid for this range
                               };   
             
    #The main calculation is performed here, returns the model output
    def _kernal(self, dataToUse):
        modelOutput = self.coefs[0] + self.coefs[1]*dataToUse["SSS"]; 
        outputUncertaintyDueToInputUncertainty = self.coefs[1]*dataToUse["SSS_err"];
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;

#Andreev 2010 The distribution of the carbonate parameters in the waters of Anadyr Bay of the Bering Sea and in the western part of the Chukchi Sea
#bering sea 
class Andreev2010_at(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "Andreev2010_at: And10(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS"];
    
    @staticmethod
    def output_name():
        return "AT";    
    
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        
    def _equation1(self, data):
        coefs = [1545, 20]; #intersept, salinity slope,
      
        rmsd = None
        r = 0.996; # 
        dataToUse = data
        modelOutput = coefs[0] + coefs[1]*dataToUse["SSS"]; 
        outputUncertaintyDueToInputUncertainty = coefs[1]*dataToUse["SSS_err"];
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    def _equation2(self, data):
        coefs = [70, 60]; #intersept, salinity slope,
        coefsUncertainty = [None, None]; 
        rmsd = None
        r = 0.987; #
    
        dataToUse = data
        modelOutput = coefs[0] + coefs[1]*dataToUse["SSS"]; 
        outputUncertaintyDueToInputUncertainty = coefs[1]*dataToUse["SSS_err"];
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
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


# Wong 2002 Seasonal cycles of nutrients and dissolved inorganic carbon at high and mid latitudes in the North Pacific Ocean during the Skaugran cruises: Determination of new production and nutrient uptake ratios
#chukchi sea s>31
class Wong2002_at(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "Wong2002_at: Wong02(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS"];
    
    @staticmethod
    def output_name():
        return "AT";    
    
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        self.coefs = [797.7, 44.4]; #intersept, salinity slope,
        # salinity coeffient error 2.9
        self.rmsd = None;
        self.coefsUncertainty = [None, 2.9]; 
        self.r = None; # fig 3
       #Specify rectangular regions which the algorithm is valid for. Defaults to global when empty.
        #See fig 2, 3 for extents used by authors
        self.includedRegionsLons = [ 
                                ];
        self.includedRegionsLats = [
                                    ];
                        
        #If the matchup dataset contains values outside of these ranges they will be flagged to the user
        self.flagRanges = {
                           }; 
    #Algorithm will only be applied to values inside these ranges
        self.restrictRanges = {"SSS": (31, 37.0), #Algorithm valid for this range
                               };   
             
    #The main calculation is performed here, returns the model output
    def _kernal(self, dataToUse):
        modelOutput = self.coefs[0] + self.coefs[1]*dataToUse["SSS"]; 
        outputUncertaintyDueToInputUncertainty = self.coefs[1]*dataToUse["SSS_err"];
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;


#DeGrandpre 2019 Inorganic Carbon and pCO2 Variability During Ice Formation in the Beaufort Gyre of the Canada Basin
class DeGrandpre2019_at(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "DeGrandpre2019_at: De19(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS"];
    
    @staticmethod
    def output_name():
        return "AT";    
    
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        self.coefs = [333.64, 60.268]; #intersept, salinity slope, equation 1
        self.coefsUncertainty = [None, None]; 
        self.rmsd = 38
        self.r =  (np.sqrt(0.88));
           
        #Specify rectangular regions which the algorithm is valid for. Defaults to global when empty.
        #See fig 2, 3 for extents used by authors
        self.includedRegionsLons = [ 
                                ];
        self.includedRegionsLats = [
                                    ];
        
        #Algorithm will only be applied to values inside these ranges
        self.restrictRanges = { "SSS": (25.5, 30.5), 
                               };
        
        #If the matchup dataset contains values outside of these ranges they will be flagged to the user
        self.flagRanges = {
                           }; 
             
    #The main calculation is performed here, returns the model output
    def _kernal(self, dataToUse):
        modelOutput = self.coefs[0] + self.coefs[1]*dataToUse["SSS"]; 
        outputUncertaintyDueToInputUncertainty = self.coefs[1]*dataToUse["SSS_err"];
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;
    
#Ko 2020 Origin and Accumulation of an Anthropogenic CO2 and 13C Suess Effect in the Arctic Ocean
#bering sea 
class Ko2020_at(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "Ko2020_at: Ko20(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS"];
    
    @staticmethod
    def output_name():
        return "AT";    
    
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        self.coefs = [536, 51.4]; #intersept, salinity slope, equation 5
        self.coefsUncertainty = [None, None]; 
        self.rmsd = None
        self.r = None; 
        
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
        modelOutput = self.coefs[0] + self.coefs[1]*dataToUse["SSS"]; 
        outputUncertaintyDueToInputUncertainty = self.coefs[1]*dataToUse["SSS_err"];
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;   
    
#Zhongyong 2013 Summertime freshwater fractions in the surface water of the western Arctic Ocean evaluated from total alkalinity
# western arctic 3rd chinare arctic cruise PiD
class Zhongyong2013_at(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "Zhongyong2013_at: Zhon13(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS"];
    
    @staticmethod
    def output_name():
       return "AT";    
    
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        
    def _equation1(self, data):
        coefs = [71.237]; #intersept, salinity slope,
        dataToUse = data
        rmsd = None
        r = (np.sqrt(0.7799)); #figure 2 

        modelOutput = coefs[0]*dataToUse["SSS"]; 
        outputUncertaintyDueToInputUncertainty = coefs[0]*dataToUse["SSS_err"];
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;    
    
    def _equation2(self, data):
        coefs = [70.657]; #intersept, salinity slope,
       
        rmsd = None
        r =   (np.sqrt(0.7643)); #figure 2 
        dataToUse = data
        modelOutput = coefs[0]*dataToUse["SSS"]; 
        outputUncertaintyDueToInputUncertainty = coefs[0]*dataToUse["SSS_err"];
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;    
        
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
    
    
    
#Requires NO3- (as fitted to potential alkalinity)
#Takahashi, T., Sutherland, S.C., Chipman, D.W., Goddard, J.G., Ho, C., Newberger, T., Sweeney, C. and Munro, D.R., 2014. Climatological distributions of pH, pCO2, total CO2, alkalinity, and CaCO3 saturation in the global surface ocean, and temporal changes at selected locations. Marine Chemistry, 164, pp.95-125.
class Takahashi2013_at(BaseAlgorithm): 
    #String representation of the algorithm
    def __str__(self):
        return "Takahashi2013_at: TS13(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS", "NO3"]; #NO3 used to convert from potential alkalinity to TA
    @staticmethod
    def output_name():
        return "AT";
    
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        
        #import region mask data
        from netCDF4 import Dataset;
        self.regionMasks = Dataset(settings["algorithmSpecificDataPaths"][type(self).__name__], 'r');
        
        #If the matchup dataset contains values outside of these ranges they will be flagged to the user
        self.flagRanges = {
                           };
    
    #West GIN seas (greenland, iceland, norweign seas ) 66°N - 80°N, 30°W - 0°
    #Note: Multiple models for a single algorithm is ok here because together spatial extent of each model covers all of the OceanSODA regions (except osoda_mediterranean).
    
    def _zone1(self, data): 
            #For coefficients see table 1
        coefs = [1796.2, 14.12]; #intersept, SSS
        rmsd = 6.1; #table 1
        
        #Subset data to only rows valid for this zone. See table 1 and fig 4
        dataToUse = subset_from_mask(data, self.regionMasks, "zone1_West_GIN_seas"); 
        dataToUse = dataToUse[(dataToUse["SSS"] > 24) & #See fig 4
                              (dataToUse["SSS"] < 37)];
        
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + \
                      coefs[1]*(dataToUse["SSS"]);
        
        outputUncertaintyDueToInputUncertainty = coefs[1]*dataToUse["SSS_err"];
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    
    #East GIN Seas  66°N - 80°N, 0° - 30°E
    def _zone2(self, data):
        #For coefficients see table 1
        coefs = [232.0, 59.57]; #intersept, SSS
        rmsd = 12.3; #table 1
        
        #Subset data to only rows valid for this zone. See table 1 and fig 4
        dataToUse = subset_from_mask(data, self.regionMasks, "zone2_West_GIN_seas");
        dataToUse = dataToUse[(dataToUse["SSS"] > 24) & #See fig 4
                              (dataToUse["SSS"] < 37)];
        
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + \
                      coefs[1]*(dataToUse["SSS"]);
        
        outputUncertaintyDueToInputUncertainty = coefs[1]*dataToUse["SSS_err"];
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    
# High arctic N of 80°N 
    def _zone3(self, data):
        #For coefficients see table 1
        coefs = [1340.7, 27.30]; #intersept, SSS
        rmsd = 16.8; #table 1
        
        #Subset data to only rows valid for this zone. See table 1 and fig 4
        dataToUse = subset_from_mask(data, self.regionMasks, "zone3_ High_arctic");
        dataToUse = dataToUse[(dataToUse["SSS"] > 24) & #See fig 
                              (dataToUse["SSS"] < 37)];
        
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + \
                      coefs[1]*(dataToUse["SSS"]);
        
        outputUncertaintyDueToInputUncertainty = coefs[1]*dataToUse["SSS_err"];
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
   
    #Beaufort sea 66°N - 80°N, 140°W - 180° 
    def _zone4(self, data):
        #For coefficients see table 1
        coefs = [285.8, 61.29]; #intersept, SSS
        rmsd = 60.5; #table 1
        
        #Subset data to only rows valid for this zone. See table 1 and fig 4
        dataToUse = subset_from_mask(data, self.regionMasks, "zone4_Beaufort_sea");
        dataToUse = dataToUse[(dataToUse["SSS"] > 24) & #See fig 4
                              (dataToUse["SSS"] < 37)];
        
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + \
                      coefs[1]*(dataToUse["SSS"]);
        
        outputUncertaintyDueToInputUncertainty = coefs[1]*dataToUse["SSS_err"];
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
   
    #Labrador sea 55°N - 80°N, 85°W - 45°W 
    def _zone5(self, data):
        #For coefficients see table 1
        coefs = [1016.2,37.27 ]; #intersept, SSS
        rmsd = 17.2; #table 1
        
        #Subset data to only rows valid for this zone. See table 1 and fig 4
        dataToUse = subset_from_mask(data, self.regionMasks, "zone5_Labrador_sea"); 
        dataToUse = dataToUse[(dataToUse["SSS"] > 24) & #See fig 4
                              (dataToUse["SSS"] < 37)];
        
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + \
                      coefs[1]*(dataToUse["SSS"]);
        
        outputUncertaintyDueToInputUncertainty = coefs[1]*dataToUse["SSS_err"];
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    
    #Sub-Arctic Atlantic 55°N - 80°N, 40°W - 10°E
    def _zone6(self, data):
        #For coefficients see table 1
        coefs = [730.6, 45.37]; #intersept, SSS
        rmsd = 6.7 ; #table 1
        
        #Subset data to only rows valid for this zone. See table 1 and fig 4
        dataToUse = subset_from_mask(data, self.regionMasks, "zone6_Sub-Arctic_Atlantic"); 
        dataToUse = dataToUse[(dataToUse["SSS"] > 24) & #See fig 4
                              (dataToUse["SSS"] < 37)];
        
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + \
                      coefs[1]*(dataToUse["SSS"]);
        
        outputUncertaintyDueToInputUncertainty = coefs[1]*dataToUse["SSS_err"];
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
        
   #N. Central Pacific 44°N - 60°N, W of 150°W 
    def _zone7(self, data):
        #For coefficients see table 1
        coefs = [-395.7, 79.92]; #intersept, SSS
        rmsd = 14.7 ; #table 1
        
        #Subset data to only rows valid for this zone. See table 1 and fig 4
        dataToUse = subset_from_mask(data, self.regionMasks, "zone7_N_Central_Pacific");
        dataToUse = dataToUse[(dataToUse["SSS"] > 30) & #See fig 4
                              (dataToUse["SSS"] < 38)];
        
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + \
                      coefs[1]*(dataToUse["SSS"]);
        
        outputUncertaintyDueToInputUncertainty = coefs[1]*dataToUse["SSS_err"];
        
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
        run_single_zone(self._zone7, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);  
        run_single_zone(self._zone6, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);
        run_single_zone(self._zone5, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);
        run_single_zone(self._zone4, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);
        run_single_zone(self._zone3, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);
        run_single_zone(self._zone2, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);
        run_single_zone(self._zone1, dataToUse, modelOutput, outputUncertaintyDueToInputUncertainty, rmsds);
        
        #Convert from potential alkalinity to TA
        #PALK = TA + NO3-, so calculate TA using:
        modelOutput = modelOutput - dataToUse["NO3"];
        outputUncertaintyDueToInputUncertainty = np.sqrt( outputUncertaintyDueToInputUncertainty**2 + dataToUse["NO3_err"]**2);
        
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertainty;
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsds;


#Lee, K., Tong, L.T., Millero, F.J., Sabine, C.L., Dickson, A.G., Goyet, C., Park, G.H., Wanninkhof, R., Feely, R.A. and Key, R.M., 2006. Global relationships of total alkalinity with salinity and temperature in surface waters of the world's oceans. Geophysical research letters, 33(19).
#All zones/equations
class Lee2006_at(BaseAlgorithm):
    #String representation of the algorithm
    def __str__(self):
        return "Lee2006_at: L06(at)";
    
    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS", "SST"];
    @staticmethod
    def output_name():
        return "AT";
    
    def __init__(self, settings):
        #super().__init__(settings); #Call the parent class's initator
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        
        from netCDF4 import Dataset;
        self.regionMasks = Dataset(settings["algorithmSpecificDataPaths"][type(self).__name__], 'r');
 #North Atlantic
    def _zone3(self, data):
        coefs = [2305, 53.97, 2.74, -1.16, -0.040]; #intersept, salinity, salinity^2, SST, SST^2 see table 1
        rmsd = 6.4; #See table 1 (zone 3)
        
        #Subset data to only rows valid for this zone. See Table 1
        dataToUse = subset_from_mask(data, self.regionMasks, "zone3_mask");
        dataToUse = dataToUse[(dataToUse["SST"] > 0) &
                              (dataToUse["SST"] < 20) &
                              (dataToUse["SSS"] > 31) &
                              (dataToUse["SSS"] < 37)
                              ];
        
        SSS = dataToUse["SSS"]-35;
        SST = dataToUse["SST"]-20;
        
        #Equation from table 1 (zone 3)
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + \
                      coefs[1]*SSS + \
                      coefs[2]*(SSS**2) + \
                      coefs[3]*SST + \
                      coefs[4]*(SST**2);
        
        #Calculate each uncertainty term serparately, for simplicity
        uterm1 = coefs[1] * dataToUse["SSS_err"]; #B*SSS
        uterm2 = coefs[2] * 2.0*dataToUse["SSS_err"]*SSS; #B*SSS^2. Rearranged form of Taylor eq. 3.10: if x=q^n, then dx = n*u*q^(n-1), where u is uncertainty on q
        uterm3 = coefs[3] * dataToUse["SST_err"]; #B*SST
        uterm4 = coefs[4] * 2.0*dataToUse["SST_err"]*SST; #B*SST^2. Rearranged form of Taylor eq. 3.10: if x=q^n, then dx = n*u*q^(n-1), where u is uncertainty on q
        #Add in quadrature
        outputUncertaintyDueToInputUncertainty = np.sqrt( uterm1**2 + uterm2**2 + uterm3**2 + uterm4**2 );
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    
    #North Pacific
    def _zone4(self, data):
        coefs = [2305, 53.23, 1.85, -14.72, -0.158, 0.062]; #intersept, salinity, salinity^2, SST, SST^2, SST*longitude see table 1
        rmsd = 8.7; #See table 1 (zone 4)
        
        #Subset data to only rows valid for this zone. See Table 1
        dataToUse = subset_from_mask(data, self.regionMasks, "zone4_mask");
        dataToUse = dataToUse[(dataToUse["SST"] < 20) &
                              (dataToUse["SSS"] > 31) &
                              (dataToUse["SSS"] < 35)
                              ];
        
        SSS = dataToUse["SSS"]-35;
        SST = dataToUse["SST"]-20;
        lon = dataToUse["lon"]+180; #Should longitude be (-180, 180) or (0 360)?
        
        #Equation from table 1 (zone 4)
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + \
                      coefs[1]*SSS + \
                      coefs[2]*(SSS**2) + \
                      coefs[3]*SST + \
                      coefs[4]*(SST**2) + \
                      coefs[5]*SST*lon; #Should longitude be (-180, 180) or (0 360)?
        
        #Calculate each uncertainty term serparately, for simplicity
        uterm1 = coefs[1] * dataToUse["SSS_err"]; #B*SSS
        uterm2 = coefs[2] * 2.0*dataToUse["SSS_err"]*SSS; #B*SSS^2. Rearranged form of Taylor eq. 3.10: if x=q^n, then dx = n*u*q^(n-1), where u is uncertainty on q
        uterm3 = coefs[3] * dataToUse["SST_err"]; #B*SST
        uterm4 = coefs[4] * 2.0*dataToUse["SST_err"]*SST; #B*SST^2. Rearranged form of Taylor eq. 3.10: if x=q^n, then dx = n*u*q^(n-1), where u is uncertainty on q
        uterm5 = coefs[5] * dataToUse["SST_err"]*lon; #B*SST*longitude. Assume 0 uncertainty in longitude.
        #Add in quadrature
        outputUncertaintyDueToInputUncertainty = np.sqrt( uterm1**2 + uterm2**2 + uterm3**2 + uterm4**2 + uterm5**2 );
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
   
    def _kernal(self, dataToUse):
        #Create empty output array
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        outputUncertaintyDueToInputUncertainty = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        rmsds = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        
        #Perform calculations for each zone
              
        zoneData, zoneUncertainty, zoneRmsd = self._zone3(dataToUse);
        if np.any(np.isfinite(modelOutput[zoneData.index])==True): #Sanity check for overlaps
            raise RuntimeError("Overlapping zones in Lee06_at. Something has done wrong!");
        modelOutput[zoneData.index] = zoneData;
        outputUncertaintyDueToInputUncertainty[zoneData.index] = zoneUncertainty;
        rmsds[zoneData.index] = zoneRmsd;
        
        zoneData, zoneUncertainty, zoneRmsd = self._zone4(dataToUse);
        if np.any(np.isfinite(modelOutput[zoneData.index])==True): #Sanity check for overlaps
            raise RuntimeError("Overlapping zones in Lee06_at. Something has done wrong!");
        modelOutput[zoneData.index] = zoneData;
        outputUncertaintyDueToInputUncertainty[zoneData.index] = zoneUncertainty;
        rmsds[zoneData.index] = zoneRmsd;
       
                
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertainty;
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsds;
   
#Corbière, A., Metzl, N., Reverdin, G., Brunet, C. and Takahashi, T., 2007. Interannual and decadal variability of the oceanic carbon sink in the North Atlantic subpolar gyre. Tellus B: Chemical and Physical Meteorology, 59(2), pp.168-178.
class Corbiere2007_at(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "Corbiere2007_at: Co07(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS"];
    @staticmethod
    def output_name():
        return "AT";
    
    #Set algorithm specific variables
    def __init__(self, settings):
        self.settings = settings;
        self.coefs = [713.5, 45.808]; #intersept, salinity slope, see eq 1
        self.coefsUncertainty = [None, None]; #Uncertainty reported for the coefficients, see eq 1
        self.rmsd = 10.3; #See eq 1
        self.r = 0.92**0.5;
        
        #Specify rectangular regions which the algorithm is valid for. Defaults to global when empty.
        self.includedRegionsLons = [(-60, -20)]; #See fig 1
        self.includedRegionsLats = [(44, 65)]; #See fig 1
        
        #Algorithm will only be applied to values inside these ranges
        self.restrictRanges = {"SSS": (31, 35.5), #See fig 2
                               };
        
        #If the matchup dataset contains values outside of these ranges they will be flagged to the user
        self.flagRanges = {"SST": (1.0, 16.0), #See fig 3a
                           };

    #The main calculation is performed here, returns the model output
    def _kernal(self, dataToUse):
        modelOutput = self.coefs[0] + self.coefs[1]*dataToUse["SSS"]; #See fig 3
        outputUncertaintyDueToInputUncertainty = self.coefs[1]*dataToUse["SSS_err"];
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;

#Millero, F.J., Lee, K. and Roche, M., 1998. Distribution of alkalinity in the surface waters of the major oceans. Marine Chemistry, 60(1-2), pp.111-130.
class Millero1998_at(BaseAlgorithm):
    #String representation of the algorithm
    def __str__(self):
        return "Millero1998_at: M98(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SST", "SSS"];
    @staticmethod
    def output_name():
        return "AT";
    
    def __init__(self, settings):
        BaseAlgorithm.__init__(self, settings); #Call the parent class's initator
        self.settings = settings;
        
        #import region mask data
        from netCDF4 import Dataset;
        self.regionMasks = Dataset(settings["algorithmSpecificDataPaths"][type(self).__name__], 'r');
        
        #If the matchup dataset contains values outside of these ranges they will be flagged to the user
        self.flagRanges = {"SSS": (33.75, 36), #See fig 7
                           };
    def _zone2(self, data):
        coefs = [2291.0, -2.69, -0.046]; #intersept, SST, SST^2 see table 4
        rmsd = 5.0; #See table 4
        
        #Subset data to only rows valid for this zone. See Table 4
        dataToUse = subset_from_mask(data, self.regionMasks, "zone2_mask");
        dataToUse = dataToUse[(dataToUse["SST"] > 0) &
                              (dataToUse["SST"] < 20)
                              ];
        
        SST = dataToUse["SST"]-(20);
        
        #equation from table 4
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + \
                      coefs[1]*SST + \
                      coefs[2]*(SST**2);
        
        #Calculate each uncertainty term serparately, for simplicity
        uterm1 = coefs[1] * dataToUse["SST_err"]; #B*SST
        uterm2 = coefs[2] * 2.0*dataToUse["SST_err"]*SST; #B*SST^2. Rearranged form of Taylor eq. 3.10: if x=q^n, then dx = n*u*q^(n-1), where u is uncertainty on q
        #Add in quadrature
        outputUncertaintyDueToInputUncertainty = np.sqrt( uterm1**2 + uterm2**2 );
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    def _zone5(self, data):
        coefs = [2300, -7.0, -0.158]; #intersept, SST, SST^2 see table 4
        rmsd = 5.0; #See table 4
        
        #Subset data to only rows valid for this zone. See Table 4
        dataToUse = subset_from_mask(data, self.regionMasks, "zone5_mask");
        dataToUse = dataToUse[(dataToUse["SST"] > 7) &
                              (dataToUse["SST"] < 20)
                              ];
        
        SST = dataToUse["SST"]-20;
        
        #equation from table 4
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput = coefs[0] + \
                      coefs[1]* + \
                      coefs[2]*(SST**2);
        
        #Calculate each uncertainty term serparately, for simplicity
        uterm1 = coefs[1] * dataToUse["SST_err"]; #B*SST
        uterm2 = coefs[2] * 2.0*dataToUse["SST_err"]*SST; #B*SST^2. Rearranged form of Taylor eq. 3.10: if x=q^n, then dx = n*u*q^(n-1), where u is uncertainty on q
        #Add in quadrature
        outputUncertaintyDueToInputUncertainty = np.sqrt( uterm1**2 + uterm2**2 );
        
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsd;
    
        #The main calculation is performed here, returns the model output
    def _kernal(self, dataToUse):
        #Create empty output array
        modelOutput = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        outputUncertaintyDueToInputUncertainty = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        rmsds = pd.Series([np.nan]*len(dataToUse), index=dataToUse.index);
        modelOutput[:] = rmsds[:] = np.nan;
        
        #Perform calculations for each zone
        
        zoneData, zoneUncertainty, zoneRmsd = self._zone2(dataToUse);
        if np.any(np.isfinite(modelOutput[zoneData.index])==True): #Sanity check for overlaps
            raise RuntimeError("Overlapping zones in Lee06_at. Something has done wrong!");
        modelOutput[zoneData.index] = zoneData;
        outputUncertaintyDueToInputUncertainty[zoneData.index] = zoneUncertainty;
        rmsds[zoneData.index] = zoneRmsd;
                     
        
        zoneData, zoneUncertainty, zoneRmsd = self._zone5(dataToUse);
        if np.any(np.isfinite(modelOutput[zoneData.index])==True): #Sanity check for overlaps
            raise RuntimeError("Overlapping zones in Lee06_at. Something has done wrong!");
        modelOutput[zoneData.index] = zoneData;
        outputUncertaintyDueToInputUncertainty[zoneData.index] = zoneUncertainty;
        rmsds[zoneData.index] = zoneRmsd;
        
      
        
        #This algorithm gives AT normalised to 35 PSU salinity. Reverse normalisation:
        
        outputUncertaintyDueToInputUncertaintyRatio = (outputUncertaintyDueToInputUncertainty/modelOutput) + (dataToUse["SSS_err"]/dataToUse["SSS"]); #Propagate uncertainty through normalisation
        modelOutput = modelOutput / (35.0/dataToUse["SSS"]);
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertaintyRatio*modelOutput; #two steps to avoid duplicate calculation
        
        outputUncertaintyDueToInputUncertainty = outputUncertaintyDueToInputUncertainty;
        return modelOutput, outputUncertaintyDueToInputUncertainty, rmsds;
    
#Brewer, P.G., Glover, D.M., Goyet, C. and Shafer, D.K., 1995. The pH of the North Atlantic Ocean: Improvements to the global model for sound absorption in seawater. Journal of Geophysical Research: Oceans, 100(C5), pp.8761-8776.
#Implementation of equation 8 (<250m depth)
class Brewer1995_at(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "Brewer1995_at: B95(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS", "DO", "SiO4", "PO4", "NO3"];

    @staticmethod
    def output_name():
        return "AT";
    
    #Set algorithm specific variables
    def __init__(self, settings):
        self.settings = settings;

        self.coefs = [530.0, 51.132, -0.033, 0.973, 59.3, -4.31]; #intersept, salinity, DO, SiO4, PHO4, NO3 see equation 8
        self.coefsUncertainty = [None, None, None, None, None, None]; #Uncertainty reported for the coefficients, see fig 11
        self.rmsd = None;
        self.r = 0.975**0.5; #equation 8
        
        #Specify rectangular regions which the algorithm is valid for. Defaults to global when empty.
        self.includedRegionsLons = [(-100, 30)]; #See fig 1a
        self.includedRegionsLats = [(0, 80)]; #See fig 1a
        
        
        #Algorithm will only be applied to values inside these ranges
        self.restrictRanges = {"SSS": (31, 37.5), #See fig 4
                               };
        
        #If the matchup dataset contains values outside of these ranges they will be flagged to the user
        self.flagRanges = {"SST": (-2, 28), #See fig 5
                           "PO4": (0, 2.2), #See fig 5 (continued, second page)
                           "SiO4": (0, 65), #See fig 5 (continues, 3rd page)  
                           "NO3": (0, 34), #See fig 5 (continues, 3rd page)
                           };

    #The main calculation is performed here, returns the model output
    def _kernal(self, dataToUse):
        modelOutput = self.coefs[0] + self.coefs[1]*dataToUse["SSS"]; #See fig 11
        outputUncertaintyDueToInputUncertainty = self.coefs[1]*dataToUse["SSS_err"];
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;

#Cai, W.J., Hu, X., Huang, W.J., Jiang, L.Q., Wang, Y., Peng, T.H. and Zhang, X., 2010. Alkalinity distribution in the western North Atlantic Ocean margins. Journal of Geophysical Research: Oceans, 115(C8).
#"Labrador Sea" - fig 3 (shown spatially in fig 1)
class Cai2010_at(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "Cai2010_at: Ca10(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS"];
    @staticmethod
    def output_name():
        return "AT";
    
    #Set algorithm specific variables
    def __init__(self, settings):
        self.settings = settings;
        self.coefs = [1124.4, 33.0]; #intersept, salinity slope, see fig 3
        self.coefsUncertainty = [103.1, None]; #Uncertainty reported for the coefficients, see fig 3
        self.rmsd = 12.7; #See fig 11
        self.r = None;
        
        #Specify rectangular regions which the algorithm is valid for. Defaults to global when empty.
        self.includedRegionsLons = [(-60, -45)]; #See "Labrador Sea" fig 1
        self.includedRegionsLats = [(50, 62)]; #See "Labrador Sea" fig 1
        
        #Algorithm will only be applied to values inside these ranges
        self.restrictRanges = {"SSS": (33, 35), #See fig 3
                               };
        
        #If the matchup dataset contains values outside of these ranges they will be flagged to the user
        self.flagRanges = {
                           };

    #The main calculation is performed here, returns the model output
    def _kernal(self, dataToUse):
        modelOutput = self.coefs[0] + self.coefs[1]*dataToUse["SSS"]; #See fig 3
        outputUncertaintyDueToInputUncertainty = self.coefs[1]*dataToUse["SSS_err"];
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;
    
#Tait, V.K., Gershey, R.M. and Jones, E.P., 2000. Inorganic carbon in the Labrador Sea: Estimation of the anthropogenic component. Deep Sea Research Part I: Oceanographic Research Papers, 47(2), pp.295-308.
class Tait2000_at(BaseAlgorithm):    
    #String representation of the algorithm
    def __str__(self):
        return "Tait2000_at: Ta00(at)";

    #common names of input and output variables (see global_settings for definitions of these
    @staticmethod
    def input_names():
        return ["SSS", "SST"];
    @staticmethod
    def output_name():
        return "AT";
    
    #Set algorithm specific variables
    def __init__(self, settings):
        self.settings = settings;
        self.coefs = [785.3, 43.01, 2.046]; #intersept, SSS, SST (as potential temperature), equation 6
        self.coefsUncertainty = [None, None, None]; #Uncertainty reported for the coefficients, equation 1
        self.rmsd = None;
        self.r = None;
        self.standardError = 5.4;
        
        #Specify rectangular regions which the algorithm is valid for. Defaults to global when empty.
        #Estimated from fig 1
        self.includedRegionsLons = [(-58, -42),
                                    ];
        self.includedRegionsLats = [(51, 62),
                                    ];
        
        #Algorithm will only be applied to values inside these ranges
        self.restrictRanges = {"SSS": (32, 35), #See fig 2
                               };
        
        #If the matchup dataset contains values outside of these ranges they will be flagged to the user
        self.flagRanges = { #None reported
                           };

    #The main calculation is performed here, returns the model output
    def _kernal(self, dataToUse):
        SST = dataToUse["SST"]-273.15;
        modelOutput = self.coefs[0] + self.coefs[1]*dataToUse["SSS"] + self.coefs[2]*SST; #From Tait2000 eq. 6
        outputUncertaintyDueToInputUncertainty = np.sqrt( (self.coefs[1]*dataToUse["SSS_err"])**2 + (self.coefs[2]*dataToUse["SST_err"])**2 );
        return modelOutput, outputUncertaintyDueToInputUncertainty, self.rmsd;
    

