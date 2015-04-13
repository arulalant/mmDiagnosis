"""
.. module:: compute_season_stati_score_spatial_distribution.py
    :synopsis: This programme is to calculate te various statistical scores
               corresponding to each lat-long location,(i.e spatially).

Example:
     Let 'TS'(Threat Score) is a statistical score,
     we are calculate this spatially.

Written by: Dileepkumar R
            JRF- IIT DELHI
Date: 02.09.2011;

Updated By : Arulalan.T
Date : 17.09.2011
Date : 06.10.2011

"""

import os
import sys
import numpy
import cdms2
import ctgfunction
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__diagnosisDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__diagnosisDir__, '..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diag_setup.varsdict import variables
from diag_setup.globalconfig import models, threshold, processfilesPath, \
                               obsrainfalls
import diag_setup.netcdf_settings
from datetime import datetime

def genStatisticalScorePath(modelname, modelhour, rainfallPath,
                                          rainfallXmlName=None):
    """
    :func:`genStatisticalScorePath`: It should make the existing path of
    process files statistical score. Also if that is correct path means, it
    should calls the function `genStatisticalScoreSpatialDistribution` to
    compute the statistical score in spatially distributed way.

    Inputs : modelname and modelhour are the part of the directory hierarchy
         structure.

    """

    procStatiPath = os.path.join(processfilesPath, modelname, 'StatiScore')
    statiYears = os.listdir(procStatiPath)
    for year in statiYears:
        statiPath = os.path.join(procStatiPath, year, 'Season')
        statiSeasons = os.listdir(statiPath)
        for season in statiSeasons:
            statiSeasonPath = os.path.join(statiPath, season)
            statiHr = os.path.join(statiSeasonPath, modelhour[0])
            fcstRainfall = [nc for nc in os.listdir(statiHr)
                            if nc.endswith('fcst_rainfall.nc')]
            if fcstRainfall:
                # this season hours has '*fcst_rainfall.nc'. So calling fn
                # if we passed lt, lon values, then we are shrinking the model
                # lat,lon while doing statistical score spatially distribution
                genStatisticalScoreSpatialDistribution(modelname, modelhour,
                                              season, year, statiSeasonPath,
                                              rainfallPath, rainfallXmlName),
                                              #lat = (0, 40), lon = (60, 100))
            else:
                print "%s directory doesn't have the file endswith \
            'fcst_rainfall.nc'. So skipping %s season" % (statiHr, season)
            # end of if fcstRainfall:
        # end of for season in statiSeasons:
    # end of for year in statiYears:
# end of def genStatisticalScorePath(modelname, modelhour):

