#######################################################################################################
#######################################################################################################
## 
##raw2snow: Process raw files using Maahn and Kollias method (2012)
##
##
#######################################################################################################
#######################################################################################################


def raw2snow(file_in,file_out, TRES = 60, Descr = "MRR data", author = "APRES3 project",ncForm="NETCDF3_CLASSIC"): #convert raw files in MRR Doppler moments
    import os, time, warnings, sys
    import matplotlib.pyplot as plt
    path_IMProToo="/IMProToo/" #See more in https://github.com/maahn/IMProToo
    print("IMProToo = ", path_IMProToo)
    sys.path.append(path_IMProToo)
    import core3 as IMProToo
    warnings.filterwarnings("ignore") #Ignore IMProToo warmings
    rawData = IMProToo.mrrRawData(file_in) # Read RawData
    processedSpec = IMProToo.MrrZe(rawData) #create the IMProToo object and load rawData
    processedSpec.averageSpectra(TRES)# integrates the data in 60 seconds by default.
    processedSpec.co["ncCreator"] = author
    processedSpec.co["ncDescription"] = Descr
    processedSpec.co["dealiaseSpectrum"] = True 
    processedSpec.rawToSnow() # Converts RawData into Radar moments
    processedSpec.writeNetCDF(file_out,ncForm=ncForm) # Saves the processed data in a nc file    
