'''
Usage:
 This programme is to creating the netcdf file corresponding to the 24, 48...120 hr forcast and observed rainfall data of rainfall data.
	Written by: Dileepkumar R
		    JRF- IIT DELHI

	Date: 23.06.2011;
'''
import numpy.ma

import ctgfunction

import data_access

import cdms2

import cdutil

from regrid2 import Regridder


gobj = data_access.Grib_Access(dataPath = '/home/dileep/Desktop/NCMRWF/NCMRWF/Monsoon_2010',modelName = 'NCMRWF2010')

obs = data_access.Rainfall_Access(xmlPath = '/home/dileep/rainfall_regrided/rainfall_regrided.xml', xmlVar = 'pobs')

time_list_grib=('2010-6-1','2010-9-30')

time_fcst=[24, 48, 72, 96, 120]

for i in xrange(len(time_fcst)):
	rain,fcst_grib = gobj.getRainfallDataPartners(date = time_list_grib, hour = time_fcst[i], level = 'all',orginData = 1,datePriority = 'o',rainObject = obs, lat=(0,40),lon=(60,100))
	
	fcst_grib.id='fcst_grib_%d' %(time_fcst[i])	

	filename_2='/home/dileep/NCMR_fcst_obs_nc/ncmr_fcst_%d.nc' %(time_fcst[i])
	filename_1='/home/dileep/NCMR_fcst_obs_nc/ncmr_obs.nc' 
	if i==0:
		rain.id='rain_obs' 

		f=cdms2.open(filename_1, 'w')
		f.write(rain)
		f.close()
	g=cdms2.open(filename_2, 'w')
	
	g.write(fcst_grib)
	
	g.close()



	

