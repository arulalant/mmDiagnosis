"""
.. module::
   :synopsis:

Written by: Arulalan.T

Date: 20.04.2012

"""

import os
import sys
import numpy
import cdms2
import cdutil
import MV2
from genutil.statistics import correlation, std
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
import diagnosisutils.plot as plot
from diagnosisutils.regions import regions
from diag_setup.globalconfig import models, seasons, processfilesPath, \
                                plotsgraphsPath, obsrainfalls
from diag_setup.varsdict import variables
from diag_setup.gendir import createDirsIfNotExists
import diag_setup.netcdf_settings

# create time utility object
timobj = TimeUtility()

def _standardization(data, avgtype='temporal'):    
    
    if avgtype == 'temporal':                
        # Calculate the avg over time axis. 
        # so the mean val contains the lat x lon axis.                
        data_mean = cdutil.averager(data, axis = 't', weights = 'equal')                    
    elif avgtype == 'spatial':
        # Calculate the spatial mean. i.e. averge over the time, lat &
        # lon axies. so the mean val should be single real number. 
        #
        # first average over the time axis.        
        data_mean = cdutil.averager(data, axis = 't', weights = 'equal')        
        # then the averge over the lat,lon axis
        data_mean = cdutil.averager(data_mean, axis = 'yx', weights = None)                
    else:
        raise ValueError("No such type '%s' of average. \
                          Pass avg either temporal or spatial." % avgtype)
    # standardization of data. i.e. = x - mean(x)
    data = data - data_mean
    # make free memory 
    del data_mean
    # return the result data 
    return data
# end of def _standardization(data, avgtype='temporal'):

