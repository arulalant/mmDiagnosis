import numpy, MV2
from numpy import sin, arcsin, cos, pi


def getArcDistance(x1, y1, x2, y2, radius=6371):
    """
    `func` : get the Arc distance

             Using equation of distance between two points on arc line.

             We can use this function to find out the distances between
             some list of latitudes & longitudes positions to some other
             single/list of lat, lon position of the earth. For this we need
             to pass the radius of the earth.

    Inputs :
        x1, x2 - single latitude / list of latitudes
        y1, y2 - single longitude/ list of longitudes

        But x1 & y1 should be same shape. Also x2 & y2 should be same shape.

        radius - radius of the circle. By default it takes the earth's radius
                 in kilometer.

    Written By : Arulalan.T

    Date : 23.09.2012

    """

    x1 = numpy.array(x1)
    x2 = numpy.array(x2)
    y1 = numpy.array(y1)
    y2 = numpy.array(y2)

    radion_conv = pi / 180.0
    delta_x = numpy.absolute(x1 - x2) * radion_conv
    delta_y = numpy.absolute(y1 - y2) * radion_conv
    # angle b/w two lat,lon points
    angle = 2 * (arcsin(((sin(delta_x / 2)) ** 2) +
                      (cos(x1 * radion_conv)) * (cos(x2 * radion_conv)) *
                      ((sin(delta_y / 2)) ** 2)) ** 0.5)
    # calculate the diagonal distance.
    dgn_distance = angle * radius
    return dgn_distance
# end of def getArcDistance(x1, y1, x2, y2, radius=6371):


