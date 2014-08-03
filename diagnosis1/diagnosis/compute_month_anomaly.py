"""
.. module:: compute_month_anomaly.py
   :synopsis: This script should calculate the anomaly for every month and
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
from diag_setup.globalconfig import models, climatologies, processfilesPath
from diag_setup.gendir import createDirsIfNotExists
import diag_setup.netcdf_settings

# create time utility object
timobj = TimeUtility()

# timeAxis check value to skip the anomaly process for the existing month in
# the mean nc file
__timeCheck__ = True


def genMonthAnomalyDirs(modelname, modelpath, climregridpath, climpfilename,
                                                           climatologyyear):
    """
    :func:`genMonthAnomalyDirs` : It should generate the directory structure
            whenever it needs. It reads the timeAxis information of the
            model data xml file(which is updating it by cdscan), and once
            the full months is completed, then it should check either that
            month directory is empty or not.

            case 1: If that directory is empty means, it should call the
                    function called `genMonthAnomalyFiles`, to calculate
                    the mean analysis and anomaly for that month and should
                    store the processed files in side that directory.

            case 2: If that directory is non empty means,
                    ****have to update*****

    Inputs : modelname is the model data name, which will become part of the
             directory structure.
             modelpath is the absolute path of data where the model xml files
             are located.
             climregridpath is the absolute path of the climatolgy regridded
             path w.r.t to this model data resolution (both horizontal and
             vertical)
             climpfilename is the climatolgy Partial File Name to combine the
             this passed name with (at the end) of the climatolgy var name to
             open the climatolgy files.
             climatolgyyear is the year of climatolgy data.

    Outputs : It should create the directory structure in the processfilesPath
              and create the processed nc files.

    Written By : Arulalan.T

    Date : 01.12.2011

    """

    xmlobj = xml_data_access.GribXmlAccess(modelpath)
    # get one model var name from the global 'vars.txt' file
    mvar = variables.get(modelname).values()[0].model_var
    modeldataset = xmlobj[mvar, 'a']
    # get the timeAxis of modeldata set and correct its bounds
    modeltime = timobj._correctTimeAxis(modeldataset.getTime())
    # get the fully available months
    availableMonths = timobj.getTimeAxisFullMonths(modeltime)

    # create modelname, Anomaly directories if it is not exists
    childMeanPath = createDirsIfNotExists(processfilesPath,
                                         [modelname, 'Anomaly'])

    for year in availableMonths:
        # get the months dictionary
        monthdic = availableMonths.get(year)
        # sort the months in correct order
        months = timobj._sortMonths(monthdic.keys())
        year = str(year)
        # create Mean Root Year,Month directories if it is not exists
        meanAnomalyPath = createDirsIfNotExists(childMeanPath,
                                                  [year, 'Month', 'Analysis'])
        # generate mean analysis month path
        meanAnalysisPath = os.path.join(processfilesPath, modelname, 'Mean',
                                                   year, 'Month', 'Analysis')
        for month in months:
            # get the start & end date of the month
            sedate = monthdic.get(month)
            month = month.lower()
            # combaine month and its startdate & enddate within tuple
            monthdate = (month, sedate)
            # calling function to create all nc files mean monthly anomaly
            genMonthAnomalyFiles(meanAnomalyPath, meanAnalysisPath,
                             climregridpath, climpfilename, climatologyyear,
                              monthdate, year, modelName = modelname,
                              modelXmlObj = xmlobj)
        # end of for month in months:
        # close all the opened xml file objects
        xmlobj.closeXmlObjs()
    # end of for year in availableMonths.keys():
# end of def genMonthAnomalyDirs()

def genMonthAnomalyFiles(meanAnomalyPath, meanAnalysisPath, climRegridPath,
                                            climPFileName, climatologyYear,
                                                  monthdate, year, **model):
    """
    :func:`genMonthAnomalyFiles` : It should calculate monthly mean anomaly
            from the monthly mean analysis and monthly mean climatolgy,
            for the month (of year) and process it. Finally
            stores it as nc files in corresponding directory path which are
            passed in this function args.

    Inputs : meanAnomalyPath is the absolute path where the processed mean
             anomaly nc files are going to store.
             meanAnalysisPath is the absolute path where the processed mean
             analysis nc files were already stored.
             climRegridPath is the absolute path where the regridded monthly
             mean climatologies (w.r.t the model vertical resolution)
             nc files were already stored.
             climPFileName is the partial nc filename of the climatolgy.
             climatologyYear is the year of the climatolgy to access it.
             monthdate (which contains monthname, startdate & enddate) and
             year are the inputs to extract the monthly data.

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

    Outputs : It should create mean anomaly for the particular variables which
              are all set the clim_var option in the vars.txt file. Finally
              store it as nc file formate in the proper directories structure
              (modelname, process name, year and then month hierarchy).

    Written By : Arulalan.T

    Date : 08.09.2011
    Updated : 07.12.2011

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
    if not os.path.isdir(meanAnalysisPath):
        raise RuntimeError("The monthly mean analysis directory doesnt \
                           exists in the path %s " % (meanAnalysisPath))
    # get the nc files name of mean analysis
    anlfiles = [f for f in os.listdir(meanAnalysisPath) if f.endswith('.nc')]
    if not anlfiles:
        raise RuntimeError("monthly mean analysis directory is empty. \
                 So couldnt compute anomaly. Stopping the process \
                 for %s month" % (month))

    # get the nc files name of mean anomaly
    ncfiles = [f for f in os.listdir(meanAnomalyPath) if f.endswith('.nc')]
    # make ncfiles as dictionary with key as var name
    ncfiledic = {}
    for ncfile in ncfiles:
        var = ncfile.split('_')[0]
        ncfiledic[var] = ncfile
    # make memory free
    del ncfiles

    anlvariables = xmlobj.listvariable(Type = 'a')

    # get the namedtuple object from the global 'vars.txt' file
    totalvars = variables.get(modelName)
    for globalvar in totalvars.itervalues():
        # get the model var name
        mvar = globalvar.model_var
        # get the climatolgy var name
        cvar = globalvar.clim_var

        if not cvar:
            print "Climatology var name is empty string. So skipping anomaly \
                process for %s model var name " % mvar
            continue
        # end of if not cvar:

        if not mvar in anlvariables:
            print "The variable %s is not available in the xml anl file object" % mvar
            print "So skipping the anomaly and mean analysis processes \
                   for this variable %s which is one of the keys of the \
                   variables dictionary" % mvar
            continue
        # end of if not mvar in allvariables:

        # partial nc file name
        pFileName = mvar + '_'+ modelName + '_' + year

        # store anomaly into proper nc file
        if mvar in ncfiledic:
            anomalyFileName = ncfiledic.get(mvar)
            meanAnomalyFilePath = meanAnomalyPath + '/' + anomalyFileName
            try:
                # open nc file in append mode
                anomalyFile = cdms2.open(meanAnomalyFilePath, 'a')
                # get the ncfile timeAxis
                fileTime = anomalyFile[mvar].getTime()
                # Do check either this month timeAxis is already exists in
                # the nc file's timeAxis or not. If exists means skip it.
                if __timeCheck__:
                    if modelDataTimeRange[0] in fileTime.asComponentTime():
                        print "The mean anomaly is already exists in the \
                               file %s. So skipping var '%s' " % \
                                        (anomalyFileName, mvar)
                        anomalyFile.close()
                        continue
                # end of if __timeCheck__:
            except cdms2.error.CDMSError, AttributeError:
                # if it getting this error means, it may not written
                # properly. So open nc file in write mode freshly.
                print "Got Problem. nc file is correpted at last time. \
                       May be lost the previous months data.\
                       Now creating same nc file '%s' freshly w.r.t current \
                       month %s" % (anomalyFileName, month)
                anomalyFile = cdms2.open(meanAnomalyFilePath, 'w')
        else:
            # generate the nc filename
            anomalyFileName = pFileName + '_mean_anomaly.nc'
            meanAnomalyFilePath = meanAnomalyPath + '/' + anomalyFileName
            # open new nc file in write mode
            anomalyFile = cdms2.open(meanAnomalyFilePath, 'w')
        # end of if mvar in ncfiledic:

        print "Collecting model mean analysis data of variable '%s' for the \
                                      %s month %s year" % (mvar, month, year)
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
            print "So skipping the anomaly and mean analysis processes\
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

        # generate the climatology file name
        climatologyFile = cvar + climPFileName
        cfile = cdms2.open(climRegridPath + '/' + climatologyFile, 'r')
        climDataTimeRange = timobj.monthFirstLast(monthdate[0], climatologyYear)

        try:
            # get the climatolgy data for this month alone
            meanClimatology = cfile(cvar, time = climDataTimeRange[0])
        except:
            print "Coundn't get the climatolgy data for the variable %s and \
                   time %s " % (cvar, climDataTimeRange[0])
            print "So skipping anomaly for the variable %s" % mvar
            continue
        finally:
            cfile.close()
        # end of try:
        print "Calculating Monthly Anomaly"
        # anomaly
        anomaly = meanAnalysis - meanClimatology
        # make memory free
        del meanAnalysis, meanClimatology

        # setting model time axis to the anomaly
        if modelLevel:
            anomaly.setAxisList([meanTime, modelLevel, modelLatitude,
                                                            modelLongitude])
        else:
            anomaly.setAxisList([meanTime, modelLatitude, modelLongitude])
        anomaly.id = mvar
        anomaly.units = varunits
        anomaly.long_name = title
        anomaly.comments = 'monthly mean anomaly of %s model data of %s' % (modelName, year)

        print "Writing mean anomaly into %s file \n" % (anomalyFileName)
        anomalyFile.write(anomaly)
        anomalyFile.close()
        # make memory free
        del anomaly
    # end of for globalvar in totalvars.itervalues():