def genIndividualModelsMultiHoursTaylorDiagrams(vartype, modelname, modelpath, modelhour, 
                        reference, refstr='Obs', institution='', avg='spatial', 
                        normalization=True, monseason='month', region='CIndia'):
    """
    :func:`genIndividualModelsMultiHoursTaylorDiagrams`:

    """
    # pre defined 10 model color codes
    modelcolors = [241, 249, 242, 246, 250, 247, 243, 248, 250, 251]
    # forecast hours string 
    fcstdays = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']
    # get the region object for user passed region name
    myregion = regions[region]
    
    xmlobj = xml_data_access.GribXmlAccess(modelpath)
    # setting modlename to access the getRainfallDataPartners() method
    xmlobj.rainfallModel = modelname

    # generate the observation rainfall xml file path
    if reference in ['anl', 'analysis']:
        # get the analysis xml object
        refobj = xmlobj._getXmlAccessObj('anl')        
        # get the model variable name from the global variables, which
        # has set in the global 'vars.txt' file.
        referenceXmlVar = variables.get(modelname).get(vartype).model_var   
        # reference string in the legend
        # change reference string as 'Anl' if user not passed new string for that.
        refstr = 'Anl' if refstr == 'Obs' else refstr    
    else:
        # open the reference path file by cdms2 to access the data 
        refobj = cdms2.open(reference)
        # get the obs variable name from the global variables, which
        # has set in the global 'vars.txt' file.
        referenceXmlVar = variables.get(modelname).get(vartype).obs_var        
    
    if not referenceXmlVar:
        raise ValueError('reference xml var is None')
    
    # get the model variable name from the global variables, which
    # has set in the global 'vars.txt' file.
    fcstModelXmlVar = variables.get(modelname).get(vartype).model_var   
    # get the ref data info only. Not full data. i.e. Transiant object.
    ref_data = refobj[referenceXmlVar]
    # get the timeAxis of rainfall observation and correct its bounds
    ref_data_time = timobj._correctTimeAxis(ref_data.getTime())
    # get the fully available months
    availableMonths = timobj.getTimeAxisFullMonths(ref_data_time)

    for year in availableMonths:
        monthdic = availableMonths.get(year)                    
        year = str(year)
        
        # get the levels of the data 
        levels = ref_data.getLevel()
        if not levels:
            levels = [None]
        
        if monseason == 'season':
            # sort the months in correct order
            months = timobj._sortMonths(monthdic.keys())
            seasonCollections = {}
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
                # append the months as season name, season start date & 
                # season end date to the tmp dictionary.
                seasonCollections[seasonName] = (seasonMonthDate[0][1][0], 
                                                 seasonMonthDate[-1][1][1])
            # create the directory structure for season
            tyPath = createDirsIfNotExists(plotsgraphsPath,
                                   [modelname, 'Taylor', year, 'Season'])
            
            
        elif monseason == 'month':
            seasonCollections = monthdic
            # create the directory structure for month 
            tyPath = createDirsIfNotExists(plotsgraphsPath,
                                   [modelname, 'Taylor', year, 'Month'])    
        else:
            raise ValueError("Type '%s' not support" % monseason)
            
        for msname, dates in seasonCollections.iteritems():
            # create the least sub directory (month name or season name)
            outPath = createDirsIfNotExists(tyPath, [msname.lower(), 'Single', vartype])
            
            # reference startdate and enddate 
            m_startdate, m_enddate = dates            
            
            for lev in levels:                
                # get the reference data w.r.t time and region            
                if reference in ['anl', 'analysis']:
                    # the refobj is instance of GribXmlAccess. So access the data 
                    # by calling the 'getData' method.
                    ref_data = refobj.getXmlData(var = referenceXmlVar, 
                                        date = dates, level = lev, 
                                        region = myregion, squeeze = 1)
                    
                else:
                    # it must be cdms2 opened object only. So access the data as 
                    # it is.
                    ref_data = refobj(referenceXmlVar, myregion, time = dates, 
                                      level = lev, squeeze = 1) 
                
                # standardization of reference data. i.e. = x - mean(x)                                 
                ref_data = _standardization(ref_data, avg)
                
                # taylor input is list containing of list which contains the 
                # standard deviation and correlation values.
                taylorInput = []            
                refStdValue = std(ref_data, axis='tyx')
                # adding the observed (reference) point
                if normalization:
                    # normalization takes place. i.e. all the standard deviation
                    # values should be within 0 to 1 scale.
                    # so for the reference point's standard deviation is 1.
                    # also correlation of reference data and reference data is 1.
                    taylorInput.append([1, 1])
                else:
                    # here no normalization. So keeping the standard deviation 
                    # value as it is. Correlation of reference data and reference
                    # data is 1.
                    taylorInput.append([refStdValue.data, 1])
                
                for hr in modelhour:
                    # get the partners data of observation rainfall
                    # (i.e. get the model fcst rainfall)
                    print "Collecting fcst rainfall data for % hr of %s month \
                         of %s of %s model" % (hr, msname, year, modelname)

                    # write the fcst_data into nc appropriate file
                    # fastup way
                    # get the startdate, enddate of the season of fcst partner in model
                    p_startdate = xmlobj.findPartners(Type = 'anl',
                                        date = m_startdate, hour = hr)
                    p_enddate = xmlobj.findPartners(Type = 'anl',
                                        date = m_enddate, hour = hr)
                    
                    try:
                        # get the model's forecast data w.r.t partner's data, 
                        # hour & region 
                        fcst_data = xmlobj.getData(var = fcstModelXmlVar, 
                                  Type = 'fcst', date = (p_startdate, p_enddate),
                                  hour = hr, level = lev, region = myregion, 
                                  squeeze = 1)                    
                    except:
                        print "Couldn't get the fcst rainfall partner data \
                            w.r.t obs data b/w ", p_startdate, p_enddate
                        print "So skipping it"
                        continue
                    
                    # standardization of model forecast data. i.e. = x - mean(x)                                
                    fcst_data = _standardization(fcst_data, avg)
                    
                    # get the correlation value b/w reference data (either 
                    # obeservation or model analysis) and model forecast data.
                    corrValue = correlation(ref_data, fcst_data, axis = "tyx")
                    # get the standard deviation value of model forecast data
                    stdValue = std(fcst_data, axis='tyx')
                    # doing the normalization for std of forecast data. i.e. 
                    # make the standard deviation value of model forecast data 
                    # within o to 1 scale.
                    stdValue = stdValue.data/refStdValue.data if normalization else stdValue.data     
                    # store all the forecast hours data std and correlation value      
                    taylorInput.append([stdValue, corrValue.data])                
                # end of for hr in modelhour:            
                 
                # generate the title of the plot
                if reference in ['anl', 'analysis']:
                    title = 'Anl' + ' ('+ modelname + ') '
                else:
                    title = refstr + ' ('+ institution + ') ' + modelname
                
                title += ' ' + vartype.capitalize() + ' '
                if lev:
                    title += str(int(lev)) + 'hPa '
                title += region + ' ' + avg.capitalize() + ' ' + msname.upper() + ' ' + year
                # get the max std value from the taylorInput 2D list., which get
                # max value of fist dimension.
                maxstd = max(taylorInput)[0]
                # set the maximum limit of standard deviation.
                if normalization:
                    setmaxstd = float(round(maxstd, 1) + 0.2)
                    referenceVal = 1
                else:
                    setmaxstd = int(round(maxstd, 0) + 2)
                    referenceVal = refStdValue.data
                # model colors in ty 
                mcolors = modelcolors[:len(taylorInput)]
                # model symbols 
                msymbols = ["dot"]*len(taylorInput)
                # legend strings
                legstr = [refstr] + fcstdays[:len(modelhour)]
                # make the input data as masked variabe
                taylorInput = MV2.array(taylorInput)
                # plot & save the image
                plot.tylorPlot(taylorInput, reference = referenceVal,
                               maxvalue = setmaxstd, name = title,
                               colors = mcolors,
                               symbols = msymbols,
                               legendstrings = legstr,                           
                               path = outPath, 
                               png = 1, svg = 0)
            # end of for lev in levels:  
        # end of for month, dates in seasonCollections.iteritems():  
    # end of for year in availableMonths:
    refobj.close()
# end of def genIndividualModelsMultiHoursTaylorDiagrams(...):