def genStatisticalScoreSpatialDistribution(modelname, modelhour, season,
                                     year, statiSeasonPath, rainfallPath,
                                rainfallXmlName=None, lat=None, lon=None):
    """
    :func: `genStatisticalScoreSpatialDistribution` : It should compute the
        statistical scores like " Threat Score, Equitable Threat Score,
        Accuracy(Hit Rate), Bias Score, Probability Of Detection, Odds Ratio,
        False Alarm Rate, Probability Of False Detection, Kuipers Skill Score,
        Log Odd Ratio, Heidke Skill Score, Odd Ratio Skill Score, &
        Extreame Dependency Score" in spatially distributed way (i.e compute
        scores in each and every lat & lon points) by accessing the
        observation and forecast data.

    Inputs : modelname, modelhour, season, year are helps to generate the
             path. statiSeasonPath is the partial path of process statistical
             score season path.
             rainfallPath is the path of the observation rainfall.
             rainfallXmlName is the name of the xml file name, it is an
             optional one. By default it takes 'rainfall_regrided.xml'.
             lat, lon takes tuple args. If we passed it, then the model lat,
             lon should be shrinked according to the passed lat,lon.
             Some times it may helpful to do statistical score in spatially
             distributed in particular region among the global lat,lon.

    Outputs : It should store the computed statistical scores in spatially
              distributed way for all the modelhour(s) as nc files in the
              appropriate directory hierarchy structure.

    """

    Threshold = cdms2.createAxis(threshold)
    Threshold.id = 'threshold'

    # get the model and obs variable name from the global variables, which
    # has set in the global 'vars.txt' file.
    totalvars = variables.get(modelname)
    obsVar = totalvars.get('rain').obs_var
    fcstVar = totalvars.get('rain').model_var
    # generate the observation rainfall xml file path
    if rainfallXmlName:
        # If user set rainfallXmlName in the global config.txt settings
        ObsRainfall = rainfallPath + '/' + rainfallXmlName
    else:
        # If user didnt set rainfallXmlName in the global config.txt settings
        # then it should takes default xml filename.
        ObsRainfall = rainfallPath + '/' + 'rainfall_regrided.xml'

    obsfile = cdms2.open(ObsRainfall)
    # get lataxis, lonaxis of obs
    Lat = obsfile[obsVar].getLatitude()
    Lon = obsfile[obsVar].getLongitude()

    # Calculating lat & lon resolution(we are assuming that our grid is
    # uniform resolution)
    lat_model_resolution = Lat[:][1] - Lat[:][0]
    lon_model_resolution = Lon[:][1] - Lon[:][0]

    if lat and lon:
        # Assaining new lat & lon in 'newlat'& 'newlon'
        newlat = []
        newlon = []
        # The logic is substacting the our input region lat & lon from model/
        # lat lon array, then find the arg. of lest positive number in that list
        for ind in [0, 1]:
            latdiff = Lat-lat[ind]
            myarg_la = numpy.argwhere(latdiff >= 0)[0]
            print myarg_la
            newlat.append(Lat[myarg_la])

            londiff = Lon-lon[ind]
            myarg_lo = numpy.argwhere(londiff >= 0)[0]
            print myarg_lo
            newlon.append(Lon[myarg_lo])

        newlat=numpy.unique1d(numpy.array(newlat))
        newlon=numpy.unique1d(numpy.array(newlon))
        print "latitude shape before slice w.r.t arg lat", Lat.shape
        print "longitude shpe before slice w.r.t arg lon", Lon.shape
        # slicing the lat,lon with respect to argument lat,lon
        Lat = Lat[:]
        Lon = Lon[:]
        Lat = Lat.compress(Lat >= newlat[0])
        Lat = Lat.compress(Lat <= newlat[1])
        Lon = Lon.compress(Lon >= newlon[0])
        Lon = Lon.compress(Lon <= newlon[1])
        Lat = cdms2.createAxis(Lat)
        Lat.id = 'latitude'
        Lat.designateLatitude()
        Lon = cdms2.createAxis(Lon)
        Lon.id = 'longitude'
        Lon.designateLongitude()

        print "latitude shape after slice w.r.t arg lat", Lat.shape
        print "longitude shpe after slice w.r.t arg lon", Lon.shape
        print "\naccoring to the new shape the statistical score spatially \
               distribution takes place\n"
    # end of if lat and lon:

    print "The model latitude resolution is ", lat_model_resolution
    print "The model longitude resolution is ", lon_model_resolution
    print "Depence on the lat lon resolution this computational time will be\
           increase to find out the statistical score in spatially \
           distributed way"

    latlen = len(Lat)
    lonlen = len(Lon)
    thlen = len(threshold)

    print "Started to compute statistical spatially distributed at", str(datetime.now())

    # get the obs data.
    obs = obsfile(obsVar)

    for i in range(len(modelhour)):
        statihour = os.path.join(statiSeasonPath, modelhour[i])
        fcstRainfall = [nc for nc in os.listdir(statihour)
                        if nc.endswith('fcst_rainfall.nc')]
        if fcstRainfall:
            fcstRainfall = statihour +'/' + fcstRainfall[0]
        else:
            print "%s directory doesn't have the file endswith \
            'fcst_rainfall.nc'. So skipping %s hour " % (statihour, modelhour[i])
            continue
        # end of if fcstRainfall:
        fcstfile = cdms2.open(fcstRainfall)

        stati_ncfile = 'stati_spatial_distribution_score''_%shr_%s_%s_%s.nc' \
                                     % (modelhour[i], season, year, modelname)
        print "Calculating statistical score in spatially distributed way \
               for %s hour of %s season %s %s model" % (modelhour[i],
                                                    season, year, modelname)
        # creating dummy numpy array to store the scores
        dummy = numpy.zeros((thlen, latlen, lonlen), dtype = numpy.float32)
        TS_list = dummy.copy()
        ETS_list = dummy.copy()
        HR_list = dummy.copy()
        BS_list = dummy.copy()
        POD_list = dummy.copy()
        FAR_list = dummy.copy()
        POFD_list = dummy.copy()
        KSS_list = dummy.copy()
        HSS_list = dummy.copy()
        ODR_list = dummy.copy()
        LODR_list = dummy.copy()
        ORSS_list = dummy.copy()
        EDS_list = dummy.copy()
        # make free memory
        del dummy

        # get the fcst data.
        fcst = fcstfile(fcstVar)
        fcst_lat = fcst.getLatitude()
        fcst_lon = fcst.getLongitude()
        fcst_time = fcst.getTime()
        # convert fcst data, by replacing -ve into 0 values if
        # present. We are replacing all negative value to 0, by
        # giving the condition as 'fcst>0' for replacing
        # negative value by '0'----Why?---->{We are givig all
        # value as 0 if it is 'false', if we give condition as
        # 'fcst<0' then all values which are 'false' replaced
        # by '0' thats why we givig the condition as
        # 'fcst>0'}
        fcst = numpy.ma.where(fcst > 0, fcst, 0)

        fcst = cdms2.createVariable(fcst)
        fcst.setAxisList([fcst_time, fcst_lat, fcst_lon])


        print "%s modelhour spatially statistical started at %s\n" % (modelhour[i], str(datetime.now()))
        for j in range(latlen):
            for k in range(lonlen):
