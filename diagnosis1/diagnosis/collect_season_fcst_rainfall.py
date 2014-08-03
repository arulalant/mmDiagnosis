"""
.. module:: collect_season_fcst_rainfall.py
   :synopsis: It should create the directories hierarchy structure. And
              It should get the partners data of observation rainfall data,
              i.e. model fcst rainfall data for 24, 48, etc hours which is set
              in the global configuration file. And store it as nc files,
              inside the appropriate directory.

Written by: Dileepkumar R
            JRF- IIT DELHI
Date: 23.06.2011

Updated By : Arulalan.T
Date: 14.09.2011
Date: 19.10.2011

"""

import os
import sys
import numpy
import cdms2
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__diagnosisDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__diagnosisDir__, '..'))
# adding the previous path to python path
sys.path.append(previousDir)
# import xml_data_acces.py from previous directory uv_cdat_code.diagnosisutils
import uv_cdat_code.diagnosisutils.xml_data_access as xml_data_access
from uv_cdat_code.diagnosisutils.timeutils import TimeUtility
from diag_setup.globalconfig import models, seasons, processfilesPath, obsrainfalls
from diag_setup.varsdict import variables
from diag_setup.gendir import createDirsIfNotExists
import diag_setup.netcdf_settings

# create time utility object
timobj = TimeUtility()