def genIndividualHoursMultiModelsTaylorDiagrams(vartype, reference, 
                            refmodel='', refstr='Obs', institution='',
                        avg='spatial', normalization=True, 
                        monseason='month', region='CIndia'):
    """
    :func:`genIndividualHoursMultiModelsTaylorDiagrams`:
    
    01.06.2012
    """
    
    # pre defined 10 model color codes
    modelcolors = [241, 249, 242, 246, 250, 247, 243, 248, 250, 251]
    # get the region object for user passed region name and its 1 degree 
    # reduced region object     
    myregion = regions[region]
    myregion_1 = regions[region + '_1']
    
    if reference in ['anl', 'analysis']:
        # find out the reference model object from the available models
        model = [mod for mod in models if mod.name == refmodel]
        if model:
            # just get the model obj 
            model = model[0]
        else:
            raise ValueError("Passed reference model name does not exists,\
                              to choose analysis file ")
        # get the model xml collection of objects
        refxmlobj = xml_data_access.GribXmlAccess(model.path)
        # get the analysis xml object
        refobj = refxmlobj._getXmlAccessObj('anl')
        # get the model variable name from the global variables, which
        # has set in the global 'vars.txt' file.
        referenceXmlVar = variables.get(refmodel).get(vartype).model_var
    else:
        refobj = cdms2.open(reference)
        # get the obs variable name from the global variables, which
        # has set in the global 'vars.txt' file.
        referenceXmlVar = variables.get(refmodel).get(vartype).obs_var
                    
    # get the ref data info only. Not full data. i.e. Transiant object.
    ref_data = refobj[referenceXmlVar]    
    # get the timeAxis of rainfall observation and correct its bounds
    ref_data_time = timobj._correctTimeAxis(ref_data.getTime())
    # get the fully available months
    availableMonths = timobj.getTimeAxisFullMonths(ref_data_time)
    
        
    # create stdcorr axis which is the last/inner most dimension of the 
    # variable which will be generated by this function. It contains the 
    # standard_deviation_and_correlation values of all the models & obs/anl.
    stdcorrAxis = cdms2.createAxis([0, 1])
    stdcorrAxis.id = 'stdcorr'
    stdcorrAxis.long_name = 'standard_deviation_and_correlation'
    stdcorrAxis.namelist = "['std', 'corr']"
    
    for year in availableMonths:
        monthdic = availableMonths.get(year)                    
        year = str(year)   
        # sort the months in correct order.
        # Imp reason for sorting the months is when we append var into nc file 
        # the time series should be in accending order. Then only we can 
        # append the var in cdms2 var obj or/and the nc file.
        month_season_names = timobj._sortMonths(monthdic.keys())
        
        if monseason == 'season':
            
            seasonCollections = {}
            for seasonName, season in seasons.iteritems():
                # find out xml time axis months has the seasonal months or not
                seasonMonths = [month for smonth in season for month in month_season_names
                                if smonth[:3].lower() == month[:3].lower()]
                if len(seasonMonths) == len(season):
                    print "Got the seasonal months for %s season" % seasonName
                else:
                    print "Seasonal months are not available for %s season" % seasonName
                    continue
                # get the list of months of the season in order with its start &
                # end date
                seasonMonthDate = [(month, monthdic.get(month)) for month in month_season_names]
                if seasonName.isupper():
                    seasonName = seasonName.lower()
                # append the months as season name, season start date & 
                # season end date to the tmp dictionary.
                seasonCollections[seasonName] = (seasonMonthDate[0][1][0], 
                                                 seasonMonthDate[-1][1][1])
            # end of for loop
            month_season_names = seasonCollections.keys()
            # create the directory structure for season plot 
            tyPlotPath = createDirsIfNotExists(plotsgraphsPath,
                                   [refmodel, 'Taylor', year, 'Season'])
            # create the directory structure for season process  
            tyProcPath = createDirsIfNotExists(processfilesPath,
                                   [refmodel, 'Taylor', year, 'Season'])
            # create/generate nc file name 
            tyncfile = refmodel + '_Taylor_Inputs_' + region + '_' + avg.capitalize() + '_Seasons_' + year 
            
        elif monseason == 'month':
            seasonCollections = monthdic
            # create the directory structure for month plot 
            tyPlotPath = createDirsIfNotExists(plotsgraphsPath,
                                   [refmodel, 'Taylor', year, 'Month']) 
            # create the directory structure for month process
            tyProcPath = createDirsIfNotExists(processfilesPath,
                                   [refmodel, 'Taylor', year, 'Month']) 
            # create/generate nc file name 
            tyncfile = refmodel + '_Taylor_Inputs_' + region + '_' + avg.capitalize() + '_Months_' + year  
              
        else:
            raise ValueError("Type '%s' not support" % monseason)        
        
        if normalization:
            tyncfile += '_normalization' + '.nc'
        else:
            tyncfile += '.nc'
        # get the levels of the data 
        levels = ref_data.getLevel()
        # collect level axis info to store the std, corr values into nc file 
        levelAxis = ref_data.getLevel()
        if not levels:
            levels = [None]
            
        for msname in month_season_names:
            # loop through the sorted months/seasons name 
            
            # get the month's or season's startdate & enddate
            dates = seasonCollections.get(msname)

            # reference startdate and enddate 
            m_startdate, m_enddate = dates            
             
            # genearate time axis which is the first/ first outer most 
            # dimension of the variable which will be generated by this 
            # function. It contains the std, corr values of all the models & 
            # obs/anl. 
            if monseason == 'month':
                # generate time axis for monthly mean
                timeAxis = timobj._generateMonthlyMeanTimeAxis(m_startdate, m_enddate)                
            elif monseason == 'season':
                # generate time axis for seasonly mean
                # get the start & end day count of the year 
                m_startday = timobj._getDayCountOfYear(m_startdate)
                m_endday = timobj._getDayCountOfYear(m_enddate)
                # get the bounds for the season 
                m_bounds = timobj._generateBounds([m_startday, m_endday])                
                # generate the seasonly mean time axis 
                timeAxis = timobj._generateTimeAxis([m_startday], 
                              startdate = year + '-1-1', bounds = m_bounds)
            # collection store list of std, corr of forecast hours
            taylorInputFcstHoursCollection = []
            
            hours = []
            for hour in models[0].hour:
                # create the least sub directories of month name or season name
                outPlotPath = createDirsIfNotExists(tyPlotPath, [msname.lower(), 
                                         'MultiHours', str(hour), vartype])
                hour = int(hour)
                day = hour / 24.0
                # keep as float if day is not 24's multiple
                if not hour % 24.0:
                    day = int(day)
                hourname = 'D0' + str(day)                
                                         
                # collection store list of std, corr of levels
                taylorInputLevelsCollection = []
                for lev in levels:                
                    print "Collecting the reference data "
                    # get the reference data w.r.t time and region            
                    if reference in ['anl', 'analysis']:
                        # the refobj is instance of GribXmlAccess. So access the data 
                        # by calling the 'getData' method.
                        ref_data = refobj.getXmlData(var = referenceXmlVar, 
                                            date = dates, level = lev, 
                                            region = myregion, squeeze = 1)
                        # reference string in the legend.
                        # change reference string as 'Anl' if user not passed 
                        # new string for that.
                        refstr = 'Anl' if refstr == 'Obs' else refstr
                    else:
                        # it must be cdms2 opened object only. So access the data as 
                        # it is.
                        ref_data = refobj(referenceXmlVar, myregion, time = dates, 
                                          level = lev, squeeze = 1)                
                     
                    # standardization of reference data. i.e. = x - mean(x)                                
                    ref_data = _standardization(ref_data, avg)          
                        
                    # taylor input is list containing of list which contains the 
                    # standard deviation and correlation values.
                    taylorInput = [] 
                    nameslist = [refstr]           
                    refStdValue = std(ref_data, axis='tyx')
                    # reference data grid 
                    ref_data_grid = ref_data.getGrid()
                    # adding the observed (reference) point
                    if normalization:
                        # normalization takes place. i.e. all the standard deviation
                        # values should be within 0 to 1 scale.
                        # so for the reference point's standard deviation is 1.
                        # also correlation of reference data and reference data is 1.
                        taylorInput.append([1, 1])
                    else:
                        # here no normalization. So keeping the standard deviation 
                        # value as it is. Correlation of reference data and reference
                        # data is 1.
                        taylorInput.append([refStdValue.data, 1])

                    for model in models:
                        for obsrainfall in obsrainfalls:
                            if not (model.count == obsrainfall.count):
                                pass
                                continue
                            else:
                                xmlobj = xml_data_access.GribXmlAccess(model.path)
                                xmlobj.rainfallModel = model.name                            
                                
                                # get the model partners data of observation rainfall
                                # (i.e. get the model fcst rainfall)
                                print "Collecting fcst rainfall data for % hr of %s month \
                                     of %s of %s model" % (str(hour), msname, year, model.name)

                                # get the startdate, enddate of the season of fcst partner in model
                                p_startdate = xmlobj.findPartners(Type = 'a',
                                                date = m_startdate, hour = hour)
                                p_enddate = xmlobj.findPartners(Type = 'a',
                                                date = m_enddate, hour = hour)
                                print p_startdate, p_enddate
                                # get the model's forecast variabe name
                                print model.name
                                fcstModelXmlVar = variables.get(model.name).get(vartype).model_var
                                
                                if vartype == 'rainfall': 
                                    # for obeservation extract exact region 
                                    regiontype = myregion
                                else:
                                    # for analysis, we need to extract extended 
                                    # by 1 degree than exact region. So that it 
                                    # will be easy to regrid.
                                    regiontype = myregion_1
                                try:
                                    fcst_data = xmlobj.getData(var = fcstModelXmlVar,
                                                     Type = 'f',
                                                     date = (p_startdate, p_enddate),
                                                     hour = hour, level = lev,
                                                     region = regiontype)

                                except:
                                    print "Couldn't get the fcst rainfall partner data \
                                        w.r.t obs data b/w ", p_startdate, p_enddate
                                    print "So skipping it"
                                    continue
                                
                                if vartype == 'rainfall':
                                    # collecting already regridded rainfall 
                                    # observation w.r.t model resolution.
                                    # so that we can do std, correlation 
                                    # calculations. i.e. same resolution.
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
                                    
                                    # here again we are accessing the regridded observation
                                    # w.r.t model resolution, to do the correlation with 
                                    # this model (loop over the models) forecast.
                                    rainfallXml = obsrainPath + '/' + 'rainfall_regrided.xml'
                                    obs_ = cdms2.open(rainfallXml)
                                     # get the obs variable name from the global variables, which
                                    # has set in the global 'vars.txt' file.
                                    obsvar = variables.get(model.name).get('rainfall').obs_var
                                    ref_data = obs_(obsvar, myregion, time = dates)
                                    # standardization of reference data.                                
                                    ref_data = _standardization(ref_data, avg)
                                    obs_.close()
                                else:
                                    # for non observation variables (i.e. analysis
                                    # variables).
                                    print "Regridding takes place for %s model w.r.t reference model %s" % (model.name, refmodel)
                                    # get time axis of fcst data before regrid 
                                    fcsttime = fcst_data.getTime()
                                    # reference data lat, lon axis 
                                    reflat = ref_data.getLatitude()
                                    reflon = ref_data.getLongitude()
                                    # do regrid model forecast data w.r.t 
                                    # reference model analysis resolution. 
                                    print len(fcsttime.asComponentTime()),
                                    print fcst_data.getGrid(), ref_data_grid
                                    print fcst_data.getLatitude()[:],reflat[:]
                                    print fcst_data.getLongitude()[:], reflon[:]                                 
                                    fcst_data = fcst_data.regrid(ref_data_grid)
                                    # extract the exact region.
                                    fcst_data = fcst_data(myregion)                                
                                    # reset the fcst data's axis 
                                    fcst_data.setAxisList((fcsttime, reflat, reflon))
                                # end of if vartype == 'rainfall':
                                    
                                # standardization of model forecast data.                            
                                fcst_data = _standardization(fcst_data, avg)
                                
                                # get the correlation value b/w reference data (either 
                                # obeservation or model analysis) and model forecast data.
                                corrValue = correlation(ref_data, fcst_data, axis = "tyx")
                                # get the standard deviation value of model forecast data
                                stdValue = std(fcst_data, axis='tyx')
                                # free memory
                                del fcst_data
                                # doing the normalization for std of forecast data. i.e. 
                                # make the standard deviation value of model forecast data 
                                # within o to 1 scale.
                                stdValue = stdValue.data/refStdValue.data if normalization else stdValue.data     
                                # store all the forecast hours data std and correlation value      
                                taylorInput.append([stdValue, corrValue.data])    
                                # adding the model name to the legend strings
                                nameslist.append(model.name)                    
                    # end of for model in models:
                                    
                    # generate the title of the plot
                    title = hourname + ' '
                    if reference in ['anl', 'analysis']:
                        title += 'Anl' + ' ('+ refmodel + ') '
                    else:
                        title += refstr + ' ('+ institution + ') '
             
                    title += vartype.capitalize() + ' '
                    if lev:
                        title += str(int(lev)) + 'hPa '
                    title += region + ' ' + avg.capitalize() + ' ' + msname.upper() + ' ' + year
                    # get the max std value from the taylorInput 2D list., which get
                    # max value of fist dimension.
                    maxstd = max(taylorInput)[0]
                    # set the maximum limit of standard deviation.
                    if normalization:
                        setmaxstd = float(round(maxstd, 1) + 0.2)
                        referenceVal = 1
                    else:
                        setmaxstd = int(round(maxstd, 0) + 2)
                        referenceVal = refStdValue.data
                    # make the input data as masked variabe
                    taylorInput = MV2.array(taylorInput)           
                    # plot & save the image
                    plot.tylorPlot(taylorInput, reference = referenceVal,
                                   maxvalue = setmaxstd, name = title,
                                   colors = modelcolors[:len(nameslist)], 
                                   symbols = ["dot"],
                                   legendstrings = nameslist, path = outPlotPath,
                                   svg = 0, png = 1)
                    
                    # storing the taylorInput (std, corr)                                 
                    taylorInputLevelsCollection.append(taylorInput)
                # end of for lev in levels:    
                
                if levels == [None]:
                    # i.e it has no levels. so remove level list and append to 
                    # forecast collection                    
                    taylorInputFcstHoursCollection.append(taylorInputLevelsCollection[0])
                else:
                    # it has levels also. so just append the collection of levels
                    # taylor input into the forecast collection list 
                    taylorInputFcstHoursCollection.append(taylorInputLevelsCollection)
                
                # append hour into hours list to generate the forecast axis
                hours.append(hour)
            # end of for hour in models[0].hour:            
            
            # create the cdms2 variable to store into nc file.       
            var = cdms2.createVariable(taylorInputFcstHoursCollection)
            
            tyncfilepath = os.path.join(tyProcPath, tyncfile)
            if os.path.isfile(tyncfilepath):
                # open the nc file in append mode 
                tyncfobj = cdms2.open(tyncfilepath, 'a')
                print "\n\n opening in append mode \n\n"
            else:
                # file doesnt exist. so open the nc file in write mode(first time)
                tyncfobj = cdms2.open(tyncfilepath, 'w')
                print "opening in write model \n\n"
                
            if referenceXmlVar != "prmslmsl":
                fcstAxis = tyncfobj("prmslmsl").getAxis(1)
                modelAxis = tyncfobj("prmslmsl").getAxis(2)
                stdcorrAxis = tyncfobj("prmslmsl").getAxis(3)
            else:
                # create forecast axis which is the second/second most outer 
                # dimension of the variable which will be generated in the 
                # previous cmd line. It contains the standard deviation and 
                # correlation values of all the models & obs/anl of all the 
                # forecast hours and all the levels of this months or this season
                # in the loop            .
                fcstAxis = cdms2.createAxis(hours)
                fcstAxis.id = 'fcst'
                fcstAxis.long_name = 'forecast days/hours dimension'        
                
                # create the model axis which is inner most second dimension
                modelAxis = cdms2.createAxis(range(len(nameslist)))
                modelAxis.id = 'model'
                modelAxis.long_name = 'models'
                modelAxis.namelist = str(nameslist)
            
            allAxisList = [timeAxis, fcstAxis, modelAxis, stdcorrAxis]
            
            # adding the timeAxis dimension to the var
            newshape = list(var.shape)
            newshape.insert(0, 1)
            var = var.reshape(newshape)
                
            if levelAxis:
                # if it has level axis, then insert at proper dimension/position
                newshape = list(var.shape)
                newshape.insert(2, 1)
                var = var.reshape(newshape)
                allAxisList.insert(2, levelAxis)            
            
            # fianlly the axis dimension inorder [time, fcst, level, model, stdcorr]
            # if level is None, then level dimension wont be there.
            
            # setting the axis information
            var.setAxisList(allAxisList)
            var.id = referenceXmlVar #vartype
            var.comments = "Std & Correlation for over the '%s' region" % region
            
            
            # write/store the generated variable which contains 
            # standard_deviation_and_correlation of all the models & obs/anl
            # into nc file. 
            print "\n\n\nwriting the variabe ", var.info()
            tyncfobj.write(var)
            tyncfobj.close()
            print "nc file closed\n\n"
            
        # end of for month, dates in seasonCollections.iteritems():        
    # end of for year in availableMonths:
    refobj.close()
    #refxmlobj.close()
