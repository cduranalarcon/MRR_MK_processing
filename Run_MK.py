
import numpy as np
from  netCDF4 import Dataset
import calendar, datetime, time, glob, os, sys, shutil


sys.path.append("lib/") # adding lib path
sys.path.append("lib/IMProToo/") # adding lib path


from MRR_functions import raw2snow # Process raw data into Doppler moments using MK2012
import core3 as IMProToo

np.warnings.filterwarnings('ignore')#to avoid the error messages


df = open('default_parameters.txt','r')

df_lines = df.readlines()

df.close()

Root_desc = df_lines[0].replace('\t','').replace('\n','').split('=')[0]
TRES_desc = df_lines[1].replace('\t','').replace('\n','').split('=')[0]
Short_name_station_desc = df_lines[2].replace('\t','').replace('\n','').split('=')[0]

KtoX_desc = df_lines[3].replace('\t','').replace('\n','').split('=')[0]
KtoX_a_desc = df_lines[4].replace('\t','').replace('\n','').split('=')[0]
KtoX_b_desc = df_lines[5].replace('\t','').replace('\n','').split('=')[0]

ZeToS_desc = df_lines[6].replace('\t','').replace('\n','').split('=')[0]
ZeToS_A_desc = df_lines[7].replace('\t','').replace('\n','').split('=')[0]
ZeToS_B_desc = df_lines[8].replace('\t','').replace('\n','').split('=')[0]

Root = df_lines[0].replace('\t','').replace('\n','').split('=')[1]
TRES = int(df_lines[1].replace('\t','').replace('\n','').replace(' ','').split('=')[1])
Short_name_station = df_lines[2].replace('\t','').replace('\n','').split('=')[1]

KtoX = df_lines[3].replace('\t','').replace('\n','').replace(' ','').split('=')[1]
KtoX_a = float(df_lines[4].replace('\t','').replace('\n','').replace(' ','').split('=')[1])
KtoX_b = float(df_lines[5].replace('\t','').replace('\n','').replace(' ','').split('=')[1])

ZeToS = df_lines[6].replace('\t','').replace('\n','').replace(' ','').split('=')[1]
ZeToS_A = float(df_lines[7].replace('\t','').replace('\n','').replace(' ','').split('=')[1])
ZeToS_B = float(df_lines[8].replace('\t','').replace('\n','').replace(' ','').split('=')[1])



#Parameters
print("Define parameters (data path, temporal resolution, etc.). YES (Y,y,yes): update parameters, or NOT (N,n,not,Enter): Use default parameters (already defined by the user).")
answer =  input()  #input from the user
if (answer == "Y") or (answer == "y") or (answer == "YES") or (answer == "yes"):

	print('Insert input Data path (Press Enter for default = ' + Root + '):')
	answer =  input()
	if answer != '': Root=answer  #input from the user 

	print("Insert output temporal resolution in seconds (Press Enter for default = " + str(TRES) + "s):")
	answer =  input()  #input from the user
	if answer != '': TRES =  int(answer)


	print('Insert short name of the station (Press Enter for default = ' + Short_name_station + '):')
	answer =  input()
	if answer != '': Short_name_station = answer

	print('Perform Linear correction of radome attenuation (K to X band conversion)? (Press Enter for default = ' + KtoX + '):')
	answer =  input()
	if answer != '': KtoX = answer

	if (KtoX == 'True') or (KtoX == 'T') or (KtoX == 'TRUE') or (KtoX == 'true') or (KtoX == 't'): 
		print('Insert the slope parameter for the radome attenuation correction (Press Enter for default = ' + str(KtoX_a) + '):')
		answer =  input()
		if answer != '': KtoX_a = float(answer)
		print('Insert the intercept parameter for the radome attenuation correction (Press Enter for default = ' + str(KtoX_b) + '):')
		answer =  input()
		if answer != '': KtoX_b = float(answer)

	print('Convert Ze to Precipitation rate? (Press Enter for default = ' + ZeToS + '):')
	answer =  input()
	if answer != '': ZeToS = answer

	if (ZeToS == 'True') or (ZeToS == 'T') or (ZeToS == 'TRUE') or (ZeToS == 'true') or (ZeToS == 't'): 
		print('Insert the "A" parameter (constant in Ze-S relationship) (Press Enter for default = ' + str(ZeToS_A) + '):')
		answer =  input()
		if answer != '': ZeToS_A = float(answer)
		print('Insert the "B" parameter (Exponent in Ze-S relationship) (Press Enter for default = ' + str(ZeToS_B) + '):')
		answer =  input()
		if answer != '': ZeToS_B = float(answer)


	df = open('default_parameters.txt','w')
	df.write(Root_desc+"\t"+"="+'\t'+Root+"\n")
	df.write(TRES_desc+"\t"+"="+'\t'+str(TRES)+"\n")
	df.write(Short_name_station_desc+"\t"+"="+'\t'+Short_name_station+"\n")

	df.write(KtoX_desc+"\t"+"="+'\t'+KtoX+"\n")
	df.write(KtoX_a_desc+"\t"+"="+'\t'+str(KtoX_a)+"\n")
	df.write(KtoX_b_desc+"\t"+"="+'\t'+str(KtoX_b)+"\n")

	df.write(ZeToS_desc+"\t"+"="+'\t'+ZeToS+"\n")
	df.write(ZeToS_A_desc+"\t"+"="+'\t'+str(ZeToS_A)+"\n")
	df.write(ZeToS_B_desc+"\t"+"="+'\t'+str(ZeToS_B)+"\n")

	df.close()

