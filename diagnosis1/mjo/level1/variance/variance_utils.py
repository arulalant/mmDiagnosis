import os
import sys
import numpy
import cdms2
import cdtime
import vcs
#import numarray.fft.fftpack as fftpack
from genutil import statistics
from genutil import statusbar
from regrid2 import Regridder
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
diagDir = os.path.abspath(os.path.join(__curDir__, '../../..'))
# adding the previous diagnosisutils path to python path
sys.path.append(diagDir)
from uv_cdat_code.diagnosisutils.timeutils import TimeUtility
import diag_setup.netcdf_settings


# create time utility object
timobj = TimeUtility()
__showStatusBar = False


def convertTimeIntegratedToNormal(data, hour):
    # Time integrated data unit Wsm^-2. Converted to Wm^2.
    return data / (float(hour) * 60 * 60)
# end of def convertTimeIntegratedToNormal(data, hour, sign=1):


def anomaly(data, climatology, climyear=1, **kwarg):
    """
    Calculating anomaly.
    Anomaly = model data - climatology

    In this function, it should find out either data has leap year day data
    or not. Also find out either climatology data has leap year day data or
    not.

    Depends upon these case, it should remove the leap day data from either
    model data or climatology data, when shapes are mis-match (i.e. both leap
    and non leap year data has passed as arguments) to compute anomaly.

    KWargs :
        When data and climatology shapes are mis-match, then
        cregrid : if True, then climatology data will be regridded w.r.t
                  model/obs/data and then anomaly will be calculated.

        dregrid : if True, then model/obs/data will be regridded w.r.t
                 climatology data and then anomaly will be calculated.

        ..note:: We can not enable both cregrid and dregrid at the same time.

    Written By : Arulalan.T

    Date : 11.06.2012
    Updated : 24.06.2013

    """

    timeAxis = data.getTime()
    latAxis = data.getLatitude()
    lonAxis = data.getLongitude()

    modelCompTime = timeAxis.asComponentTime()
    startday = modelCompTime[0]
    endday = modelCompTime[-1]

    varid = data.id
    modeldays = len(modelCompTime)
    climyear = str(climyear)

    cregrid = kwarg.get('cregrid', False)
    dregrid = kwarg.get('dregrid', False)

    if modeldays < 365:
        # the data time axis length is less than 365. i.e. it has partial data
        # of the year. So need to calculate anomaly according to that dates
        # of the climatology data.

        # generate the climatology start day and endday w.r.t available data
        cstartday = climyear + '-' + str(startday.month) + '-' + str(startday.day)
        cendday = climyear + '-' + str(endday.month) + '-' + str(endday.day)

        # generate the leap day to check the leap year status
        leapday = cdtime.comptime(startday.year, 2, 29, startday.hour)

        if leapday in modelCompTime:
            # it contains leap day data
            leapYear = True
        else:
            # it doesnt have leap day data
            leapYear = False

    elif modeldays == 365:
        if (startday.day == 1 and startday.month == 1
            and endday.day == 31 and endday.month == 12):
            # generate the climatology start day & end day of the whole year
            cstartday = climyear + '-1-1'
            cendday = climyear + '-12-31'
            # it is non-leap year. so need to remove the leap day data from
            # the climatology data, if that contains leap day data.
            leapYear = False
        else:
            raise ValueError("The passed data time axis doesnt start & end \
                with proper year dates. (%s, %s). Pass the correct data " %
                (startday, endday))

    elif modeldays == 366:
        if (startday.day == 1 and startday.month == 1
            and endday.day == 31 and endday.month == 12):
            # generate the climatology start day & end day of the whole year
            cstartday = climyear + '-1-1'
            cendday = climyear + '-12-31'
            # it is leap year. so either climatology data should contains
            # leap day data or remove the leap day data from the model data,
            # in case climatology doesnt have leap day data.
            leapYear = True
        else:
            raise ValueError("The passed data time axis doesnt start & end \
                with proper year dates. (%s, %s). Pass the correct data " %
                (startday, endday))
    else:
        raise ValueError("Data passed with more than 366 days. Please pass \
                            correct data set")

    # get the total days in climatology data
    climCompTime = climatology.getTime().asComponentTime()
    climdays = len(climCompTime)
    if not (climCompTime[0] == cdtime.comptime(int(climyear), 1, 1) and
            climCompTime[-1] == cdtime.comptime(int(climyear), 12, 31)):
        print "Climatology Start Date ", climCompTime[0]
        print "Climatology End Date ", climCompTime[-1]
        raise ValueError("The climatology data timeAxis is not correct")
    # extract the needed climatology data alone (w.r.t to the model data timeAxis)
    climatology = climatology(time=(cstartday, cendday))

    if climdays == 366:
        # climatology data contains 366 days. i.e. including leap day data
        if not leapYear:
            # i.e. previous leapYear flag is False. So we need to remove
            # leap day data from climatology.
            # generate the leap day to check the leap year status
            cleapday = cdtime.comptime(int(climyear), 2, 29)
            # climatology component time
            climTime = climatology.getTime().asComponentTime()
            if cleapday in climTime:
                # get the index of the leap day
                leapidx = climTime.index(cleapday)
                # remove leap day from the climatology data
                climatology = climatology[:leapidx].tolist() + climatology[leapidx + 1:].tolist()
                climatology = numpy.array(climatology)

    elif climdays == 365:
        # climatology data contains 365 days only. i.e. it doesnt have leap
        # day data.
        if not leapYear:
            # i.e. previous leapYear flag is False. So we need to remove
            # leap day data from model.
            # generate the leap day to check the leap year status
            mleapday = cdtime.comptime(startday.year, 2, 29, startday.hour)
            if mleapday in timeAxis:
                # get the index of the leap day
                leapidx = timeAxis.indexof(mleapday)
                # remove leap day from the model data
                data = data[:leapidx].tolist() + data[leapidx + 1:].tolist()
                data = numpy.array(data)
                # re-genearate the time axis obj excluding the leap day
                timeAxis = timobj._genTimeAxis(startday, endday, cdtime.NoLeapCalendar)
    else:
        raise ValueError("The climatology data has wrong length of time axis %d" % climdays)

    data = data(squeeze=1)
    levAxis = data.getLevel()
    if data.shape == climatology.shape:
        # calculate anomaly
        anomaly = data - climatology
    else:
        clim_grid = climatology.getGrid()
        data_grid = data.getGrid()
        if cregrid and not dregrid:
            # Regridding the climatology data
            # Creating the horizontal lat,lon regrid
            # Here 'clim_grid' is the source and 'data_grid' is the target
            regridfunc = Regridder(clim_grid, data_grid)
            climatology = regridfunc(climatology)
        elif dregrid and not cregrid:
            # Regridding the model/obs data
            # Creating the horizontal lat,lon regrid
            # Here 'data_grid' is the source and 'clim_grid' is the target
            regridfunc = Regridder(data_grid, clim_grid)
            data = regridfunc(data)
            # update the regridded data axis
            latAxis = climatology.getLatitude()
            lonAxis = climatology.getLongitude()
            levAxis = climatology.getLevel()
        elif dregrid and cregrid:
            raise ValueError("Can not do both 'cregrid' and 'dregrid'. Make one option as False.")
        elif not dregrid and not cregrid:
            print "model data shape ", data.shape
            print "climatology data shape ", climatology.shape
            raise ValueError("model data and climatology data shapes are mis-match.")
        # end of if cregrid and not dregrid:
        # calculate anomaly for regridded data sets.
        anomaly = data - climatology
    # end of if data.shape == climatology.shape:
    # make free memory
    del data, climatology

    # get the needed axis list
    axislist = [axis for axis in (timeAxis, levAxis, latAxis, lonAxis) if axis]
    # set the axis information to the anomaly
    anomaly.setAxisList(axislist)
    anomaly.id = varid

    return anomaly