# end of def genIndividualHoursMultiModelsTaylorDiagrams(...):


def genMultiHoursMultiModelsTaylorDiagrams(vartype, reference=None, 
                            refmodel='', refstr='Obs', institution='',
                            avg='spatial', normalization=True, 
                            monseason='month', region='CIndia', year=''):
    """
    03.06.2012
    """
    # pre defined 10 model color codes
    modelcolors = [241, 249, 242, 246, 250, 247, 243, 248, 250, 251]
    # pre defined 11 model symbols 
    fcstsymbols = ["dot", "triangle_up_fill", "square_fill", "diamond_fill", 
                   "triangle_down_fill", "star", "plus", "circle", "cross", 
                   "diamond", "triangle_up", "square"]
    # forecast hours string 
    fcstdays = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']
        
    # create the directory structure for season process  
    tyProcPath = os.path.join(processfilesPath,
                           refmodel, 'Taylor', year, monseason.capitalize())
    # create/generate nc file name 
    tyncfile = refmodel + '_Taylor_Inputs_' + region + '_' + avg.capitalize() 
    tyncfile += '_' + monseason.capitalize() +'s_' + year
    if normalization:
        tyncfile += '_normalization' + '.nc'
    else:
        tyncfile += '.nc'       
        
    tyncfilepath = os.path.join(tyProcPath, tyncfile)
    
    if not os.path.isfile(tyncfilepath):
        raise ValueError("The '%s' is not exists in its path. Unable to proceed" % tyncfilepath)
        
    # create the directory structure for month plot 
    tyPlotPath = createDirsIfNotExists(plotsgraphsPath,
                           [refmodel, 'Taylor', year, monseason.capitalize()])     
    
    tyncfobj = cdms2.open(tyncfilepath)    
    # get the obs variable name from the global variables, which
    # has set in the global 'vars.txt' file.
    if vartype in ['rainfall']:
        referenceXmlVar = variables.get(refmodel).get(vartype).obs_var
    else:
        referenceXmlVar = variables.get(refmodel).get(vartype).model_var
    
    if not referenceXmlVar in tyncfobj.listvariables():
        raise ValueError("The '%s' variabe is not available" % referenceXmlVar)
        
    dataTimeAxis = tyncfobj[referenceXmlVar].getTime()
    dataTime = dataTimeAxis.asComponentTime()
    bounds = dataTimeAxis.getBounds()
    
    for dtime in dataTime:
        if monseason == 'month':
            # get the month string name 
            msname = cdutil.getMonthString(dtime.month)
        elif monseason == 'season':            
            sbound, ebound = bounds[dataTime.index(dtime)]
            msname = timobj.getSeasonName(sbound, ebound, year)
        # create the least sub directories of month name or season name
        outPlotPath = createDirsIfNotExists(tyPlotPath, [msname.lower(), 
                             'MultiHoursMultiModels', vartype])
                             
        data = tyncfobj(referenceXmlVar)
        fcsthours = data.getAxis(1)[:]
        
        levels = data.getLevel()
        
        if not levels:
            levels = [None]
            modelAxisPos = 2
        else:
            modelAxisPos = 1
        
        models = eval(data.getAxis(modelAxisPos).namelist)
        fcstlen = len(fcsthours)
        modellen = len(models)
        for lev in levels:            
            # getting data excluding the reference (to avoid 
            # duplication of reference values) for multiple fcst hours.
            tydata = data(time = dtime, level = lev, model = (1, len(models)), squeeze = 1)
            orshape = tydata.shape            
            newshape = (orshape[0] * orshape[1], orshape[2])            
            taylorInput = tydata.reshape(newshape)
            
            taylorInput = numpy.array(taylorInput).tolist()          
            # reference point symbol "dot"
            fcstSymbols = [fcstsymbols[0]]
            # add the symbols (same symbol for same forecast days but diff models)
            for sym in fcstsymbols[0: fcstlen+1]:
                fcstSymbols += [sym] * (modellen-1) 
            
            # genearate the model colors for all the forecast days.
            # same color for same models but diff fcst days.
            modelColors = modelcolors[1:modellen] * fcstlen
            # reference point color "black" 
            modelColors.insert(0, modelcolors[0])           

            # get the std value of obs/anl to set reference line in taylor diagram.
            referenceVal = data(time = dtime, fcst = 24, level = lev, model = 0, stdcorr = 0, squeeze = 1)         
            # add the reference std, corr at first position
            taylorInput.insert(0, [referenceVal, 1])            
            
            # make memory free 
            del data
            # generate the title of the plot            
            title = models[0] + ' ('
            if institution:
                title += institution + ') '
            else:
                title += refmodel + ') '
     
            title += vartype.capitalize() + ' '
            if lev:
                title += str(int(lev)) + 'hPa '
            title += region + ' ' + avg.capitalize() + ' ' + msname.upper() + ' ' + year
            # get the max std value from the taylorInput 2D list., which get
            # max value of fist dimension.
            maxstd = max(taylorInput)[0]
            # set the maximum limit of standard deviation.
            if normalization:
                setmaxstd = float(round(maxstd, 1) + 0.2)                
            else:
                setmaxstd = int(round(maxstd, 0) + 2)
            #print modelcolors[:modellen] + [modelcolors[0]] * len(fcsthours)
            #print [fcstsymbols[0]] * len(models) + fcstsymbols[:fcstlen]
            # make the input data as masked variabe
            taylorInput = MV2.array(taylorInput) 
            
            # plot & save the image
            plot.tylorPlot(taylorInput, reference = referenceVal,
                           maxvalue = setmaxstd, name = title,
                           colors = modelColors, 
                           symbols = fcstSymbols,
                           legendstrings = models + fcstdays[:len(fcsthours)], 
                           lcolors = modelcolors[:modellen] + [modelcolors[0]] * len(fcsthours),
                           lsymbols = [fcstsymbols[0]] * len(models) + fcstsymbols[:fcstlen],
                           path = outPlotPath,
                           svg = 0, png = 1)
        # end of for lev in levels:
    # end of for dtime in dataTime:
    tyncfobj.close()                           
