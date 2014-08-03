import os
import sys
import numpy
import cdms2
import cdtime
import cdutil
from numpy.fft.fftpack import fftpack
#import numarray.fft.fftpack as fftpack

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


def powerSpectrum(varName, fpath, sday, smon, eday, emon, hr=0, nodays=None, **kwarg):
    """
    varName - variable
    fpath or data :
           This anomaly data should not be spatial one. It should be spatially
           averaged, daily data.
           It may contains many years data with proper time axis.

    nodays : No of days. though its averaged data, pass the no of days of the
             data of each year which has averaged.
             For 180 days summer/winter season averaged of multi-year data,
             you have to pass nodays=180.

    Written By : Arulalan.T

    Date : 31.10.2012

    """

    #timeAxis = data.getTime()
    f = cdms2.open(fpath)
    timeAxis = f[varName].getTime()
    comptime = timeAxis.asComponentTime()
    avlyears = timobj._getYears(timeAxis, deepsearch=True)
    year = kwarg.get('year', None)
    if year:
        if isinstance(year, int):
            if year in avlyears:
                avlyears = [year]
            else:
                raise ValueError("Passed year %d is not available" % year)
        elif isinstance(year, (tuple, list)):
            if len(year) == 2:
                syearIdx = avlyears.index(year[0])
                eyearIdx = avlyears.index(year[1])
                avlyears = avlyears[syearIdx: eyearIdx + 1]
    # end of if year:

    # check if smon > emon or (smon == emon and sday >= eday):
    # if end day and end month is lower than the start day and start
    # month, then we need to extract the both current and next year
    # data. For eg : Winter Season (November to April).
    # It can not be reversed for this winter season. We need to
    # extract data from current year november month upto next year
    # march month.
    #
    scomp = cdtime.comptime(1, smon, sday)
    ecomp = cdtime.comptime(1, emon, eday)
    if ecomp.cmp(scomp) == -1:
        # satisfied if smon > emon or (smon == emon and sday >= eday):
        # The end day and end month is lower than the start day and start
        # month.
        # increase one year to the enddate to extract the next year data.
        adjyear = 1
        # increase one year to the enddate comptime
        ecomp = cdtime.comptime(2, emon, eday)
    else:
        # satisfied smon < emon
        adjyear = 0
    # end of if ecomp.cmp(scomp) == -1:

    if not nodays:
        # get the no of days between the start and end of the season.
        nodays = int(ecomp.torel('days since %s' % str(scomp)).value)
    # end of if not nodays:

    # no of coefficients to be genearated
    nocoef = float(nodays/2.)
    # function rffti initializes the array wsave which is used in rfftf.
    # nodays must be int, not float to calculate rffti. !!!
    wsave = fftpack.rffti(nodays)
    # Averaged variance initalized.
    total_variance = numpy.zeros(nocoef)
    totalYears = 0
    for year in avlyears:
        # loop through available years of the data
        # genearate the start of the current year (season)
        sdate = cdtime.comptime(year, smon, sday, hr)
        print "Start", sdate
        if not sdate in comptime:
            print (str(sdate) + ' is not available in the model data time')
            print "So selecting which ever is available in the passed season"

        # adjust the year (nextyear) to get the end season year to extract
        # the season data correctly in both winter/summer seasons.
        year = year + adjyear

        # generate the end date either for current year or next year.
        edate = cdtime.comptime(year, emon, eday, hr)
        # initializes the segmantData size with dummy array
        segmantData = numpy.zeros(nodays)
        try:
            # extract the season data from file object
            seasonalData = f(varName, time=(sdate, edate), squeeze=1)
            #seasonalData = data(time=(sdate, edate))
        except cdms2.error.CDMSError, e:
            print "Couldnt extracted seasonalData successfully for the year", year
            print str(e), "So Skipping without extracting data"
            continue
        # end of try:
        print "Extracted seasonalData successfully for the year", year

        segmantData[0:len(seasonalData)] = seasonalData[0:nodays]#?

        # make memory free
        del seasonalData
        # increament the no of years (only successfully extracted data !)
        totalYears += 1
        # length of signal to be transformed
        #nodays = len(seasonalData)  ## ???