# end of def anomaly(...):


def computeAnomaly(mvar, modelPath, cvar, climPath, climyear, outPath,
                            convertTI2N=False, hour=None, sign=1, **kwarg):
    """

    computeAnomaly : compute the anomaly by opening the model and climatology
        data from the files. Finally writes the output anomaly into outpath
        file.

    Input :
        mvar - model variable name
        modelPath - model nc file absolute path
        cvar - climatology variable name
        climPath - climatology nc file absolute path
        climyear - Year in climatology file
        outPath - anomaly nc file (output) absolute path
        convertTI2N - It takes either True or False. If it is True, then the
            model data will be converted from Time Integrated to Normal form.
            i.e. Units will be converted from Wsm^-2 to Wm^2.
        hour - hour of the model data (will be used in convertTI2N function)
        sign - change sign of the model data (will be used in convertTI2N fn)

        kWargs :-
            long_name - long name for the output anomaly
            comments - comments for the output anomaly
            cregrid - climatology data will be regridded w.r.t model data
            dregrid - model data will be regridded w.r.t climatology data
                      by default both cregrid & dregrid are False
    Refer : anomaly, convertTimeIntegratedToNormal

    Written By : Arulalan.T

    Date : 11.06.2012

    """

    # Opening model (OLR) Data
    mfile = cdms2.open(modelPath)
    model_data = mfile[mvar]

    #print model_data.getTime(), type(model_data.getTime())
    avlYears = timobj._getYears(model_data.getTime())

    # Opening Climatology Data
    cfile = cdms2.open(climPath)
    clim_data = cfile(cvar)
    cfile.close()

    timeAxisCollections = []
    lname = ''
    cmt = ''

    if 'long_name' in kwarg:
        lname = kwarg.get('long_name')
    if 'comments' in kwarg:
        cmt = kwarg.get('comments')

    for year in avlYears:
        sdate = str(year) + '-1-1'
        edate = str(year) + '-12-31 23:59.0'
        model_data = mfile(mvar, time=(sdate, edate))
        if convertTI2N:
            # Time integrated data unit Wsm^-2. Converted to Wm^2.
            model_data = convertTimeIntegratedToNormal(model_data, hour)
        if sign == -1:
            # Changing Sign and making OLR data Positive
            model_data = model_data * (-1)
        # get anomaly
        ano = anomaly(model_data(squeeze=1), clim_data, climyear, **kwarg)
        # make free memory
        del model_data
        timeAxisCollections.append(ano.getTime())
        ano = cdms2.createVariable(ano)
        ano.id = mvar
        ano.long_name = lname
        ano.comments = cmt
        if os.path.isfile(outPath):
            f = cdms2.open(outPath, 'a')
        else:
            f = cdms2.open(outPath, 'w')
        f.write(ano)
        f.close()
        # make free memory
        del ano
    # for year in avlYears:
    # make memory free
    del clim_data
    # close the file
    mfile.close()
    print "The Output Anomaly File has Created ", outPath