def get1LatLonFromNonRectiLinearGrid(grid, lat, lon, diff=0.5):
    """
    `func` : get1LatLonFromNonRectiLinearGrid
             It is locating the input lat & lon in the non-rectilinear grid
             data and returning its corresponding first dimension index (i) &
             second dimension index (j) (of the grid which is very close to
             the input lat & lon values).

    Inputs :
        grid : Its the cdms2 dataset grid value. Use x.getGrid() to pass
               the dataset grid value, where x is cdms2 dataslab.
        lat : latitude which you looking for.
        lon : longitude which you looking for.
        diff : By default it takes 0.5. It is the purpose of masking the
               outer region other than (lat-diff, lat+diff) and
               (lon-diff, lon+diff).

    Logic :
        Here we are getting the lat_vertices and lon_vertices data as well as
        lat_slab and lon_slab from the grid.  i.e. Using grid.getBounds(),
        grid.getLatitude() & grid.getLongitude() functions.

        Do the mask operation on the lat_vertices where ever outer than the
        (lat-diff, lat+diff).

        Do the mask operation on the lon_vertices where ever outer than the
        (lon-diff, lon+diff).

        Multiply the resultant masked boolean array of lat & lon gives us the
        near about 10 grids location which are all with in the range of
        (lat-diff, lat+diff) and (lon-diff, lon+diff) both matched together.

        So from this 10 grids locations, using distance b/w two points in the
        curved line equation, we can identify the minimum distance from the
        input lat & lon.

        Finally we can loate the minimum distance grid cell's first dimension
        index (i) and its second dimension index (j).

        Here index i belongs to longitude and index j belongs to latitude.

    Return :
        Return the first dimension index (i) & second dimension index (j)
        value where we located the nearest grid cell of the input lat, lon
        passed by the user.

    Reference :
        function 'getArcDistance()'

    Example :

        eg 1:
            >>> f = cdms2.open("zos_Omon_ACCESS1-0_rcp45_r1i1p1.xml")
            >>> x = f('zos', time=slice(1), squeeze=1)
            >>> lat, lon = 10, 300
            >>> latidx, lonidx = get1LatLonFromNonRectiLinearGrid(x.getGrid(), lat, lon)
            >>> val = x[latidx][lonidx]

             ..note:: Here val is the data value of that lat, lon. Mind that
                      index (i/lonidx) is first dimension and index (j/latidx)
                      is second dimension of the data.
                      Though to access the data here, we need pass latidx as
                      1st and lonidx as 2nd. Just work out this example, you
                      will understand.

        eg 2:
            >>> latidx, lonidx = get1LatLonFromNonRectiLinearGrid(x.getGrid(), lat, lon)
            >>> # extract the time series data points of 10N, 60S position alone
            >>> val = f(var, i=(lonidx), j=(latidx))
            >>> val.shape
            (365,)

             ..note:: Mind that i belongs to longitude & j belongs to latitude.
        eg 3:
            # efficient manner.
            >>> f = cdms.open("zos_Omon_ACCESS1-0_rcp45_r1i1p1.xml")
            # getting variable access alone, not the whole data.
            >>> x = f['zos']
            >>> latidx, lonidx = get1LatLonFromNonRectiLinearGrid(x.getGrid(), lat, lon)


             ..note:: Since we can not directly use latitude, longitude values
               in the non-rectilinear grid data, we are using 1st dimension
               (j) for latitude and 2nd dimension (i) for longitude as
               corresponding indecies to get the data.

    Written By : Arulalan.T

    Date : 19.09.2012

    """

    # get the lat_vertices & lon_vertices data
    # shape are (i, j, 4), (i, j, 4) for both bounds
    lat_v, lon_v = grid.getBounds()
    # do the mask other than the (lat-diff) and (lat+diff).
    # So here masked_lat is boolean only. Not real numbers.
    masked_lat = MV2.masked_outside(lat_v, lat - diff, lat + diff)
    # make memory free
    del lat_v

    lon_org = lon
    if lon < 0:
        # i.e. -ve (-180 to 0). so make it as circle from 0 to 360.
        lon += 360
    elif lon == 360:
        lon = 0
    # end of if lon < 0:

    # get the lon left region
    lon_dec = lon - diff
    if lon_dec < 0:
        lon_dec += 360
    # end of if lon_dec < 0:

    # get the lon right region
    lon_inc = lon + diff
    if lon_inc >= 360:
        # i.e. it goes beyond the 360. So make it as within circle point.
        lon_inc = 360 - lon_inc
    # end of if lon_inc >= 360:

    # do the mask other than the (lon_dec) and (lon_inc).
    # So here masked_lon is boolean only. Not real numbers.
    masked_lon = MV2.masked_outside(lon_v, lon_dec, lon_inc)
    # make memory free
    del lon_v
    
    if not (masked_lat.all() and masked_lon.all()):
        _err = "Passed lat=%r & lon=%r is out of the region of the given grid" + \
         "resolution %r (or data not available for this lat,lon position)." +\
          "Try to pass lat, lon within the region of the grid."
        raise ValueError(_err % (lat, lon_org, grid.shape))
    # end of if not (masked_lat.all() and masked_lon.all()):
    
    # do the muliplication operation b/w masked_lat & masked_lon.
    # so we will get the resultant masked_lat_lon (i.e. where ever True in
    # both masked_lat and masked_lon only returns True, otherwise False.)
    masked_lat_lon = masked_lat * masked_lon
    # get the indices of masked_lat_lon where ever True comes.
    masked_lat_lon_idx = numpy.argwhere(masked_lat_lon)
    # make memory free
    del masked_lat, masked_lon, masked_lat_lon

    if not masked_lat_lon_idx.any():
        _err = "Passed lat=%r & lon=%r is out of the region of the given grid" + \
         "resolution %r (or data not available for this lat,lon position)." +\
          "Try to pass lat, lon within the region of the grid."
        raise ValueError(_err % (lat, lon_org, grid.shape))
    # end of if not masked_lat_lon_idx:

    # get the both lat and lon data - shape is (i, j).
    # i.e. it contains the real numbers of latitudes and longitudes
    lat_slab = grid.getLatitude()
    lon_slab = grid.getLongitude()

    masked_lat_values = []
    masked_lon_values = []
    masked_lat_lon_indices = []

    for latidx, lonidx, _ in masked_lat_lon_idx:
        # just append the only masked lat index and masked lon index.
        # skip the masked vertices index.
        masked_lat_lon_indices.append((latidx, lonidx))
        # append the real latitude & longitude values (not boolean).
        masked_lat_values.append(lat_slab[latidx][0].data)
        masked_lon_values.append(lon_slab[0][lonidx].data)
    # end of for latidx, lonidx, _ in masked_lat_lon_idx:

    # make memory free
    del lat_slab, lon_slab

    # find the difference b/w lat & lon using the following formula
    # the distance b/w two points on a curved line
    latlondistance = getArcDistance(masked_lat_values,
                                    masked_lon_values, lat, lon)
    # get the shortest distance from the needed lat, lon
    minlatlondist = latlondistance.min()
    # convert the numpy array into list
    latlondistance = latlondistance.tolist()
    # get the index of this min distance from the lat lon difference list
    indexOfMinDist = latlondistance.index(minlatlondist)
    # finally get the j and i (i.e indices to get the passed lat, lon
    # from the non-rectilinear grid data)
    j, i = masked_lat_lon_indices[indexOfMinDist]
    # get the closest lat & lon values
    lat_closest = masked_lat_values[indexOfMinDist]
    lon_closest = masked_lon_values[indexOfMinDist]

    # find out the delta of input lat, lon to the closest lat, lon position
    d_lat = abs(lat - lat_closest)
    d_lon1 = abs(lon - lon_closest)
    d_lon2 = abs(d_lon1 - 360)
    d_lon = min(d_lon1, d_lon2)

    print "The given inputs are lat = %r and lon = %r" % (lat, lon_org),
    if lon_org != lon: print "(%r)" % lon,
    print " & grid size : (lat x lon) =  (%r x %r)" % grid.shape
    print "The 1st/latitude dimension index j = %i & its lat value = %f (delta = %f)" \
                                                 % (j, lat_closest, d_lat)
    print "The 2nd/longitude dimension index i = %i & its lon value = %f (delta = %f)" \
                                                  % (i, lon_closest, d_lon)

    # return the second dimension / latitude dimension index (j) and first
    # dimension / longitude dimension index (i) which are corresponding to
    # the passed lat and lon inputs
    return j, i
# end of def get1LatLonFromNonRectiLinearGrid(datapath, lat, lon, diff=0.5):


if __name__ == '__main__':

    import cdms2
    datapath = raw_input("Enter the datapath : ")
    var = raw_input("Enter the variable : ")
    lat = float(raw_input("Enter the latitude you looking for : "))
    lon = float(raw_input("Enter the longitude you looking for : "))
    f = cdms2.open(datapath)
    x = f(var, time=slice(1), squeeze=1)
    f.close()
    latidx, lonidx = get1LatLonFromNonRectiLinearGrid(x.getGrid(), lat, lon)
    print "The value is = %f for the given lat=%r, lon=%r " % (x[latidx][lonidx], lat, lon)
# end of if __name__ == '__main__':