#        # totvar = sum of all variance
#        totvar = 0

        # computes the fourier coefficients
        coeff_var = fftpack.rfftf(segmantData, wsave)
        # get the real & imaginary parts of the fourier coefficients
        coef1 = coeff_var.real / nocoef
        coef2 = coeff_var.imag / nocoef

        #variance = numpy.zeros(nocoef)
        variance = (coef1**2 + coef2**2) / 2.

        nocoef = int(nocoef)
        if nodays % 2 == 0:
            # even days
            variance[-1] = ((coef1[nocoef]/2)**2 + coef2[nocoef]**2)
        else:
            # odd days
            variance[-1] = (coef1[nocoef]**2 + coef2[nocoef]**2)/2
        # end of if nodays % 2 == 0:

        total_variance += variance[1:]   # ? got 1 extra dimension in rfftf function

    # end of for year in avlyears:

    # finally got the averaged variances over the no of years
    power = total_variance / totalYears
    power = cdms2.createVariable(power, id='power')
    # total of averaged variance
    total_variance_avg = sum(total_variance)
    # calculate the frequency
    frequency = numpy.arange(1, nocoef+1) / float(nodays)
    frequency = cdms2.createVariable(frequency, id='frequency')
    f.close()
    return power, frequency
# end of def powerSpectrum(data, sday, smon, eday, emon, hr=0):


def summerPowerSpectrum(varName, fpath, sday=1, smon=5, eday=31, emon=10, hr=0, **kwarg):
    return powerSpectrum(varName, fpath, sday, smon, eday, emon, hr, **kwarg)
# end of def summerPowerSpectrum(...):


def winterPowerSpectrum(varName, fpath, sday=1, smon=11, eday=30, emon=4, hr=0, **kwarg):
    return powerSpectrum(varName, fpath, sday, smon, eday, emon, hr, **kwarg)
# end of def winterPowerSpectrum(...):


def waveNumber(varName, fpath, sday, smon, eday, emon, hr=0, **kwargs):
    """
    varName - variable
    fpath or data :
           This anomaly data should be meridionally averaged one.
           It should be daily data.
           It may contains many years data with proper time axis.

    KWArgs :-
    nodays : No of days. though its averaged data, pass the no of days of the
             data of each year which has averaged.
             For 180 days summer/winter season averaged of multi-year data,
             you have to pass nodays=180.

    window : do cosine window if True

    iglimit : ignore newlon_limit days. By default it takes 10 days.
              i.e. If extracted season data is less than the (actual seasonal
              days - iglimit) it will throw an error.

    Date : 28.11.2012, 02.12.2012

    """

    nodays = kwargs.get('nodays', None)
    window = kwargs.get('window', True)
    iglimit = kwargs.get('iglimit', 10)

    #timeAxis = data.getTime()
    f = cdms2.open(fpath)
    timeAxis = f[varName].getTime()
    comptime = timeAxis.asComponentTime()
    avlyears = timobj._getYears(timeAxis, deepsearch=True)
    year = kwargs.get('year', None)
    if year:
        if isinstance(year, int):
            if year in avlyears:
                avlyears = [year]
            else:
                raise ValueError("Passed year %d is not available" % year)
        elif isinstance(year, (tuple, list)):
            if len(year) == 2:
                syearIdx = avlyears.index(year[0])
                eyearIdx = avlyears.index(year[1])
                avlyears = avlyears[syearIdx: eyearIdx + 1]
    # end of if year:

    # check if smon > emon or (smon == emon and sday >= eday):
    # if end day and end month is lower than the start day and start
    # month, then we need to extract the both current and next year
    # data. For eg : Winter Season (November to April).
    # It can not be reversed for this winter season. We need to
    # extract data from current year november month upto next year
    # march month.
    #
    scomp = cdtime.comptime(1, smon, sday)
    ecomp = cdtime.comptime(1, emon, eday)
    if ecomp.cmp(scomp) == -1:
        # satisfied if smon > emon or (smon == emon and sday >= eday):
        # The end day and end month is lower than the start day and start
        # month.
        # increase one year to the enddate to extract the next year data.
        adjyear = 1
        # increase one year to the enddate comptime
        ecomp = cdtime.comptime(2, emon, eday)
    else:
        # satisfied smon < emon
        adjyear = 0
    # end of if ecomp.cmp(scomp) == -1:

    if not nodays:
        # get the no of days between the start and end of the season.
        nodays = int(ecomp.torel('days since %s' % str(scomp)).value) - 1  # ? why
    # end of if not nodays:

    totalYears = 0  # set totalYears as zero
    #longitude = data.getLongitude()
    longitude = f[varName].getLongitude()
    NT = nodays  # No of days per segment
    NL = len(longitude)  # No of longitude