# end of def computeAnomaly(...):


def calculateVariance(varName, fpath, speed=True, **kwarg):
    """
    calculate Variance for anomaly data in temporal way.All Seasonal Variance.

    if speed is True, then it should calculate the variance for the whole
    data.

    If data size is too large which cant handle by normal system, then we
    should off the speed arg. speed = False. So it will take the partial data
    (in latitude and/or level wise) with its full time axis. By this way, we
    can calculate the variance for large size of data.

    It should loop through the each and every latitude grid point, (but not by
    longitude) get the full time series with full longitude wise data and
    compute the statistics.variance and store it.

    KWargs:
        year : Its optional only. By default it is None. i.e. It will
             extract all the available years data to compute variance over timeAxis.
             If one interger year has passed means, then it will do
             extract of that particular year data alone.
             If two years has passed in tuple, then it will extract
             the range of years data from year[0] to year[1].
             eg1 : year=2005 it will extract seasonData of 2005 alone.
             eg2 : year=(1971, 2013) it will extract seasonData from
                   1971 to 2013 years.

    Written By : Arulalan.T

    Date : 26.07.2012

    """
    year = kwarg.get('year', None)
    if year:
        if isinstance(year, int):
            tyear = cdtime.comptime(year, 1, 1)
        elif isinstance(year, tuple):
            syear = cdtime.comptime(year[0], 1, 1)
            eyear = cdtime.comptime(year[0], 12, 31, 23, 59)
            tyear = (syear, eyear)
        print "Extract & do variance of data for time", tyear
    # end of if year:

    # open the file path
    f = cdms2.open(fpath)
    if speed:
        # if speed flag is true, then the calculate the variance in time axis
        # (temporal) and return it.
        # Cause : If user passes the very large size data,
        # then it may not work. For large size data, user may off the speed
        # arg flag.
        if year:
            data = f(varName, time=tyear)
        else:
            data = f(varName)
        # end of if year:
        f.close()
        # calculate variance over timeAxis
        resultVariance = statistics.variance(data, axis='t')
        # By default it id has changed into variance. So reset its varName
        resultVariance.id = varName
        return resultVariance
    # end of if speed:

    # speed is slow/off/0, to handle the large size data, by calculate
    # variance along its levels, latitude wise. It may be slow. But it works
    # for large time scale data with its levels(optional).

    # get the data information
    data = f[varName]  # (transiant object)
    # collect the lat, lon details from the data
    latAxis = data.getLatitude()
    lonAxis = data.getLongitude()
    levAxis = data.getLevel()
    latlen = len(latAxis)
    lonlen = len(lonAxis)

    if levAxis:
        levlen = len(levAxis)
        resultVariance = numpy.zeros((1, levlen, latlen, lonlen), float)
    else:
        levlen = 1
        resultVariance = numpy.zeros((1, latlen, lonlen), float)
    # end of if level:

    for levidx in range(0, levlen):
        # loop through the level (if data doesnt have level, it is single
        # dummy loop)
        for latidx in range(0, latlen):
            # Loop through the latitude axis. i.e. calculate the variance of
            # the data along with its time axis and longitude axis of each &
            # every latitude points. By this way we can handle the large size
            # data. But it is slow, because it needs to loop through the lat
            # axis fully.
            if levAxis:
                # if data have level, then variance will be stored w.r.t level
                # index also.
                if year:
                    resultVariance[0, levidx, latidx] = statistics.variance(
                        f(varName, time=tyear, level=slice(levidx, levidx+1),
                                 latitude=slice(latidx, latidx+1)), axis='t')
                else:
                    resultVariance[0, levidx, latidx] = statistics.variance(
                                 f(varName, level=slice(levidx, levidx+1),
                                 latitude=slice(latidx, latidx+1)), axis='t')
                # end of if year:

            else:
                if year:
                    resultVariance[0, latidx] = statistics.variance(
                     f(varName, time=tyear, latitude=slice(latidx, latidx+1)), axis='t')
                else:
                    resultVariance[0, latidx] = statistics.variance(
                      f(varName, latitude=slice(latidx, latidx+1)), axis='t')
                # end of if year:
            # end of if levAxis:
       # end of for latidx in range(0, latlen):
    # end of for levidx in range(0, levlen):

    # create the resultant variance data variable
    resultVariance = cdms2.createVariable(resultVariance)
    resultVariance.id = varName
    vtime = timobj._generateTimeAxis(1, cdtime.comptime(1, 1, 1))

    # get the needed axis list
    axislist = [axis for axis in (vtime, levAxis, latAxis, lonAxis) if axis]
    # set the axis information
    resultVariance.setAxisList(axislist)

    # close the data file obj
    #f.close() #??? Have to fix this transiant variable file close problem
    # return the variance
    return resultVariance
