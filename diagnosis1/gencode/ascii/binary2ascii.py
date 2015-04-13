import cdms2, cdtime, string, numpy, os


def binary2ascii(var, fpath, opath=None, dlat=None, dlon=None, freq='daily',
                                    missing_value='default', speedup='True'):
    """
    binary2ascii : Convert the binary file such as nc, ctl, pp into ascii csv
                   files. It should create individual files for each years.
                   Csv file contains the month, day, lat & lon information
                   along with its corresponding data.

                   It has optimised code to extract data and write into file
                   by using numpy.tofile() function. Its just extract the
                   particular/each lat grid, extract all the longitude values
                   in single dimension array and write into file object at a
                   time. So it is more optimised.

    Inputs :
        var - variable name

        fpath - binary file input absolute path

        opath - output directory path. Inside this folder, it should create
                csv files with variable name along with year. If user didnt
                pass any value for this, then it should create variable name
                as folder name for the output in the current working
                directory path.

        dlat - need data lat shape in ascii. eg (0, 40)
        dlon - need data lon shape in ascii. eg (60, 100)

        freq - it takes either 'daily' or 'monthly'.
               It is just to fastup the time dimension loop by skipping 365
               days in daily and 12 months in monthly to access the another/
               next year dataset.

        missing_value - if missing_value passed by user, then that value
                should be set while writing into csv file. By default it takes
                'default' value, i.e. it will take fill_value from the binary
                file information itself.
        speedup - This binary2ascii.py works fine only for all 12 months or 
                  365 days data. If some months are missing in b/w means, 
                  it will fail to work. So in that case, you switch off this 
                  speedup option. 
        todo - to get the available years, we need to use timeutils.py module.
                in that case, the above speedup option no need.


    Written By : Arulalan.T

    Date : 22.08.2012

    """

    inf = cdms2.open(fpath)
    ftime = inf[var].getTime().asComponentTime()
    latitude = inf[var].getLatitude()
    longitude = inf[var].getLongitude()
    lon = numpy.array(longitude)

    preyear = None
    premon = None
    outf = None
    
    if speedup:
        if freq == 'daily':
            ftime = ftime[::365]
        elif freq == 'monthly':
            ftime = ftime[::12]
        else:
            pass

    if opath is None:
        if not os.path.isdir(var):
            os.mkdir(var)
            print "Created Directory called ,", var
        # end of if not os.path.isdir(var):
        print "All the output files will be written inside the directory, ", var
        opath = var
    # end of if opath is None:

    for ytime in ftime:
        # loop through available years in the time axis
        year = ytime.year
        if preyear == year:
            continue
        else:
            if outf and preyear:
                print "The file writing finished for the year ", preyear
                outf.close()
            # end of if outf and preyear:
            fname = var + '_' + str(year) + '.csv'
            outf = open(opath + '/' + fname, 'w')
            preyear = year
            print "The file has created ", fname
            print "Writing ..."

            # year period
            startPeriod = cdtime.comptime(year, 1, 1, ytime.hour)
            endPeriod = cdtime.comptime(year, 12, 31, ytime.hour)
            # get the data of one/each year & load into memory
            if dlat and dlon:
                # extract specified lat, lon for one/each year
                data = inf(var, time=(startPeriod, endPeriod), latitude=dlat,
                                                              longitude=dlon)
                # get the lat, lon axis w.r.t user need
                latitude = data.getLatitude()
                longitude = data.getLongitude()
                lon = numpy.array(longitude)
            else:
                # extract all lat, lon for one/each year
                data = inf(var, time=(startPeriod, endPeriod))
            dtime = data.getTime()
            if missing_value != 'default':
                data.missing_value = missing_value
            # end of if missing_value != 'default':

            # make it as filled value and reset its axis informations
            data = data.filled()
            data = cdms2.createVariable(data)
            # set the time, lat, lon axis w.r.t extracted shape of data
            data.setAxisList([dtime, latitude, longitude])
        # end of if preyear != year:

        for ctime in dtime.asComponentTime():
            # loop thorugh daily time for one/each year. i.e. 365/366
            year = str(year)
            mon = str(ctime.month)
            day = str(ctime.day)

            if premon != mon:
                lonstr = string.joinfields(['Year', 'Mon', 'Day', 'Lat/Lon'], ',')
                outf.write('\n' + lonstr + ',')
                lon.tofile(outf, sep=',')
                outf.write('\n')
                premon = mon
                print "Writing Month, ", mon
            # end of if premon != mon:

            latbegingstr = string.joinfields([year, mon, day], ',')
            for lat in latitude:
                latstr = latbegingstr + ',' + str(lat)
                outf.write(latstr + ',')
                # get the particular lat and all the longitude grid data.
                val = numpy.array(data(time=ctime, latitude=lat))
                # write the numpy array into fileobject with separation of
                # comma. It is optimised one.
                val.tofile(outf, sep=',')
                outf.write('\n')
            # end of for lat in latitude:
        # end of for ctime in dtime.asComponentTime():
        del data
    # end of for time in ftime:
    inf.close()
# end of def binary2ascii(var, fpath, opath):


if __name__ == '__main__':

    binary2ascii('precip', 'srb1.xml')