#    NT = nodays  # No of days per segment
#    NL = len(longitude) -1 # No of longitude

    # make decision about the resultant latAxis, lonAxis dimension
    # w.r.t either passed data is seasonal or yearly dataset.
    if nodays <= 185:
        # got season
        newlon_limit = 11
        newlon_size = 21
        #NT = 180
    elif nodays >= 360:
        # got annual
        newlon_limit = 20
        newlon_size = 39
        #NT = 364
    else:
        print "Oops ! This season is more than 6 months !!! "
    # end of if nodays <= 185:
    newlat_size = 11

    globmean = 0
    totvar = 0
    # Initial Real data set. Function of space and time
    EE = numpy.zeros((NT, NL), dtype=complex)
    #OEE = numpy.zeros((NT+1,NL/2+1), dtype=float)
    OEE = numpy.zeros((newlon_size, newlat_size), dtype=float)
    PEE = numpy.zeros((NT+1, NL+1))

    wsave1 = fftpack.cffti(NL)  # Initialize FFT for Longitude direction
    wsave2 = fftpack.cffti(NT)  # Initialize FFT for time direction

    # cos window
    if window:
        cos_window = (1 - numpy.cos(numpy.arange(45.) * numpy.pi/45.0)) * 0.5
    # end of if window:

    for year in avlyears:
        # loop through available years of the data
        # genearate the start of the current year (season)
        sdate = cdtime.comptime(year, smon, sday, hr)

        if not sdate in comptime:
            print (str(sdate) + ' is not available in the model data time')
            print "So selecting which ever is available in the passed season"
        # end of if not sdate in comptime:

        # adjust the year (nextyear) to get the end season year to extract
        # the season data correctly in both winter/summer seasons.
        year = year + adjyear
        # generate the end date either for current year or next year.
        edate = cdtime.comptime(year, emon, eday, hr)

        try:
            # extract the season data from file object
            seasonalData = f(varName, time=(sdate, edate), squeeze=1)
            #seasonalData = data(time=(sdate, edate))
        except cdms2.error.CDMSError, e:
            print "Couldnt extracted seasonalData successfully for the year", year
            print str(e), "So Skipping without extracting data"
            continue
        # end of try:
        print "Extracted seasonalData successfully for the year", year

        sdata_len = len(seasonalData)

        if sdata_len < (nodays - iglimit):
            print "The extracted seasonalData length %i is less than %i days" \
                                             % (sdata_len, nodays-iglimit)
            print "So skip this data to calculate the wavenumber for the year", year
            continue
        # end of if sdata_len < (nodays - iglimit):

        # increament the no of years (only successfully extracted data !)
        totalYears += 1

        if nodays >= sdata_len:
            segmantData = numpy.zeros((nodays, NL))
            segmantData[0:sdata_len] = seasonalData  # [:-1]#?
        else:
            endday = abs(nodays - sdata_len)
            segmantData = seasonalData[:-endday]  # [:-1]#?
        # end of if nodays >= len(seasonalData):

        # make memory free
        del seasonalData