# end of def calculateVariance(varName, fpath, speed=True):


def calculateSeasonalVariance(varName, fpath, sday, smon, eday, emon,
                                                        hr=0, **kwarg):
    """
    calculateSeasonalVariance : calculate Variance for anomaly seasonal data
          in temporal way. It should extract the data only for the seasonal
          days of the year. Even it has more years, then it should extract
          only the seasonal days data of all the years, and then calculate
          the variance for the seasonal days of the all the years of the data.

    Inputs:
        varName : anomaly variable name
        fpath : anomaly (nc) file path
        sday : starting day of the season [of all the years of the data].
        smon : starting month of the season [of all the years of the data].
        eday : ending day of the season [of all the years of the data].
        emon : ending month of the season [of all the years of the data].
        hr : hour for both start and end date

    KWargs:
        year : Its optional only. By default it is None. i.e. It will
             extract all the available years seasonalData.
             If one interger year has passed means, then it will do
             extract of that particular year seasonData alone.
             If two years has passed in tuple, then it will extract
             the range of years seasonData from year[0] to year[1].
             eg1 : year=2005 it will extract seasonData of 2005 alone.
             eg2 : year=(1971, 2013) it will extract seasonData from
                   1971 to 2013 years.

    ..note::    If end day and end month is lower than the start day and start
             month, then we need to extract the both current and next year
             data. For eg : Winter Season (November to April).
             It can not be reversed for this winter season. We need to
             extract data from current year november month upto next year
             march month.
                If you pass one year data and passed the above
             winter season, then it will be extracted november and december
             months data and will be calculated variance for that alone.
                If you will pass two year data then it will extract the data
             from november & december of first year and january, feburary &
             march of next year will be extracted and calculated variance
             for that.

    Written By : Arulalan.T

    Date : 26.07.2012

    """

    # season data for all the years of the data
    seasonalData = timobj.getSeasonalData(varName, fpath, sday, smon,
                                              eday, emon, hr, **kwarg)

    # calculate the statistics.variance for all the seasonalData of the all
    # the years.
    seasonalVariance = statistics.variance(seasonalData, axis='t')

    # get the lat, lon axis information
    latAxis = seasonalData.getLatitude()
    lonAxis = seasonalData.getLongitude()
    levAxis = seasonalData.getLevel()
    # make memory free
    del seasonalData

    # genearate the variance single dimension time axis
    vtime = timobj._generateTimeAxis(1, cdtime.comptime(1, 1, 1, hr))
    seasonalVariance = cdms2.createVariable(seasonalVariance)
    seasonalVariance.id = varName

    newshape = list(seasonalVariance.shape)
    newshape.insert(0, 1)
    seasonalVariance = seasonalVariance.reshape(newshape)
    # get the needed axis list
    axislist = [axis for axis in (vtime, levAxis, latAxis, lonAxis) if axis]
    # set axis information
    seasonalVariance.setAxisList(axislist)
    # return the variance
    return seasonalVariance