# end of def genMultiHoursMultiModelsTaylorDiagrams(...):
                        
if __name__ == '__main__':

    if len(models) == len(obsrainfalls) == 1:
        print "Obtained one model and one obsrainfall "
    elif len(models) == len(obsrainfalls):
        print "Obtained %d models and obsrainfalls" % len(models)
    else:
        print "Obtained %d models and %d obsrainfalls" % (len(models), len(obsrainfalls))

    ###
    # Generating the taylor diagrams for individual models with
    # multi forecast hours data along with obs/anl as reference point.
    ###
    
#    for model in models:
#        for vtype in variables.get(model.name): 
#            if vtype == 'rainfall':
#                continue
#                
#            genIndividualModelsMultiHoursTaylorDiagrams(vtype, model.name, model.path,
#                                        model.hour, reference = 'anl', 
#                                        avg = 'spatial', monseason = 'month')
#            genIndividualModelsMultiHoursTaylorDiagrams(vtype, model.name, model.path,
#                                        model.hour, reference = 'anl',
#                                        avg = 'temporal', monseason = 'month')
#            genIndividualModelsMultiHoursTaylorDiagrams(vtype, model.name, model.path,
#                                        model.hour, reference = 'anl',
#                                        avg = 'spatial', monseason = 'season')
#            genIndividualModelsMultiHoursTaylorDiagrams(vtype, model.name, model.path,
#                                        model.hour, reference = 'anl',
#                                       avg = 'temporal', monseason = 'season')
        # end of for vtype in variables.get(model.name):
                                      