os.chdir(Root)

name_station = '_'.join(Short_name_station.split(' '))

Descr = "MRR data at " + name_station + ", first MRR processed with MK12 method v.0.103."

folder=Root
dircf=glob.glob(Root+'*.raw')
dircf=np.sort(dircf)

if len(dircf) == 1:
	print('In this folder there is '+str(len(dircf))+' raw file')
else:
	print('In this folder there are '+str(len(dircf))+' raw files')

for name in dircf:

	NameFile=name 

	count=0

	NameFile_out = NameFile[:-4]+'-MK.nc' #create a new file
	raw2snow(NameFile,NameFile_out, TRES = TRES, Descr = Descr) # Convert Raw into Doppler Moments using MK2012

	##Including S estimates using Grazioli et al, 2017.
	if (KtoX == 'True') or (KtoX == 'T') or (KtoX == 'TRUE') or (KtoX == 'true') or (KtoX == 't'): 
		print("Converting K to X band using Grazioli et al, 2017, TC.")
		ds = Dataset(NameFile_out,'a')
		Ze = ds.variables["Ze"][:]
		ZeX = ds.createVariable('ZeX', 'f', ('time', 'range',),fill_value=-9999.)
		#print(type(KtoX_a),type(KtoX_b))
		ZeX[:] = KtoX_a*Ze+KtoX_b
		ZeX.description = "Ze converted into X-band to take into accound the radome attenuation (see Grazioli et al. 2017, TC)"
		ZeX.units = "dBZe"

		if (ZeToS == 'True') or (ZeToS == 'T') or (ZeToS == 'TRUE') or (ZeToS == 'true') or (ZeToS == 't'):	
			print("Including S estimates using Grazioli et al, 2017.")
			S = ds.createVariable('SnowfallRate', 'f', ('time', 'range',),fill_value=-9999.)
			S[:] = ((10**(ZeX[:]/10.))/(1.*ZeToS_A))**(1./ZeToS_B) 	
			S.description = "Snowfall rate derived from S-Ze relationship in Grazioli et al. (2017, TC)"
			S.units = "mm h-1"

		ds.close()     
	else:
		if (ZeToS == 'True') or (ZeToS == 'T') or (ZeToS == 'TRUE') or (ZeToS == 'true') or (ZeToS == 't'):	#In case there is not a Radome only perform the Z-S conversion
			print("Including S estimates using Grazioli et al, 2017, TC.")
			ds = Dataset(NameFile_out,'a')
			Ze = ds.variables["Ze"][:]
			S = ds.createVariable('SnowfallRate', 'f', ('time', 'range',),fill_value=-9999.)
			S[:] = ((10**(Ze[:]/10.))/(1.*ZeToS_A))**(1./ZeToS_B) 	
			S.description = "Snowfall rate derived from S-Ze relationship in Grazioli et al. (2017, TC)"
			S.units = "mm h-1"

			ds.close()     
		


##default Parameters

#Input data path	=	/home/claudio/Projects/git/MRR_DDU/Data/DDU/RawSpectra/201702/
#output temporal resolution in seconds	=	60
#Short name of the station	=	DDU
#Radome attenuation correction (k to x band) (True or False) = True
#Radome attenuation (k to x band), a slope (dBZ) = 0.99
#Radome attenuation (k to x band), b intercept (dBZ) = 6.14
#Snowfall rate conversion (Z-S) (True or False) = True
#Z-S relationship, A parameter (constant) = 76
#Z-S relationship, B parameter (exponent) = 0.91