# end of def calculateSeasonalVariance(...):


def summerVariance(varName, fpath, sday=1, smon=5, eday=31, emon=10,
                                                      hr=0, **kwarg):
    """
    summerVariance : summer season (May to October) variance

    Inputs :
      varName - anomaly variable name
      fpath - anomaly file path
      sday : starting day of the summer season [of all the years of the data].
      smon : starting month of the summer season [of all the years of the data].
      eday : ending day of the summer season [of all the years of the data].
      emon : ending month of the summer season [of all the years of the data].
      hr : hour for both start and end date

    KWargs :
        year : It could be single year or range of years in tuple.
               By default it is None. So it will calculate all available years
               summerVariance
    Refer: calculateSeasonalVariance

    Written By : Arulalan.T

    Date : 26.07.2012

    """
    return calculateSeasonalVariance(varName, fpath, sday, smon,
                                        eday, emon, hr, **kwarg)
# end of def summerVariance(...):


def winterVariance(varName, fpath, sday=1, smon=11, eday=30, emon=4,
                                                      hr=0, **kwarg):
    """
    winterVariance : winter season (November to April) variance

    Inputs :
      varName - anomaly variable name
      fpath - anomaly file path
      sday : starting day of the winter season [of all the years of the data].
      smon : starting month of the winter season [of all the years of the data].
      eday : ending day of the winter season [of all the years of the data].
      emon : ending month of the winter season [of all the years of the data].
      hr : hour for both start and end date

    KWargs :
        year : It could be single year or range of years in tuple.
               By default it is None. So it will calculate all available years
               winterVariance
    Refer: calculateSeasonalVariance

    Written By : Arulalan.T

    Date : 26.07.2012

    """
    return calculateSeasonalVariance(varName, fpath, sday, smon,
                                        eday, emon, hr, **kwarg)