#        print segmantData.shape
        # average over both time and longitude axis
        globmean = cdutil.averager(segmantData, axis='01', weights=['equal', 'equal'])  #(EEr /  float(NT*NL))
        # average over time axis
        ave_EEr = cdutil.averager(segmantData, axis='0', weights='equal')  # hope its correct
        # according to the fortran code of mjo.. why is it so ?!
#        ave_EEr = cdutil.averager(segmantData, axis='01',
#                    weights=['equal', 'equal'], action='sum') / float(NT)  # wrong method.. yes.
        #print "Ave_EER", ave_EEr
        # average over the longitude axis
        zm_EEr = cdutil.averager(segmantData, axis='1', weights='equal')
        # remove the time mean
        EEr = segmantData - ave_EEr
#        print globmean.shape
        # remove the global mean
#       # EEr = EEr - globmean  # is this only for allseason ????

        # make memory free
        del segmantData

        if window:
            # Taper first and last 45 days with cosine window
            cos_window = (1 - numpy.cos(numpy.arange(46) * numpy.pi/45.0)) * 0.5
            EEr[0:46] = EEr[0:46] * cos_window[:, numpy.newaxis]
            #print EEr[NT-46:].shape
            #cos_window = (1 - numpy.cos(numpy.arange(2., 48) * numpy.pi/45.0)) * 0.5
            EEr[-46:] = EEr[-46:] * cos_window[::-1, numpy.newaxis]
            #cos_window = (1 - numpy.cos(numpy.arange(47., 1, -1) * numpy.pi/45.0)) * 0.5
            #EEr[-46:] = EEr[-46:] * cos_window[:, numpy.newaxis]
        # end of if window:

        # do the square of the above anomaly val and then do average over
        # both time and longitude axis
        totvar = cdutil.averager(EEr**2, axis='01', weights=['equal', 'equal'])  # /float(NT*NL)
        # Convert the multi-dimensional data into Complex format
        CEE = numpy.vectorize(complex)(EEr)
        del EEr
        coef1 = fftpack.cfftf(CEE, wsave1) / float(NL)
        del CEE
        # here EE is the complex power spectrum array.
        for nl in range(NL):
            EE[:, nl] = fftpack.cfftf(coef1[:, nl], wsave2) / float(NT)
        # end of for nl in range(NL):
        del coef1
        # Now lets Create array PEE(NL+1,NT+1) which contains
        # the real power spectrum.

        half_NL = NL/2
        half_NT = NT/2

        # get the 1st dimension from 0 to half_NT+1. i.e exactly first half of
        # the 1st dimension array.
        # also get the 2nd dimension from 0 to half_NL+1. i.e exactly first
        # half of the 2nd dimension array.
        # Note : In half_NT+1 and half_NL+1, +1 plays role to indicate upto
        # half_NT and half_NL.
        tmpval = (abs(EE[0:half_NT+1, 0:half_NL+1]))**2
        # concatenate the reverse of 2nd dimension of above tmpval array and
        # the ascending order of 2nd dimension of above tmpval array excluding
        # one zeroth index values. (we need only one zeroth index values)
        tmpval = numpy.concatenate((tmpval[:, ::-1], tmpval[:, 1:]), axis=1)
        # reverse the first dimension of the above tmpval array and store it
        # into first half of PEE array.
        PEE[0:half_NT+1] =  tmpval[::-1]

        # get the 1st dimension from half_NT to NT-1. i.e exactly second half
        # of the 1st dimension array.
        # also get the 2nd dimension from 0 to half_NL+1. i.e exactly first
        # half of the 2nd dimension array.
        # Note : In half_NT+1 and half_NL+1, +1 plays role to indicate upto
        # half_NT and half_NL.
        tmpval = (abs(EE[half_NT:, 0:half_NL+1]))**2
        # concatenate the reverse of 2nd dimension of above tmpval array and
        # the ascending order of 2nd dimension of above tmpval array excluding
        # one zeroth index values. (we need only one zeroth index values)
        tmpval = numpy.concatenate((tmpval[:, ::-1], tmpval[:, 1:]), axis=1)
        # reverse the first dimension of the above tmpval array and store it
        # into second half of PEE array.
        PEE[half_NT+1:] =  tmpval[::-1]


        # extract the OEE dimension from the PEE array
        t1 = half_NT+1- newlon_limit
        t2 = half_NT + newlon_limit
        l1 = half_NL
        l2 = half_NL+ newlat_size

        # add the resultant OEE through out the years loop.
        OEE += PEE[t1:t2, l1:l2]
    # end of for year in avlyears:

    # get the average of OEE by divide the totalYears
    OEE = OEE / float(totalYears)

    # Frequency
    ff = (numpy.arange(NT+1) - half_NT) / float(NT)
    #ss = (numpy.arange(NL+1) - half_NL)  #???
    #ss = ss[half_NT-newlon_limit+1: half_NT+newlon_limit]   #???
    # slicing the needed frequencies alone. length should be newlon_size.
    ff = ff[half_NT-newlon_limit+1: half_NT+newlon_limit]
    ss = numpy.arange(0.0, 11.0)

    latAxis = cdms2.createAxis(ss)
    latAxis.id = 'frequency'  # 'latitude'
    #latAxis.units = 'degrees_north'
    #latAxis.designateLatitude()

    lonAxis = cdms2.createAxis(ff)
    lonAxis.id = 'wavenumber'  # 'longitude'
    #lonAxis.units = 'degrees_east'
    #lonAxis.designateLongitude()

    var = cdms2.createVariable(OEE)
    var = var.reorder('1')
    var.setAxisList([latAxis, lonAxis])
    var.id = varName # 'power'
    var.long_name = 'Power of ' + varName
    f.close()
    return var
