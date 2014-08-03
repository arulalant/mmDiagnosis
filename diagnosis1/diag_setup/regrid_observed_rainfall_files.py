"""
.. module::
    :synopsis: This programe is for regridding the observed rainfall data
               w.r.t forcast rainfall data. Since Observed and forcasted
               rainfall data are not in the same grid resolution.

    Example: In NCMRWF data observed data is 1x1 degree resolution, but our
             forecasted data is 0.5x0.5 degree resolution, therefore we regrid
             the observed data according to forecasted data for calcuating
             statistical score and other purposes.

    ..note:: Also we change the -ve data of obs into zero if it presents

Written by: Dileepkumar R
            JRF- IIT DELHI

Date: 23.06.2011

Updated By: Arulalan.T
Date : 14.09.2011

"""

import os
import sys
import numpy
import cdms2
from regrid2 import Regridder
from varsdict import variables
from globalconfig import models, obsrainfalls, processfilesPath
import netcdf_settings
from gendir import createDirsIfNotExists
# getting the absolute path of the previous directory
previousDir = os.path.abspath(os.path.join(os.getcwd(), '..'))
# adding the previous path to python path
sys.path.append(previousDir)
# import xml_data_acces.py from previous directory uv_cdat_code.diagnosisutils
import uv_cdat_code.diagnosisutils.xml_data_access as xml_data_access


def createRegridedRainfallObservation(modelname, modelPath,
                                    rainfallOriginalPath, rainfallRegridPath,
                                    rainfallXmlName=None):
    """
    :func:`createRegridedRainfallObservation` : creating the regridded
            rainfall observation data w.r.t its model forecast rainfall data
            grid resolution. Also it should create xml file by using cdscan
            in the rainfallregridpath which is set in the global config file.

    """
    # Reading observed rainfall data.
    xmlobj = xml_data_access.GribXmlAccess(modelPath)
    # setting modelname in xmlobj to access the fcst rainfall data by get
    # its variable name form the 'vars.txt'
    xmlobj.rainfallModel = modelname
    # Collecting the name of files & directories
    l = os.listdir(rainfallOriginalPath)
    #'ctl_files' are list of filenames ends with '.ctl'
    ctl_files=[i for i in l if i.endswith('.ctl')]
    # get the observed rainfall variable name from the global vars.txt file
    rvar = variables.get(modelname).get('rain').obs_var
    for i in xrange(len(ctl_files)):

        filename = rainfallOriginalPath + '/' + ctl_files[i]
        f = cdms2.open(filename)
        # get the observation rainfall data
        obs_rain_orginal = f(rvar)

        # We no need to calculate the regrid function on every itteration.
        # So if we find the regrid function on one time, then we can use
        # this function for further
        if i == 0:
            obslat = obs_rain_orginal.getLatitude()[:]
            obslon = obs_rain_orginal.getLongitude()[:]
            # get the obs lat,lon to extract fcst data
            fcstlat = (min(obslat), max(obslat))
            fcstlon = (min(obslon), max(obslon))
            rdate = obs_rain_orginal.getTime().asComponentTime()[0]
            # get the fcst rainfall data
            fcst_rain = xmlobj.getRainfallDataPartners(date = rdate,
                hour = 24, level = 'all', orginData = 0, datePriority = 'o',
                lat = fcstlat, lon = fcstlon)

            model_rain_grid = fcst_rain.getGrid()
            print 'Shape of model(forecast) rainfall grid = ', model_rain_grid.shape
            obs_rain_grid = obs_rain_orginal.getGrid()
            print 'Shape of observed rainfall grid = ', obs_rain_grid.shape
            # create regrid function
            regridfunc_rain = Regridder(obs_rain_grid, model_rain_grid)
        # end of if i == 0:
        #
        # Regridding part
        #
        # Apply regridfunc_rain to observed rain data
        obs_rain_regridded = regridfunc_rain(obs_rain_orginal)

        ### convert obs data, by replacing -ve into 0 values if present ###
        obs_masked = numpy.ma.array(obs_rain_regridded)

        # We are replacing all negative value  to 0
        # We are giving the condition as 'obs_masked>0' for replacing negative
        # value by '0'----Why?---->{We are givig all value as 0 if it is
        # 'false', if we give condition as 'obs_masked<0' then the all value
        # which are 'false' replaced by '0' thats why we givig the condition
        # as 'obs_masked>0'}
        obs_masked = numpy.ma.where(obs_masked>0, obs_masked, 0)
        obsPData = numpy.array(obs_masked)
        obsPData = cdms2.createVariable(obsPData,
                                        axes = [obs_rain_regridded.getTime(),
                                        obs_rain_regridded.getLatitude(),
                                        obs_rain_regridded.getLongitude()])
        obsPData.id = rvar
        # make free memory
        del obs_masked, obs_rain_regridded
        # save into nc file
        regridfilename = ctl_files[i].split('.nc')[0] + '_regridded.nc'
        f1 = cdms2.open(rainfallRegridPath + '/' + regridfilename, 'w')
        f1.write(obsPData)
        f1.close()
        f.close()
    # end of for i in xrange(len(ctl_files)):
    presentDir = os.getcwd()
    os.chdir(rainfallRegridPath)

    if not rainfallXmlName:
        # setting default rainfall_regrided.xml name, if user didnt set in the
        # global configure.txt file.
        rainfallXmlName = 'rainfall_regrided.xml'
    # creating xml file for fcstsyserr with levels option
    result = os.system('/opt/uv-cdat/bin//cdscan -x %s *.nc' % rainfallXmlName)
    if not result:
        print "Successfully created XML file '%s' in the path %s using cdscan" % (rainfallXmlName, rainfallRegridPath)
    else:
        print "Problem while creating XML file '%s' in the path %s using cdscan" % (rainfallXmlName, rainfallRegridPath)
    os.chdir(presentDir)
# end of def createRegriddedRainfallObservation(...):

if __name__ == '__main__':

    if len(models) == len(obsrainfalls) == 1:
        print "Obtained one model and one obsrainfall "
    elif len(models) == len(obsrainfalls):
        print "Obtained %d models and obsrainfalls" % len(models)
    else:
        print "Obtained %d models and %d obsrainfalls" % (len(models), len(obsrainfalls))

    for model in models:
        for obsrainfall in obsrainfalls:
            if model.count == obsrainfall.count:
                # creating obsrainfall directory w.r.t obsrainfall name in the
                # processfilesPath, modelname, Regrid, ObsRain directory.
                obsrainRegridPath = createDirsIfNotExists(processfilesPath,
                                          [model.name, 'Regrid', 'ObsRain',
                                                         obsrainfall.name])
                if obsrainfall.regrid == 'yes':
                    # calling the obsrainfall regrid function to do process
                    createRegridedRainfallObservation(model.name, model.path,
                                         obsrainfall.path, obsrainRegridPath,
                                         obsrainfall.xml)
                else:
                    print "Skipping regrid observation rainfall, since \
                            regrid has set as 'no' in the configure.txt file \
                            for obsrain name is %s and its count is %s" \
                                % (obsrainfall.name, obsrainfall.count)
            else:
                pass
                # obsrainfall configuration and model data configuration are not equal in the text file
                # handle this case, in diff manner. The same loop should works.
                # But need to check all the cases.
# end of if __name__ == '__main__':