# end of def winterVariance(...):


def lfilter(data, weights, cyclic=True, **kwarg):
    """
    Lanczos Filtered
    Todo : Write doc of the work flow
    KWarg:
        returntlen : return time axis length. By default it takes None.
                     It can take positive or negative integer as value.
                     If it is +ve no, then it will do filter only to
                     the first no days rather than doing filter to the
                     whole available days of the data.
                     If it is -ve no, then it will do filter only to
                     the last no days.
                     Timeaxis also will set properly w.r.t return data.
                     if cyclic is enabled or disabled, then returntlen
                     index will change according to cyclic flag.

                     Lets assume weights length is 101.
                     Eg1: Lets consider data length is 365.
                          If cyclic is False, then filteredData length is
                          365-(100*2)=165 when returntlen is None.
                          If returntlen = 10, so filteredData length is 10
                          and its index is range(100, 110).
                          If returntlen = -10, so filteredData length is 10
                          and its index is range(255, 265).

                     Eg2: If cyclic is True, then filteredData length is
                          365 when returntlen is None.
                          If returntlen = 10, so filteredData length is 10
                          and its index is range(0, 10).
                          If returntlen = -10, so filteredData length is 10
                          and its index is range(355, 365).

                    So returntlen option is useful when we need to filter
                    only to the certain days. But regardless of returntlen
                    option, we need to pass the full data to apply Lanczos
                    Filter to either returntlen days or full days.
                    This option will save a lot of time when returntlen is
                    very less compare to the total length of the data.

    Written By : Arulalan.T

    Date : 15.09.2012
    Updated : 22.09.2013
    """

    returntlen = kwarg.get('returntlen', None)
    if returntlen:
        if not isinstance(returntlen, int):
            raise ValueError("Keyword arg returntlen must be an integer")
    # end of if returntlen:

    timeAxis = data.getTime()
    latAxis = data.getLatitude()
    lonAxis = data.getLongitude()
    levAxis = data.getLevel()

    dataid = data.id
    # get the total length of the timeAxis of the original data
    tlen = len(timeAxis)
    # get the units of timeAxis of the original data
    tunits = timeAxis.units

    # we can use the below option if we dont want to initialize it with
    # size/dimension. But we need to add append option instead of assign
    # resultant filteredData.
    #filteredData = numpy.array([0])
    zweight = weights[0]
    weights = numpy.array(weights[1:])
    wlen = len(weights)
    # get the axis length shape
    axshape = [len(axis) for axis in [levAxis, latAxis, lonAxis] if axis]
    # reshape the weights according to the passed data shape
    # (just to shape match to multiply with data)
    wshape = [1 for axis in [levAxis, latAxis, lonAxis] if axis]
    wshape.insert(0, wlen)
    weights = weights.reshape(wshape)
    # set flag if returntlen is -ve integer
    reverse = True if returntlen < 0 else False
    if cyclic:
        # for cyclic, the filteredData timeAxis should be same as passed
        # data's timeAxis. i.e. tlen length.
        # get full tlen or returntlen as length of the return filteredData
        loopCount = abs(returntlen) if returntlen else tlen
        if reverse:
            # return the last loopCount days
            loopdays = xrange(tlen-loopCount, tlen)
            timeAxisList = timeAxis[tlen-loopCount: tlen]
        else:
            # return loopCount days from the begining of the data
            loopdays = xrange(loopCount)
            timeAxisList = timeAxis[:loopCount]
        # end of if reverse:
    else:
        # if it non-cyclic, then we will lost the timeAxis length of wlen*2
        # days. i.e tlen-(wlen*2) length.
        # get tlen-(wlen*2) or returntlen as length of the return filteredData
        loopCount = abs(returntlen) if returntlen else tlen-(wlen*2)
        if reverse:
            # return the last loopCount days
            loopdays = xrange(tlen-wlen-loopCount, tlen-wlen)
            timeAxisList = timeAxis[tlen-wlen-loopCount: tlen-wlen]
        else:
            # return loopCount days from the begining of the data
            loopdays = xrange(wlen, wlen+loopCount)
            timeAxisList = timeAxis[wlen: wlen+loopCount]
        # end of if reverse:
    # end of if cyclic:

    # insert the tlength at first in the axis length shape
    axshape.insert(0, loopCount)
    # filteredDate dummy initialization shape
    filteredData = numpy.zeros(axshape)

    # overwrite the timeAxis
    timeAxis = cdms2.createAxis(timeAxisList)
    timeAxis.id = 'time'
    timeAxis.units = tunits
    timeAxis.designateTime()

    preview = 0
    for idx, cday in enumerate(loopdays):
        # loop through all the days (check above)
        # apply zeroth weight to the current day data
        cfilter = data[cday] * zweight
        ps = (tlen - wlen) + cday
        #pe = (tlen + cday) % tlen

        if ps <= tlen:
            preData = numpy.concatenate((data[ps:], data[:cday]))
        elif ps > tlen:
            ps = ps % tlen
            preData = data[ps:cday]
        # end of if ps <= tlen:

        # reverse the previous data of length wlen
        preData = preData[::-1]
        ns = cday + 1
        ne = ns + wlen

        if ne <= tlen:
            nextData = data[ns:ne]
        elif ne > tlen:
            ne = ne % tlen
            nextData = numpy.concatenate((data[ns:], data[:ne]))  #data[ns:ne]
        # end of if ne <= tlen:

        # add together the wlen days previous (reversed) data & wlen days next
        # data (with out reversed) to the current day data.
        # And then multiplied with wlen size of weights
        # (multiplied in all dimensions).
        # now sum together, the time dimension length becomes one.
        wlenfilter = sum((preData + nextData) * weights)
        # finally again sum together the above wlenfilter (wlength filtered
        # data) with current day filtered (zeroth day filtered) data.

        if not cyclic:
            # get the proper index to store into the filteredData array
            cday = cday % wlen
        # end of if not cyclic:

        # store to the filteredData array
        filteredData[idx] = cfilter + wlenfilter
        # make memory free
        del preData, nextData, wlenfilter
        if __showStatusBar:
            preview = statusbar(cday, total=loopCount,
                        title='Filtering', prev=preview)
        # end of if __showStatusBar:
    # end of for idx, cday in enumerate(loopdays):
    print
    # make memory free
    del data

    # get the needed axis list
    axislist = [axis for axis in (timeAxis, levAxis, latAxis, lonAxis) if axis]
    # set the axis information to the filteredData variable
    filteredData = cdms2.createVariable(filteredData)
    filteredData.id = dataid
    filteredData.setAxisList(axislist)

    return filteredData
