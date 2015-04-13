"""
.. module:: compute_daly_anomaly.py
   :synopsis: This script should calculate the anomaly for every day and
              store it as nc files in the appropriate directories.
.. moduleauthor:: Arulalan.T <arulalant@gmail.com>

"""

import os
import sys
import cdms2
import cdtime
from regrid2 import Horizontal
from genutil import statusbar
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
from diag_setup.globalconfig import models, climatologies, processfilesPath, logpath
from diag_setup.gendir import createDirsIfNotExists
from diag_setup.logsetup import createLog
import diag_setup.netcdf_settings

# create time utility object
timobj = TimeUtility()

# timeAxis check value to skip the anomaly process for the existing month in
# the mean nc file
__timeCheck__ = True
__showStatusBar = False

# create log object to written into logfile
logfile = __file__.split('.py')[0] + '.log'
log = createLog(__file__, os.path.join(logpath, logfile))


def convertTimeIntegratedToNormal(data, hour):
    # Time integrated data unit Wsm^-2. Converted to Wm^2.
    return data / (float(hour) * 60 * 60)
# end of def convertTimeIntegratedToNormal(data, hour, sign=1):


def genDailyAnomalyDirs(modelname, modelpath, modelhour, climregridpath,
                                   climpfilename, climatologyyear, **kwarg):
    """
    :func:`genDailyAnomalyDirs` : It should generate the directory structure
            whenever it needs. It reads the timeAxis information of the
            model data xml file(which is updating it by cdscan). It can
            calculate daily anomaly for model analysis and its forecast hours.
            It should become daily progress.

    Inputs : modelname is the model data name, which will become part of the
             directory structure.
             modelpath is the absolute path of data where the model xml files
             are located.
             modelhour is the forecast hours to do anomaly.
             climregridpath is the absolute path of the climatology regridded
             path w.r.t to this model data resolution (both horizontal and
             vertical)
             climpfilename is the climatology Partial File Name to combine the
             this passed name with (at the end) of the climatology var name to
             open the climatology files.
             climatologyyear is the year of climatology data.

    Outputs : It should create the directory structure in the processfilesPath
              and create the processed nc files.

    KWargs :
        anopath - It should be the abspath with already created. After this path
                  year, Daily and Analysis/Fcst hours sub directories will be
                  created. If this anopath is not passed means (by default)
                  it will create the directory structure as processfiles,
                  modelname, Anomaly, year, Daily and Analysis/Fcst hours.

    Written By : Arulalan.T

    Date : 30.12.2011
    Updated : 04.08.2013

    """

    xmlobj = xml_data_access.GribXmlAccess(modelpath)
    # get one model var name from the global 'vars.txt' file
    mvar = variables.get(modelname).values()[0].model_var
    modeldataset = xmlobj[mvar, 'a']
    # no need to do _correctTimeAxis now. Lets remove it later
    # get the timeAxis of modeldata set and correct its bounds
    modeltime = timobj._correctTimeAxis(modeldataset.getTime())

    childMeanPath = kwarg.get('anopath', None)
    if childMeanPath is None:
        # create modelname, Anomaly directories if it is not exists
        childMeanPath = createDirsIfNotExists(processfilesPath,
                                         [modelname, 'Anomaly'])

    latestday = modeltime.asComponentTime()[-1]
    # get the year
    year = str(latestday.year)
    # create Mean Root Year,Month directories if it is not exists
    meanAnomalyPath = createDirsIfNotExists(childMeanPath,
                                              [year, 'Daily'])

    # calling below fn to create daily anomaly for model analysis
    dailyAnlAnomalyPath = createDirsIfNotExists(meanAnomalyPath, 'Analysis')
    Type = 'a'
    genDailyAnomalyFiles(dailyAnlAnomalyPath, Type, None, year,
                         climregridpath, climpfilename, climatologyyear,
                          modelName=modelname, modelXmlObj=xmlobj, **kwarg)

    # calling below fn to create daily anomaly for model fcst hours
    for hr in modelhour:
        Type = 'f'
        dailyFHrAnomalyPath = createDirsIfNotExists(meanAnomalyPath, hr)
        genDailyAnomalyFiles(dailyFHrAnomalyPath, Type, hr, year,
                        climregridpath, climpfilename, climatologyyear,
                        modelName=modelname, modelXmlObj=xmlobj, **kwarg)
    # close all the opened xml file objects
    xmlobj.closeXmlObjs()
    # end of for year in availableMonths.keys():
