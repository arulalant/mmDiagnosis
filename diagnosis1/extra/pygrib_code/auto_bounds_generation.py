import numpy as np
import sys
import cdms2
class Auto_Bounds_Generation():
	''' getting the input as latitudes and return its bounds as Axis object '''
	
	def __init__(self,latitude,longitude):
		self.latitude = latitude
		self.longitude = longitude
		
		# comment it because we are going the following methods from other module. so comment it for , not calling auto matically.
		#self.latitude_properties_checking()
		#self.longitude_property_checking()
		
	def latitude_properties_checking(self):
		''' checking lats properties and calling corresponding methods to generate its bounds '''
		
		#
		# Checking the passed latitude is Global one or not
		#
		
		# we can comment the next block, if we no need to check the its pure global lat,lon are not
		lat_len = len(self.latitude)
		if lat_len % 2 == 0 :
			if all(0 for i in range(lat_len / 2) if self.latitude[i] != -(self.latitude[lat_len-1-i]) ) :
				print " passed Global latitude \n"
			else:
				print "latitude is not in global range \n. pass correct latitudes\n"
				sys.exit()
		else:
			# if latitude lenght is an odd no 
			if all(0 for i in range(lat_len / 2) if self.latitude[i] != -(self.latitude[lat_len-1-i]) ) :
				if ( self.latitude[(lat_len/2)] < self.latitude[(lat_len/2)+1] < self.latitude[(lat_len/2)+2] ) :
					print " passed Global latitude \n"
				else :
					print "This is not global latitudes at center point\n"
					sys.exit()
			else:
				print "latitude is not in global range \n. pass correct latitudes\n"
				sys.exit()
			
		
		#
		# checking the passed latitudes are within the range(-90,90)
		#
		if 90>= max(self.latitude) and -90<= min(self.latitude) :
			#print "within range"
				
			spacing_of_latitude = ( self.latitude[i+1]-self.latitude[i] for i in range(len(self.latitude)-1) )
		
			# len(set(list))==1 means, the list contains same element in spacing_of_latitude
			delta = list(set(spacing_of_latitude)) 
			
			if len(delta) == 1: # check the diff of consecutive elements in latitude list is same or not.
				# equally spaced latitudes... calling createEqualIntervalLatitude function to generate its bounds
				return self.createEqualIntervalLatitude(latitude=self.latitude, delta = delta[0])
			
			else :
				# so latitude is not equally spaced.
				print 'not equally spaced'
				from math import sin,radians		
				#checking the latitudes consecutive sin value diff is either same or not. if not means, the latitudes is not equalAreaAxis. we are rounding the floating precision as 6, since floating makes wrong decsion making.
		
				sin_diff_value = [ str(round(sin(radians(self.latitude[i])) - sin(radians(self.latitude[i+1])),6))[0:6] for i in range(len(self.latitude)-1) ]
				#print sin_diff_value		
				
				checking_diff =	[ 'not_equal' for i in range(len(sin_diff_value)-1) if sin_diff_value[i+1]!=sin_diff_value[i] ]
			
				if 'not_equal' not in checking_diff :
					# the difference b/w consecutive latitude of sin value are same, if that is equal_Area_Axis.
					# the latitude is equal_Area_Axis. So we calling createEqualAreaLatitude function to generate its bounds
					return self.createEqualAreaLatitude(latitude=self.latitude) 
									
				else:
					print "Latitude is not an EqualAreaAxis"
					
					# calling last option to find out its bounds
					gaussian = self.gaussian_latitude_axis(latitude=self.latitude)
					if gaussian == 0:
						# lats
						print "Error : passed latitude is not matching to any one of the pattern to create its bounds. Please pass correct format of lats\n"
						sys.exit()
					else:
						return gaussian # returning the gaussian bounds axis
					
		else :
			print "Error : latitude valsues not within the range of -90 to 90\n"
			sys.exit()		
				
				
	def longitude_property_checking(self):
		''' checking the longitude properties and call the createEqualIntervalLongitude method to get its bounds '''
		
		# since longitude is range from 0 to 360, we no need to check the following global check up. it should check it has [-90,0,90] only. ok.
		
		'''
		#
		# Checking the passed longitude is Global one or not
		#
		
		lon_len = len(self.longitude)
		if lon_len % 2 == 0 :
			if all(0 for i in range(lon_len / 2) if self.longitude[i] != -(self.longitude[lon_len-1-i]) ) :
				print " passed Global latitude \n"
			else:
				print "longitude is not in global range \n. pass correct longitude\n"
				sys.exit()
		else:
			# if longitude lenght is an odd no 
			if all(0 for i in range(lon_len / 2) if self.longitude[i] != -(self.longitude[lon_len-1-i]) ) :
				if ( self.longitude[(lon_len/2)] < self.longitude[(lon_len/2)+1] < self.longitude[(lon_len/2)+2] ) :
					print " passed Global longitude \n"
				else :
					print "This is not global longitude at center point\n"
					sys.exit()
			else:
				print "longitude is not in global range \n. pass correct longitude\n"
				sys.exit() '''
				
		#
		# checking the passed longitude are within the range(0,360)
		#
		if 360>= max(self.longitude) and 0<= min(self.longitude) :
			#print "within range"
				
			spacing_of_longitude = ( self.longitude[i+1]-self.longitude[i] for i in range(len(self.longitude)-1) )
		
			# len(set(list))==1 means, the list contains same element in spacing_of_longitude
			delta = list(set(spacing_of_longitude))
			if len(delta) == 1: # check the diff of consecutive elements in longitude list is same or not.
				# equally spaced longitude... calling createEqualIntervalLongitude function to generate its bounds
				return self.createEqualIntervalLongitude(longitude=self.longitude,delta=delta[0])
			
			else :
				# so longitude is not equally spaced.
				print 'not equally spaced'
				sys.exit()
				
	def createEqualIntervalLongitude(self,longitude, delta):
		''' calling cdms2.createUniformLongitudeAxis to genrate its bounds and axis '''
		
		lon_start = longitude[0]
		lon_end =longitude[-1]
		length = len(np.asarray(np.arange(lon_start,lon_end+delta,delta))) # we cant call xrange here, since xrange takes only int arg not float. delta may have float. so we are calling here numpy arange
		
		eq_interval_long = cdms2.createUniformLongitudeAxis(startLon = lon_start, nlon = length, deltaLon = delta) 
		
		#print 	eq_interval_long[:]
		#print 	eq_interval_long.getBounds()
		return 	eq_interval_long
		
		
		
	def createEqualIntervalLatitude(self,latitude,delta):
		''' return generated bounds according to passed latitudes. return as Axis object 
			eg input latitude = [-90,-80,-70,...80,90]
		'''
		lat_start = latitude[0]
		lat_end = latitude[-1]
		length = len(np.asarray(np.arange(lat_start,lat_end+delta,delta))) # we cant call xrange here, since xrange takes only int arg not float. delta may have float. so we are calling here numpy arange
		
		eq_interval_lat = cdms2.createUniformLatitudeAxis(startLat = lat_start, nlat = length, deltaLat = delta)
		
		#print eq_interval_lat[:]
		#print eq_interval_lat.getBounds()
		return eq_interval_lat
		
		#
		# commenting the following my own code, since we are going to use cdat inbuild methods
		#
		'''
		bounds = np.zeros((len(latitude),2)) # initilizing bounds list
		space = (latitude[0]-latitude[1])/2 # return the bounds spacing period
		for i in xrange(len(latitude)-1):
			bounds[i][0] = latitude[i] + space
			bounds[i][1] = latitude[i+1] + space
			
		# last value of bounds list
		bounds[-1][0],bounds[-1][1] = latitude[-1] + space, latitude[-1] - space 
		
		if latitude[0] == -90 :
			# setting bounds start as -90 if the latitudes begings with -90.
			bounds[0][0] = -90 
				
		if latitude[-1] == 90 :
			# setting bounds ends as 90 if the latitudes ends with 90.
			bounds[-1][1] = 90 
			
		print latitude
		print bounds
		'''
		
		

	def createEqualAreaLatitude(self,latitude, increaselat=0, tc=np.float32):
		"""Create a EqualAreaLatitude.

		#####This grid is regular in longitude and regular in sine of latitude

		Arguments:
		reslat -- Number of latitude points
		reslon -- Number of longitude points
		startlon -- Starting longitude
		increaselat -- Order of the latitudes (0 = decreasing, 1 increasing)
		tc -- np type code of the axes' values

		Output:
		
		"""
				
		rlat = len(latitude)
		
		eq_area_axis = cdms2.createEqualAreaAxis(rlat)
		
		#commenting the following codes, since we are going to use cdms2 inbuild method itself...
		
		# the below code may help if the lat may be equal area axis but removed some of the lats means, the length should vary.. at that time the above rlat formula makes the wrong lats values.... so at that time we our self hv to generate the boundaries by using the below method.
		
		'''		
		# Compute latitude values
		lstart = np.asarray(1., tc)
		lstep = np.asarray(2./rlat, tc)
		lastedge = np.asarray(-90., tc)
		if increaselat:
		    lstart = -lstart
		    lstep = -lstep
		    lastedge = -lastedge
	
		lvals = np.arcsin(lstart -(np.arange(np.asarray(rlat, tc)) +np.asarray(0.5, tc)) * lstep) *np.asarray(180. / np.pi, tc)
		
		
		#lvals = np.arcsin((np.array(latitude, tc) +np.asarray(0.5, tc)) * lstep) #*np.asarray(180. / np.pi, tc)
		# Compute latitude bounds
		ledges = np.zeros(rlat + 1, tc)
		ledges[:-1] = np.arcsin(lstart -(np.arange(np.asarray(rlat,tc))) * lstep) * np.asarray(180. / np.pi, tc)
		#ledges[:-1] = np.arcsin((np.array(latitude,tc)) * lstep) #* np.asarray(180. / np.pi, tc)
		ledges[-1] = lastedge
		lbounds = np.zeros((rlat, 2), tc)
		for i in xrange(rlat):
		    lbounds[i, 0] = ledges[i]
		    lbounds[i, 1] = ledges[i + 1]
		
		print lvals
		print lbounds
		
		'''
		
		#print eq_area_axis[:]
		#print eq_area_axis.getBounds()
		return eq_area_axis
	
	def gaussian_latitude_axis(self,latitude):
		''' gaussian latitude axis checking and generating its bounds using in-build method of cdms2. '''
		# have to develop this function in some other manner soon
		
		#checking the given latitude is either gaussian's latitude axis or not in nasty way at present
		
		gaussian_axis = cdms2.createGaussianAxis(len(latitude))
		gaussian_axis_latitude = gaussian_axis[:]
		
		gaussian_axis_latitude = map(str,gaussian_axis_latitude)
		latitude = map(str,latitude)
				
		if len([ 'match' for i in range(len(latitude)) if latitude[i][0:5] == gaussian_axis_latitude[i][0:5]  ] ) == len(latitude) :
			#print 'match'
			#print gaussian_axis[:]
			#print gaussian_axis.getBounds()
			return gaussian_axis
		else:
			#print 'dont match'
			print " Latitude is not matching to gaussian pattern \n"
			return 0
	
	

