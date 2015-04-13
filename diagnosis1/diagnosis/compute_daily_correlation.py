"""
.. module:: compute_daly_anomaly.py
   :synopsis: This script should calculate the anomaly for every day and
              store it as nc files in the appropriate directories.
.. moduleauthor:: Arulalan.T <arulalant@gmail.com>

"""

import os
import sys
import cdms2
from genutil.statistics import correlation
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
from diag_setup.globalconfig import models, processfilesPath
from diag_setup.gendir import createDirsIfNotExists
import diag_setup.netcdf_settings

# create time utility object
timobj = TimeUtility()

# timeAxis check value to skip the anomaly process for the existing month in
# the mean nc file
__timeCheck__ = True


def genDailyAnomalyCorrealationDirs(modelname, modelpath, modelhour):
    """
    :func:`genDailyAnomalyCorrealationDirs` : It should generate the directory structure
            whenever it needs. It reads the timeAxis information of the
            model data xml file(which is updating it by cdscan). It can
            calculate daily anomaly for model analysis and its forecast hours.
            It should become daily progress.

    Inputs : modelname is the model data name, which will become part of the
             directory structure.
             modelpath is the absolute path of data where the model xml files
             are located.
             modelhour is the forecast hours to do anomaly.
             climregriadir is the absolute path of the climatolgy regridded
             path w.r.t to this model data resolution (both horizontal and
             vertical)
             climpfilename is the climatolgy Partial File Name to combine the
             this passed name with (at the end) of the climatolgy var name to
             open the climatolgy files.
             climatolgyyear is the year of climatolgy data.

    Outputs : It should create the directory structure in the processfilesPath
              and create the processed nc files.

    Written By : Arulalan.T

    Date : 02.01.2012

    """

    xmlobj = xml_data_access.GribXmlAccess(modelpath)
    # get one model var name from the global 'vars.txt' file
    mvar = variables.get(modelname).values()[0].model_var
    modeldataset = xmlobj[mvar, 'a']
    # get the timeAxis of modeldata set
    modeltime = modeldataset.getTime()

    # create modelname, 'Statistics', 'Correlation' directories if it is not
    # exists
    childCorrPath = createDirsIfNotExists(processfilesPath,
                                   [modelname, 'Statistics', 'Correlation'])

    firstday = modeltime.asComponentTime()[0]
    # get the year
    year = str(firstday.year)
    # create Mean Root Year,Month directories if it is not exists
    correlationPath = createDirsIfNotExists(childCorrPath, [year, 'Daily'])

    dailyAnomalyPath = os.path.join(processfilesPath, modelname, 'Anomaly',
                                                                year, 'Daily')
    # calling below fn to create daily anomaly for model fcst hours
    for hr in modelhour:
        dailyCorrelationPath = createDirsIfNotExists(correlationPath, hr)
        
        genDailyCorrelationFiles(dailyAnomalyPath, dailyCorrelationPath, year,
                             hr, modelName = modelname, modelXmlObj = xmlobj)
    # close all the opened xml file objects
    xmlobj.closeXmlObjs()
    # end of for year in availableMonths.keys():
# end of def genDailyAnomalyCorrealationDirs()

