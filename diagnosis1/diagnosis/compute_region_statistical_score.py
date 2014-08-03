"""
.. module:: compute_region_statistical_score.py
    :synopsis: This module is to calculate the various statistical score
               corresponding to various regions.

Example:
    Let 'ts'(Threat Score) is a statistical score,
    we are calculate this for different regions.

Written by: Dileepkumar R
           JRF- IIT DELHI
Date: 02.08.2011;

Updated By : Arulalan.T
Date : 16.09.2011

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
# import timeutils.py from previous directory uv_cdat_code.diagnosisutils
from uv_cdat_code.diagnosisutils.timeutils import TimeUtility
from uv_cdat_code.diagnosisutils.regions import regions
from diag_setup.varsdict import variables
from diag_setup.globalconfig import models, seasons, threshold, region, \
                               processfilesPath, obsrainfalls, plotsgraphsPath
from diag_setup.gendir import createDirsIfNotExists
import diag_setup.netcdf_settings

# create time utility object
timobj = TimeUtility()


def genStatisticalScoreDirs(modelname, modelhour, rainfallPath,
                                          rainfallXmlName=None):
    """
    :func: `genStatisticalScoreDirs` : It should generate the appropriate
        directory hierarchy structure for 'StatiScore' in both the processfiles
        path and plotgraph path. In plotgraph path, it should create 'CSV'
        directory to store the 'statistical scores' in csv file formate.

        This function should call the `genStatisticalScore` function to
        compute and statistical score.

    Inputs : modelname and modelhour are the part of the directory hierarchy
             structure.
             rainfallPath is the path of the observation rainfall.
             rainfallXmlName is the name of the xml file name.

    """

    procStatiPath = os.path.join(processfilesPath, modelname, 'StatiScore')
    # create model, StatiScore directories in plotsgraphsPath if it is not exists
    plotStati = createDirsIfNotExists(plotsgraphsPath, [modelname, 'StatiScore'])

    years = os.listdir(procStatiPath)
    for year in years:
        # create year, Season directories in plotsgraphsPath if it is not exists
        plotSeason = createDirsIfNotExists(plotStati, [year, 'Season'])
        procStatisSeasonPath = os.path.join(procStatiPath, year, 'Season')
        seasonNames = os.listdir(procStatisSeasonPath)
        for season in seasonNames:
            procStatiSeason = os.path.join(procStatisSeasonPath, season)
            # checking process begins that is this having fcst_rainfall file
            statihour = os.path.join(procStatiSeason, modelhour[0])
            fcst_rain_file = [ncfile for ncfile in os.listdir(statihour) \
                                 if ncfile.endswith('fcst_rainfall.nc')]

            if fcst_rain_file:
                fcst_rain_file = fcst_rain_file[0]
                # create SeasonName, CSV directories in plotsgraphsPath
                # if it is not exists
                plotCSV = createDirsIfNotExists(plotSeason, [season, 'CSV'])
                # create Region directory in processfiles if it is not exists
                procRegion = createDirsIfNotExists(procStatiSeason, 'Region')
                # calling function to create statistical scores
                genStatisticalScore(modelname, modelhour, season, year,
                                     procStatiSeason, procRegion, plotCSV,
                                     rainfallPath, rainfallXmlName)
            else:
                # this season directory does not has the fcst_rainfall files
                # so not calling the function to create statistical score
                pass
            # end of if fcst_rain_file:
        # end of for season in seasonNames:
    # end of for year in years:
# end of def genStatisticalScoreDirs(modelname, modelhour):

def genStatisticalScore(modelname, modelhour, seasonName, year,
                               procStatiSeason, procRegion, plotCSV,
                                 rainfallPath, rainfallXmlName=None):
    """
    :func:`genStatisticalScore` : It should compute the statistical scores
        like " Threat Score, Equitable Threat Score, Accuracy(Hit Rate),
        Bias Score, Probability Of Detection, False Alarm Rate, Odds Ratio,
        Probability Of False Detection, Kuipers Skill Score, Log Odd Ratio,
        Heidke Skill Score, Odd Ratio Skill Score, & Extreame Dependency Score"
        by accessing the observation and forecast data.

        It should compute the statistical scores for different regions.

        Finally it should store the scores variable in both csv and nc files
        in appropriate directory hierarchy structure.

        ..note:: We are replacing the -ve values with zeros of both the
                 observation and fcst data to make correct statistical scores.

    Inputs : modelname, modelhour, seasonName, year are helps to generate the
             path. procStatiSeason is the partial path of process statistical
             score season path.
             procRegion is an absolute path to store the nc files
             plotCSV is an absolute path to store the csv files.
             rainfallPath is the path of the observation rainfall.
             rainfallXmlName is the name of the xml file name, it is an
             optional one. By default it takes 'rainfall_regrided.xml'

    Outputs : It should store the computed statistical scores for all the
              regions and store it as both ncfile and csv files in the
              appropriate directory hierarchy structure.

    """

    global threshold
    # correct modelhour and threshold
    mhour = [int(hr) for hr in modelhour]

    Threshold = cdms2.createAxis(threshold, id = 'threshold')
    Forcast_hrs = cdms2.createAxis(mhour, id = 'fcsthour')
    hourlen, thlen = len(modelhour), len(threshold)
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
    obsData = obsfile[obsVar]
    # get the timeAxis of rainfall observation and correct its bounds
    obs_rainfall_time = timobj._correctTimeAxis(obsData.getTime())
    # get the fully available months
    availableMonths = timobj.getTimeAxisFullMonths(obs_rainfall_time)
    months = availableMonths.get(int(year))
    dataTimeRange = None
    for name, season in seasons.iteritems():
        # find out xml time axis months has the seasonal months or not
        seasonMonths = [(month, dates) for smonth in season \
                        for month, dates in months.iteritems() \
                        if smonth[:3].lower() == month[:3].lower()]
        if len(seasonMonths) == len(season):
            print "Got the seasonal months for %s season" % name
        else:
            print "Seasonal months are not available for %s season" % name
            continue

        # get the startdate, enddate of the whole season for model
        startdate = seasonMonths[0][1][0]
        enddate = seasonMonths[-1][1][1]
        dataTimeRange = (startdate, enddate)
    # for name, season in seasons.iteritems():
    if not dataTimeRange:
        raise ValueError("Doesn't match observation rainfall timeAxis months\
            %s with seasonal months %s. So couldn't do statistical process" %
                                  (str(months.keys()), str(seasons.keys())))

    # get the obs data
    obsData = obsfile(obsVar, time = dataTimeRange)

    obsfile.close()
    obsMask = numpy.ma.array(obsData)
    # get timeaxis, lataxis, lonaxis of obs
    time = obsData.getTime()
    lat = obsData.getLatitude()
    lon = obsData.getLongitude()
    # make free memory
    del obsData
    # We are replacing all negative value by '0'. We are giving the
    # condition as 'obsMask > 0' for replacing negative value by '0'.
    # ----Why?---->{ We are givig all value as 0 if it is 'false',
    # if we give condition as 'obsMask < 0' then all the value which are
    # 'false' replaced by '0' thats why we giving the condition as
    # 'obsMask > 0' }
    obsMasked = numpy.ma.where(obsMask > 0, obsMask, 0)
    obsMasked = numpy.array(obsMasked)
    # Now we have the data is masked array variable, for applying
    # 'sub region' (region extraction) command we have to change this
    # into cdms2 variable, for that we have to set the axis again.
    obs_rainfall = cdms2.createVariable(obsMasked, axes = [time, lat, lon])

    for regionName in region:
        if not regionName in regions.keys():
            raise ValueError('region %s is not present in the predefined \
                      regions. Unable to do statistical score' % regionName)

        # 'csvfile' is the file name of '.csv' file,
        # in which we are writing statistical score in this file
        csvfile = 'statistical_score_%s_%s_%s_%s.csv' % (regionName,
                                               seasonName, year, modelname)
        # open the csv file to write statistical scores
        F = open(plotCSV + '/' + csvfile, 'w')
        heading = 'Region' + ','+ 'Th' + ',' + 'Fcst_Hrs' + ',' + 'TS' + ','
        heading += 'ETS' + ',' + 'HR' + ',' + 'BS' + ',' + 'POD' + ',' + 'FAR'
        heading += ',' + 'POFD' + ',' + 'KSS' + ',' + 'HSS' + ',' + 'Odd Ratio'
        heading += ',' + 'LOR' + ',' + 'ORSS' + ',' + 'EDS' + '\n'
        F.writelines(heading)

        # 'stati_ncfile' is the file name of 'netcdf' file, in which we are
        # writing statistical score
        stati_ncfile = 'statistical_score_%s_%s_%s_%s.nc' % (regionName,
                                                 seasonName, year, modelname)
        # open the nc file to write region wise statistical score
        F_nc = cdms2.open(procRegion + '/' + stati_ncfile, 'w')
        # creating dummy numpy array to store the scores
        dummy = numpy.zeros((hourlen, thlen), float)
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

        # get the region variable from the predefined regions
        extractRegion = regions.get(regionName)
        # do region extraction
        obs = obs_rainfall(extractRegion)
        obs = numpy.array(obs)

        for i in range(hourlen):
            print "Calculating statistical score for %s region %s hour" % \
                                                (regionName, modelhour[i])
            proStatiHour = os.path.join(procStatiSeason, modelhour[i])
            fcst_rain_file = [ncfile for ncfile in os.listdir(proStatiHour) \
                                 if ncfile.endswith('fcst_rainfall.nc')]
            if fcst_rain_file:
                fcst_rain_file = fcst_rain_file[0]
            else:
                print "Coundn't get the *fcst_rainfall.nc file in the %s \
                        path. So skipping statistical for %s \
                        hour " % (proStatiHour, modelhour[i])
                continue
            # end of if fcst_rain_file:

            # generate the forecast rainfall nc file path
            fcstRainfall = proStatiHour + '/' + fcst_rain_file
            fcstfile = cdms2.open(fcstRainfall)
            print fcstfile
            # get the fcst data. Here we no need to pass time, since it as
            # already return for timeaxis (partners data time range)
            fcst = fcstfile(fcstVar)
            fcstfile.close()
            # do region extraction
            fcst = fcst(extractRegion)
            # convert fcst data, by replacing -ve into 0 values if
            # present. We are replacing all negative value to 0, by
            # giving the condition as 'fcst>0' for replacing
            # negative value by '0'----Why?---->{We are givig all
            # value as 0 if it is 'false', if we give condition as
            # 'fcst<0' then all values which are 'false' replaced
            # by '0' thats why we givig the condition as
            # 'fcst>0'}
            fcst = numpy.ma.where(fcst > 0, fcst, 0)

            fcst = numpy.array(fcst)
            if obs.shape != fcst.shape:
                print "The shape of observation rainfall %s and fcst rainfall\
                        %s are mismatch. So skipping statistical score for %s\
                        hour " % (obs.shape, fcst.shape, modelhour[i])
                continue
            for j in range(thlen):
                th = threshold[j]
                #----CONTIGENCY TABLE----#
                ctgTable = ctgfunction.contingency_table_2x2(obs, fcst, th)
                print ctgTable
                #----THREAT SCORE------#
                threat_score = ctgfunction.ts(ctg_table = ctgTable)
                TS_list[i, j] = threat_score
                #----EQUITABLE THREAT SCORE------#
                ETS = ctgfunction.ets(ctg_table = ctgTable)
                ETS_list[i, j] = ETS
                #----ACCURACY(HIT RATE)------#
                Accuracy = ctgfunction.accuracy(ctg_table = ctgTable)
                HR_list[i, j] = Accuracy
                #----BIAS SCORE----#
                Bias = ctgfunction.bias_score(ctg_table = ctgTable)
                BS_list[i, j] = Bias
                #-----PROBABILITY OF DETECTION------#
                POD = ctgfunction.pod(ctg_table = ctgTable)
                POD_list[i, j] = POD
                #-----FALSE ALARM RATE--------#
                FAR = ctgfunction.far(ctg_table = ctgTable)
                FAR_list[i, j] = FAR
                #-----PROBABILITY OF FALSE DETECTION----#
                POFD = ctgfunction.pofd(ctg_table = ctgTable)
                POFD_list[i, j] = POFD
                #-----KUIPERS SKILL SCORE----#
                KSS = ctgfunction.kss(ctg_table = ctgTable)
                KSS_list[i, j] = KSS
                #-----HEIDKE SKILL SCORE-----#
                HSS = ctgfunction.hss(ctg_table = ctgTable)
                HSS_list[i, j] = HSS
                #-----ODDS RATIO------#
                ODR = ctgfunction.odr(ctg_table = ctgTable)
                ODR_list[i, j] = ODR
                #-----LOG ODD RATIO----#
                LODR = ctgfunction.logodr(ctg_table = ctgTable)
                LODR_list[i, j] = LODR
                #-----ODD RATIO SKILL SCORE-----#
                ORSS = ctgfunction.orss(ctg_table = ctgTable)
                ORSS_list[i, j] = ORSS
                #-----EXTREAME DEPENDENCY SCORE----#
                EDS = ctgfunction.eds(ctg_table = ctgTable)
                EDS_list[i, j] = EDS

                # We save as coma separated variable values(csv)
                line = regionName + ',' + str(threshold[j]) + ','
                line += str(modelhour[i]) + ',' + str(threat_score) + ','
                line += str(ETS) + ',' + str(Accuracy) + ',' + str(Bias) + ','
                line += str(POD) + ',' + str(FAR) + ',' + str(POFD) + ','
                line += str(KSS) + ',' + str(HSS) + ',' + str(ODR) + ','
                line += str(LODR) + ',' + str(ORSS) + ',' + str(EDS) + '\n'
                F.write(line)
                # end of for j in range(len(threshold)):
            #end of for i in range(len(modelhour)):
        # Writing the various statistical score into netcdf file
        F.close()
        print "Writing statistical score for %s in %s/%s file" % (regionName,
                                                     procRegion, stati_ncfile)
        # comment info for all variables
        commentline = "'%s' model statistical score '%s' region '%s' season of %s" \
                                % (modelname, regionName, seasonName, year)
        # Threat Score
        TS = cdms2.createVariable(TS_list)
        TS.id = 'ts'
        TS.long_name = 'Threat Score'
        TS.setAxisList([Forcast_hrs, Threshold])
        TS.comments = commentline
        # write this variables into nc file
        F_nc.write(TS)
        # make free memory
        del TS_list, TS

        # Equitable Threat Score
        ETS = cdms2.createVariable(ETS_list)
        ETS.id = 'ets'
        ETS.long_name = 'Equitable Threat Score'
        ETS.setAxisList([Forcast_hrs, Threshold])
        ETS.comments = commentline
        # write this variables into nc file
        F_nc.write(ETS)
        # make free memory
        del ETS_list, ETS

        # Hit Rate
        HR = cdms2.createVariable(HR_list)
        HR.id = 'hr'
        HR.long_name = 'Hit Rate'
        HR.setAxisList([Forcast_hrs, Threshold])
        HR.comments = commentline
        # write this variables into nc file
        F_nc.write(HR)
        # make free memory
        del HR_list, HR

        # Bias Score
        BS = cdms2.createVariable(BS_list)
        BS.id = 'bs'
        BS.long_name = 'Bias Score'
        BS.setAxisList([Forcast_hrs, Threshold])
        BS.comments = commentline
        # write this variables into nc file
        F_nc.write(BS)
        # make free memory
        del BS_list, BS

        # Probability of Detectio
        POD = cdms2.createVariable(POD_list)
        POD.id ='pod'
        POD.long_name = 'Probability of Detection'
        POD.setAxisList([Forcast_hrs, Threshold])
        POD.comments = commentline
        # write this variables into nc file
        F_nc.write(POD)
        # make free memory
        del POD_list, POD

        # False Alarm Rate
        FAR = cdms2.createVariable(FAR_list)
        FAR.id = 'far'
        FAR.long_name = 'False Alarm Rate'
        FAR.setAxisList([Forcast_hrs, Threshold])
        FAR.comments = commentline
        # write this variables into nc file
        F_nc.write(FAR)
        # make free memory
        del FAR_list, FAR

        # Probability of False Detection
        POFD = cdms2.createVariable(POFD_list)
        POFD.id = 'pofd'
        POFD.long_name = 'Probability of False Detection'
        POFD.setAxisList([Forcast_hrs, Threshold])
        POFD.comments = commentline
        # write this variables into nc file
        F_nc.write(POFD)
        # make free memory
        del POFD_list, POFD

        # Kuipers Skill Score
        KSS = cdms2.createVariable(KSS_list)
        KSS.id = 'kss'
        KSS.long_name = 'Kuipers Skill Score'
        KSS.setAxisList([Forcast_hrs, Threshold])
        KSS.comments = commentline
        # write this variables into nc file
        F_nc.write(KSS)
        # make free memory
        del KSS_list, KSS

        # Heidke Skill Score
        HSS = cdms2.createVariable(HSS_list)
        HSS.id = 'hss'
        HSS.long_name = 'Heidke Skill Score'
        HSS.setAxisList([Forcast_hrs, Threshold])
        HSS.comments = commentline
        # write this variables into nc file
        F_nc.write(HSS)
        # make free memory
        del HSS_list, HSS

        # Odds Ratio
        ODR = cdms2.createVariable(ODR_list)
        ODR.id = 'odr'
        ODR.long_name = 'Odds Ratio'
        ODR.setAxisList([Forcast_hrs, Threshold])
        ODR.comments = commentline
        # write this variables into nc file
        F_nc.write(ODR)
        # make free memory
        del ODR_list, ODR

        # Log Odd Ratio
        LODR = cdms2.createVariable(LODR_list)
        LODR.id = 'lodr'
        LODR.long_name = 'Log Odd Ratio'
        LODR.setAxisList([Forcast_hrs, Threshold])
        LODR.comments = commentline
        # write this variables into nc file
        F_nc.write(LODR)
        # make free memory
        del LODR_list, LODR

        # Odds Ratio Skill Score
        ORSS = cdms2.createVariable(ORSS_list)
        ORSS.id = 'orss'
        ORSS.long_name = 'Odds Ratio Skill Score'
        ORSS.setAxisList([Forcast_hrs, Threshold])
        ORSS.comments = commentline
        # write this variables into nc file
        F_nc.write(ORSS)
        # make free memory
        del ORSS_list, ORSS

        # Extreame Dependency Score
        EDS = cdms2.createVariable(EDS_list)
        EDS.id = 'eds'
        EDS.long_name = 'Extreme Dependency Score'
        EDS.setAxisList([Forcast_hrs, Threshold])
        EDS.comments = commentline
        # write this variables into nc file
        F_nc.write(EDS)
        # make free memory
        del EDS_list, EDS

        # close nc file
        F_nc.close()
    # end of for regionName in region:
# end of def genStatisticalScore(...):

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
                genStatisticalScoreDirs(model.name, model.hour,
                                        obsrainPath, obsrainfall.xml)
            else:
                pass
                # obsrainfall configuration and model data configuration are not equal in the text file
                # handle this case, in diff manner. The same loop should works.
                # But need to check all the cases.
    print "Done! Creation of Statistical scores netCdf Files"
# end of if __name__ == '__main__':
