import os
import sys
import numpy
import cdms2
import cdutil
from genutil import statusbar
# getting the absolute path of the previous directory
previousDir = os.path.abspath(os.path.join(os.getcwd(), '..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diagnosisutils.timeutils import TimeUtility
import netcdf_settings
cdms2.setAutoBounds('on')


timobj = TimeUtility()
__showStatusBar =  True


def dailyClimatology(varName, infile, outfile, leapday=False, **kwarg):
    """
    dailyClimatology : It will create the daily climatolgy and stored
                       in the outfile.
    Inputs:
        varName : variable name to extract from the input file
        infile : Input file absolute path
        outfile : outfile absolute path (will be created in write mode)
        leapday : False | True
                  If it is True, then it will create 366 days climatolgy
                  (include 29th feb)
                  If it is False, then it will create 365 days climatolgy

    KWargs:

        ovar : out varName. If it is passed then the climatology variable
               name will be set as ovar. Otherwise the input varName will
               be set to it.
        squeeze : 1 (it will squeeze single dimension in the climatolgy)

    todo : need to set year 1 for 366 days climatology.

    Written By : Arulalan.T
    Date : 13.08.2013

    """

    ovar = kwarg.get('ovar', None)
    squeeze = kwarg.get('squeeze', 1)
    timobj = TimeUtility()

    if leapday:
        tlen = 366
        year = 4
        cunits = 'days since 4-1-1'
        # change the above units into 1-1-1 if cdtime.ClimLeapcaleder Bug fixed
    else:
        tlen = 365
        year = 1
        cunits = 'days since 1-1-1'
    # end of if leapday:

    f = cdms2.open(infile)
    latAxis = f[varName].getLatitude()
    lonAxis = f[varName].getLongitude()
    levAxis = f[varName].getLevel()

    clim = numpy.array([])
    ctimeAxisVal = []
    preview = 0
    for day in range(tlen):
        cdate = timobj._dayCount2Comp(day, year)
        data = timobj.getSameDayData(varName, infile, day=cdate.day,
                                    mon=cdate.month, squeeze=squeeze)
        avg = cdutil.averager(data, axis='t', weights='weighted')
        ### the above avg works fine.
        ### need to test the above method with missing values.
        ### If it fails, the below commented lines should works correctly.

#        dataSum = cdutil.averager(data, axis='t', action='sum') # weights=data.mask) #'weighted')
#       ### This count will counts the no of False in the masked array
#       ### with same shape. i.e. returns total no of elements
#       count = data.count(axis=0)
#        avg = dataSum / count
        # make memory free
        del data
        fillvalue = avg.fill_value
        if clim.shape == (0,):
            clim = avg.filled()
        else:
            clim = numpy.concatenate((clim, avg.filled()))
        # end of if clim.shape == (1,):
        ctimeAxisVal.append(day)
        # make memory free
        del avg
        if __showStatusBar:
            preview = statusbar(day, total=tlen,
                        title='Climatology', prev=preview)
            # Either averager function or setSlabTimeBoundsDaily
            # fucnction will print 'convention.getDsetnodeAuxAxisIds'
            # msg. So status bar unable to retain the same line.
            # To avoid that I added the below line.
            # The character '\x1b' is the escape character.
            # The character [1A moves the cursor to 1 previous line.
            # (i.e. at the end of the previous line \n char).
            # The character [80D moves cursor to 80 positions to the left.
            # The character [K clears the line.
            # Refer ANSCII escape sequence for more details.
            sys.stdout.write("\x1b[1A" + "\x1b[80D"  + "\x1b[K")
       # end of if __showStatusBar:
    # end of  for day in range(tlen):
    print
    climMask = (clim == fillvalue)
    clim = cdms2.createVariable(clim)
    if climMask.any():
        clim.mask = climMask
    # end of if climMask.any():
    if ovar:
        clim.id = ovar
    else:
        clim.id = varName
    # end of if ovar:

    # create climatolgy timeAxis
    ctimeAxis = cdms2.createAxis(ctimeAxisVal, id='time')
    ctimeAxis.units = cunits
    ctimeAxis.designateTime()
    #ctimeAxis.calendar = cdtime.ClimLeapCalendar ????

    axislist = [axis for axis in [ctimeAxis, levAxis, latAxis, lonAxis] if axis]
    if squeeze:
        # squeezing the axis lists
        axislist = [axis for axis in axislist if len(axis[:]) > 1]
    # end of if squeeze:
    # set the axis information to the clim data
    clim.setAxisList(axislist)
    cdutil.setSlabTimeBoundsDaily(clim)
    # save/write the climatolgy data
    outf = cdms2.open(outfile, 'w')
    outf.write(clim)
    outf.close()
    f.close()

    print "The Climatology data year is",
    if leapday:
        print 4
    else:
        print 1
    print "The climatolgy data has written into", outfile
# end of def dailyClimatology(varName, infile, ...):


def monthlyClimatology(varName, infile, outfile, memory='low', **kwarg):
    """
    monthlyClimatology : It will create the monthly climatolgy.
                         Its timeaxis dimension length is 12.

    memory : 'low'/'high'.
              If it is low, then it compute climatology in optimized
              manner by extracting full timeseries data of particular
              latitude, longitude & level points by loop throughing
              each latitude, longitude & level axis. It needs low RAM memory.

              If it is 'high', then it load the whole data from the input
              file and compute climatology. It needs high RAM memory.

    KWargs:

        ovar : out varName. If it is passed then the climatology variable
               name will be set as ovar. Otherwise the input varName will
               be set to it.
        squeeze : 1 (it will squeeze single dimension in the climatolgy)

    todo : need to give option to create 366 days climatology.

    Written By : Arulalan.T
    Date : 13.08.2013

    """

    ovar = kwarg.get('ovar', None)
    squeeze = kwarg.get('squeeze', 1)
    inf = cdms2.open(infile)
    if memory in [1, 'high']:
        data = inf(varName)
        # calculate climatology over timeAxis for global data
        clim = cdutil.ANNUALCYCLE.climatology(data)
        if ovar: clim.id = ovar
        # write the climatology data into nc file
        outf = cdms2.open(outfile, 'w')
        outf.write(clim)
        outf.close()
    elif memory in [0, 'low']:
        ctlen = 12
        latitudes = inf[varName].getLatitude()
        longitudes = inf[varName].getLongitude()
        levels = inf[varName].getLevel()
        # create climatology time axis
        ctimeAxis = cdms2.createAxis(range(ctlen), id='time')
        ctimeAxis.units = 'months since 1-1-1'
        ctimeAxis.designateTime()
        # create dummy array to stroe the climatology data
        if levels:
            clim = numpy.zeros((ctlen, len(levels), len(latitudes), len(longitudes)))
        else:
            clim = numpy.zeros((ctlen, len(latitudes), len(longitudes)))

        preview = 0
        for latidx, lat in enumerate(latitudes):
            if levels:
                for levidx, lev in enumerate(levels):
                    # calculate climatology over timeAxis for particular
                    # lat, lon & level point data in loop
                    data = inf(varName, level=(lev, lev), latitude=(lat, lat))
                    # store the climatology data into dummy array
                    cdata = cdutil.ANNUALCYCLE.climatology(data)(squeeze=1)
                    clim[:, levidx, latidx, :] = cdata
            else:
                # calculate climatology over timeAxis for particular
                # lat, lon point data in loop
                data = inf(varName, latitude=(lat, lat))
                # store the climatology data into dummy array
                clim[:, latidx, :] = cdutil.ANNUALCYCLE.climatology(data)
            # end of if levels:
            if __showStatusBar:
                preview = statusbar(latidx, total=len(latitudes),
                               title='Climatology', prev=preview)
                # Either averager function or setSlabTimeBoundsDaily
                # fucnction will print 'convention.getDsetnodeAuxAxisIds'
                # msg. So status bar unable to retain the same line.
                # To avoid that I added the below line.
                # The character '\x1b' is the escape character.
                # The character [1A moves the cursor to 1 previous line.
                # (i.e. at the end of the previous line \n char).
                # The character [80D moves cursor to 80 positions to the left.
                # The character [K clears the line.
                # Refer ANSCII escape sequence for more details.
                sys.stdout.write("\x1b[1A" + "\x1b[80D"  + "\x1b[K")
           # end of if __showStatusBar:
        # end of for latidx, lat in enumerate(latitudes):
        print
        axislist = [axis for axis in [ctimeAxis, levels, latitudes, longitudes] if axis]
        if squeeze:
            clim = clim.squeeze()
            # squeezing the axis lists
            axislist = [axis for axis in axislist if len(axis[:]) > 1]
        # end of if squeeze:
        # create the climatology cdms2 variable with its axis information
        clim = cdms2.createVariable(clim)
        if ovar:
            clim.id = ovar
        else:
            clim.id = varName
        clim.setAxisList(axislist)
        cdutil.setSlabTimeBoundsMonthly(clim)
        # write the climatology data into nc file
        outf = cdms2.open(outfile, 'w')
        outf.write(clim)
        outf.close()
    # end of if memory in [1, 'high']:
    inf.close()
    print "The Climatology data year is", 1
    print "The climatolgy data has written into", outfile
# end of def createClimatology(...):