# end of def genDailyAnomalyDirs()


def genDailyAnomalyFiles(dailyAnomalyPath, modelType, modelHour, year,
                climRegridPath, climPFileName, climatologyYear, **kwarg):
    """
    :func:`genDailyAnomalyFiles` : It should calculate daily anomaly
            from the daily analysis and daily climatology for the current day.
            i.e. daily model analysis - daily climatology
            Finally stores it as nc files in corresponding directory path
            which are passed in this function args.

            Do the same procedure for the model forecast hours anomaly.
            i.e. daily model forecast - daily climatology

    Inputs : dailyAnomalyPath is the absolute path where the processed mean
             anomaly nc files are going to store.
             modelType is either 'a' for 'analysis' or 'f' for 'forecast'.
             modelHour is the forecast hour.
             climRegridPath is the absolute path #[where the regridded monthly
             mean climatologies (w.r.t the model vertical resolution) optional]#
             nc files were already stored.
             climPFileName is the partial nc filename of the climatology.
             climatologyYear is the year of the climatology to access it.

    KWargs: modelName, modelXmlPath, modelXmlObj, cregrid, dregrid,

        modelName - is the model data name which will become part of the
                    process nc files name.
        modelPath - is the absolute path of data where the model xml files
                    are located.
        modelXmlObj - is an instance of the GribXmlAccess class instance.
             If we are passing modelXmlObj means, it will be optimized one
             when we calls this same function for same model for different
             months.
             We can pass either modelXmlPath or modelXmlObj KWarg is enough.

        ovar - output anomaly variable. By default it will be same as
               model variable name. If user need to change it, then
               they can pass new variable name for anomaly data.

        convertTI2N - It takes either True or False. If it is True, then the
            model data will be converted from Time Integrated to Normal form.
            i.e. Units will be converted from Wsm^-2 to Wm^2.

        sign - change sign of the model data (will be used in convertTI2N fn)

        When modeldata and climatology shapes are mis-match, then
        cregrid : if True, then climatology data will be regridded w.r.t
                  model/obs/data and then anomaly will be calculated.

        dregrid : if True, then model/obs/data will be regridded w.r.t
                 climatology data and then anomaly will be calculated.

        ..note:: We can not enable both cregrid and dregrid at the same time.

   CAUTION: If "from diag_setup.varsdict import variables" contains 'anl_hour' arg
        in any of the variable statement, then instead of 'analysis' modelType,
        it will take input data from the 'fcst' modelType and its hour will be
        its corresponding anl_hour. It will be useful when 'analysis' type
        'olr' variable is not available, then we can use '00'th fcst hour's olr.
        But the output filename reamains ends with same as analysis

    Outputs : It should create daily anomaly for the particular variables which
              are all set the clim_var option in the vars.txt file. Finally
              store it as nc file formate in the proper directories structure
              (modelname, 'Anomaly', year, daily and then 'analysis' or
              fcst hours hierarchy).

    Written By : Arulalan.T

    Date : 30.12.2011
    Updated Date : 02.07.2013

    """

    modelXmlObj, modelPath = None, None
    if 'modelName' in kwarg:
        modelName = kwarg.get('modelName')
    else:
        raise RuntimeError("KWarg modelName must be passed")

    if 'modelXmlObj' in kwarg:
        modelXmlObj = kwarg.get('modelXmlObj')
    elif 'modelXmlPath' in kwarg:
        modelPath = kwarg.get('modelXmlPath')
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

    ovar = kwarg.get('ovar', '')
    cregrid = kwarg.get('cregrid', False)
    dregrid = kwarg.get('dregrid', False)
    convertTI2N = kwarg.get('convertTI2N', False)
    sign = kwarg.get('sign', 1)
    arglog = kwarg.get('log', None)
    if arglog is not None:
        log = arglog
    # end of if arglog is not None:
    # get the nc files name of mean anomaly
    ncfiles = [f for f in os.listdir(dailyAnomalyPath) if f.endswith('.nc')]
    # make ncfiles as dictionary with key as var name
    ncfiledic = {}
    for ncfile in ncfiles:
        vari = ncfile.split('_')
        if vari[1].isdigit():
            # for mjo works, variable_level_foo.nc has mentioned.
            vari = vari[:2]
        else:
            vari = [vari[0]]
        # end of if vari[1].isdigit():
        var = '_'.join(vari)
        ncfiledic[var] = ncfile
    # make memory free
    del ncfiles

    # get the namedtuple object from the global 'vars.txt' file
    totalvars = variables.get(modelName)
    for globalvar in totalvars.itervalues():
        if modelType in ['a', 'anl', 'f', 'fcst']:
            # get the model var name
            mvar = globalvar.model_var
        elif modelType in ['o', 'obs']:
            # get the observation var name
            mvar = globalvar.obs_var
        # get the climatology var name
        cvar = globalvar.clim_var
        # get the model variable level
        mlevel = globalvar.model_level
        if globalvar.anl_hour is not None and modelType in ['a', 'anl', 'analysis']:
            # overwrite the mtype and its hour to extract this variable data
            # alone from fcst and globalvar.anl_hour (for eg fcst 00 th hour).
            # But the output filename reamains ends with same as analysis
            mtype = 'f'  # fcst type
            mhour = globalvar.anl_hour
        else:
            mtype = modelType
            mhour = modelHour
        # end of if globalvar.anl_hour is not None ... :

        if not cvar:
            print "Climatology var name is empty string. So skipping anomaly \
                process for %s model var name " % mvar
            continue
        # end of if not cvar:

        modelvariables = xmlobj.listvariable(Type=mtype, hour=mhour)
        if not mvar in modelvariables:
            print "The variable %s is not available in the xml anl/obs file object" % mvar
            print "So skipping the anomaly and mean analysis processes \
                   for this variable %s which is one of the keys of the \
                   variables dictionary" % mvar
            continue
        # end of if not mvar in allvariables:

        # partial nc file name
        pFileName = [mvar, modelName, year, 'daily_']
        # variable name key generating to access ncfiledic
        ncvar = mvar
        if mlevel:
            strlevel = str(int(mlevel))
            pFileName.insert(1, strlevel)
            ncvar += '_' + strlevel
        # end of if mlevel:
        pFileName = '_'.join(pFileName)
        if modelType in ['a', 'anl']:
            pFileName += 'anl'
        elif modelType in ['o', 'obs']:
            pFileName += 'obs'
        elif modelType in ['f', 'fcst']:
            pFileName += 'f' + modelHour + 'hr'
        # end of if modelType in ['a', 'anl']:
        anomalyLatestDate = None

        # store anomaly into proper nc file
        if ncvar in ncfiledic:
            anomalyFileName = ncfiledic.get(ncvar)
            anomalyFilePath = os.path.join(dailyAnomalyPath, anomalyFileName)
            anomalyLatestDate = None
            try:
                # open nc file in append mode
                anomalyFile = cdms2.open(anomalyFilePath, 'a')  # append mode.
                # get the ncfile timeAxis
                xmlFileLatestDate = xmlobj[mvar, mtype, mhour].getTime().asComponentTime()[-1]
                anomalyLatestDate = anomalyFile[mvar].getTime().asComponentTime()[-1]
                # Do check either this month timeAxis is already exists in
                # the nc file's timeAxis or not. If exists means skip it.
                if __timeCheck__:
                    print anomalyFilePath, xmlFileLatestDate, anomalyLatestDate
                    if anomalyLatestDate == xmlFileLatestDate:
                        log.info("The daily anomaly is already exists in the \
                                  file %s for '%s'. So skipping var '%s' ",
                                  anomalyFileName, mvar, str(anomalyLatestDate))
                        anomalyFile.close()
                        continue
                # end of if __timeCheck__:
            except (AttributeError, cdms2.error.CDMSError):
                # if it getting this error means, it may not written
                # properly. So open nc file in write mode freshly.
                log.warning("Got Problem. nc file is correpted at last time. \
                       May be lost the previous days data.\
                       Now creating same nc file '%s' freshly & fully ",
                                                       anomalyFileName)
                # remove it
                os.remove(anomalyFilePath)
                # create it freshly
                anomalyFile = cdms2.open(anomalyFilePath, 'w')
            except Exception, e:
                print e
        else:
            # generate the nc filename
            anomalyFileName = pFileName + '_anomaly.nc'
            anomalyFilePath = dailyAnomalyPath + '/' + anomalyFileName
            # open new nc file in write mode
            anomalyFile = cdms2.open(anomalyFilePath, 'w')
            log.info("opening anomaly file in write mode '%s'", anomalyFilePath)
        # end of if ncvar in ncfiledic:

        # generate the climatology file name
        climatologyFile = cvar + climPFileName
        cfile = cdms2.open(climRegridPath + '/' + climatologyFile, 'r')

        # get the model data
        modelObj = xmlobj[mvar, mtype, mhour]
        modelTime = modelObj.getTime().asComponentTime()
        modelFirstYear = modelTime[0].year
        levAxis = modelObj.getLevel()
        latAxis = modelObj.getLatitude()
        lonAxis = modelObj.getLongitude()

        regridfunc = None

        if anomalyLatestDate:
            nextIndex = modelTime.index(anomalyLatestDate) + 1
            modelTime = modelTime[nextIndex:]
            log.info("The last successfull anomaly date is '%s'. \
                So continuing anomaly from the next day onwards", anomalyLatestDate)
        # end of if anomalyLatestDate:

        log.info("Writing daily anomaly into %s file", anomalyFileName)
        preview = 0
        for mdate in modelTime:
            try:
                # get the model data for this day alone
                modelData = xmlobj.getData(mvar, Type=mtype,
                              hour=mhour, date=mdate, level=mlevel, squeeze=1)
            except:
                print "Coundn't get the analysis data of %s var %s time" \
                                                         % (mvar, mdate)
                print "So skipping the anomaly for the '%s' variable" % mvar
                continue
            # end of try:

            climDataTime = cdtime.comptime(climatologyYear, mdate.month, mdate.day)

            try:
                # get the climatology data for this month alone
                climatologyData = cfile(cvar, time=climDataTime, squeeze=1)
            except:
                print "Coundn't get the climatology data for the variable %s and \
                       time %s " % (cvar, climDataTime)
                print "So skipping anomaly for the variable %s" % mvar
                continue
            # end of try:
            if not __showStatusBar:
                log.info("Calculating Daily Anomaly on %s", str(mdate))
            # end of if not __showStatusBar:

            if convertTI2N:
                # Time integrated data unit Wsm^-2. Converted to Wm^2.
                modelData = convertTimeIntegratedToNormal(modelData, modelHour)
            # end of if convertTI2N:
            if sign == -1:
                # Changing Sign and making OLR data Positive
                modelData = modelData * (-1)
            # end of if sign == -1:

            # anomaly
            if modelData.shape == climatologyData.shape:
                # calculate anomaly
                anomaly = modelData - climatologyData
            else:
                clim_grid = climatologyData.getGrid()
                data_grid = modelData.getGrid()
                if cregrid and not dregrid:
                    # Regridding the climatology data
                    # Creating the horizontal lat,lon regrid
                    # Here 'clim_grid' is the source and 'data_grid' is the target
                    if not regridfunc:
                        regridfunc = Horizontal(clim_grid, data_grid)
                    # end of if not regridfunc:
                    climatologyData = regridfunc(climatologyData)
                elif dregrid and not cregrid:
                    # Regridding the model/obs data
                    # Creating the horizontal lat,lon regrid
                    # Here 'data_grid' is the source and 'clim_grid' is the target
                    if not regridfunc:
                        regridfunc = Horizontal(data_grid, clim_grid)
                        # update the regridded data axis
                        latAxis = climatologyData.getLatitude()
                        lonAxis = climatologyData.getLongitude()
                        levAxis = climatologyData.getLevel()
                    # end of if not regridfunc:
                    modelData = regridfunc(modelData)
                elif dregrid and cregrid:
                    raise ValueError("Can not do both 'cregrid' and 'dregrid'. \
                                         Make one option as False.")
                elif not dregrid and not cregrid:
                    print "model data shape ", modelData.shape
                    print "climatology data shape ", climatologyData.shape
                    raise ValueError("model data and climatology data shapes are mis-match.")
                # end of if cregrid and not dregrid:
                # calculate anomaly for regridded data sets.
                anomaly = modelData - climatologyData
            # end of if data.shape == climatology.shape:
            # make free memory
            del modelData, climatologyData

            mstart = timobj._getDayCountOfYear(mdate, year=modelFirstYear)
            startDayOfYear = '%s-1-1' % str(modelFirstYear)
            dailyAnomalyTime = timobj._generateTimeAxis([mstart], startDayOfYear)

            # setting model time axis to the anomaly
            # reshape the anomaly to set timeAxis
            anoshape = list(anomaly.shape)
            anoshape.insert(0, 1)
            anomaly = anomaly.reshape(anoshape)
            # get the needed axis list
            if len(anoshape) == 3:
                axislist = (dailyAnomalyTime, latAxis, lonAxis)
            elif len(anoshape) == 4:
                axislist = (dailyAnomalyTime, levAxis, latAxis, lonAxis)
            # end of if len(anoshape) == 3:
            axislist = [axis for axis in axislist if axis]
            # set the axis information to the anomaly
            anomaly.setAxisList(axislist)
            if ovar:
                anomaly.id = ovar
            else:
                anomaly.id = mvar
            #anomaly.comments = 'monthly mean anomaly of %s model data of %s' % (modelName, year)

            # check the file status is closed or not. This is cdms2 fileobj.
            if anomalyFile._status_ == 'closed':
                # file is closed, so reopen it in append mode.
                #
                anomalyFile = cdms2.open(anomalyFilePath, 'a')
            # end of  if anomalyFile.closed:
            anomalyFile.write(anomaly)
            anomalyFile.close()
            ### file has to close inside the modelTime loop itself.
            # Otherwise if we run a big year data in loop,
            # it may get failure to write when system crashes.
            # If we close the file obj inside loop, the previous loop anomaly work
            # has been saved/written into the fileobj. So be cool.
            ###
            # make memory free
            del anomaly

            if __showStatusBar:
                preview = statusbar(modelTime.index(mdate), total=len(modelTime),
                                                   title='Anomaly', prev=preview)
           # end of if __showStatusBar:
        # end of for mdate in modelTime:
        print
    # end of for globalvar in totalvars.itervalues():
# end of def genDailyAnomalyFiles(...):

if __name__ == '__main__':

    if len(models) == len(climatologies) == 1:
        print "Obtained one model and one climatology"
    elif len(models) == len(climatologies):
        print "Obtained %d models and climatologies" % len(models)
    else:
        print "Obtained %d models and %d climatologies" % (len(models),
                                                        len(climatologies))
    for model in models:
        for climatology in climatologies:
            if model.count == climatology.count:
                # generate the climatology regrid path which has already
                # created
                climatologyRegridPath = os.path.join(processfilesPath,
                    model.name, 'Regrid', 'Climatology', climatology.name)
                if climatology.dfile:
                    # calling the genDailyAnomalyDirs function to do process
                    genDailyAnomalyDirs(model.name, model.path, model.hour,
                                    climatologyRegridPath, climatology.dfile,
                                    climatology.year)
                else:
                    print "In configure.txt climpartialdayfile not mentioned. \
                           So can not compute daily anomaly."
            else:
                pass
                # climatology configuration and model data configuration are
                # not equal in the text file handle this case, in diff manner.
                # The same loop should works.
                # But need to check all the cases.
    # end of for model in models:
    print "Done! Creation of Daily Anomaly netCdf Files"
# end of if __name__ == '__main__':