# end of def lfilter(data, weights, cyclic=True, **kwarg):


def plotVariance(data, outfile, season, title='', pdf=1, png=0, **kwarg):
    """

    Written By : Alok Singh, Arulalan.T

    Date : 28.05.2012
    Updated : 08.07.2013

    """

    bg = kwarg.get('bg', 1)
    x = kwarg.get('x', None)
    if x is None:
        x = vcs.init()
    # end of if x is None:
    x.clear()
    isofill = x.getisofill('quick')
    x.setcolormap("ASD")
    isofill.levels = [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600,
                      1800, 2000, 2200, 2100, 2400, 2600, 2800, 3000,
                                  3200, 3400, 3600, 3800, 4000, 4200]
    isofill.fillareacolors = [252, 112, 117, 125, 137, 155, 171, 185,
                              190, 200, 204, 215, 225, 229, 12, 22,
                                             25, 30, 35, 40, 45, 50]
    ##### remove the below comments
    #isofill.fillareacolors=[252,253,254,116,120,125,130,135,141,148,155,162,166,171,185,190,197,200,204,210]
    #isofill.fillareacolors=[252,253,10,30,40,55,65,90,110,125,155,162,166,171,185,190,197,200,204,210]
    #[252,40,30,25,20,15,12,95,110,117,125,137,155,171,185,190,200,204,215,225,229]
    ##### remove the above comments

    if 'genVTemplate' in x.listelements('template'):
        # get the 'genTemplate' template object from temporary memory of vcs
        # template
        gentemp = x.gettemplate('genVTemplate')
    else:
        # creating 'genTemplate' object
        gentemp = x.createtemplate('genVTemplate', 'ASD')
        gentemp.mean.priority = 0
        gentemp.min.priority = 0
        gentemp.max.priority = 0
        gentemp.dataname.priority = 0
        gentemp.units.priority = 0
        gentemp.crdate.priority = 0
        gentemp.crtime.priority = 0
        gentemp.tvalue.priority = 0
        gentemp.tname.priority = 0
        gentemp.tunits.priority = 0
        gentemp.comment1.priority = 0
        gentemp.comment2.priority = 0
        gentemp.comment3.priority = 0
        gentemp.comment4.priority = 0
        gentemp.source.priority = 0
        gentemp.title.priority = 1
        gentemp.zvalue.priority = 0
        gentemp.title.x = .5
        gentemp.title.y = .92

        to = x.createtextorientation('new', 'centerup')
        to.height = 23
        to.angle = 0
        gentemp.title.textorientation = to
    # end of if 'genVTemplate' in x.listelements('template'):

    if 'tropbox' in x.listelements('line'):
        # get the 'genTemplate' line object from temporary memory of vcs
        tropbox = x.getline('tropbox')
    else:
        tropbox = x.createline('tropbox')
        tropbox.color = [241]
        tropbox.width = [3.0]
        tropbox.type = ['solid']
        tropbox.viewport = [gentemp.data.x1, gentemp.data.x2,
                            gentemp.data.y1, gentemp.data.y2]
        tropbox.worldcoordinate = [0., 360., -90., 90.]
    # end of if 'tropbox' in x.listelements('line'):

    x.plot(data, isofill, gentemp, title=title, bg=bg)
    x.flush()
    if season in ['sum', 'jjas']:
        # summer boxes
        tropbox.x = [[80., 100.], [80., 80.], [100., 80.], [100., 100.],
                     [75., 100.], [75., 100.], [100., 100.], [75., 75.],
                     [115., 140.], [115., 140.], [115., 115.], [140., 140.]]
        tropbox.y = [[10., 10.], [10., 20.], [20., 20.], [20., 10.],
                     [5., 5.], [-10., -10.], [5., -10.], [5., -10.],
                     [25., 25.], [10., 10.], [25., 10.], [25., 10.]]
        x.plot(tropbox, bg=bg)

    elif season in ['win', 'djf']:
        #winter Boxes
        tropbox.x = [[115., 145.], [115., 145.], [115., 115.], [145., 145.],
                     [75., 100.], [75., 100.], [100., 100.], [75., 75.],
                     [160., 185.], [160., 185.], [160., 160.], [185., 185.]]
        tropbox.y = [[-2.5, -2.5], [-17.5, -17.5], [-2.5, -17.5], [-2.5, -17.5],
                     [5., 5.], [-10., -10.], [5., -10.], [5., -10.],
                     [-5., -5.], [-20., -20.], [-5., -20.], [-5., -20.]]
        x.plot(tropbox, bg=bg)
    # end of if season in ['sum', 'jjas']:
    x.flush()
    x.update(1)

    if pdf:
        x.pdf(outfile + '.pdf')
    if png:
        x.png(outfile + '.png')
    x.clear()
    # make memory free
    del data
# end of def plotVariance(data, outfile, season, title='', pdf=1, png=0):