def genDailyCorrelationFiles(dailyAnomalyPath, dailyCorrelationPath, year, hour, **model):
    """
    :func:`genDailyAnomalyFiles` : It should calculate daily anomaly
            from the daily analysis and daily climatolgy for the current day.
            i.e. daily model analysis - daily climatolgy
            Finally stores it as nc files in corresponding directory path
            which are passed in this function args.

            Do the same procedure for the model forecast hours anomaly.
            i.e. daily model forecast - daily climatolgy

    Inputs : dailyAnomalyPath is the absolute path where the processed mean
             anomaly nc files are going to store.
             modelType is either 'a' for 'analysis' or 'f' for 'forecast'.
             modelHour is the forecast hour.
             climRegriadir is the absolute path where the regridded monthly
             mean climatologies (w.r.t the model vertical resolution)
             nc files were already stored.
             climPFileName is the partial nc filename of the climatolgy.
             climatologyYear is the year of the climatolgy to access it.

    KWargs: modelName, modelXmlPath, modelXmlObj

             modelName is the model data name which will become part of the
             process nc files name.
             modelPath is the absolute path of data where the model xml files
             are located.
             modelXmlObj is an instance of the GribXmlAccess class instance.
             If we are passing modelXmlObj means, it will be optimized one
             when we calls this same function for same model for different
             months.

             We can pass either modelXmlPath or modelXmlObj KWarg is enough.

    Outputs : It should create daily anomaly for the particular variables which
              are all set the clim_var option in the vars.txt file. Finally
              store it as nc file formate in the proper directories structure
              (modelname, 'Anomaly', year, daily and then 'analysis' or
              fcst hours hierarchy).

    Written By : Arulalan.T

    Date : 02.01.2012

    """

    modelXmlObj, modelPath = None, None
    if 'modelName' in model:
        modelName = model.get('modelName')
    else:
        raise RuntimeError("KWarg modelName must be passed")

    if 'modelXmlObj' in model:
        modelXmlObj = model.get('modelXmlObj')
    elif 'modelXmlPath' in model:
        modelPath = model.get('modelXmlPath')
    else:
        raise RuntimeError("you must pass atleast one KWargs of modelXmlPath \
                            or modelXmlPath ")

    if not modelXmlObj:
        xmlobj = xml_data_access.GribXmlAccess(modelPath)
    else:
        if isinstance(modelXmlObj, xml_data_access.GribXmlAccess):
            xmlobj = modelXmlObj
        else:
            raise ValueError("Passed modelXmlObj instance %s is not an \
                    instance of GribXmlAccess class " % type(modelXmlObj))

    ncAnoFileDic = {}
    anomalyDirs = ['Analysis', hour]
    for adir in anomalyDirs:
        apath = '/'.join([dailyAnomalyPath, adir])
        ncAnoFileDic[adir] = {}
        # get the nc files name of mean anomaly
        ncfiles = [f for f in os.listdir(apath) if f.endswith('.nc')]
        # make ncfiles as dictionary with key as var name
        for ncfile in ncfiles:
            var = ncfile.split('_')[0]
            anomalyFilePath = apath + '/' + ncfile
            ncAnoFileDic[adir][var] = anomalyFilePath
        # make memory free
        del ncfiles

    ncCorrFileDic = {}
    # get the nc files name of mean anomaly
    ncfiles = [f for f in os.listdir(dailyCorrelationPath) if f.endswith('.nc')]
    # make ncfiles as dictionary with key as var name
    for ncfile in ncfiles:
        var = ncfile.split('_')[0]
        correlationFilePath = dailyCorrelationPath + '/' + ncfile
        ncCorrFileDic[var] = correlationFilePath
    # make memory free
    del ncfiles

    modelvariables = xmlobj.listvariable(Type = 'a')

    # get the namedtuple object from the global 'vars.txt' file
    totalvars = variables.get(modelName)
    for globalvar in totalvars.itervalues():
        # get the model var name
        mvar = globalvar.model_var
#        # get the climatolgy var name
#        cvar = globalvar.clim_var

