'''
Usage:

This programe is for regridding the observed rainfall data to forcast rainfall data. Since Observed and forcasted rainfall data are not same grid resolution.

	Example:
	 In NCMRWF data observed data is 1x1 degree resolution, but our forecasted data is 0.5x0.5 degree resolution, therefore we regrid the observed 
	 data according to forecasted data for calcuating statistical score
	 
	Written by: Dileepkumar R
		    JRF- IIT DELHI

	Date: 23.06.2011;

'''

import cdms2, cdutil

import data_access

from regrid2 import Regridder

import os


# Collecting the name of files & directories 
l=os.listdir('/home/dileep/Desktop/NCMRWF/NCMRWF/Monsoon_2010/rainfall')

#'ctl_files' are list of filenames ends with '.ctl'
ctl_files=[i for i in l if i.endswith('.ctl')]

#Reading observed rainfall data. 
gobj = data_access.Grib_Access(dataPath = '/home/dileep/Desktop/NCMRWF/NCMRWF/Monsoon_2010',modelName = 'NCMRWF2010')
obs = data_access.Rainfall_Access(xmlPath = '/home/dileep/Desktop/NCMRWF/NCMRWF/Monsoon_2010/rainfall/rainfall.xml', xmlVar = 'pobs')

for i in xrange(len(ctl_files)):
	
	filename='/home/dileep/Desktop/NCMRWF/NCMRWF/Monsoon_2010/rainfall/%s' %(ctl_files[i])
	f= cdms2.open(filename)
	ctl_data=f('pobs')
	# We no need to calculate the regrid function on every itteration. So if we find the regrid function on one time we can use this for further
	if i == 0:	
		fcst_grib = gobj.getRainfallDataPartners(date = '2010-6-1', hour = 24, level = 'all',orginData = 0,datePriority = 'o',rainObject = obs,lat=(0,40),lon=(60,100))
		#print fcst_grib
		model_rain_grid= fcst_grib.getGrid()
		print 'Shape of model_grid_rain = ', model_rain_grid.shape
		ctl_grid=ctl_data.getGrid()
		print 'Shape of observed (forcast) grid=',ctl_grid.shape 
		  
		regridfunc_rain = Regridder(ctl_grid, model_rain_grid)	
		#
		# Regridding part
		#
	
		# Apply regridfunc_rain to rain data
	regridded_obs_rain = regridfunc_rain(ctl_data) 

	ncfilename = ctl_files[i].split('.')[0] + '_regridded.nc'
	ncfilename_path = '/home/dileep/rainfall_regrided/' + ncfilename 
	k=cdms2.open(ncfilename_path,'w')
	k.write(regridded_obs_rain)
	k.close()

	
