"""
.. module:: compute_month_fcst_sys_error.py
   :synopsis: This script should calculate the fcstsyserr for every month and
              store it as nc files in the appropriate directories.
.. moduleauthor:: Arulalan.T <arulalant@gmail.com>

"""

import os
import sys
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
from diag_setup.varsdict import variables
from diag_setup.globalconfig import models, processfilesPath
from diag_setup.gendir import createDirsIfNotExists
import diag_setup.netcdf_settings

# create time utility object
timobj = TimeUtility()

# timeAxis check value to skip the fcstsyserr process for the existing month
# in the mean nc file
__timeCheck__ = True


def genMonthFcstSysErrDirs(modelname, modelpath, modelhour):
    """
    :func:`genMonthFcstSysErrDirs` : It should generate the directory structure
            whenever it needs. It reads the timeAxis information of the
            model data xml file(which is updating it by cdscan), and once
            the full months is completed, then it should check either that
            month directory is empty or not.

            case 1: If that directory is empty means, it should call the
                    function called `genMonthFcstSysErrFiles`, to calculate
                    the mean analysis and fcstsyserr for that month and should
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

    # create modelname, fcstsyserr directories if it is not exists
    childMeanPath = createDirsIfNotExists(processfilesPath,
                                         [modelname, 'FcstSysErr'])

    for year in availableMonths:
        # get the months dictionary
        monthdic = availableMonths.get(year)
        # sort the months in correct order
        months = timobj._sortMonths(monthdic.keys())
        year = str(year)
        # create Mean Root Year,Month directories if it is not exists
        meanFcstSysErrPath = createDirsIfNotExists(childMeanPath,
                                                  [year, 'Month'])
        # generate mean month path
        meanPath = os.path.join(processfilesPath, modelname, 'Mean',
                                                      year, 'Month')
        for month in months:
            # get the start & end date of the month
            sedate = monthdic.get(month)
            month = month.lower()
            # combaine month and its startdate & enddate within tuple
            monthdate = (month, sedate)
            # calling below function to create all nc files in mean analysis
            # and fcst hours directories
            genMonthFcstSysErrFiles(meanFcstSysErrPath, meanPath, monthdate,
                               year, modelhour, modelName = modelname,
                               modelXmlObj = xmlobj)
        # end of for month in months:
        # close all the opened xml file objects
        xmlobj.closeXmlObjs()
    # end of for year in availableMonths.keys():
# end of def genMonthFcstSysErrDirs()

def genMonthFcstSysErrFiles(meanFcstSysErrPath, meanPath, monthdate, year,
                                                     modelhour, **model):
    """
    :func:`genMonthFcstSysErrFiles` : It should calculate mean analysis &
            fcstsyserr for the passed month (of year) and process it. Finally
            stores it as nc files in corresponding directory path which are
            passed in this function args.

    Inputs : meanFcstSysErrPath is the absolute path where the processed mean
             fcstsyserr nc files are going to store.
             meanPath is the absolute path (partial path) where the processed
             monthly mean analysis and fcst hour nc files were stored already.
             monthdate (which contains monthname, startdate & enddate) and
             year are the inputs to extract the monthly data.
             modelhour is the list of model data hours, which will become
             part of the directory structure.

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

    Outputs : It should create mean forecast systematic error for all the
              available variables in the vars.txt file & store it as nc file
              formate in the proper directories structure
              (modelname, process name, year, month and then hours hierarchy).

    Written By : Arulalan.T

    Date : 08.09.2011
    Updated : 08.12.2011

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
    # end of if not modelXmlObj:
    month = monthdate[0]
    # get the startdate, enddate of this month for both model & climatolgy
    modelDataTimeRange = monthdate[1]

    anlvariables = xmlobj.listvariable(Type = 'a')
    meanAnalysisPath = os.path.join(meanPath, 'Analysis')

    if not os.path.isdir(meanAnalysisPath):
        raise RuntimeError("The monthly mean analysis directory doesnt \
                           exists in the path %s " % (meanAnalysisPath))

    # get the nc files name of mean analysis
    anlfiles = [f for f in os.listdir(meanAnalysisPath) if f.endswith('.nc')]

    if not anlfiles:
        raise RuntimeError("monthly mean analysis directory is empty. \
                 So couldnt compute forecast systematic error. Stopping  \
                 the process for %s month" % (month))

    # get the namedtuple object from the global 'vars.txt' file
    totalvars = variables.get(modelName)

    for globalvar in totalvars.itervalues():
        # get the model var name
        mvar = globalvar.model_var

        if not mvar in anlvariables:
            print "The variable '%s' is not available in the xml 'anl' file object" % mvar
            print "So skipping the mean fcst systematic error processes \
                   for the variable '%s' which is one of the keys of the \
                   variables dictionary" % mvar
            continue
        # end of if not mvar in allvariables:

        print "Collecting model mean analysis data of variable '%s' for the \
                                      %s month %s year" % (mvar, month, year)
        # partial nc file name
        pFileName = mvar + '_'+ modelName + '_' + year
        # generate the mean analysis nc file name
        analysisFileName = pFileName + '_mean_analysis.nc'
        # open the monthly mean analysis nc file
        analysisFile = cdms2.open(meanAnalysisPath + '/' + analysisFileName, 'r')
        try:
            # get the model data for this month alone (monthly mean analysis)
            meanAnalysis = analysisFile(mvar, time = modelDataTimeRange[0])
        except:
            print "Coundn't get the analysis data of %s var %s time" \
                                        % (mvar, modelDataTimeRange[0])
            print "So skipping the fcstsyserr and mean analysis processes\
                       for the '%s' variable" % mvar
            continue
        finally:
            analysisFile.close()
        # end of try:
        # extracting units from the title of the data
        title = meanAnalysis.title
        stitle = title.find('[')
        etitle = title.find(']')
        if stitle!= -1 and etitle!= -1:
            varunits = title[stitle + 1: etitle]
        else:
            varunits = ''
        # store mean analysis into proper nc file
        modelLevel = meanAnalysis.getLevel()
        modelLatitude = meanAnalysis.getLatitude()
        modelLongitude = meanAnalysis.getLongitude()
        print "\n monthly time axis has been copied from the mean analysis"
        meanTime = meanAnalysis.getTime()

        for hr in modelhour:
            fname = 'f' + hr + 'hr'
            fcstvariables = xmlobj.listvariable(Type = 'f', hour = hr)
            if not mvar in fcstvariables:
                print "The variable '%s' is not available in the xml 'f%s hr' file object" % (hr, mvar)
                print "So skipping the mean fcst systematic error processes \
                       for the variable '%s' which is one of the keys of the \
                       variables dictionary" % mvar
                continue
            # end of if not mvar in allvariables:

            meanFcstHrPath = os.path.join(meanPath, hr)
            # get the nc files name of mean forecast value
            fcstfiles = [f for f in os.listdir(meanFcstHrPath) if f.endswith('.nc')]

            if not fcstfiles:
                print " monthly mean forecast %s hour directory is empty. \
                        So couldnt compute forecast systematic error. \
                        Stopping the process for %s month" % (hr, month)
                continue
            # end of  if not fcstfiles:

            # create fcst sys err hour directory if it is not exists
            meanFcstSysErrHrPath = createDirsIfNotExists(meanFcstSysErrPath, hr)

            # get the nc files name of mean fcstsyserr
            ncfiles = [f for f in os.listdir(meanFcstSysErrHrPath) if f.endswith('.nc')]
            # make ncfiles for fcst as dictionary with key as var name
            ncfiledic = {}
            for ncfile in ncfiles:
                var = ncfile.split('_')[0]
                ncfiledic[var] = ncfile
            # make memory free
            del ncfiles

            # store fcstsyserr into proper nc file
            if mvar in ncfiledic:
                fcstsyserrFileName = ncfiledic.get(mvar)
                fcstFilePath = meanFcstSysErrHrPath + '/' + fcstsyserrFileName
                try:
                    # open nc file in append mode
                    fcstsyserrFile = cdms2.open(fcstFilePath, 'a')
                    # get the ncfile timeAxis
                    fileTime = fcstsyserrFile[mvar].getTime()
                    # Do check either this month timeAxis is already exists in
                    # the nc file's timeAxis or not. If exists means skip it.
                    if __timeCheck__:
                        if modelDataTimeRange[0] in fileTime.asComponentTime():
                            print "The fcstsyserr %s is already exists in the \
                                   file %s. So skipping var '%s' " % \
                                   (fname, fcstsyserrFileName, mvar)
                            fcstsyserrFile.close()
                            continue
                    # end of if __timeCheck__:
                except cdms2.error.CDMSError, AttributeError:
                    # if it getting this error means, it may not written
                    # properly. So open nc file in write mode freshly.
                    print "Got Problem. nc file is correpted at last time. \
                       May be lost the previous months data.\
                       Now creating same nc file '%s' freshly w.r.t current \
                       month %s" % (fcstsyserrFileName, month)
                    fcstsyserrFile = cdms2.open(fcstFilePath, 'w')
            else:
                # generate the nc filename
                fcstsyserrFileName = pFileName + '_mean_fcstsyserr_' + fname + '.nc'
                fcstFilePath = meanFcstSysErrHrPath + '/' + fcstsyserrFileName
                # open new nc file in write mode
                fcstsyserrFile = cdms2.open(fcstFilePath, 'w')
            # end of if mvar in ncfiledic:

            # generate the mean fcst nc file name
            fcstFile = pFileName + '_mean_' + fname + '.nc'
            meanFcstPath = os.path.join(meanPath, hr)
            fcstFile = cdms2.open(meanFcstPath + '/' + fcstFile, 'r')

            try:
                # get the climatolgy data for this month alone
                meanFcst = fcstFile(mvar, time = modelDataTimeRange[0])
            except:
                print "Coundn't get the climatolgy data for the variable %s and \
                       time %s " % (mvar, modelDataTimeRange[0])
                print "So skipping fcstsyserr for the variable %s" % mvar
                continue
            finally:
                fcstFile.close()
            # end of try:
            print "Calculating Monthly fcstsyserr for '%s' hour" % hr
            # fcstsyserr
            fcstsyserr = meanFcst - meanAnalysis
            # make memory free
            del meanFcst

            # setting model time axis to the fcstsyserr
            if modelLevel:
                fcstsyserr.setAxisList([meanTime, modelLevel, modelLatitude,
                                                             modelLongitude])
            else:
                fcstsyserr.setAxisList([meanTime, modelLatitude,
                                                 modelLongitude])
            fcstsyserr.id = mvar
            fcstsyserr.units = varunits
            fcstsyserr.long_name = title
            fcstsyserr.comments = 'monthly mean fcstsyserr of %s hour of %s model data of %s' % (hr, modelName, year)

            print "Writing mean fcstsyserr into %s file \n" % (fcstsyserrFileName)
            fcstsyserrFile.write(fcstsyserr)
            fcstsyserrFile.close()
            # make memory free
            del fcstsyserr
        # end of for hr in modelhour:
        # make memory free
        del meanAnalysis
    # end of for globalvar in totalvars.itervalues():
# end of def genMonthFcstSysErrFiles(...):

if __name__ == '__main__':

    for model in models:
        # calling the genMonthFcstSysErrDirs function to do process
        genMonthFcstSysErrDirs(model.name, model.path, model.hour)
    # end of for model in models:
    print "Done! Creation of Monthly Mean Fcst Systematic Error netCdf Files"
# end of if __name__ == '__main__':