#        if not cvar:
#            print "Climatology var name is empty string. So skipping anomaly \
#               correlation process for %s model var name " % mvar
#            continue
#        # end of if not cvar:

        if not mvar in modelvariables:
            print "The variable %s is not available in the xml anl file object" % mvar
            print "So skipping the anomaly correlation process \
                   for this variable %s which is one of the keys of the \
                   variables dictionary" % mvar
            continue
        # end of if not mvar in allvariables:

        if not mvar in ncAnoFileDic['Analysis']:
            print "The variable %s is not available in processed anomaly \
              analysis directory. So skipping the anomaly correlation process \
              for this variable %s " % (mvar, mvar)
            continue

        correlationLatestDate = None
        # generate the nc filename
        anomalyCorrFileName = mvar + '_'+ modelName + '_' + year
        anomalyCorrFileName += '_daily_f' + hour + 'hr'
        anomalyCorrFileName += '_anomaly_correlation.nc'

        anomalyAnlFilePath = ncAnoFileDic['Analysis'].get(mvar)
        try:
            anoAnlFile = cdms2.open(anomalyAnlFilePath, 'r')
        except:
            raise ValueError("Couldnt open the anomaly analysis file '%s'.\
           so can not perform the daily correlation" % anomalyAnlFilePath)

        anoAnlTime = anoAnlFile[mvar].getTime().asComponentTime()
        levAxis = anoAnlFile[mvar].getLevel()
        if mvar in ncCorrFileDic:

            anomalyCorrFilePath = ncCorrFileDic.get(mvar)
            correlationLatestDate = None
            try:
                # open nc file in append mode
                anomalyCorrFile = cdms2.open(anomalyCorrFilePath, 'a')
                # get the ncfile timeAxis
                fileTime = anomalyCorrFile[mvar].getTime().asComponentTime()
                anomalyLatestDate = anoAnlTime[-1]
                correlationLatestDate = fileTime[-1]
                # Do check either this month timeAxis is already exists in
                # the nc file's timeAxis or not. If exists means skip it.
                if __timeCheck__:
                    if anomalyLatestDate in fileTime:
                        print "The daily anomaly is already exists in the \
                               file %s. So skipping var '%s' " % \
                                        (anomalyCorrFile, mvar)
                        anomalyCorrFile.close()
                        continue
                # end of if __timeCheck__:
            except (AttributeError, cdms2.error.CDMSError):
                # if it getting this error means, it may not written
                # properly. So open nc file in write mode freshly.
                print "Got Problem. nc file is correpted at last time. \
                       May be lost the previous days data.\
                       Now creating same nc file '%s' freshly & fully " \
                       % (anomalyCorrFilePath)
                anomalyCorrFile = cdms2.open(anomalyCorrFilePath, 'w')
        else:
            anomalyCorrFilePath = dailyCorrelationPath + '/' + anomalyCorrFileName
            # open new nc file in write mode
            anomalyCorrFile = cdms2.open(anomalyCorrFilePath, 'w')
        # end of if mvar in ncAnoFileDic:

        anomalyHrFilePath = ncAnoFileDic[hour].get(mvar)
        try:
            anoHrFile = cdms2.open(anomalyHrFilePath, 'r')
        except:
            raise ValueError("Couldnt open the anomaly fcst %s hour file '%s'.\
           so can not perform the daily correlation" % (hour, anomalyHrFilePath))
        
        anoFirstYear = anoAnlTime[0].year
        if correlationLatestDate:
            nextIndex = anoAnlTime.index(correlationLatestDate) + 1
            anoAnlTime = anoAnlTime[nextIndex:]
        print "Writing daily anomaly correlation into %s file \n" % (anomalyCorrFileName)
        for adate in anoAnlTime:
            partnerDate = xmlobj.findPartners('a', adate, hour)
            #print "Extracting the fcst", hour, " partner data on ", partnerDate, "of analysis data on ", adate

            try:
                # get the climatolgy data for this month alone
                anoHrData = anoHrFile(mvar, time = partnerDate)
            except:
                print "Coundn't get the anomaly fcst '%s' hour data of %s var \
                             %s time" % (hour, mvar, partnerDate)
                print "So skipping the anomaly correlation for the '%s' variable" % mvar
                continue
            # end of try:

            try:
                # get the model data for this day alone
                anoAnlData = anoAnlFile(mvar, time = adate)
            except:
                print "Coundn't get the anomaly analysis data of %s var %s time" \
                                                         % (mvar, adate)
                print "So skipping the anomaly correlation for the '%s' \
                         variable on '%s'" % (mvar, adate)
                continue
            # end of try:

            print "Calculating Daily Anomaly Correlation on ", adate
            # anomaly correlation
            if levAxis:
                corrValue = correlation(anoAnlData, anoHrData, axis = "tyx")
            else:
                corrValue = correlation(anoAnlData, anoHrData, axis = "tzyx")
            # make memory free
            del anoAnlData, anoHrData

            fcststart = timobj._getDayCountOfYear(partnerDate, year=anoFirstYear)
            startDayOfYear = '%s-1-1' % anoFirstYear
            dailyCorrTime = timobj._generateTimeAxis([fcststart], startDayOfYear)

            corrValue = corrValue.reshape((1, len(corrValue)))
            corrValue = cdms2.createVariable(corrValue)
            if levAxis:
                corrValue.setAxisList([dailyCorrTime, levAxis])
            else:
                corrValue.setAxis(0, dailyCorrTime)
            corrValue.id = mvar
            #corrValue.comments = 'monthly mean anomaly of %s model data of %s' % (modelName, year)
            anomalyCorrFile.write(corrValue)
            # make memory free
            del corrValue
        # end of for mdate in modelTime:
        anomalyCorrFile.close()
    # end of for globalvar in totalvars.itervalues():
# end of def genDailyAnomalyFiles(...):

if __name__ == '__main__':

    for model in models:
        # calling the genDailyAnomalyCorrealationDirs function to do process
        genDailyAnomalyCorrealationDirs(model.name, model.path, model.hour)
    # end of for model in models:
    print "Done! Creation of Daily Anomaly netCdf Files"
# end of if __name__ == '__main__':