#        for obsrainfall in obsrainfalls:
#            if model.count == obsrainfall.count:
#                if obsrainfall.regrid == 'yes':
#                    # generate regridded obsrainfall directory w.r.t
#                    # obsrainfall name in the
#                    # processfilesPath, modelname, Regrid, ObsRain directory.
#                    obsrainPath = os.path.join(processfilesPath,
#                                                 model.name, 'Regrid',
#                                           'ObsRain', obsrainfall.name)
#                elif obsrainfall.regrid == 'no':
#                    # user passed 'no' option. It means the obsrainfall.path
#                    # obsrainfall data is w.r.t to model fcst data.
#                    obsrainPath = obsrainfall.path
#                else:
#                    pass
#                    
#                if obsrainfall.xml is None:
#                    obsrainXmlPath = obsrainPath + '/rainfall_regrided.xml'
#                else:
#                    obsrainXmlPath = os.path.join(obsrainPath, obsrainfall.xml)
#                # calling the function                            
#                genIndividualModelsMultiHoursTaylorDiagrams('rainfall', model.name, model.path,
#                                    model.hour, reference = obsrainXmlPath, 
#                                    institution = 'NCMRWF', 
#                                    avg = 'spatial', monseason = 'month')
#                genIndividualModelsMultiHoursTaylorDiagrams('rainfall', model.name, model.path,
#                                    model.hour, reference = obsrainXmlPath, 
#                                    institution = 'NCMRWF', 
#                                    avg = 'temporal', monseason = 'month')
#                genIndividualModelsMultiHoursTaylorDiagrams('rainfall', model.name, model.path,
#                                    model.hour, reference = obsrainXmlPath,  
#                                    institution = 'NCMRWF', 
#                                    avg = 'spatial', monseason = 'season')
#                genIndividualModelsMultiHoursTaylorDiagrams('rainfall', model.name, model.path,
#                                    model.hour, reference = obsrainXmlPath, 
#                                    institution = 'NCMRWF', 
#                                    avg = 'temporal', monseason = 'season')
#            else:
#                pass
#                # obsrainfall configuration and model data configuration are not equal in the text file
#                # handle this case, in diff manner. The same loop should works.
#                # But need to check all the cases.
        
        
    print "Done! "

    ###
    # Generating the taylor diagrams for individual forecast hours with
    # multi models fcst data along with obs/anl as reference point.
    ###
    for vtype in variables.get('T254'):
        # for non obs rainfall variables only.
        if vtype in ['rainfall']:
            continue
        for refmodname in ['T254']:#, 'ECMWF']:
            # take these 'ECMWF' & 'T254' model analysis as reference to 
            # compare against with other models forecast.
            print vtype
            genIndividualHoursMultiModelsTaylorDiagrams(vtype, 
                            reference = 'anl', refmodel = refmodname, 
                            avg = 'spatial', monseason = 'month')
