"""
.. module:: weatherutils.py
   :synopsis: The module contains the function to get the centred highs, lows.
    

 Reference : http://www.metservice.com/learning/how-to-read-maps
             H >= 1015
             L <= 1000
 
Author : Arulalan.T

Date: 17.05.2012
"""

import numpy
from numutils import nextmin, nextmax


def is_surrounding_less (data, lat, lon):
    """
    is_surrounding_less : Find either the surrounded lat, lon position 
        values are lesser to the centre value on passed lat, lon of the data.
        
        i.e. check the surrounded lat, lon position values against to the 
        passed lat, lon position value. If all the surrounded position values
        are lesser than the center value (passed lat, lon position value)
        then return this center value. 
        
        In any case while checking the surrounded lat, lon position value is 
        higher than the center value, then immediately come out the function
        by returning False.
        
        If any case while checking the surrounded lat, lon position value is
        equal to the center value, then again check that point's (position's)
        surrounded lat, lon position value and do comparison. It has some 
        default limit.
        
    Author : Arulalan.T
    
    Date : 17.05.2012
     
    """
    # get the latitude, longitude as list 
    dlat = list(data.getLatitude()[:])
    dlon = list(data.getLongitude()[:])
    # get the lengths of the above lat, lon list 
    dlatlen = len(dlat)
    dlonlen = len(dlon)
    # get the value of the center point which is passed by the argument 
    # lat, lon of the data 
    centerVal = data(latitude = lat, longitude = lon, squeeze = 1)
    # get the lat,lon index.
    # Here we are using lat, lon index instead of using actual lat, lon value 
    # itself. Because the lat,lon resolution may be in float point. 
    # To avoid this, we are using lat, lon index integer value itself, to 
    # compare the surrounded lat, lon values and the centerVal. 
    latIndex = dlat.index(lat)
    lonIndex = dlon.index(lon)
    
    ## We are going to increment/decrement the both latindex, lonindex, 
    ## and get the value at the new position. Compare that value against the 
    ## centerVal. If that is lesser than the centerVal, then return the 
    ## centerVal, else return None.
    ## If any point (value) is higher than the centerVal, then do immediately
    ## return None. 
    for latInc, lonInc in [(1,0), (0, 1), (-1, 0), (0, -1)]:    
        
        # get the new lat, lon position by adding the iter value (lat and 
        # lon increment or decrement).
        latpos = latIndex + latInc
        lonpos = lonIndex + lonInc
        
        # check either the new lat & lon position is lesser than the length 
        # of the latitude, longitude list or not.
        if not (latpos < dlatlen and lonpos < dlonlen):
            # lat, lon position is equal or higher than the latitude, 
            # longitude length. So skip the operation and do continue.
            continue
        
        # get the val of the new position
        val = data(latitude = dlat[latpos], longitude = dlon[lonpos], 
                                                        squeeze = 1)
        if val < centerVal:
            # val is less than the centerVal, so continue the loop.
            continue
        elif val == centerVal:
            # val is equal to the centerVal. Here we need to check next to 
            # the current position value also. We have to do this check upto 
            # some limit.
            
            # limit of the iteration to compare the next value
            iteration = 5
            # next increment to lat, lon position            
            next = 2
            while iteration:   
                # get the val of the next lat, lon position             
                val = data(latitude = dlat[latIndex + latInc*next],
                       longitude = dlon[lonIndex + lonInc*next], squeeze = 1)
                
                if val < centerVal:  
                    # found that val is less than centerVal. So we have to 
                    # break this while loop.                  
                    break
                elif val == centerVal:
                    # still val is equal to the centerVal. So continue the 
                    # while loop by increment the next position.
                    next += 1
                    iteration -= 1
                else:                   
                    # val is greater than the centerVal. So we can break out 
                    # of the function by using return statement. 
                    return False                
            # end of while iteration:
        else:
            # val is greater than the centerVal. So we can break out 
            # of the function by using return statement.
            return False
    # end of for latInc, lonInc in [(1,0), (0, 1), (-1, 0), (0, -1)]: 
    
    # Here surrounded lat, lon values are less than the center value. 
    # so return the center value.
    return centerVal
# end of def is_surrounding_less(data, lat, lon):