# uncomment it and  call for testing the module itself.
'''
		

a = Auto_Bounds_Generation([ 64.15806724 , 44.427004  ,  30. ,         17.45760312,   5.73917048,
-5.73917048 ,-17.45760312 , -30.,         -44.427004 ,  -64.15806724],[-180, -175, -170, -165, -160, -155, -150, -145, -140, -135, -130, -125, -120, -
115, -110, -105, -100, -95, -90, -85, -80, -75, -70, -65, -60, -55, -50, -45, -40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140,145, 150, 155, 160, 165, 170, 175,180]) 
#a.latitude_properties_checking()
#a.createEqualIntervalLatitude([-90,-80,-70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
#a.createEqualAreaLatitude([ 64.15806779 , 44.42700416 , 29.99999986 , 17.4576027 ,   5.73916977,  -5.73917149, -17.45760449, -30.00000183, -44.42700655, -64.15807171])

b = Auto_Bounds_Generation([-90,-80,-70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90],[-180, -175, -170, -165, -160, -155, -150, -145, -140, -135, -130, -125, -120, -115, -110, -105, -100, -95, -90, -85, -80, -75, -70, -65, -60, -55, -50, -45, -40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140,145, 150, 155, 160, 165, 170, 175,180])
  
b = Auto_Bounds_Generation([ 76.88245793 , 59.88994169,  42.79752184,  25.68323419,   8.5616985,  -8.5616985 , -25.68323419, -42.79752184, -59.88994169, -76.88245793])

'''