# end of def waveNumber(data, sday, smon, eday, emon, hr=0, nodays=None):


def summerWaveNumber(varName, fpath, sday=1, smon=5, eday=31, emon=10, hr=0,
                                cos_window=1, nodays=180, **kwargs):
    return waveNumber(varName, fpath, sday, smon, eday, emon, hr,
                        window=cos_window, nodays=nodays, **kwargs)
# end of def summerPowerSpectrum(...):


def winterWaveNumber(varName, fpath, sday=1, smon=11, eday=30, emon=4, hr=0,
                                cos_window=1, nodays=180, **kwargs):
    return waveNumber(varName, fpath, sday, smon, eday, emon, hr,
                        window=cos_window, nodays=nodays, **kwargs)
# end of def winterPowerSpectrum(...):


def annualWaveNumber(varName, fpath, sday=1, smon=1, eday=31, emon=12, hr=0,
                                 cos_window=0, nodays=None, **kwargs):
    return waveNumber(varName, fpath, sday, smon, eday, emon, hr,
                        window=cos_window, nodays=nodays, **kwargs)
# end of def winterPowerSpectrum(...):


def _getDataFromFObj(varName, fobj, **kwarg):
    """
    varName : variable name to extract data.

    fobj : It is cdms2.opened file object.
           It will not close this file obj. You have to close it.

    KWArgs:
        year : It takes either integer or tuple of integers.
               It will extract the passed years data.

        time : It takes cdtime.comptime formate or tuple or
               string of comptime.

        region : It is region object
        latitude : latitude tuple or integer
        longitude : longitude tuple or integer
        level : level list or integer

    Returns :
        Extracted data.
    """

    lat = kwarg.get('latitude', None)
    lon = kwarg.get('longitude', None)
    region = kwarg.get('region', None)
    lev = kwarg.get('level', None)
    year = kwarg.get('year', None)
    if year:
        if isinstance(year, int):
            sdate = cdtime.comptime(year, 1, 1)
            edate = cdtime.comptime(year, 12, 31, 23, 59)
        elif isinstance(year, tuple):
            sdate = cdtime.comptime(year[0], 1, 1)
            edate = cdtime.comptime(year[1], 12, 31, 23, 59)
        time = (sdate, edate)
    else:
        time = kwarg.get('time', None)

    if time and lev:
        if region:
            data = fobj(varName, region, time=time, level=lev)
        elif lat and lon:
            data = fobj(varName, time=time, level=lev, latitude=lat, longitude=lon)
        elif lat:
            data = fobj(varName, time=time, level=lev, latitude=lat)
        elif lon:
            data = fobj(varName, time=time, level=lev, longitude=lon)
        else:
            data = fobj(varName, time=time, level=lev)
        # end of if region:
    elif time and not lev:
        if region:
            data = fobj(varName, region, time=time)
        elif lat and lon:
            data = fobj(varName, time=time, latitude=lat, longitude=lon)
        elif lat:
            data = fobj(varName, time=time, latitude=lat)
        elif lon:
            data = fobj(varName, time=time, longitude=lon)
        else:
            data = fobj(varName, time=time)
        # end of if region:
    elif not time and lev:
        if region:
            data = fobj(varName, region, level=lev)
        elif lat and lon:
            data = fobj(varName, level=lev, latitude=lat, longitude=lon)
        elif lat:
            data = fobj(varName, level=lev, latitude=lat)
        elif lon:
            data = fobj(varName, level=lev, longitude=lon)
        else:
            data = fobj(varName, level=lev)
        # end of if region:
    elif not time and not lev:
        if region:
            data = fobj(varName, region)
        elif lat and lon:
            data = fobj(varName, latitude=lat, longitude=lon)
        elif lat:
            data = fobj(varName, latitude=lat)
        elif lon:
            data = fobj(varName, longitude=lon)
        else:
            data = fobj(varName)
        # end of if region:
    else:
        pass
    # end of if time and lev:
    return data