#            genIndividualHoursMultiModelsTaylorDiagrams(vtype, 
#                            reference = 'anl', refmodel = refmodname, 
#                            avg = 'spatial', monseason = 'season')
#            genIndividualHoursMultiModelsTaylorDiagrams(vtype, 
#                            reference = 'anl', refmodel = refmodname, 
#                            avg = 'temporal', monseason = 'month')
#            genIndividualHoursMultiModelsTaylorDiagrams(vtype, 
#                            reference = 'anl', refmodel = refmodname, 
#                            avg = 'temporal', monseason = 'season')

    #
    # For observation rainfall. Take NCMRWF's observation as reference to 
    # compare against with all the models forecast.
    #

    # take the observation1 as reference
    obsref = obsrainfalls[0]
    obsrainXMLPath = os.path.join(processfilesPath, 'T254', 'Regrid',
                                'ObsRain', obsref.name, 
                                'rainfall_regrided.xml')
    
    genIndividualHoursMultiModelsTaylorDiagrams('rainfall', 
                    reference = obsrainXMLPath, refmodel = 'T254', refstr = 'Obs', 
                    institution = 'NCMRWF', avg = 'spatial', 
                    monseason = 'month')
#    genIndividualHoursMultiModelsTaylorDiagrams('rainfall',  
#                    reference = obsrainXMLPath, refmodel = 'T254', 
#                    institution = 'NCMRWF', avg = 'spatial', 
#                    monseason = 'season')
#    genIndividualHoursMultiModelsTaylorDiagrams('rainfall', 
#                    reference = obsrainXMLPath, refmodel = 'T254', 
#                    institution = 'NCMRWF', avg = 'temporal', 
#                    monseason = 'month')
#    genIndividualHoursMultiModelsTaylorDiagrams('rainfall', 
#                    reference = obsrainXMLPath, refmodel = 'T254', 
#                    institution = 'NCMRWF', avg = 'temporal', 
#                    monseason = 'season')
    
    print "Done! "      
#    for vtype in variables.get('T254'):
#        for refmodname in ['T254', 'ECMWF']:
#            genMultiHoursMultiModelsTaylorDiagrams(vtype, 
#                                refmodel = refmodname,
#                                avg = 'spatial', monseason = 'month', 
#                                year = '2010')
#            genMultiHoursMultiModelsTaylorDiagrams(vtype, 
#                                refmodel = refmodname,
#                                avg = 'spatial', monseason = 'season', 
#                                year = '2010')
                
# end of if __name__ == '__main__':