def createSeaonFcstRainfallData(modelname, modelpath, modelhour, rainfallPath,
                                                        rainfallXmlName=None):
    """
    :func:`createSeaonFcstRainfallData`: It should create model hours forecast
            rainfall data nc files, in side the 'StatiScore' directory of
            processfilesPath in hierarchy structure. The fcst rainfall
            timeAxis are in partners timeAxis w.r.t observation rainfall and
            fcst hours.

    """

    xmlobj = xml_data_access.GribXmlAccess(modelpath)
    # setting modlename to access the getRainfallDataPartners() method
    xmlobj.rainfallModel = modelname

    # generate the observation rainfall xml file path
    if rainfallXmlName:
        # If user set rainfallXmlName in the global config.txt settings
        rainfallXml = rainfallPath + '/' + rainfallXmlName
    else:
        # If user didnt set rainfallXmlName in the global config.txt settings
        # then it should takes default xml filename.
        rainfallXml = rainfallPath + '/' + 'rainfall_regrided.xml'
    # end of if rainfallXmlName:

    # get the obs variable name from the global variables, which
    # has set in the global 'vars.txt' file.
    obsRainfallXmlVar = variables.get(modelname).get('rain').obs_var
    fcstRainfallXmlVar = variables.get(modelname).get('rain').model_var

    obs = cdms2.open(rainfallXml)
    obs_rainfall = obs[obsRainfallXmlVar]

    # get the timeAxis of rainfall observation and correct its bounds
    obs_rainfall_time = timobj._correctTimeAxis(obs_rainfall.getTime())
    # get latAxis, lonAxis of rainfall observation
    obslat = obs_rainfall.getLatitude()
    obslon = obs_rainfall.getLongitude()
    # get the obs lat,lon to extract fcst data
    fcstlat = (min(obslat), max(obslat))
    fcstlon = (min(obslon), max(obslon))
    # get the fully available months
    availableMonths = timobj.getTimeAxisFullMonths(obs_rainfall_time)

    # create model, StatiScore directories if it is not exists
    statistical_score = createDirsIfNotExists(processfilesPath,
                                      [modelname, 'StatiScore'])

    for year in availableMonths.keys():
        months = availableMonths.get(year)
        year = str(year)
        # create year, Season directory if it is not exists
        statistical_season = createDirsIfNotExists(statistical_score,
                                                    [year, 'Season'])

        for seasonName, season in seasons.iteritems():
            # find out xml time axis months has the seasonal months or not
            seasonMonths = [(month, dates) for smonth in season \
                            for month, dates in months.iteritems() \
                            if smonth[:3].lower() == month[:3].lower()]
            if len(seasonMonths) == len(season):
                print "Got the seasonal months for %s season" % seasonName
            else:
                print "Seasonal months are not available for %s season" % seasonName
                continue
            if seasonName.isupper():
                seasonName = seasonName.lower()
            # create seasonName directory if it is not exists
            stati_seasonname = createDirsIfNotExists(statistical_season,
                                                              seasonName)
            # get the startdate, enddate of the whole season for model
            m_startdate = seasonMonths[0][1][0]
            m_enddate = seasonMonths[-1][1][1]

            for hr in modelhour:
                # create seasonName directory if it is not exists
                stati_hour = createDirsIfNotExists(stati_seasonname, hr)
                # get the partners data of observation rainfall
                # (i.e. get the model fcst rainfall)
                print "Collecting fcst rainfall data for % hr of %s season \
                     of %s of %s model" % (hr, seasonName, year, modelname)

                # generate the rainfall nc file name
                filename = fcstRainfallXmlVar + '_' + seasonName + '_' + year
                filename += '_' + modelname + '_' + hr + 'hr_fcst_rainfall.nc'
                rainfilepath = stati_hour + '/' + filename

                print "and Writing fcst rainfall data into ", rainfilepath
                # write the fcst_rain into nc appropriate file
                # fastup way
                # get the startdate, enddate of the season of fcst partner in model
                p_startdate = xmlobj.findPartners(Type = 'a',
                                    date = m_startdate, hour = hr)
                p_enddate = xmlobj.findPartners(Type = 'a',
                                    date = m_enddate, hour = hr)

                # generate the component time ranges of partners date
                modelDataTimeRange = timobj.tRange(p_startdate, p_enddate,
                                                              stepday = 1)

                f = cdms2.open(rainfilepath, 'w')
                for index in range(0, len(modelDataTimeRange)):
                    try:
                        # fastup way
                        # get the fcst partner data of appropriate date
                        fcst_rain = xmlobj.getData(var = fcstRainfallXmlVar, Type = 'f',
                                         date = (modelDataTimeRange[index], modelDataTimeRange[index]),
                                         hour = hr, level = 'all',
                                         lon = (60, 100, 'cob'), lat = (0., 40, 'cob'))#lat = fcstlat, lon = fcstlon)
                    except:
                        print "Couldn't get the fcst rainfall partner data \
                            w.r.t obs data date on", modelDataTimeRange[index]
                        print "So skipping it"
                        continue
                    # end of try:
                    if index == 0:
                        flat = fcst_rain.getLatitude()
                        flon = fcst_rain.getLongitude()
                        fstartdate = str(fcst_rain.getTime().asComponentTime()[0])
                        tunits = 'days since %s' %(str(fstartdate))
                        f = cdms2.open(rainfilepath, 'w')
                        print modelDataTimeRange[index]
                    else:
                        f = cdms2.open(rainfilepath, 'a+')
                    # end of if index == 0:
                    # creating the time axis for every day forecast partners.
                    # To set common time axis startdate of the var in the nc
                    # file, we have to create time axis like below.
                    ftime = cdms2.createAxis([index])
                    ftime.designateTime()
                    ftime.id = 'time'
                    ftime.units = tunits

                    

                    # Forcast data is in kg/m^2/day i.e mm/s but observed is mm/day,
                    # therefore we are going to change
                    # it into milimeter, since observed data is in millimeter
                    ####fcst_rain = fcst_rain*1

                    # Recreating the variable after make it as fully +ve
                    #fcst_rain = cdms2.createVariable(fcst_rain,
                    #                            axes = [ftime, flat, flon])

                    #fcst_rain.id = fcstRainfallXmlVar
                    if index == 0:
                        fcst_rain.comments = 'fcst rain for %s hour %s season\
                                  of %s model' % (hr, seasonName, modelname)
                    # write in to the file object on the same variable again
                    # and again but the time axis is differnt.
                    f.write(fcst_rain)
                    f.close()
                    # make free memory
                    del fcst_rain
                # end of for index in range(0, len(modelDataTimeRange)):
            # end of for hr in modelhour:
        # end of for seasonName, season in seasons.iteritems():
    # end of for year in availableMonths.keys():
# end of def createSeaonFcstRainfallData(modelname, modelpath, modelhour):

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
                if obsrainfall.regrid == 'yes':
                    # generate regridded obsrainfall directory w.r.t
                    # obsrainfall name in the
                    # processfilesPath, modelname, Regrid, ObsRain directory.
                    obsrainPath = os.path.join(processfilesPath,
                                                 model.name, 'Regrid',
                                           'ObsRain', obsrainfall.name)
                elif obsrainfall.regrid == 'no':
                    # user passed 'no' option. It means the obsrainfall.path
                    # obsrainfall data is w.r.t to model fcst data.
                    obsrainPath = obsrainfall.path
                else:
                    pass

                # calling the genFcstErrMeanAnlDirs function to do process
                createSeaonFcstRainfallData(model.name, model.path,
                                            model.hour, obsrainPath,
                                                     obsrainfall.xml)
            else:
                pass
                # obsrainfall configuration and model data configuration are not equal in the text file
                # handle this case, in diff manner. The same loop should works.
                # But need to check all the cases.
    print "Done! Creation of fcst rainfall netCdf Files"
# end of if __name__ == '__main__':