# end of def _getData(varName, fobj, **kwarg):


def areaAvg(varName, fpath, **kwarg):
    """
    Returns the area averaged data by accessing the var data from the fpath
    itself by extracting needed portion of data only by the following
    key word arguments.

    KWargs : (latitude and/or longitude) or (region) and/or level

    Written by : Arulalan.T

    Date : 08.01.2013

    """

    f = cdms2.open(fpath)
    data = _getDataFromFObj(varName, f, **kwarg)
    f.close()
    # do the area average over lat, lon alone.
    # The time & level axis should retain after done the area avg.
    avgData = cdutil.averager(data, axis='xy')
    # make memory free
    del data
    # reset its id
    avgData.id = varName
    return avgData
# end of def areaAvg(varName, fpath, **kwarg):


def zonalAvg(varName, fpath, **kwarg):
    """
    Returns the zonal averaged data by accessing the var data from the fpath
    itself by extracting needed portion of data only by the following
    key word arguments.

    KWargs : (latitude and/or longitude) or (region) and/or level

    Returns : It vanishes the latitude in the input data and returns it.

    Written by : Arulalan.T

    Date : 08.01.2013

    """

    f = cdms2.open(fpath)
    data = _getDataFromFObj(varName, f, **kwarg)
    f.close()

#    lonAxis = data.getLongitude()
#    timeAxis = data.getTime()
#    levAxis = data.getLevel()

    # do the area average over latitude alone.
    # The time & level axis should retain after done the area avg.
    avgData = cdutil.averager(data, axis='y') #, weight='equal') ##?? 'equal' or 'area'
    # reset its id
    avgData.id = varName

#    axislist = [axis for axis in (timeAxis, levAxis, lonAxis) if axis]
#    setAxisList(axislist)
    # uncomment the above lines if it dont have axis information
    # make memory free
    del data

    return avgData
# end of def zonalAvg(varName, fpath, **kwarg):