def is_surrounding_greater (data, lat, lon):
    """
    is_surrounding_greater : Find either the surrounded lat, lon position 
        values are greater to the centre value on passed lat, lon of the data.
        
        i.e. check the surrounded lat, lon position values against to the 
        passed lat, lon position value. If all the surrounded position values
        are greater than the center value (passed lat, lon position value)
        then return this center value. 
        
        In any case while checking the surrounded lat, lon position value is 
        lower than the center value, then immediately come out the function
        by returning False.
        
        If any case while checking the surrounded lat, lon position value is
        equal to the center value, then again check that point's (position's)
        surrounded lat, lon position value and do comparison. It has some 
        default limit.
        
    Author : Arulalan.T
    
    Date : 17.05.2012
     
    """
    # get the latitude, longitude as list 
    dlat = list(data.getLatitude()[:])
    dlon = list(data.getLongitude()[:])
    # get the lengths of the above lat, lon list 
    dlatlen = len(dlat)
    dlonlen = len(dlon)
    # get the value of the center point which is passed by the argument 
    # lat, lon of the data 
    centerVal = data(latitude = lat, longitude = lon, squeeze = 1)
    # get the lat,lon index.
    # Here we are using lat, lon index instead of using actual lat, lon value 
    # itself. Because the lat,lon resolution may be in float point. 
    # To avoid this, we are using lat, lon index integer value itself, to 
    # compare the surrounded lat, lon values and the centerVal. 
    latIndex = dlat.index(lat)
    lonIndex = dlon.index(lon)
    
    ## We are going to increment/decrement the both latindex, lonindex, 
    ## and get the value at the new position. Compare that value against the 
    ## centerVal. If that is lesser than the centerVal, then return the 
    ## centerVal, else return None.
    ## If any point (value) is higher than the centerVal, then do immediately
    ## return None. 
    for latInc, lonInc in [(1,0), (0, 1), (-1, 0), (0, -1)]:    
        
        # get the new lat, lon position by adding the iter value (lat and 
        # lon increment or decrement).
        latpos = latIndex + latInc
        lonpos = lonIndex + lonInc
        
        # check either the new lat & lon position is lesser than the length 
        # of the latitude, longitude list or not.
        if not (latpos < dlatlen and lonpos < dlonlen):
            # lat, lon position is equal or higher than the latitude, 
            # longitude length. So skip the operation and do continue.
            continue
        
        # get the val of the new position
        val = data(latitude = dlat[latpos], longitude = dlon[lonpos], 
                                                        squeeze = 1)
        if val > centerVal:
            # val is greater than the centerVal, so continue the loop.            
            continue
        elif val == centerVal:
            # val is equal to the centerVal. Here we need to check next to 
            # the current position value also. We have to do this check upto 
            # some limit.
            
            # limit of the iteration to compare the next value
            iteration = 5
            # next increment to lat, lon position            
            next = 2
            while iteration:   
                # get the val of the next lat, lon position             
                val = data(latitude = dlat[latIndex + latInc*next],
                       longitude = dlon[lonIndex + lonInc*next], squeeze = 1)
                
                if val > centerVal:  
                    # found that val is greater than centerVal. So we have to 
                    # break this while loop.                  
                    break
                elif val == centerVal:
                    # still val is equal to the centerVal. So continue the 
                    # while loop by increment the next position.
                    next += 1
                    iteration -= 1
                else:                   
                    # val is less than the centerVal. So we can break out 
                    # of the function by using return statement. 
                    return False                
            # end of while iteration:
        else:
            # val is less than the centerVal. So we can break out 
            # of the function by using return statement.
            return False
    # end of for latInc, lonInc in [(1,0), (0, 1), (-1, 0), (0, -1)]: 
    
    # Here surrounded lat, lon values are greater than the center value. 
    # so return the center value.
    return centerVal
# end of def is_surrounding_greater (data, lat, lon): 

def getHighs (data, value=1015):
    """
    getHighs : get the centred highs values along with its latitude, longitude  
               of the passed data. Centred highs means the surrounded lat, lon 
               values are should be less than the centre high value.
    
    arguments:
            data : cdms2 variable with latitude, longitude axis information
            value : the centred highs are greate than or equal to this value.
                    default val is 1015.
    
    return : returning the list containing tuples which are containing lat, 
             lon and centred high values. If there is no centred highs
             less or equal to the passed value arg, then return an empty list. 
    
            eg: [(35.5, 85.5, 1027.11), (37.5, 73.5, 1024.29),
                 (31.0, 83.0, 1019.28), (40.0, 91.5, 1015.39)]
                  
    Author : Arulalan.T
    
    Date : 17.05.2012
    
    """
    highs = []
    _indices = []    
    
    # get the latitude, longitude list values
    lat = data.getLatitude()[:]
    lon = data.getLongitude()[:]
    
    # get the maximum value of the data and convert to the integer type to 
    # fastup the finding high values over the passed data.
    maxp = int(data.max())
    while maxp >= value:
        # maxp is greater than then arg value.
        
        # get the masked data which is less than the maxp. 
        mdata = numpy.ma.masked_less(data, maxp)        
        # get the location (lat, lon) values of the above masked data.
        location = numpy.nonzero(mdata)
        # free memory
        del mdata
        
        for latIndex, lonIndex in zip(location[0], location[1]):
            # set flag as true to find either the val is high or not
            computeHigh = True
            for lat_ind, lon_ind in _indices:
                # loop through previously stored high's lat, lon indexes.
                # Get the +ve diff b/w previou lat, lon indexes and current lat, 
                # lon indexes.
                lat_diff = abs(lat_ind - latIndex)
                lon_diff = abs(lon_ind - lonIndex)
                
                if lat_diff <= 3 or lon_diff <=3:
                    # the diff is less than some limit.
                    # so make the flag as false and break the loop.
                    computeHigh = False
                    break
            # end of for lat_ind, lon_ind in lat_indices, lon_indices:            
            if computeHigh:                    
                # flag is true. so need to compute the high.
                
                # get the proper lat, lon values
                latval = lat[latIndex]
                lonval = lon[lonIndex]
                # call the below function by passing the data, lat, lon values
                # If the returned is not false, then the returned val is high.
                high = is_surrounding_less(data, latval, lonval)
                if high:
                    # found high value. append it in to the proper list.
                    # store the lat,lon & high values
                    highs.append((latval, lonval, high))
                    # stor the lat, lon indexes values. So while finding next 
                    # high value, we can compare it.
                    _indices.append((latIndex, lonIndex))                    
            # end of if computeHigh: 
        # end of for latIndex, lonIndex in zip(loc[0], loc[1]):
                
        # find the next maximum value of the data and convert to the integer 
        # type to fastup the finding next high values over the passed data. 
        maxp = int(nextmax(data, maxp))       
    # end of while maxp >= value:
    # return all the highes along with its lat, lon in a list 
    return highs
