"""
.. module:: compute_season_mean.py
   :synopsis: This module do the calculating the mean analysis and forecast
              systematic error for every season and store it as nc files in
              the appropriate directories.
              Finally it should create xml files by cdscaning all the nc files
              in the appropriate directories, with levels option.
.. moduleauthor:: Arulalan.T <arulalant@gmail.com>

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
# import xml_data_acces.py from previous directory diagnosisutils
import diagnosisutils.xml_data_access as xml_data_access
from diagnosisutils.timeutils import TimeUtility
from diag_setup.varsdict import variables
from diag_setup.globalconfig import models, processfilesPath, seasons
from diag_setup.gendir import createDirsIfNotExists
import diag_setup.netcdf_settings

# create time utility object
timobj = TimeUtility()

# timeAxis check value to skip the season mean process for the existing month
#  in the mean nc file
__timeCheck__ = True


def genMeanAnlFcstErrDirs(modelname, modelpath, modelhour):
    """
    :func:`genMeanAnlFcstErrDirs` : It should create the directory structure
            whenever it needs. It reads the timeAxis information of the
            model data xml file(which is updating it by cdscan), and once
            the full seasonal months are completed, then it should check
            either that season directory is empty or not.

            case 1: If that directory is empty means, it should call the
                    function called `genSeasonMeanFiles`, to calculate
                    the mean analysis and fcstsyserr for that season and should
                    store the processed files in side that directory.

            case 2: If that directory is non empty means,
                    ****have to update*****

    Inputs : modelname is the model data name, which will become part of the
             directory structure.
             modelpath is the absolute path of data where the model xml files
             are located.
             modelhour is the list of model data hours, which will become
             part of the directory structure.

    Outputs : It should create the directory structure in the processfilesPath
              and create the processed nc files.

    Written By : Arulalan.T

    Date : 08.12.2011

    """

    xmlobj = xml_data_access.GribXmlAccess(modelpath)
    # get one model var name from the global 'vars.txt' file
    mvar = variables.get(modelname).values()[0].model_var
    modeldataset = xmlobj[mvar, 'a']
    # get the timeAxis of modeldata set and correct its bounds
    modeltime = timobj._correctTimeAxis(modeldataset.getTime())
    # get the fully available months
    availableMonths = timobj.getTimeAxisFullMonths(modeltime)
    # generate model directory path
    childPath = os.path.join(processfilesPath, modelname)
    # generate Mean directory path
    childMeanPath = os.path.join(childPath, 'Mean')
    # generate FcstSysError directory path
    childFcstErrPath = os.path.join(childPath, 'FcstSysErr')

    for year in availableMonths:
        monthdic = availableMonths.get(year)
        # sort the months in correct order
        months = timobj._sortMonths(monthdic.keys())

        year = str(year)
        # create Mean Year,Season directories if it is not exists
        childMeanSeasonPath = createDirsIfNotExists(childMeanPath,
                                                    [year, 'Season'])
        # create Anomaly Year, Season directories if it is not exists
        childFcstErrSeasonPath = createDirsIfNotExists(childFcstErrPath,
                                                       [year, 'Season'])

        for seasonName, season in seasons.iteritems():
            # find out xml time axis months has the seasonal months or not
            seasonMonths = [month for smonth in season for month in months
                            if smonth[:3].lower() == month[:3].lower()]
            if len(seasonMonths) == len(season):
                print "Got the seasonal months for %s season" % seasonName
            else:
                print "Seasonal months are not available for %s season" % seasonName
                continue
            # get the list of months of the season in order with its start &
            # end date
            seasonMonthDate = [(month, monthdic.get(month)) for month in months]

            if seasonName.isupper():
                seasonName = seasonName.lower()

            # create Mean SeasonName, Analysis directory if it is not exists
            anlSeasonPath = createDirsIfNotExists(childMeanSeasonPath,
                                                    [seasonName, 'Analysis'])
            # generate the monthly mean analysis directory path
            anlMonthPath = os.path.join(childMeanPath, year, 'Month', 'Analysis')

            # calling below function to create seasonly mean analysis nc files
            genSeasonMeanFiles(anlSeasonPath, anlMonthPath, seasonName,
                                     seasonMonthDate, year, Type = 'a',
                            modelName = modelname, modelXmlObj = xmlobj)

            # create fcstsyserr Sub SeasonName directory if it is not exists
            fcstErrSeasonPath = createDirsIfNotExists(childFcstErrSeasonPath,
                                                                  seasonName)
            # generate the monthly mean FcstSysError directory path
            fcstMonthPath = os.path.join(childPath, 'FcstSysErr', year, 'Month')

            # calling below function to create seasonly mean fcstsyserr nc files
            genSeasonMeanFiles(fcstErrSeasonPath, fcstMonthPath, seasonName,
                    seasonMonthDate, year, Type = 'f', modelName = modelname,
                                 modelXmlObj = xmlobj, modelHour = modelhour)
        # end of for seasonName, season in seasons.iteritems():
        # close all the opened xml file objects
        xmlobj.closeXmlObjs()
    # end of for year in availableMonths.keys():
# end of def genMeanAnlFcstErrDirs()

def genSeasonMeanFiles(meanSeasonPath, meanMonthPath, seasonName,
                                        seasonMonthDate, year, Type, **model):
    """
    :func:`genSeasonMeanFiles` : It should calculate the seasonly mean for
            either analysis or forecast systematic error. It can be choosed by
            the Type argment. Finally stores it as nc files in corresponding
            directory path which are passed in this function args.

    Inputs : meanSeasonPath is the absolute path where the processed season
             mean analysis or forecast systematic error nc files are going to
             store. Inside the fcst hours directories will be created in this
             path, if needed.

             meanMonthPath is the absolute path where the processed monthly
             mean analysis or monthly mean fcstsyserr nc files were stored,
             already.
             seasonName is the name of the season.
             seasonMonthDate(list of months which contains monthname,
             startdate & enddate) for the season.
             year is the part of the directory structure.
             Type is either 'a' for analysis or 'f' for fcstsyserr.

    KWargs: modelName, modelXmlPath, modelXmlObj

             modelName is the model data name which will become part of the
             process nc files name.
             modelHour is the model hours as list, which will become part of
             the directory structure.
             modelPath is the absolute path of data where the model xml files
             are located.
             modelXmlObj is an instance of the GribXmlAccess class instance.
             If we are passing modelXmlObj means, it will be optimized one
             when we calls this same function for same model for different
             months.

             We can pass either modelXmlPath or modelXmlObj KWarg is enough.

    Process : This function should compute the seasonly mean for analysis and
              fcstsyserr by just opening the monthly mena analysis/fcstsyserr
              nc files (according to the season's months) and multiply the
              monthly mean into its weights value. So that monthly mean data
              should become monthly full data (not mean). Then add it together
              for the season of months. Finally takes the average by just
              divide the whole season data by sum of monthly mean weights.
                So it should simplify our life, just extracting data which
              timeAxis length is 4, for 4 months in season. (eg JJAS).

    Outputs : It should create seasonly mean analysis and forecast systematic
              error for all the available variables in the vars.txt file,
              and store it as nc file in the proper directory structure
              (modelname, process name, year, season, and/or hours hierarchy).

    Written By : Arulalan.T

    Date : 08.12.2011

    """

    modelXmlObj, modelPath = None, None

    if 'modelName' in model:
        modelName = model.get('modelName')
    else:
        raise RuntimeError("KWarg modelName must be passed")

    if 'modelHour' in model:
        modelHour = model.get('modelHour')
    else:
        if Type in ['f', 'fcst']:
            raise RuntimeError("KWarg modelHour must be passed, since Type \
                                has passed as 'f' ")

    if 'modelXmlObj' in model:
        modelXmlObj = model.get('modelXmlObj')
    elif 'modelXmlPath' in model:
        modelPath = model.get('modelXmlPath')
    else:
        raise RuntimeError("you must pass atleast one KWargs of modelXmlPath \
                            or modelXmlObj ")

    if not modelXmlObj:
        xmlobj = xml_data_access.GribXmlAccess(modelPath)
    else:
        if isinstance(modelXmlObj, xml_data_access.GribXmlAccess):
            xmlobj = modelXmlObj
        else:
            raise ValueError("Passed modelXmlObj instance %s is not an \
                    instance of GribXmlAccess class " % type(modelXmlObj))
    # end of if not modelXmlObj:

    if Type in ['a', 'anl']:
        modelHour = [None]
        fname = 'analysis'
        allvariables = xmlobj.listvariable(Type = 'a')
    elif Type in ['f', 'fcst']:
        fname = 'fcstsyserr'
    else:
        raise RuntimeError("Type must be either 'a' or 'f' only")

    if not os.path.isdir(meanMonthPath):
        raise RuntimeError("The monthly mean path doesnot exists '%s'. So \
                couldnt compute the season mean process" % (meanMonthPath))

    # get the namedtuple object from the global 'vars.txt' file
    totalvars = variables.get(modelName)
    for hr in modelHour:
        if hr:
            meanMonthSubPath = meanMonthPath + '/' + hr
            allvariables = xmlobj.listvariable(Type = 'f', hour = hr)
            comment = '%s season mean %s of %s hour of %s model data of %s' % (seasonName, fname, hr, modelName, year)
            # create hour directory if it is not exists
            meanSeasonSubPath = createDirsIfNotExists(meanSeasonPath, hr)
            lastname = 'f' + hr + 'hr'
        else:
            meanMonthSubPath = meanMonthPath
            comment = '%s season mean %s of %s model data of %s' % (seasonName, fname, modelName, year)
            meanSeasonSubPath = meanSeasonPath
            lastname = None
        # get the nc files name
        mfiles = [f for f in os.listdir(meanMonthSubPath) if f.endswith('.nc')]

        if not mfiles:
            print "monthly mean %s directory path '%s' is empty. So skipping \
                   the process " % (fname, meanMonthSubPath)
            continue
        # get the nc files name of season mean
        ncfiles = [f for f in os.listdir(meanSeasonSubPath) if f.endswith('.nc')]
        # make ncfiles as dictionary with key as var name
        ncfiledic = {}
        for ncfile in ncfiles:
            var = ncfile.split('_')[0]
            ncfiledic[var] = ncfile
        # make memory free
        del ncfiles

        for globalvar in totalvars.itervalues():
            # get the model var name
            mvar = globalvar.model_var
            if not mvar in allvariables:
                print "The variable %s is not available in the xml file object" % mvar
                print "So skipping the season mean %s processes for the \
                       variable %s which is one of the keys of the \
                       variables dictionary" % (fname, mvar)
                continue
            # end of if not mvar in allvariables:
            # partial nc file name
            pFileName = mvar + '_'+ modelName + '_' + year
            # generate the nc filename
            ncMoFileName = pFileName + '_mean_' + fname
            if lastname:
                ncMoFileName += '_' + lastname + '.nc'
            else:
                ncMoFileName += '.nc'

            if not ncMoFileName in mfiles:
                print "nc file %s not available in the path %s" % (ncMoFileName, meanMonthSubPath)
                print "So skipping variable %s for season mean " % (mvar)
                continue
            # end of if not ncMoFileName in mfiles:

            # store season mean into proper nc file
            if mvar in ncfiledic:
                ncSeFileName = ncfiledic.get(mvar)
                meanSeasonFilePath = meanSeasonSubPath + '/' + ncSeFileName
                try:
                    # open nc file in append mode
                    seasonFile = cdms2.open(meanSeasonFilePath, 'a')
                    # get the ncfile timeAxis
                    fileTime = seasonFile[mvar].getTime()
                    # Do check either this month timeAxis is already exists in
                    # the nc file's timeAxis or not. If exists means skip it.
                    if __timeCheck__:
                        if seasonMonthDate[0][1][0] in fileTime.asComponentTime():
                            print "The mean anomaly is already exists in the \
                                   file %s. So skipping var '%s' " % \
                                            (ncSeFileName, mvar)
                            seasonFile.close()
                            continue
                    # end of if __timeCheck__:
                except cdms2.error.CDMSError, AttributeError:
                    # if it getting this error means, it may not written
                    # properly. So open nc file in write mode freshly.
                    print "Got Problem. nc file is correpted at last time. \
                           May be lost the previous months data.\
                           Now creating same nc file '%s' freshly w.r.t current \
                           season %s" % (ncSeFileName, seasonName)
                    seasonFile = cdms2.open(meanSeasonFilePath, 'w')
            else:
                # generate the season mean nc filename
                ncSeFileName = pFileName + '_' + seasonName + '_mean_' + fname
                if lastname:
                    ncSeFileName += '_' + lastname + '.nc'
                else:
                    ncSeFileName += '.nc'
                seasonFile = cdms2.open(meanSeasonSubPath + '/' + ncSeFileName, 'w')
            # end of if mvar in ncfiledic:

            monthFile = cdms2.open(meanMonthSubPath + '/' + ncMoFileName, 'r')
            seasonDataDaysCount = 0
            # finding the total no of days of the passed seasonal months
            flag = True
            for mon in seasonMonthDate:
                month = mon[0]
                startdate = mon[1][0]
                print "Get the %s month mean data to compute season data" % month
                try:
                    monthMeanData = monthFile(mvar, time = startdate)
                except:
                    print "Failed to get the %s month mean data" % month
                    print "So skipping the above month for season"
                    # now temporarily make it as continue. In future we need
                    # to throw error instead of print statement
                    continue
                if flag:
                    seasonStartDate = startdate
                    # get the level, lat & lon axis
                    modelLevel = monthMeanData.getLevel()
                    modelLatitude = monthMeanData.getLatitude()
                    modelLongitude = monthMeanData.getLongitude()
                    varunits = monthMeanData.units
                    title = monthMeanData.long_name
                    # creates dummy initial seasonData values with same shape
                    # of monthly mean data
                    seasonData = numpy.zeros(monthMeanData.shape)
                    flag = False
                # end of if flag:
                # get the timeAxis of the monthly mean data
                meanTime = monthMeanData.getTime()
                # get the bounds
                bounds = meanTime.getBounds()
                # find the no of days in the month (by its diff of weights)
                weightsdiff = bounds[0][1] - bounds[0][0]
                # multiply the monthly mean data with its weightsdiff & add it
                # to the seasonly data. i.e make the monthly average into
                # monthly data by multiply with its bounds. And then add it to
                # the season data. i.e. combine the monthly data together to
                # make seasonly data
                seasonData += monthMeanData * weightsdiff
                seasonDataDaysCount += weightsdiff
                # make memory free
                del monthMeanData
            # end of for mon in seasonMonthDate:
            # find out the average of the seasonly data by dividing it by its
            # total no of days present in that season.
            meanSeasonData = seasonData / seasonDataDaysCount
            # make memory free
            del seasonData
            # create cdms2 variable
            meanSeasonData = cdms2.createVariable(meanSeasonData)
            print "\n Seasonly time axis has created"
            # create season mean time axis
            seasonTime = timobj._generateMonthlyMeanTimeAxis(seasonStartDate,
                                                  days = seasonDataDaysCount)
            # setting time, level, lat & lon axis to the mean season data
            if modelLevel:
                meanSeasonData.setAxisList([seasonTime, modelLevel,
                                    modelLatitude, modelLongitude])
            else:
                meanSeasonData.setAxisList([seasonTime, modelLatitude,
                                                    modelLongitude])
            meanSeasonData.id = mvar
            meanSeasonData.units = varunits
            meanSeasonData.long_name = title
            meanSeasonData.comments = comment


            print "Writing season mean for '%s' into nc file '%s' " % (fname, ncSeFileName)
            seasonFile = cdms2.open(meanSeasonSubPath + '/' + ncSeFileName, 'w')
            seasonFile.write(meanSeasonData)
            seasonFile.close()
            # make memory free
            del meanSeasonData
        # end of for globalvar in totalvars.itervalues():
    # end of for hr in modelHour:
# end of def genSeasonMeanFiles(...):

if __name__ == '__main__':

    for model in models:
        # calling the genMeanAnlFcstErrDirs function to do process
        genMeanAnlFcstErrDirs(model.name, model.path, model.hour)
    # end of for model in models:
    print "Done! Creation of Season Mean Analysis & FcstSysErr netCdf Files"
# end of if __name__ == '__main__':