#                # get the obs data.
#                obsData = obsfile(obsVar, latitude = Lat[j],
#                                  longitude = Lon[k], squeeze = 1)
#                obs = numpy.array(obsData)
#                # make free memory
#                del obsData

#                # get the fcst data.
#                fcstData = fcstfile(fcstVar, latitude = Lat[j],
#                                  longitude = Lon[k], squeeze = 1)
#                fcst = numpy.array(fcstData)
#                # make free memory
#                del fcstData
                OBS = obs(latitude = Lat[j], longitude = Lon[k], squeeze = 1)
                OBS = numpy.array(OBS)
                FCST = fcst(latitude = Lat[j], longitude = Lon[k], squeeze = 1)
                FCST = numpy.array(FCST)
                for ths in range(thlen):
                    th = threshold[ths]
                    #----CONTIGENCY TABLE----#
                    ctgTable = ctgfunction.contingency_table_2x2(OBS, FCST, th)
                    #----BIAS SCORE----#
                    BS = ctgfunction.bias_score(ctg_table = ctgTable)
                    BS_list[ths, j, k] = BS
                    #-----ODDS RATIO------#
                    ODR = ctgfunction.odr(ctg_table = ctgTable)
                    ODR_list[ths, j, k] = ODR
                    #-----LOG ODD RATIO----#
                    LODR = ctgfunction.logodr(ctg_table = ctgTable)
                    LODR_list[ths, j, k] = LODR
                    #-----EXTREAME DEPENDENCY SCORE----#
                    EDS = ctgfunction.eds(ctg_table = ctgTable)
                    EDS_list[ths, j, k] = EDS
                    #----THREAT SCORE------#
                    threat_score = ctgfunction.ts(ctg_table = ctgTable)
                    TS_list[ths, j, k] = threat_score
                    #----EQUITABLE THREAT SCORE------#
                    ETS = ctgfunction.ets(ctg_table = ctgTable)
                    ETS_list[ths, j, k] = ETS
                    #----ACCURACY(HIT RATE)------#
                    Accuracy = ctgfunction.accuracy(ctg_table = ctgTable)
                    HR_list[ths, j, k] = Accuracy
                    #-----PROBABILITY OF DETECTION------#
                    POD = ctgfunction.pod(ctg_table = ctgTable)
                    POD_list[ths, j, k] = POD
                    #-----FALSE ALARM RATE--------#
                    FAR = ctgfunction.far(ctg_table = ctgTable)
                    FAR_list[ths, j, k] = FAR
                    #-----PROBABILITY OF FALSE DETECTION----#
                    POFD = ctgfunction.pofd(ctg_table = ctgTable)
                    POFD_list[ths, j, k] = POFD
                    #-----KUIPERS SKILL SCORE----#
                    KSS = ctgfunction.kss(ctg_table = ctgTable)
                    KSS_list[ths, j, k] = KSS
                    #-----HEIDKE SKILL SCORE-----#
                    HSS = ctgfunction.hss(ctg_table = ctgTable)
                    HSS_list[ths, j, k] = HSS
                    #-----ODD RATIO SKILL SCORE-----#
                    ORSS = ctgfunction.orss(ctg_table = ctgTable)
                    ORSS_list[ths, j, k] = ORSS
                # end of for ths in xrange(thlen):
                # make free memory
                del OBS, FCST, th
            # end of for k in range(lonlen):
        # end of for j in range(latlen):
        # make memory free
        del fcst

        print "%s modelhour spatially statistical ended at %s \n" % (modelhour[i], str(datetime.now()))
        print "Storing the computed scores variables into nc file\n"
        # open the nc file to write region wise statistical score
        F_nc = cdms2.open(statihour +'/' + stati_ncfile, 'w')

        # Threat Score Variable
        TS = cdms2.createVariable(TS_list)
        TS.id = 'ts'
        TS.long_name = 'Threat Score'
        TS.setAxisList([Threshold, Lat, Lon])
        # write this variables into nc file
        F_nc.write(TS)
        # make free memory
        del TS_list, TS

        # Equitable Threat Score Variable
        ETS = cdms2.createVariable(ETS_list)
        ETS.id = 'ets'
        ETS.long_name = 'Equitable Threat Score'
        ETS.setAxisList([Threshold, Lat, Lon])
        # write this variables into nc file
        F_nc.write(ETS)
        # make free memory
        del ETS_list, ETS

        # Hit Rate Variable
        HR = cdms2.createVariable(HR_list)
        HR.id = 'hr'
        HR.long_name = 'Hit Rate'
        HR.setAxisList([Threshold, Lat, Lon])
        # write this variables into nc file
        F_nc.write(HR)
        # make free memory
        del HR_list, HR

        # Bias Score Variable
        BS = cdms2.createVariable(BS_list)
        BS.id = 'bs'
        BS.long_name = 'Bias Score'
        BS.setAxisList([Threshold, Lat, Lon])
        # write this variables into nc file
        F_nc.write(BS)
        # make free memory
        del BS_list, BS

        # Probability of Detectio Variable
        POD = cdms2.createVariable(POD_list)
        POD.id = 'pod'
        POD.long_name = 'Probability Of Detection'
        POD.setAxisList([Threshold, Lat, Lon])
        # write this variables into nc file
        F_nc.write(POD)
        # make free memory
        del POD_list, POD

        # False Alarm Rate Variable
        FAR = cdms2.createVariable(FAR_list)
        FAR.id = 'far'
        FAR.long_name = 'False Alarm Rate'
        FAR.setAxisList([Threshold, Lat, Lon])
        # write this variables into nc file
        F_nc.write(FAR)
        # make free memory
        del FAR_list, FAR

        # Probability of False Detection Variable
        POFD = cdms2.createVariable(POFD_list)
        POFD.id = 'pofd'
        POFD.long_name = 'Probability of False Detection'
        POFD.setAxisList([Threshold, Lat, Lon])
        # write this variables into nc file
        F_nc.write(POFD)
        # make free memory
        del POFD_list, POFD

        # Kuipers Skill Score Variable
        KSS = cdms2.createVariable(KSS_list)
        KSS.id = 'kss'
        KSS.long_name = 'Kuipers Skill Score'
        KSS.setAxisList([Threshold, Lat, Lon])
        # write this variables into nc file
        F_nc.write(KSS)
        # make free memory
        del KSS_list, KSS

        # Heidke Skill Score Variable
        HSS = cdms2.createVariable(HSS_list)
        HSS.id = 'hss'
        HSS.long_name = 'Heidke Skill Score'
        HSS.setAxisList([Threshold, Lat, Lon])
        # write this variables into nc file
        F_nc.write(HSS)
        # make free memory
        del HSS_list, HSS

        # Odds Ratio Variable
        ODR = cdms2.createVariable(ODR_list)
        ODR.id = 'odr'
        ODR.long_name = 'Odds Ratio'
        ODR.setAxisList([Threshold, Lat, Lon])
        # write this variables into nc file
        F_nc.write(ODR)
        # make free memory
        del ODR_list, ODR

        # Log Odd Ratio Variable
        LODR = cdms2.createVariable(LODR_list)
        LODR.id = 'lodr'
        LODR.long_name = 'Log Odd Ratio'
        LODR.setAxisList([Threshold, Lat, Lon])
        # write this variables into nc file
        F_nc.write(LODR)
        # make free memory
        del LODR_list, LODR

        # Odds Ratio Skill Score Variable
        ORSS = cdms2.createVariable(ORSS_list)
        ORSS.id = 'orss'
        ORSS.long_name = 'Odds Ratio Skill Score'
        ORSS.setAxisList([Threshold, Lat, Lon])
        # write this variables into nc file
        F_nc.write(ORSS)
        # make free memory
        del ORSS_list, ORSS

        # Extreame Dependency Score Variable
        EDS = cdms2.createVariable(EDS_list)
        EDS.id = 'eds'
        EDS.long_name = 'Extreame Dependency Score'
        EDS.setAxisList([Threshold, Lat, Lon])
        # write this variables into nc file
        F_nc.write(EDS)
        # make free memory
        del EDS_list, EDS

        # close nc file
        F_nc.close()
        print "Wrinting spatially distributed statistical score in %s/%s" % \
                                        (statihour, stati_ncfile)
    # end of for i in range(len(modelhour)):
    # make memory free
    del obs
# end of def genStatisticalScoreSpatialDistribution(...):

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

                # calling the genStatisticalScoreDirs function to do process
                genStatisticalScorePath(model.name, model.hour,
                                        obsrainPath, obsrainfall.xml)
            else:
                pass
                # obsrainfall configuration and model data configuration are not equal in the text file
                # handle this case, in diff manner. The same loop should works.
                # But need to check all the cases.
    print "Done! Creation of Statistical scores spatially distribution netCdf Files"
# end of if __name__ == '__main__':