# end of def getHighs (data, value=1015):

def getLows (data, value=1000):
    """
    getLows : get the centred lows values along with its latitude, longitude  
              of the passed data. Centred lows means the surrounded lat, lon 
              values are should be higher than the centre low value.
    
    arguments:
            data : cdms2 variable with latitude, longitude axis information
            value : the centred lows are less than or equal to this value.
                    default val is 1000.
                    
    return : returning the list containing tuples which are containing lat, 
             lon and centred low values. If there is no centred lows less or
             equal to the passed value arg, then return an empty list. 
    
            eg: [(30.0, 74.5, 993.28003), (27.0, 80.0, 994.07001), 
                  (21.0, 90.0, 998.26001), (34.0, 100.0, 999.53998), 
                  (25.0, 95.5, 1000.3)]
                  
    Author : Arulalan.T
    
    Date : 17.05.2012
    
    """
    lows = []
    _indices = []    
    
    # get the latitude, longitude list values
    lat = data.getLatitude()[:]
    lon = data.getLongitude()[:]
    
    # get the minimum value of the data and convert to the integer type to 
    # fastup the finding lows values over the passed data.
    
    # Add 1 to this min value, since we are going to mask the data higher than
    # the this rounded min value. since this is least number, while doing 
    # masked_greater operation, the whole data should be masked. To avoid this 
    # situation, we are adding 1 to this min value.
    minp = int(data.min() + 1)
    
    # add 1 to the value to compare against previosly incremented min value.
    while minp <= value + 1:
        # minp is less than then arg value.
        
        # get the masked data which is greater than the minp. 
        mdata = numpy.ma.masked_greater(data, minp)        
        # get the location (lat, lon) values of the above masked data.
        location = numpy.nonzero(mdata)        
        # free memory
        del mdata
        
        for latIndex, lonIndex in zip(location[0], location[1]):
            # set flag as true to find either the val is low or not
            computeLow = True
            for lat_ind, lon_ind in _indices:
                # loop through previously stored low's lat, lon indexes.
                # Get the +ve diff b/w previou lat, lon indexes and current 
                # lat, lon indexes.
                lat_diff = abs(lat_ind - latIndex)
                lon_diff = abs(lon_ind - lonIndex)
                
                if lat_diff <= 3 or lon_diff <=3:
                    # the diff is less than some limit.
                    # so make the flag as false and break the loop.
                    computeLow = False
                    break
            # end of for lat_ind, lon_ind in lat_indices, lon_indices:            
            if computeLow:                    
                # flag is true. so need to compute the low.
                
                # get the proper lat, lon values
                latval = lat[latIndex]
                lonval = lon[lonIndex]
                # call the below function by passing the data, lat, lon values
                # If the returned is not false, then the returned val is high.
                low = is_surrounding_greater(data, latval, lonval)
                                 
                if low:
                    # found low value. append it in to the proper list.
                    # store the lat,lon & low values
                    lows.append((latval, lonval, low))
                    # stor the lat, lon indexes values. So while finding next 
                    # high value, we can compare it.
                    _indices.append((latIndex, lonIndex))                    
            # end of if computeHigh: 
        # end of for latIndex, lonIndex in zip(loc[0], loc[1]):
        
        # find the next minimum value of the data and convert to the integer 
        # type to fastup the finding next lows values over the passed data. 
        
        # Add 1 to this min value, since we are going to mask the data higher 
        # than the this rounded min value. since this is least number, while 
        # doing masked_greater operation, the whole data should be masked. 
        # To avoid this situation, we are adding 1 to this min value.
        minp = int(nextmin(data, minp) + 1)
    # end of while minp >= value:
    # return all the lows along with its lat, lon in a list 
    return lows
# end of def getLows (data, value=1000):