# end of def genMonthAnomalyFiles(...):

if __name__ == '__main__':

    if len(models) == len(climatologies) == 1:
        print "Obtained one model and one climatolgy"
    elif len(models) == len(climatologies):
        print "Obtained %d models and climatologies" % len(models)
    else:
        print "Obtained %d models and %d climatologies" % (len(models),
                                                        len(climatologies))
    for model in models:
        for climatolgy in climatologies:
            if model.count == climatolgy.count:
                # generate the climatolgy regrid path which has already
                # created
                climatologyRegridPath = os.path.join(processfilesPath,
                    model.name, 'Regrid', 'Climatology', climatolgy.name)
                if climatolgy.mfile:
                    # calling the genMonthAnomalyDirs function to do process
                    genMonthAnomalyDirs(model.name, model.path, climatologyRegridPath,
                                     climatolgy.mfile, climatolgy.year)
                else:
                    print "In configure.txt climpartialmonfile not mentioned. \
                           So can not compute monthly anomaly."
            else:
                pass
                # climatolgy configuration and model data configuration are
                # not equal in the text file handle this case, in diff manner.
                # The same loop should works.
                # But need to check all the cases.
    # end of for model in models:
    print "Done! Creation of Monthly Anomaly netCdf Files"
# end of if __name__ == '__main__':
