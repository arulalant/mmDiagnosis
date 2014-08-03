"""
.. module:: compute_month_mean.py
   :synopsis: This script should calculate the mean analysis and mean fcst
              for every month and store it as nc files in the appropriate
              directories.
.. moduleauthor:: Arulalan.T <arulalant@gmail.com>

"""

import os
import sys
import cdms2
import cdutil
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

# timeAxis check value to skip the mean process for the existing month in
# the mean nc file
__timeCheck__ = True


def genMonthMeanDirs(modelname, modelpath, modelhour):
    """
    :func:`genMonthMeanDirs` : It should generate the directory structure
            whenever it needs. It reads the timeAxis information of the
            model data xml file(which is updating it by cdscan), and once
            the full months is completed, then it should check either that
            month directory is empty or not.

            case 1: If that directory is empty means, it should call the
                    function called `genMonthMeanFiles`, to calculate
                    the mean analysis and anomaly for that month and should
                    store the processed files in side that directory.

            case 2: If that directory is non empty means,
                    ****have to update*****

    Inputs : modelname is the model data name, which will become part of the
             directory structure.
             modelpath is the absolute path of data where the model xml files
             are located.
             climatolgyyear is the year of climatolgy data.
             climregridpath is the absolute path of the climatolgy regridded
             path w.r.t to this model data resolution (both horizontal and
             vertical)
             climpfilename is the climatolgy Partial File Name to combine the
             this passed name with (at the end) of the climatolgy var name to
             open the climatolgy files.

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

    # create modelname, Mean directories if it is not exists
    childMeanPath = createDirsIfNotExists(processfilesPath,
                                         [modelname, 'Mean'])
    listTypeHour = [('a', None)]
    for hr in modelhour:
        listTypeHour.append(('f', hr))

    for year in availableMonths:
        # get the months dictionary
        monthdic = availableMonths.get(year)
        # sort the months in correct order
        months = timobj._sortMonths(monthdic.keys())
        year = str(year)
        # create Mean Root Year,Month directories if it is not exists
        meanMonthPath = createDirsIfNotExists(childMeanPath,
                                                  [year, 'Month'])
        for month in months:
            # get the start & end date of the month
            sedate = monthdic.get(month)
            month = month.lower()
            # combaine month and its startdate & enddate within tuple
            monthdate = (month, sedate)
            # calling below function to create all nc files in mean analysis
            # and fcst hours directories
            genMonthMeanFiles(meanMonthPath, monthdate, year,
                              typehour = listTypeHour, modelName = modelname,
                              modelXmlObj = xmlobj)
        # end of for month in months:
        # close all the opened xml file objects
        xmlobj.closeXmlObjs()
    # end of for year in availableMonths.keys():
# end of def genMonthMeanDirs()

def genMonthMeanFiles(meanMonthPath, monthdate, year, typehour, **model):
    """
    :func:`genMonthMeanFiles` : It should calculate monthly mean analysis &
            monthly mean forecast hours value for the month (of year). Finally
            stores it as nc files in corresponding directory path which are
            passed in this function args.

    Inputs : meanMonthPath is the absolute path where the processed month mean
             analysis & fcst hour nc files are going to store.
             monthdate (which contains monthname, startdate & enddate) and
             year are the inputs to extract the monthly data.
             typehour is tuple which has the type key character and fcst hour
             to create sub directories inside mean directory.

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

    Outputs : It should create monthly mean analysis and monthly mean forecast
              hours for all the available variables in the vars.txt file &
              store it as nc file formate in the proper directories structure
              (modelname, process name, year, month and then
              [Analysis or hours] hierarchy).

    Written By : Arulalan.T

    Date : 08.09.2011
    Updated : 06.12.2011

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

    for typ, hr in typehour:
        if typ == 'a':
            name = 'Analysis'
            fname = 'analysis'
        else:
            name = hr
            fname = 'f' + hr + 'hr'
        # create Mean Sub Month directory if it is not exists
        meanPath = createDirsIfNotExists(meanMonthPath, name)
        # get the nc files name
        ncfiles = [f for f in os.listdir(meanPath) if f.endswith('.nc')]
        # make ncfiles as dictionary with key as var name
        ncfiledic = {}
        for ncfile in ncfiles:
            var = ncfile.split('_')[0]
            ncfiledic[var] = ncfile
        # make memory free
        del ncfiles

        anlvariables = xmlobj.listvariable(Type = typ, hour = hr)

        # get the namedtuple object from the global 'vars.txt' file
        totalvars = variables.get(modelName)
        for globalvar in totalvars.itervalues():
            # get the model var name
            mvar = globalvar.model_var

            if not mvar in anlvariables:
                print "The variable %s is not available in the xml anl file object" % mvar
                print "So skipping the mean analysis processes \
                       for this variable %s which is one of the keys of the \
                       variables dictionary" % mvar
                continue
            # end of if not mvar in allvariables:

            if mvar in ncfiledic:
                meanFileName = ncfiledic.get(mvar)
                try:
                    # open nc file in append mode
                    meanFile = cdms2.open(meanPath + '/' + meanFileName, 'a')
                    # get the ncfile timeAxis
                    fileTime = meanFile[mvar].getTime()
                    # Do check either this month timeAxis is already exists in
                    # the nc file's timeAxis or not. If exists means skip it.
                    if __timeCheck__:
                        if modelDataTimeRange[0] in fileTime.asComponentTime():
                            print "The mean %s is already exists in the \
                                   file %s. So skipping var '%s' " % \
                                   (fname, meanFileName, mvar)
                            meanFile.close()
                            continue
                    # end of if __timeCheck__:
                except cdms2.error.CDMSError, AttributeError:
                    # if it getting this error means, it may not written
                    # properly. So open nc file in write mode freshly.
                    print "Got Problem. nc file is correpted at last time. \
                           May be lost the previous months data.\
                           Now creating same nc file '%s' freshly w.r.t current \
                           month %s" % (meanFileName, month)
                    meanFile = cdms2.open(meanPath + '/' + meanFileName, 'w')

            else:
                # generate the nc filename
                meanFileName = mvar + '_'+ modelName + '_' + year
                meanFileName += '_mean_' + fname + '.nc'
                # open new nc file in write mode
                meanFile = cdms2.open(meanPath + '/' + meanFileName, 'w')
            # end of if mvar in ncfiledic:

            print "Collecting modeldata of variable '%s' for the %s month %s \
                        year for process '%s' " % (mvar, month, year, fname)

            try:
                # get the model data for this month alone
                modelData = xmlobj.getData(mvar, Type = typ, hour = hr,
                                           date = modelDataTimeRange)
            except:
                print "Coundn't get the analysis data of %s var %s time" \
                                            % (mvar, modelDataTimeRange)
                print "So skipping the anomaly and mean analysis processes\
                           for this variable %s" % mvar
                continue
            # end of try:
            # extracting units from the title of the data
            title = modelData.title
            stitle = title.find('[')
            etitle = title.find(']')
            if stitle!= -1 and etitle!= -1:
                varunits = title[stitle + 1: etitle]
            else:
                varunits = ''
            # store mean analysis into proper nc file
            modelLevel = modelData.getLevel()
            modelLatitude = modelData.getLatitude()
            modelLongitude = modelData.getLongitude()
            print "\n monthly time axis has created"
            meanTime = timobj._generateMonthlyMeanTimeAxis(modelDataTimeRange[0],
                                                        modelDataTimeRange[1])
            print "Calculating Mean "
            meanVar = cdutil.averager(modelData, axis = 't', weights = 'equal')
            # make memory free
            del modelData
            meanVar.id = mvar
            meanVar.units = varunits
            meanVar.long_name = title
            meanVar.comments = 'monthly mean %s of %s model data of %s' % (fname, modelName, year)

            # create first dimension for the time axis.
            mshape = list(meanVar.shape)
            mshape.insert(0, 1)
            newshape = tuple(mshape)
            # setting all the axis dimension to the meanVar variable
            meanVar = meanVar.reshape(newshape)
            if modelLevel:
                meanVar.setAxisList([meanTime, modelLevel, modelLatitude,
                                                          modelLongitude])
            else:
                meanVar.setAxisList([meanTime, modelLatitude, modelLongitude])


            print "Writing mean %s into %s file \n" % (fname, meanFileName)
            meanFile.write(meanVar)
            meanFile.close()
            # make memory free
            del meanVar
        # end of for globalvar in totalvars.itervalues():
# end of def genMonthMeanFiles(...):

if __name__ == '__main__':

    for model in models:
        # calling the genMonthMeanDirs function to do process
        genMonthMeanDirs(model.name, model.path, model.hour)
    # end of for model in models:
    print "Done! Creation of Monthly Mean Analysis & Mean Fcst Hours netCdf Files"
# end of if __name__ == '__main__':
