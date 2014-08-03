__version__ = '1.0'
__author__ = 'Arulalan.T '


import numpy, pygrib, cdms2
import os,sys
from auto_bounds_generation import *
# created local regions dictionary for subRegion
#from regions import * 
import cdms2.MV2 as MV
import cdtime,cdutil







class My_Simple():

	''' Using this class we can optimise the repeated code like 'do- while' '''

    	def __init__(self,string=None,myrange=None,mytype=None):
	
		self.val = self.do_while(string,myrange,mytype)

	def do_while(self,string=None,myrange=None,mytype=None):
		''' getting the input from user untill, user will give the one input within the expected range '''
		
		run = True
		while(run):
			input_from_user = raw_input(string)
			if mytype != None:
				try:
					input_from_user = mytype(input_from_user)
				except:
					print "Please choose correct option "
					continue
			if input_from_user not in myrange:
				print "Please select correct option from this :\n %s" %(myrange)
				run = True
				continue
			else:
				run = False
				
		return input_from_user
				
		
		
		
class DaysError(Exception):
	def __init__(self,*args):
		print "\nDaysError Error : "
		for i in args:
			print i
		
class DaysStringError(DaysError):
	pass

class DaysIntegerError(DaysError):
	pass
	
class DaysTypeError(DaysError):
	pass
		
class Days():

	def __init__(self):
		pass


	def comptime(self,date):
		"""
		comptime : To convert date from yyyymmdd formate into cdtime.comptime formate
	       
	        Condition : 
	       	   passing date must be yyyymmdd formate either int or 
	        Inputs:
		   date in yyyymmdd formate
		   
	        Outputs:
	           It should return the date in cdtime.comptime object type
		   
	        Usage:
	       
		   example:
                      comptime(20110423) returns 2011-4-23 0:0:0.0 as comptype.
                      
		   
	        Written by: Arulalan.T

	        Date: 23.04.2011l;
		
		"""
		
		if isinstance(date,int): date = str(date)
		if not len(date)==8 : raise DaysStringError, 'The given date must be yyyymmdd formate only'
		year = int(date[0:4])
		month = int(date[4:6])
		day = int(date[6:8])
		return cdtime.comptime(year,month,day)
		
	# end of def comptime(self,date):
	
	def _yyyymmdd_from_comp(self,comptime):
	
		"""
		_yyyymmdd_from_comp : To convert date from cdtime.comptime into yyyymmdd formate as string
	       
	        Condition : 
	       	   passing date must be comptime formate 
	        Inputs:
		   date in comptime
		   
	        Outputs:
	           It should return the date in yyyymmdd string formate
		   
	        Usage:
	       
		   example:
		       comptime = cdtime.comptime(2010,4,29) -> 2010-4-29 0:0:0.0	
                      _yyyymmdd_from_comp(comptime) returns '20100429' in yyyymmdd string formate                      
                      
		   
	        Written by: Arulalan.T

	        Date: 29.04.2011
		
		"""
		
		try:	
			# if comptime is real comptime type, the below single line should work.
			# we couldnt find out comptime class/type by using its comptime object.
			return str(int(comptime.absvalue))
		except:
			# if comptime is string
			comptime = str(comptime)
			comptime = comptime.split(' ')[0]
			comptime = comptime.split('-')
			year = comptime[0]
			month = comptime[1]
			if len(month) == 1 : month = '0' + month 
			day = comptime[2]
			if len(day) == 1 : day = '0' + day 
			return  year + month + day 
		
	# end of def _yyyymmdd_from_comp(self,comptime):
		
	
	def first_last_date_of_month(self,month,year,calendarName=None):
	
		"""
		first_last_date_of_month : To find and return the first date and last date of the given month of the year, with cdtime.calendar option.
	       
	        Condition : 
	       	   passing month should be either integer of month or name of the month in string.
	       	   year should be an integer
	       	   calender is optional. It takes default calendar
	       	   
	        Inputs:
		   month may be even in 3 char like 'apr' or 'April' or 'aPRiL' or like any month or 4
		   year 
		   
	        Outputs:
	           It should return the first date and last date of the given month & year in yyyymmdd string formate
		   
	        Usage:
	       
		   example:
		       first_last_date_of_month(4,2010)	returns '20100401' and '20100430' in yyyymmdd string formate                      
                       first_last_date_of_month('feb',2010)	returns '20100228' and '20100228' in yyyymmdd string formate 
		   
	        Written by: Arulalan.T

	        Date: 29.04.2011
		
		"""
	
		_months = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
		
		if isinstance(month,int):
			month = int(month) #to remove zero from the passed integer no . convert 04 into 4.
			if not month in _months.values():
				raise DaysIntegerError, ' not valid month passed. month must be in between 1 to 12 '
			
		elif isinstance(month,str) :
			if len(month) <3:
				raise DaysStringError, ' pass correct month, atlease 3 char need'
			month = month.lower()[0:3]
			if _months.has_key(month):
				month = _months[month]
			else:
				raise DaysError, 'wrong month arg passed '
		else:
			raise DaysTypeError,"month either string like 'may' or interger of the month in between 1 to 12 "
		
		
		if not isinstance(year,int):
			raise DaysIntegerError, ' year must be intger '
		
		if calendarName == None:
			calendar = cdtime.DefaultCalendar
		#end of if
		else:
			if not isinstance(calendarName,int):
				raise DaysError, ' The passed calendarName is not an instance of cdtime.calendar '
			calendar = calendarName
		# end of else
		
		firstday = cdtime.comptime(year,month,1)
		nextmonth = firstday.add(1,cdtime.Month,calendar)
		lastday = nextmonth.sub(1,cdtime.Day,calendar)
		
		firstday = self._yyyymmdd_from_comp(firstday)
		lastday = self._yyyymmdd_from_comp(lastday)
		
		return firstday,lastday
		
		
	# end of def first_last_date_of_month(self,month,year,calendarName=None):
	
	
	def move_days(self,year,month,day,movedays,calendarName=None):
		"""
		move_days : To move the day both direction and get the moved date yyyymmdd format 
	       
	        Condition : 
	       	   passing year,month,day,movedays should be integer type. 
	       
	        Inputs:
		   movedays is an integer to move the date. If it is negative, then we should get the previous date with interval of the no of days [i.e. movedays ]
		   
	        Outputs:
	           It should return the string type of the date formate like yyyymmdd 	
		   
	        Usage:
	       
		   example1:
                      move_days(2011,04,03,200) returns '20111020'
                      move_days(2011,04,03,-200) returns '20100915'
                      
                   example2:
                      move_days(2011,04,03,200,cdtime.NoLeapCalendar)   yet to complete it
		   
	        Written by: Arulalan.T

	        Date: 06.04.2011
		
		"""
		
		# already imported cdtime module from cdat path
		
		if not (isinstance(year,int) and isinstance(month,int) and isinstance(day,int) and isinstance(movedays,int) ):
			raise DaysIntegerError, ' year, month, day, movedays should be interger type '
		
		if calendarName == None:
			calendar = cdtime.DefaultCalendar
		#end of if
		else:
			if not isinstance(calendarName,int):
				raise DaysError, ' The passed calendarName is not an insstnce of cdtime.calendar '
			calendar = calendarName
		# end of else
			
		comptime = cdtime.comptime(year,month,day)
		daychanges = comptime.add(movedays,cdtime.Days,calendar)
		return self._yyyymmdd_from_comp(daychanges)
		
	# end of def move_days(self,year,month,day,movedays,calendarName=None):
		
	
	def xdrange(self,startdate,enddate,stepdays = None,calendarName=None,returnType = 's'):
	
		"""
		xdrange : generate the dates in yyyymmdd or cdtime.comptime formate from startdate to enddate with stepdays. 
			  we can set the cdtime.calendarName to generate the date(s) in between the given range.
	                  xdrange means xDateRange
	        Condition : 
	       	  The startdate and enddate must be yyyymmdd formate (either string or cdtime.comptime). 
	       	  if enddate is higher than the startdate, then stepdays must be +ve.
	       	  if enddate is lower than the startdate, then stepdays must be -ve.
	       	  by default stepdays is 1 day.
	           
	        Inputs:
		  startday, endday in yyyymmdd formate either string or integer type.
		  stepdays to skip the days.
		  calendarName is one of the cdtime calendar type
		  returnType is either 's' or 'c'. if 's' means the return date should be in string type. if 'c' means the return date should be cdtime type itself.
		  Default returnType takes 's' as arg.
		   
	        Outputs:
	           It should return a generator not as list. Using this generator we can produce the date(s) in between the startdate and enddate including both the days.
	           Finally the generated date in string type.
		   
	        Usage:
	       
		   example 1:
                      gen = xdrange(20110407,20110410)
                      for i in gen:
                      	print i
                      	
                      >>> 20110407
                      >>> 20110408
                      >>> 20110409
		      >>> 20110410
		      
		   example 2:
		      gen = day.xdrange(20120227,20120301,1,cdtime.NoLeapCalendar)
		      for i in gen:
                      	print i 
			
		      >>> 20120227
		      >>> 20120228
		      >>> 20120301
			
		      Note 1: In the example 2, 2012 is leap year, since we passed cdtime.NoLeapCalendar it generated without 29th day in feb 2012.
		      we can use stepdays as any +ve integer number
		      
		      Note 2: The generator returns both startdate and enddate also.
		      
		   example 3:
                      gen = xdrange(startdate = 20110407,enddate = 20110410, returnType = 'c')
                      for i in gen:
                      	print i
                      	
                      >>> 2011-4-7 0:0:0.0
                      >>> 2011-4-8 0:0:0.0
                      >>> 2011-4-9 0:0:0.0
		      >>> 2011-4-10 0:0:0.0
		      
		      In this example it should generate the date in cdtime.comptime type itself. 
		      Because we have passed returnType = 'c' in the arg. By default it shoule return string type only
		      
		   example 4:
                      gen = xdrange(startdate = cdtime.comptime(2011,04,07),enddate = cdtime.comptime(2011,04,10), returnType = 'c')
                      for i in gen:
                      	print i
                      	
                      >>> 2011-4-7 0:0:0.0
                      >>> 2011-4-8 0:0:0.0
                      >>> 2011-4-9 0:0:0.0
		      >>> 2011-4-10 0:0:0.0 
		      
		      Here the input dates are in cdtime.comptime object itself.
		      
		   example 5:
		      gen = xdrange(startdate = cdtime.comptime(2011,04,11),enddate = cdtime.comptime(2011,04,7), stepdays = -1, returnType = 'c')
                      for i in gen:
                      	print i
                      	
		      >>> 2011-4-10 0:0:0.0
		      >>> 2011-4-9 0:0:0.0
		      >>> 2011-4-8 0:0:0.0
		      >>> 2011-4-7 0:0:0.0
                      
                      Note : In this example we have passed startdate is higher than then enddate, So we must have to pass the stepdays in -ve sign.

	        Written by: Arulalan.T

	        Date: 07.04.2011
		
		"""
		
		# finding the passed dates are cdtime.comptime type . We cant find this using 'isinstance' method. so we are using str comparision 
		if str(type(startdate)) == "<type 'comptime'>" and str(type(enddate)) == "<type 'comptime'>" :
			# convert cdtime.comptime into float using absvalue method, and convert that into int. it should be like yyyymmdd formate only
			startdate, enddate = int(startdate.absvalue), int(enddate.absvalue)
		# end of if str(type(startdate)) == "<type 'comptime'>" and str(type(enddate)) == "<type 'comptime'>" :
			
		# converting date into string
		startdate = str(startdate)
		enddate = str(enddate)
		
		if  ((len(startdate) != 8) or  (len(enddate) != 8) ):
			raise DaysStringError, 'the date(s) are must be yyyymmdd formate or cdtime.comptime formate'
		# end of if not (len(startdate) == 8 and len(enddate) == 8):
		
		if stepdays == None:
			stepdays = 1		
		else :
			if not isinstance(stepdays,int):
				raise DaysIntegerError, 'stepdays must be an integer'
			# end of if not isinstance(stepdays,int):
		# end of if stepdays == None:
		
		if calendarName == None:
			calendar = cdtime.DefaultCalendar		
		else:
			if not isinstance(calendarName,int):
				raise DaysError, ' The passed calendarName is not an insstnce of cdtime.calendar '
			calendar = calendarName
		#end of if
		
		if not returnType in ['c','s']:
			raise DaysTypeError," returnType either should 's' or 'c'. if 's' means the return date should be in string type. \
						if 'c' means the return date should be cdtime type itself"
		# end of if not returnType in [0,1]:
		
		startyear = int(startdate[0:4])
		startmonth = int(startdate[4:6])
		startday = int(startdate[-2:])
		
		
		endyear = int(enddate[0:4])
		endmonth = int(enddate[4:6])
		endday = int(enddate[-2:])
		
		startcomp = cdtime.comptime(startyear,startmonth,startday)
		endcomp = cdtime.comptime(endyear,endmonth,endday)
		compare = startcomp.cmp(endcomp)
		
		if compare == 1:
			# The end date is lower than the start date 
			if cmp(stepdays,0) != -1:
				raise DaysError, "The stepdays must be negative since the startdate is 'higher' than the enddate "
			else:
				stepdays = stepdays * -1
				sign = -1
			# end of if cmp(stepdays,0) != -1:
		elif compare == 0:
			raise DaysError, " both are same date "		
		else:
			sign = 1
			if cmp(stepdays,0) == -1:
				raise DaysError, "The stepdays must be positive since the startdate is 'lower' than the enddate "
			# end of if cmp(stepdays,0) == -1:
		# end of if compare == 1:
			
		# genearating the relative cdtime of startdate 
	    	daystring = 'days since %s' % (startyear)
		startdaysrel = startcomp.torel(daystring)
		startdays = (str(startdaysrel).split(' ')[0]).split('.')[0]
		
		# genearating the relative cdtime of enddate
		enddaysrel = endcomp.torel(daystring)
		enddays = (str(enddaysrel).split(' ')[0]).split('.')[0]
		# finding the difference days in between startdate and enddate 
		# multiplying the sign value to make it as +ve, if the difference is -ve 
		diffdays = (int(enddays) - int(startdays)) * sign 
				
		for movedays in xrange(0, diffdays + 1, stepdays):
			# here we are multiplying the movedays with sign. If that is -ve means, days goes backward
			returndate = startcomp.add(movedays * sign, cdtime.Days, calendar)			
			if returnType == 'c':
				# returning the comptime type date
				yield returndate
			else:
				# returning the string type (yyyymmdd) date
				returndate =  self._yyyymmdd_from_comp(returndate)
				yield returndate 
		# end of for movedays in xrange(0,diffdays+1,stepdays):
		
		
	# end of def xdrange(self,startdate,enddate,stepdays = None,calendarName=None):
	
# end of class Days():
			
			
class DirectoryInfoError(Exception):
	def __init__(self,*args):
		if not args == None:
			print "\nDirectoryInfoError Error : "
			for i in args:
				print i
			'''
			err = "Error : \n "
			for i in args:
				err +=i
			print err
			'''
			
			
class DirectoryInfoStringError(DirectoryInfoError):
	pass

class DirectoryInfoIntegerError(DirectoryInfoError):
	pass
	
	
class Directory_Info(My_Simple,Days):
	''' Using this Directory_Info class, we are going to list out the list of fles to analysis and \
			forcaste and then we can select single or multiple files, to do further actions'''
			
	
	
	
	def __init__(self):
		
		
	
		''' initialize variables and changing the path '''
		
		#a = My_Simple("Enter any no",['1','2','3'])
		#print a.val
				
		self.anl_files =[]
		#self.anl_files_hours = []
		self.anl_files_date =[]
		self.fcst_files = []
		self.fcst_files_date = []
		self.fcst_files_hours = []
		self.multiple_grb_files = []
		#self.anl_hours_vs_date = {}
		self.fcst_hours_vs_date = {}
		self.data_and_axlist_from_mulitple_grbs = {}
		self.axlist_for_all_grb_files = None
		self.data_part_extract_need_or_not = 'no'
		self.dataPath = None
		self.modelName = None
		self._forecastdays_ = {24:1,48:2,72:3,96:4,120:5,144:6,168:7}
		self._modelname_ = None
		self._models_ = {}
		
		
		
		
				
	# end of def __init__(self):
	
	def _set_dataPath_modelName_(self,dataPath,modelName):
	
		"""
		_set_dataPath_modelName_ : setting the dataPath and modelName
	        
	        Condition : 
	       	  we must call this function. Then only we can access the data along with our own data directory.
	       	  Also it is important to set the modelName to generate the grb filename
	       	  
	        Inputs:
		  dataPath as string with absolute path
		  modelName : It must be exist in the available models
		   
	        Outputs:
	           changing the os working directory as dataPath.
		   
	        Usage :
	        	_set_dataPath_modelName_('/mnt/ncmrw-data-2010','NCMRWF2010')
	        	
	        Written by: Arulalan.T

	        Date: 09.05.2011
		
		"""
	
		self.dataPath = dataPath
		self.modelName = modelName
		
		if self.dataPath is not None:
			if os.path.isdir(self.dataPath):
				self.cwd = self.dataPath
			else:
				raise DirectoryInfoError, ' the given path %s is not exist or not mounted ' % (self.dataPath)
				
			# end of if os.path.isdir(self.dataPath):
		else:
			print "You didnt pass the dataPath or passed it as None"
			print "So I am going to take the currecnt path as the grb directory "
			self.cwd = os.getcwd()
		
		# end of if self.dataPath is not None:
		
		os.chdir(self.cwd)
		print 'changed path',self.cwd
		self.models_grb_filename_structure() # calling the fn
		
		if self.modelName is None:
			# default model name
			self._modelname_ = 'NCMRWF2010'
		elif self._models_.has_key(self.modelName):
			# the modelName is available
			self._modelname_ = self.modelName			
		else:
			raise DirectoryInfoError("Choosen model",self.modelName,"not exists in the predefined models",self._models_.keys())
		
		return True
		# end of if self.modelName is None:
		
	# end of def _set_dataPath_modelName_(self,dataPath,modelName):
		
		
	
	def models_grb_filename_structure(self):
		
		"""
		models_grb_filename_structure : setting the model name and calling the appropriate methods which will helps to create the grb file name and its directory name.
		
		Condition : 
	       	   Whenever changing or adding new models, we must add the method and model name in this dictionary.
	       
	        Outputs:
	           It should call the particular method.And that method should return the filename, dirname strucure. It may vary, depends upon the model structure.
		   
	        Usage:
	       
		   example:
                      models['NCMRWF2010'] returns the partial dirname and partial filename
                      
		   
	        Written by: Arulalan.T

	        Date: 06.04.2011
		
		"""
		
		
		self._models_['NCMRWF2010'] = self.ncmrwf_2010_model_dir_file_name() # calling the method
		
	# end of def models_grb_filename_structure(self):
	
	
	def ncmrwf_2010_model_dir_file_name(self):
		
		"""
		ncmrwf_2010_model_dir_file_name : it should return the starting name of both the dirname and grb filename
		
		Condition : 
	       	   The returning dirname and filename is not complete or absoulte name. It has to add the date in the dirname and add the 'anl' or 'fHOUR' in the file name.
	       
	        Outputs:
	           It should return the dirname and filename structure. This structure has defined according to the NCMRWF 2010 MonSoon Data Structure.
		 
	        
	        Written by: Arulalan.T

	        Date: 06.04.2011
		
		"""
		
		directoryname = 'gdas.'
		grb_filename = 'gdas1.t00z.grb'
		return directoryname, grb_filename
		
	# end of def ncmrwf_2010_model_dir_file_name(self):
	
	
	
	def grib_filename_path(self,Type,date,hour=None):
		"""
		grib_filename_path : returning the grb file path 
		
		Condition : 
	       	   pass the hour if we passed Type as 'f'.
	       	   date should be match with grib directories date 
	       
	        Inputs:
		   Type , data and/or hour
		   
	        Outputs:
	           It should return the string type grib file name with absolute path
		   
	        Usage:
	       
		   example:
                      grib_filename_path('a','20100525') returns '/mnt/ncmrw-data-2010/gdas.20100525/gdas1.t00z.grbanl'
                      grib_filename_path('f','20100525',24) returns '/mnt/ncmrw-data-2010/gdas.20100525/gdas1.t00z.grbf24'
                      
		   
	        Written by: Arulalan.T

	        Date: 06.04.2011
		
		"""
		
		if Type == None or date == None:
			raise DirectoryInfoError, 'we must pass the Type option and date '
		# end of if Type == None or date == None:
		if Type not in ['a','A','f','F','r','R']:
			raise DirectoryInfoError, "Type option should be in any one of the following ['a','A','f','F','r','R'] "
		# end of if Type not in ['a','A','f','F','r','R']:
		if isinstance(date,int):
			date = str(date)
		# end of if isinstance(date,int):
		if len(date)!= 8:
			raise DirectoryInfoStringError, 'the date must be yyyymmdd formate'
		# end of if len(date)!= 8:
		if Type in ['f','F','r','R'] and hour == None:
			raise DirectoryInfoError, ' we must pass the hour arg to find the fcst file '
		# end of if Type in ['f','F','r','R'] and hour == None:
		
		if self._modelname_ == 'NCMRWF2010':	
					
			partial_dirname, partial_filename = self._models_[self._modelname_]		
			dirname = partial_dirname + date
		
			if Type in ['a','A']:
				end_part_filename = 'anl'
			# end of if Type in ['a','A']:
			if Type in ['f','F','r','R']:
				end_part_filename = 'f' + str(hour)
			# end of if Type in ['f','F','r','R']:
			grbfilename = partial_filename + end_part_filename
			grb_filename_path = dirname + '/'+ grbfilename
		
		# end of if self._modelname_ == 'NCMRWF2010':	
		
		return grb_filename_path	
		# return self.cwd + '/' + grb_filename_path
			
	
	
	# end of def grib_filename_path(self,Type,date,hour=None):
		
		
		
	
	def find_partners(self,Type,date,hour=None):
	
		"""
		find_partners : To find the partners of the any particular day anl grib file or any particular day and hour of the fcst grib file. Each fcst file has its truth anl file.
		                i.e. today 24 hour fcst file's partner is tomorrow's truth anl file. today 48 hour fcst file's partner is the day after tomorrow's truth anl file. 
		                keep going on the fcst vc anl files. Same concept for anl files partner but in reverse concept.
		                Today's truth anl file's partners are yesterdays' 24 hour fcst file, day before yesterday's 48 hour fcst file and keep going backward ...
		                This what we are calling as the partners of anl and fcst files. 
		                For present fcst hours partner is future anl file and for present anl partners are the past fcst hours files.
		
		  
	        Condition : 
	       	   if 'f' as passed then hour is mandatory one
	       	   else 'a' as passed then hour is None
	       	   
	        Inputs:
		   Type = 'f' or 'a' i.e fcst or anl file
		   date must be yyyymmdd string formate or cdtime.comptime formate
		   hour is like 24 multiples in case availability of the fcst grib files
		   
	        Outputs:
	           
	           If 'f' has passed this method returns a corresponding partner of the anlysis grb \
	           filename with absolute path and its date in string type within tuple
	           If 'a' has passed thid method returns a dictionary. 
	              It contains the availability of the fcst hours as key and its corresponding fcst grib filename with absoulte \
	              path and its date in string type within tuple as value of the dict.
		   
	        Usage:
	       
		   example 1:
                     	find_partners('f','20100525',24) --> ('/mnt/ncmrw-data-2010/gdas.20100526/gdas1.t00z.grbanl', '20100526')
			find_partners('f','2010-5-25',24) --> ('/mnt/ncmrw-data-2010/gdas.20100526/gdas1.t00z.grbanl', '20100526')
                     	find_partners('f',cdtime.comptime(2010,5,25),24) --> ('/mnt/ncmrw-data-2010/gdas.20100526/gdas1.t00z.grbanl', '20100526')
			
			find_partners('a','20100526') --> {24: ('/mnt/ncmrw-data-2010/gdas.20100525/gdas1.t00z.grbf24','20100525')}		
		   
		   example 2:	
		   	find_partners('f','20100525',72) --> ('/mnt/ncmrw-data-2010/gdas.20100528/gdas1.t00z.grbanl', '20100528')
		   	
			find_partners('a','20100601') --> {24: ('/mnt/ncmrw-data-2010/gdas.20100531/gdas1.t00z.grbf24', '20100531'), 
							   48: ('/mnt/ncmrw-data-2010/gdas.20100530/gdas1.t00z.grbf48', '20100530'),
							   72: ('/mnt/ncmrw-data-2010/gdas.20100529/gdas1.t00z.grbf72', '20100529'),
							   96: ('/mnt/ncmrw-data-2010/gdas.20100528/gdas1.t00z.grbf96', '20100528'), 
							   120: ('/mnt/ncmrw-data-2010/gdas.20100527/gdas1.t00z.grbf120', '20100527'),
							   144: ('/mnt/ncmrw-data-2010/gdas.20100526/gdas1.t00z.grbf144', '20100526'),
							   168: ('/mnt/ncmrw-data-2010/gdas.20100525/gdas1.t00z.grbf168', '20100525')}
					
			Note : Depends upon the availability of the fcst and anl files, it should return the files path
			
		  example 3:
		  	find_partners('a','20100601',144) --> ('/mnt/ncmrw-data-2010/gdas.20100526/gdas1.t00z.grbf144', '20100526')
		  	
		  	If not available for the passed hour means it should return None

	        Written by: Arulalan.T

	        Date: 03.04.2011
		
		"""
				
		date = str(date)
		# finding is the passed date cdtime.comptime string formate
		if len(date.split(' ')[0].split('-')) > 1:
			# Yes, passed date is in cdtime.comptime formate
			date = self._yyyymmdd_from_comp(date)
		if len(date) != 8 :
			raise DirectoryInfoStringError, "The passed date should be the format of yyyymmdd or cdtime.comptime formate "
			
		
		
		year = int(date[0:4])
		month = int(date[4:6])
		day = int(date[-2:])
		
				
		if Type in ['f','F']:
			# fcst arg passed
			if hour == None:
				raise DirectoryInfoError, "you must pass hour to find out the forecast grb partner "
				
			if self._forecastdays_.has_key(hour):
				partner_day = self._forecastdays_[hour]			
			else:
				raise DirectoryInfoError("the passed %d hour not match with keys of forecastdays dict " %(hour))
			
			# calling the move_days to find out the partner day
			# calling Days's methos move_days
			truth_anl_day = self.move_days(year,month,day,partner_day)
			filename = self.grib_filename_path('a',truth_anl_day)
			if os.path.isfile(filename):
				# returning the filename path and its date within tuple
				return (filename,truth_anl_day)
			else:
				return None
				
		if Type in ['a','A','r','R']:
			# anl arg passed or rainfall arg passed
			if not hour == None:
				# finding the partner day by passing the arg as partner hour
				if self._forecastdays_.has_key(hour):
					partner_day = self._forecastdays_[hour]			
				else:
					raise DirectoryInfoError("the passed %d hour not match with keys of forecastdays dict " %(hour))
			
				# to find the previous day, we are passing the -ve sign to the move_days
				# calling Days's methos move_days
				previous_fcst_day = self.move_days(year,month,day,partner_day*-1)
				# generating the grb filename
				filename = self.grib_filename_path('f',previous_fcst_day,hour)
				if os.path.isfile(filename):
					# returning the filename path and its date within tuple
					return (filename,previous_fcst_day)
				else:
					print " The passed hour %s is not available for the patner fcst grib files " % (hour)
					return None
			
			else:
				# hour is none. i.e. need to extract all the available fcst hours			
				grb_fcst_file_path = {}
				# loop throughing all the partner days and hours accordingly
				for partner_hour,partner_day in self._forecastdays_.items():
					# to find the previous day, we are passing the -ve sign to the move_days
					# calling Days's methos move_days
					previous_fcst_day = self.move_days(year,month,day,partner_day*-1)
					# generating the grb filename
					filename = self.grib_filename_path('f',previous_fcst_day,partner_hour)
					if os.path.isfile(filename):
						# adding to the temporary dictionay
						grb_fcst_file_path[partner_hour] = ( filename,previous_fcst_day ) # returning the filename path and its date within tuple
						
				return grb_fcst_file_path
		# end of if Type in ['a','A','r','R']:
			
	# end of def find_partners(self,Type,date,hour=None):
			
# end of class	Directory_Info()
		
		
		
class CollectionInfoError(Exception):
	
	def __init__(self,*args):
		if not args == None:
			print "\nCollectionInfoError Error : "
			for i in args:
				print i
			'''
			err = "Error : \n "
			for i in args:
				err +=i
			print err
			'''
			
			
class CollectionInfoStringError(CollectionInfoError):
	pass

class CollectionInfoIntegerError(CollectionInfoError):
	pass
		
class Collection_Info(My_Simple):
	'''Using this Collection_Info, we can assign the following variables \
	('variableName','unit','regular','leveltype','level','fcsttime','fcstdate')into any object. Have to add more doc here  '''
	
	def __init__(self):
		'''initializing the object variables '''
		self.variableName = ''
		self.unit = ''
		self.regular = ''
		self.typeOfLevel = ''
		self.level = ''
		self.fcsttime = ''
		self.fcstdate = ''
		self.sno = '' 
		self.all_vars = []
		self.all_leveltypes = []
		self.all_vars_leveltypes = []
		
		# regions are in order of longitude and latitudes
		self.regions = {
		'CIndia' : ((73,90),(22,28)),
	'PenIndia' : ((74,85),(7,21)),
	'WcstIndia' : ((70,78),(10,20)),
	'AIR' :  ((67,100),(7,37)),
	'India1' : ((20,140),(-20,60)), 
	'India2' : ((40,120),(-10,40))
		}
		
		# short names for grib variables
		self._shortVars_ = {
				"pr" : "Precipitation rate",
				"T" : "Temperature",
				"hfls" : "Surface latent heat flux",
				"T2m_min6h" : "Minimum temperature at 2 metres since last 6 hours",
				"psl" : "Mean sea level pressure",
				"zg" : "Geopotential Height",
				"ua" : "U component of wind",
				"hus" : "Specific humidity",
				"ice_cov" : "Ice cover (1=land, 0=sea)",
				"ps" : "Surface pressure",
				"prt" : "Total Precipitation",
				"theta" : "Potential temperature",
				"runoff" : "Runoff",
				"T2m" : "2 metre temperature",
				"prw" : "Precipitable water",
				"cl" : "Total Cloud Cover",
				"sndw" : "Snow depth water equivalent",
				"snfw" : "Snow Fall water equivalent",
				"v10m" : "10 metre V wind component",
				"hfss" : "Surface sensible heat flux",
				"lsmask" : "Land-sea mask",
				"orog" : "Orography",
				"p" : "Pressure",
				"sit" : "Ice thickness",
				"tcoz" : "Total column ozone",
				"T2m_max6h" : "Maximum temperature at 2 metres since last 6 hours",
				"va" : "V component of wind",
				"vorabs" : "Absolute vorticity",
				"u10m" : "10 metre U wind component",
				"alb" : "Albedo",
				"hur" : "Relative humidity",
				}
		
	# end of def __init__(self):
	

	def open_grib_file(self,name=None):
		''' opening the grib file using pygrib module'''
		# Grib file name
		if name == None :
			self.file_name = 'samplegrbanl1.grb'
		else:
			self.file_name = name
			
		print "\nOpening the file - %s to process it\n" % (self.file_name)
		# opening the grib file.
		self.file = pygrib.open(self.file_name)
		# opening the grib file index alone. This is muxh faster than just opening file.
		self.fileidx = pygrib.index(self.file_name,'name','typeOfLevel','level')

	# end of def open_grib_file(self,name=None):
	

	def read_variables(self,sno=None,line=None):
		''' read the variables from the grib file and assigning to the object variables correspondingly '''
		
		
		
		if sno == None and line == None :
			self.sno = 1 #default first element
		elif sno != None :
			self.sno = int(sno)
		elif line == None :
			#move the point to the begining of the file
			self.file.seek(0) 
			# getting the string of specified sno 
			line = self.file[self.sno] 
		elif line != None :
			# passing the extracted line from any where. by this way also we can set the attributes
			line = line
		else :
			print "pass either sno or a grib line"			
		print line
		var = str(line).split(':')
		
		# assigning values to its corresponding object elements
		self.sno = var[0]
		self.variableName = var[1]
		self.unit = var[2]
		self.regular = var[3]
		self.typeOfLevel = var[4]
		self.level = var[5]
		self.fcsttime = var[6]
		self.fcstdate = var[7]
		# end of assignments
		
	# end of def read_variables(self,sno=None,line=None):
	
		
	def get_all_vars(self):
		# make the pygrib file pointer at the start point
		self.file.seek(0)
		# collecting all the variables name,typeoflevel from the grib file
		for line in self.file:
			var = str(line).split(':')
			
			self.all_vars.append(var[1])
			self.all_leveltypes.append(var[4])
			self.all_vars_leveltypes.append((var[1],var[4])) # tuple
			
		# make the all_vars list as unique one
		self.all_vars = list(set(self.all_vars))
		self.all_leveltypes = list(set(self.all_leveltypes))
		self.all_vars_leveltypes = list(set(self.all_vars_leveltypes)) # pairs of vars and leveltype
		
		# soring list
		self.all_vars.sort()
		self.all_leveltypes.sort()
		
	# end of def get_all_vars(self):
	
	def listVariable(self):
		''' It should list out the available variables name from the chosen grib file. To use this function, you must do open_grib_file(grib_path)'''
		# calling the function to collect all the variablenames, typeoflevel,
		self.get_all_vars()
		print "\nAvailable variables in the choosen grib file '%s' \n" % (self.file_name) 
		for varname in self.all_vars:
			print ' ',varname
		# end of for varname in self.all_vars:
		print "To see the typeOfLevels use 'all_leveltypes' and to see the pair of variablename and its typeOfLevel use 'all_vars_leveltypes' \n"
	
	# end of def listVariable(self):
	
		
	def search_leveltypes_of_variable(self,variableName):
		''' searhcing the level types of particular variableName '''
		
		# the method get_all_vars should must call to access this method. If user didnt call that method, then we are calling it by ourself.
		if self.all_vars_leveltypes == []:
			self.get_all_vars()
		
		print "\n Leveltypes of the variable %s : \n" % (variableName)
		
		try:
			sno = 1
			array = []
			for pair in self.all_vars_leveltypes:
				if pair[0] == variableName :
					print sno,' : ',pair[1]
					array.append(pair[1])
					sno += 1
			return array
		except:
			print "%s variable may not be in grib file" % (variableName)
		
	# end of def search_leveltypes_of_variable(self,variableName):
	
	
	def _getVariableFromShortName_(self,shortName):
		
		"""
		_getVariableFromShortName_ : It should return the full vaiablename as string.
	       
		Condition : 
		   
	       	   The shortname must be exist in the dictionary to get the fullname of the variable
	       	   
	       	   
		Inputs:
		   shortname of the variables
		   
		   
		Outputs:
		   It should return full name of variable if we pass correct shortname.
		   If we pass full variablename itself, then it should return the same.
		   If we pass some other string that not match with pre-defined variable names, then it should return the what we passed to this function instead of raise error.
		   
		Future :
			Enable the raise error 	       		   
		  			  
			   	
		Written by: Arulalan.T

		Date: 11.05.2011
		"""
		
		if not isinstance(shortName,str):
			raise CollectionInfoStringError,'Passed shortName not string type. It must be string'
		
		if self._shortVars_.has_key(shortName):
			# shortname of the full variablename
			return self._shortVars_[shortName]
		elif shortName in self._shortVars_.values():
			# its not shorname, its full variablename
			return shortName
		
		else:	
			# passed shortName not in the dictionary self._shortVars_ keys and its values. we just return it as it is.
			return shortName
			#raise CollectionInfoError('Wrong short name as passed for variable name. Choose correct shortname from the following pair',self._shortVars_.items())
			
	# end of def _getVariableFromShortName_(self,shortName):
	
	
	def listShortVars(self):
		''' It should list out the available shortname and its full name of the variables'''
		
		print "\nAvailable Shortname for the following variables\n" 
		for shortname,varname in self._shortVars_.iteritems():
			print ' ',shortname,' : ',varname
	
		
	def __getitem__(self,index):
		''' return the element value if user will call the object's element like list method '''
		
		if index == 'sno':
			return_val = self.sno
		elif index == 'variableName':
			return_val = self.variableName
		elif index == 'unit':
			return_val = self.unit
		elif index == 'regular':
			return_val = self.regular
		elif index == 'typeOfLevel':
			return_val = self.typeOfLevel
		elif index == 'level':
			return_val = self.level
		elif index == 'fcsttime':
			return_val = self.fcsttime
		elif index == 'fcstdate':
			return_val = self.fcstdate
		else:
			return_val = '%s index is not present in current object \n' % (index)
		return return_val
	
	# end of def __getitem__(self,index):
	
		
	def new_value(self,value,lat_start_idx,lat_end_idx,lon_start_idx,lon_end_idx):
		''' we can shrink the narray values into small one (value of ndarray)\
		 by passing position of start and end of both latitude and longitude '''
				
		slice_range = (slice(lat_start_idx,lat_end_idx+1),slice(lon_start_idx,lon_end_idx+1))
		return value[slice_range]
		
	# end of def new_value(self,value,lat_start_idx,lat_end_idx,lon_start_idx,lon_end_idx):
		
		
	def possible_levels(self,gph):
		''' by paasing the gribe file reading object, generating the available levels and return the levs_list '''
		possible_levs = len(gph)
		levs_list = []
		if possible_levs != 1:
			for i in range(possible_levs):
				levs_list.append(gph[i]['level'])
			# end of for i in range(possible_levs):
		else:
			levs_list.append(gph[0]['level'])

		return levs_list
	# end of def possible_levels(self,gph):
		
# end of class Collection_Info()
	

class GribAccessError(Exception):
	def __init__(self,*args):
		print "\nGribAccessError Error : "
		for i in args:
			print i
		
class GribAccessStringError(GribAccessError):
	def __init__(self,*args):
		print "\n Error : "
		for i in args:
			print i

class GribAccessIntegerError(GribAccessError):
	pass
	
class GribAccessTypeError(GribAccessError):
	pass
	
	
class Grib_Access(My_Simple,Directory_Info,Collection_Info):
	
	def __init__(self,gph=None,**args):
		if gph!= None:
			self.gph = gph
		
		self.typeOfLevel = None
		self.variableName = None
		self.lat_axis = None
		self.lon_axis = None
		self.level_axis = None
		self.region = None
		self.lat = None
		self.lon = None
		
		# we must call the inherited class's __init__ method. then only we can access all its super class member variables
		
		# initializing the Directoy_Info's __init__ method members
		Directory_Info.__init__(self)		
		
		if not (args.has_key('dataPath') and args.has_key('modelName') ):
			raise GribAccessError, "you must pass the keyword arguments as dataPath and modelName with its corresponding value"
	
		if args.has_key('dataPath'):
			dataPath = args['dataPath']
		else:
			raise GribAccessError, "you must pass one of the keyword argument as dataPath"
		if args.has_key('modelName'):
			modelName = args['modelName']
		else:
			raise GribAccessError, "you must pass one of the keyword argument as modelName"
		
		
		# calling Directory_Info protected method by using self itself, because we have inherited that class
		self._set_dataPath_modelName_(dataPath,modelName)
		
		# initializing the Collection_Info's __init__ method members
		Collection_Info.__init__(self)
			
			
	# end of def __init__(self,gph=None,**args):
	
	def show_keys(self):
		
		for result in self.gph:
			print result, result.keys()

		#print gph[0].keys()
	# end of def show_keys(self):
	

	def grib_data_extraction(self):
	
		#
		# Extract data information
		#
		self.missing_val = self.gph[0]['missingValue']
		self.data = self.gph[0]['values']
	# end of def grib_data_extraction(self):
		
		
	def user_choice_abt_grib_lat_lon_extraction(self):
	
		if len(self.gph) == 1:
			i = 0
		else:
			i = int(raw_input('Enter the index of level range in position \n since it has some duplication in grib variable ... :  '))


		do = My_Simple("Enter any one of the key char to view and access the region of data \n G : Global \n I : India \n U : User Defined \n .... : ",['g','G','i','I','u','U'])
		user_input_abt_lat_lon = do.val
		
		# Create the global axes
		#	
		self.lat_array = self.gph[i]['distinctLatitudes'] 
		self.lon_array = self.gph[i]['distinctLongitudes']
		if user_input_abt_lat_lon == 'g' or user_input_abt_lat_lon == 'G':
				# already created global axes	
				myinfo.data_part_extract_need_or_not = 'no'
				
		elif user_input_abt_lat_lon == 'i' or user_input_abt_lat_lon == 'I':
				lat_start,lat_end,lon_start,lon_end = 0.,40.,60.,100.,
				self.grib_lat_lon_extraction(lat_start,lat_end,lon_start,lon_end)
				myinfo.data_part_extract_need_or_not = 'yes'
				
		else:
			if user_input_abt_lat_lon == 'u' or user_input_abt_lat_lon == 'U':
				print "Latitudes ... : ",self.lat_array
				lat_start = float(raw_input('Enter the start value of latitude : '))
				lat_end = float(raw_input('Enter the end value of latitude : '))
				
				print "Longitudes....: ",self.lon_array
				lon_start = float(raw_input('Enter the start value of longitude : '))
				lon_end = float(raw_input('Enter the end value of longitude : '))

				self.grib_lat_lon_extraction(lat_start,lat_end,lon_start,lon_end)
				myinfo.data_part_extract_need_or_not = 'yes'

	# end of def user_choice_abt_grib_lat_lon_extraction(self):
			
		
	def grib_lat_lon_extraction(self,lat_start,lat_end,lon_start,lon_end):	
			
		''' lat and lon shrinking from the global world lat,lon data'''
		#covert narray to normal list
		lat_array = self.lat_array.tolist()

		# shrinking the latitudes
		myinfo.lat_start_idx = lat_array.index(lat_start)
		myinfo.lat_end_idx = lat_array.index(lat_end)
		# picking the latitudes values with respect to user input
		lat_array = lat_array[myinfo.lat_start_idx : myinfo.lat_end_idx+1]

		#covert resized list into narray
		self.lat_array = numpy.array(lat_array)

		
		#covert narray to normal list
		lon_array = self.lon_array.tolist()

		# shrinking the longitudes
		myinfo.lon_start_idx = lon_array.index(lon_start)
		myinfo.lon_end_idx = lon_array.index(lon_end)
		# picking the longitudes values with respect to user input
		lon_array = lon_array[myinfo.lon_start_idx : myinfo.lon_end_idx+1]

		#covert resized list into narray
		self.lon_array = numpy.array(lon_array)

	# end of def grib_lat_lon_extraction(self,lat_start,lat_end,lon_start,lon_end):

		

		
	def create_cdms2_axes(self):
		''' calling the imported module to generate lat,lons bounds occrdingly and return it as cdms object '''
		
		
		bounds = Auto_Bounds_Generation(latitude = self.lat_array, longitude = self.lon_array)
		self.lat_axis = bounds.latitude_properties_checking()
		self.lon_axis = bounds.longitude_property_checking()

	# end of def create_cdms2_axes(self):
	
	
	def bounds_generation(self,data):
		''' creating bounds array and return it '''
		
		data_length = len(data)
		bounds = numpy.zeros((data_length,2))
		
		
		for i in range(data_length):
		
			if i == data_length-1:
				bounds[i][0] = data[i]
				bounds[i][1] = data[i]
				#print "Last boundary"
			else :
				#print i
				bounds[i][0] = data[i]
				bounds[i][1] = data[i+1]
	
		return bounds
		
	# end of def bounds_generation(self,data):
				
		
	def extract_data_with_partners(self,variableName,typeOfLevel,Type,date,hour=None,level='all',**latlonregion):
	
		
		"""
		extract_data_with_partners : It can extract the data_with_partners. i.e it returns data along with its partners data. 
		It extracts the multiple data (depends upon the level,partners and dates) and returns in single array which contains collection of MV2 variable.
		
	       
		Condition : 
		   
	       	   level is optional. level takes default 'all'. if level passed, it must be belongs to the data variable
	       	   hour is must when Type arg should be 'f' (fcst) to select the file name.
	       	   Pass either (lat,lon) or region.
	       	   
	       	   
		Inputs:
		   Type - either 'a' or 'f'
		   variableName,typeOfLevel,level must be belongs to the data file
		   startdate and enddate must be in yyyymmdd string formate. skipdays must be an integer
		   key word arg lat,lon or region should be passed
		   
		   
		Outputs:
		   It should return the list. It contanins the multiple extracted data as MV2 variable in shape of (level,lat,lon)
		   The first var of the list is the source Type, and the following vars are its partners.
		   
		Usage:
	       
		   example 1:
		        extract_data_with_partners(variableName = "Geopotential Height",typeOfLevel = "isobaricInhPa",Type = 'f', startdate = 20100525, enddate = 20100930,skipdays = 1,calendar = None, hour = 24,level = 'all' ,region = AIR ) #lat=(-90,90),lon=(0,359.5)
		   
		  			  
		Refer :
			method extract_data_of_partners(...)
			
		   	
		Written by: Arulalan.T

		Date: 09.04.2011
		"""
		
		self.checking_major_parameter_to_extract_data(Type,date,hour)
		
		datavariables = []
		
		# calling Directory_Info's method grib_filename_path
		grb_file_name = self.grib_filename_path(Type,date,hour)
		var = self.extract_data_from_grb_file_path(grb_file_name,variableName,typeOfLevel,level,**latlonregion)
		var.date = str(date)
		datavariables.append(  var )
		partners_data = self.extract_data_of_partners(variableName,typeOfLevel,Type,date,hour,level,**latlonregion)
		
		return datavariables + partners_data 
		
	# def extract_data_with_partners(self,variableName,typeOfLevel,Type,date,hour=None,level='all',**latlonregion):
	
		
	def extract_data_of_partners(self,variableName,typeOfLevel,Type,date,hour=None,level='all',**latlonregion):
		
		"""
		extract_data_of_partners : It can extract the data_of_partners. i.e it returns the partners data not along with its source Type data. 
		It extracts the multiple data (depends upon the level,partners and dates) and returns in single array which contains collection of MV2 variable.
		
	       
		Condition : 
		   
	       	   level is optional. level takes default 'all'. if level passed, it must be belongs to the data variable
	       	   hour is must when Type arg should be 'f' (fcst) to select the file name.
	       	   Pass either (lat,lon) or region.
	       	   
	       	   
		Inputs:
		   Type - either 'a' or 'f' or 'r'
		   variableName,typeOfLevel,level must be belongs to the data file
		   startdate and enddate must be in yyyymmdd string formate. skipdays must be an integer
		   key word arg lat,lon or region should be passed
		   
		   
		Outputs:
		      It should return the partners data as single MV2 variable in shape of (time,level,lat,lon). i.e with time axis,level axis, lat axis and lon axis. If level has squeezed while extract the data, then it should return only shape of (time,lat,lon).
		   
		   
		Usage:
	       
		   example 1:
		        extract_data_of_partners(variableName = "Geopotential Height",typeOfLevel = "isobaricInhPa",Type = 'f', date = 20100525, hour = 24,level = 'all' ,region = AIR ) #lat=(-90,90),lon=(0,359.5)
		   
		  			  
					 
		Refer :
			method find_partners(...) of class Days:
			
		   	
		Written by: Arulalan.T

		Date: 09.04.2011
		"""
		
		# have to enable this...
		# self.checking_major_parameter_to_extract_data(Type,date,hour) 
		datavariables = []
		
		# calling Directory_Info's method find_partners
		partner_grb_file_name_date = self.find_partners(Type,date,hour)
		if isinstance(partner_grb_file_name_date,dict):
			partner_hours = partner_grb_file_name_date.keys()
			partner_hours.sort()
			
			for hour in partner_hours :
				partner_grb_file_name,partner_date = partner_grb_file_name_date[hour]
				var = self.extract_data_from_grb_file_path(partner_grb_file_name,variableName,typeOfLevel,level,**latlonregion) 
				var.date = partner_date
				datavariables.append( var )
		else:
		        partner_grb_file_name = partner_grb_file_name_date[0]
			var = self.extract_data_from_grb_file_path(partner_grb_file_name,variableName,typeOfLevel,level,**latlonregion)
			var.date = partner_grb_file_name_date[1]
			datavariables.append( var )
		
		# get the start date from the datavariables
		startdate = datavariables[0].date
		# create the time axis  
		timeAxis = self._generateTimeAxis(len(datavariables),startdate)
		# get the level,lat,lon axis information
		levelAxis = datavariables[0].getLevel()
		latAxis = datavariables[0].getLatitude()
		lonAxis = datavariables[0].getLongitude()	
		
		
		if levelAxis == None:
			# shape (time,lat,lon)
			VAR = cdms2.createVariable(data = datavariables, axes = [timeAxis,latAxis,lonAxis])
		else:
			# shape (time,level,lat,lon)
			VAR = cdms2.createVariable(data = datavariables, axes = [timeAxis,levelAxis,latAxis,lonAxis])
		
		return VAR
		
		
	# end of def extract_data_of_partners(self,variableName,typeOfLevel,Type,date,hour=None,level='all',**latlonregion):
		
		
	def checking_major_parameter_to_extract_data(self,Type,date,hour=None):
	
		"""
		checking_major_parameter_to_extract_data : It should check the major paremeter while extract the data
	       
		Condition : 
	       	   
	       	   hour is must when Type arg should be 'f' (fcst) to select the file name.
	       	    		       	   
		Inputs:
		   Type - either 'a' or 'f'
		   date must be in yyyymmdd string formate
		   hour must be belongs to data variable
		   
		   
		Outputs:
		   It should return None.
		   
		Usage:
	       	
	       	   It just check the passed parameters are correct or incorrect. If any one is incorrect means, it should throw an error with proper reason.
		   It helps while making many method with the same args to check the parameters.
		   			   			   	
		Written by: Arulalan.T

		Date: 09.04.2011
		"""
		
		# checking the value of Type arg
		if Type == None:
			raise GribAccessStringError, " You have to pass the argment Type as either 'a' or 'A' for analysis file or \
			'f' or 'F' for forecast file. Its mandatory argument\n"
			
		else:
			if Type in ['a','A','f','F','r','R']:
				Type = Type
			else:
				raise GribAccessStringError, "you have to pass the argment Type as either 'a' or 'A' for analysis file or \
				 'f' or 'F' for forecast file or 'r' or 'R' for rainfall file, not any other char/str/nos\n" 
				
		
		# checking the hour arg value depends upon Type arg
		if Type in ['a','A']:
			#hour = None
			# hour is no need to find out the fcst files. Even if the user has passed the hour, it may return that hour file alone. For that purpose we are checking and storing the hour variable for the 'a' and 'f' also...
			if not hour==None:
				hour = int(hour) if isinstance(hour,str) else hour
				# Directory_Info attribute
				if not self._forecastdays_.has_key(hour):
					raise GribAccessError("wrong %d hour has passed as arg, its not belongs to fcst grib file hours\n\
					 Choose correct hour\n" %(hour))
					
			
		elif Type in ['f','F']:
			if hour == None:
				raise GribAccessError ,"You have to pass 'hour' as argument if you choose Type as 'f' or 'F'. \
				Please choose correct hour\n"
				
			else:
				hour = int(hour) if isinstance(hour,str) else hour
				# Directory_Info attribute
				if not self._forecastdays_.has_key(hour):
					raise GribAccessError("wrong %d hour has passed as arg, its not belongs to fcst grib file hours\n \
					Choose correct hour\n" % (hour))
					
					
		elif Type in ['r','R']:
			if not hour == None:
				hour = int(hour) if isinstance(hour,str) else hour
				# Directory_Info attribute
				if not self._forecastdays_.has_key(hour):
					raise GribAccessError("wrong %d hour has passed as arg, its not belongs to fcst grib file hours\n \
					Choose correct hour\n" % (hour))
				
										
		
		# checking the date 	
		if date == None :
			raise GribAccessError, "You have to pass the date of file to forecast or analysis further ...\n"
			
		else:
			if isinstance(date,int):
				date = str(date)
				if len(date)!= 8:
					raise GribAccessStringError, ' the passed date length not 8. it must be yyyymmdd formate '
			
			# Directory_Info attribute
			if self._modelname_ == 'NCMRWF2010':
				dir_first_name = self._models_[self._modelname_]
			
				dirname = dir_first_name[0] + date
				if not os.path.isdir(dirname) :
					raise GribAccessError("wrong date %s has passed as arg, its not belongs to the grib data directories date structure.\n \
								Choose correct date\n" % (date))
					
					
		
		# pass the Type , date, hour to generate_grb_file_name and getting the correct file name which is available in the directory
		
		return
	
	# end of def checking_major_parameter_to_extract_data(self,Type,date,hour=None):
	
	
	def extract_data_from_grb_file_path(self,grb_file_name,variableName,typeOfLevel,level,**latlonregion):
	
		"""
		extract_data_from_grb_file_path : It returns the extracted data from the grb_file_name_path as MV2 variable
	       
		Condition : 
	       	   
	       	   grb_file_name is the major parameter. And it must be full grb file name path.
	       	   level is either 'all' or level value
	       	    		       	   
		Inputs:
		   variableName,typeOfLevel,level should be passed correctly.
		   (lat,lon) or region should be passed as keyword arg.
		   
		   
		Outputs:
		   It should return the data as MV2 in shape (level,lat,lon).
		   
		Usage:
	       	
	       	   In the grib file data latlons doesnot have the boundaries. Here it should generate the propere latitude and longitude boundaries.
	       	
	       	Power of this method:
	       	
	       	   When we call this method next time to extract the data for the same (variableName,typeOfLevel,level,**latlonregion) args, the validation should not be repeated even the grb_file_name changed. So we are saving our time to validate the same thing. but all the args should be validated at first time.
		   			   			   	
		Written by: Arulalan.T

		Date: 11.03.2011
		"""
		
		# open the grib file from the grib path
		# calling collectioninfo's method open_grib_file
		self.open_grib_file(grb_file_name)
		
		# its not going to validate for the same (variableName,typeOfLevel,level,**latlonregion) args, when it call next time. But at first time it should validated
		if not ( self.variableName!= None and self.variableName == variableName and self.typeOfLevel!= None and self.typeOfLevel == typeOfLevel and self.__level__ != None and self.__level__ == level and self.lat_axis!=None and isinstance(self.lat_axis,cdms2.axis.TransientAxis) and self.lon_axis!=None and isinstance(self.lon_axis,cdms2.axis.TransientAxis) and self.level_axis!=None and isinstance(self.level_axis,cdms2.axis.TransientAxis) and ((latlonregion.has_key('region') and latlonregion['region']==self.region) or (latlonregion.has_key('lat') and latlonregion['lat']==self.lat) and (latlonregion.has_key('lon') and latlonregion['lon']==self.lon) )  ) :
			
			
			print " i can be printed only one time "
			# calling collectioninfo's method get_all_vars
			self.get_all_vars()
			
			# checking the variableName
			if variableName == None :
				raise GribAccessStringError, "Error : you have to pass the variableName to select data \n"
				
			else:
				# calling collectioninfo's member all_vars
				if variableName not in self.all_vars :
					raise GribAccessStringError("wrong variable has passed as arg, its not belongs to grib files.\n \
					Choose correct variableName from below",self.all_vars,'\n Instead you can use shortname of the following variables',self._shortVars_.items())
					
				else:
					# correct varibleName
					self.variableName = variableName
				
		
	
			# checking the typeOfLevel
			if typeOfLevel == None :
				raise GribAccessStringError, "You have to pass the typeOfLevel to select data. It must be one kind of variableName's types of levels \n"
				
			else:
				# genearate available leveltypes which are all belongs to var
				# calling collectioninfo's member all_vars
				var_leveltypes = [ x[1] for x in self.all_vars_leveltypes if x[0] == variableName ]
				if typeOfLevel not in var_leveltypes :
					raise GribAccessStringError("wrong typeOfLevel %s has passed as arg, its not belongs to variable '%s' in the grib file. \
					 Choose correct typeOfLevel which has pair with variableName.\n %s" % (typeOfLevel,variableName,str(var_leveltypes)))
					
				else:
					# correct typeOfLevel				
					self.typeOfLevel = typeOfLevel
								

			
		
			#if self.level_axis!= None and isinstance(self.level_axis,cdms2.
			# calling collectioninfo's member file object
			gph = self.file.select(name = self.variableName, typeOfLevel = self.typeOfLevel)
			
			# calling collectioninfo's method possible_levels
			levs_list = self.possible_levels(gph)
			self.level = []
			# private __level__ for checking while repeate the same fn for many times
			self.__level__ = level
			# defining the levels
			if level in ['all','ALL','All'] :
				# all levels
				self.level = levs_list
			
			else :
				if level not in levs_list :
					 raise GribAccessError("wrong level has passed as arg, its not belongs to variable %s and its leveltype %s in the grib file. \
					 choose correct level or choose 'all' to select all levels or dont pass the level arg ( it takes default all levels ) \n \
					  here is listed all the levels " % (variableName,typeOfLevel),levs_list)
					
				else:
					# correct level
					self.level.append(level)

			# **latlon is keyword argument. So that we can call this function by passing lat=somevalue,lon=somevalue. i.e. lat,lon keywod is must to pass lat,lon values in this function.
			if latlonregion == {}:
				self.lat,self.lon,self.region = None,None,None
			
			else:
				try:
					# if latlonregion keyword has only lat and lon as arg.
					self.lat = latlonregion['lat']
					self.lon = latlonregion['lon']
							
					if self.lat!=None and self.lon!= None :
						try:
							# if latlonregion has lat,lon and region, suppose the case
							self.region = latlonregion['region']
						except:
							self.region = None # user didnt pass the region as keyword arg
							print "No region keyword passed"
						
						
					else:
						# lat and lon are None and passed in the latlonregion keyword argument
						try:
							self.region = latlonregion['region']
						except:
							print "you may forget to pass region selector or lat&lon selection to extract data. \
							So now Global lat&lon extraction taking place here \n"
							#sys.exit() # if region or lat&lon is mandatory
				except:
					
					try:
						# passed only the region as latlonregion keyword arg.
						self.region = latlonregion['region']
						self.lat,self.lon = None,None # this is must here, assigning the None once again to the lat,lon vars.
					except:
						print "you may forget to pass region selector or lat&lon selection to extract data. \
						So now Global lat&lon extraction taking place, without region selector. \n"
				
					
			
			if self.lat!=None and self.lon!= None and self.region!= None :
				raise GribAccessError, "Please pass either region or lat&lon as argument. Do not pass all the three (lat,lon & region) as keyword args\n"
				
				
			# defining the region object
			#print 'region',region
			if self.region != None:
				#if isinstance(self.region,cdms2.selectors.Selector):
				# calling collectioninfo's member regions
				if self.regions.has_key(self.region):
					
					print "passed region is correct and it is an instance of the region"
				else:
					raise GribAccessStringError("region must be any one of the following keys",self.regions)
					
					# uncomment the following for future domain region
					'''
					import regions as r
					if self.region in dir(r):
						# region may passed as string
						print """you passed region variable as string like with in single or double (', " ) codes. kindly pass it as simply variable, not as string \n """
						sys.exit()
					
					else:
						print "passed region is not an instance of the cdms2.selectors.Selector or its not the variable of region.py module. pl pass correct one from the below one\n"
						list_of_regions = [ x for x in dir(r) if not x.startswith('__')]
						print list_of_regions
						print "Dont pass the region variable as string. It is a variable\n"
						sys.exit()
					'''
			
			# defining the lat,lon axis
			# Create the global axes
			#
			self.lat_array = gph[0]['distinctLatitudes'] 
			self.lon_array = gph[0]['distinctLongitudes']
			
			if self.lat!=None and self.lon!=None:
				if isinstance(self.lat,tuple) and isinstance(self.lon,tuple):
					# checked lat and lon are tuples
				
					if len(self.lat) == 2 and len(self.lon) == 2: 
						# lat , lon must be tuple or list with start and end lat,lon range
						if  all(self.lat) in self.lat_array  and all(self.lon) in self.lon_array :
							# correct lat,lon
							'''self.lat_array = gph[0]['distinctLatitudes'] 
							self.lon_array = gph[0]['distinctLongitudes']
					
							self.grib_lat_lon_extraction(lat[0],lat[1],lon[0],lon[1]) # passing lat,lon start and end to extract the needed lats & lons
							need_to_extract_partial_from_data = True '''
						
					else :
						raise GribAccessError,"wrong size of lat or lon are passed as arg. pass correct lat,lon as size is 2\n"
						
				else:
					# lat ,lon are not tuples
					raise GribAccessTypeError, "lat and lon must be tuple. pl pass it as tuple argument. eg : (5,40),(60,100) \n"
					

			
			# len of lat,lon,level
			self.lat_len = len(self.lat_array)
			self.lon_len = len(self.lon_array)
			self.level_len = len(self.level)
		
			# generating boundary array for levels,lat,lon
			level_bounds = self.bounds_generation(self.level)
			self.level_axis = cdms2.createAxis(self.level,bounds = level_bounds)
			self.level_axis.id = "level"
			self.level_axis.designateLevel()
					
			# creating cdms axis to levels,lat,lon
			bounds = Auto_Bounds_Generation(latitude = self.lat_array, longitude = self.lon_array)
			self.lat_axis = bounds.latitude_properties_checking()
			self.lon_axis = bounds.longitude_property_checking()
		
		
		# end of if not ( self.lat_axis!=None and isinstance(self.lat_axis,cdms2.axis.TransientAxis) and self.lon_axis!=None and isinstance(self.lon_axis,cdms2.axis.TransientAxis) and self.level_axis!=None and isinstance(self.level_axis,cdms2.axis.TransientAxis) ) :
		
		
		
		
		# creating numpy zeros array with dimentions of lat and lon and no of lenth of levels list. So that we can arrange numpy list according to levels list sequances.
		self.multi_data_numpy_array = numpy.zeros((self.level_len,self.lat_len,self.lon_len), dtype = 'f')
		sno = 0
		
		for level in self.level:
					print "Extracting data of Level : ",level
					# calling collectioninfo's member fileidx
					gph = self.fileidx.select(name = self.variableName, typeOfLevel = self.typeOfLevel, level = level)
					#
					# Extract data information
					#
					missing_val = gph[0]['missingValue'] # data.shape() -> (361,720) -> (y,x) -> (latitude,longitude)
					data = gph[0]['values']
					self.multi_data_numpy_array[sno] = data # copying full data # data.shape() -> (1,361,720) -> (z,y,x) -> (level,latitude,longitude)
					sno += 1
								
		
		
		final_var = cdms2.createVariable(data = self.multi_data_numpy_array, axes = [self.level_axis,self.lat_axis,self.lon_axis], fill_value = missing_val,  attributes = {'typeOfLevel' : self.typeOfLevel, 'id' : self.variableName} )
		
		if self.region!=None:
			# if region as passed then we have to return the selector instance
			# here 'region' is an instance of Selector class.refer regions.py module
			
			#final_var = final_var(self.region,squeeze=1)
			# calling collectioninfo's member region
			lon,lat = self.regions[self.region]
			final_var = final_var.subRegion(longitude = (lon[0],lon[1],'cc'), latitude = (lat[0],lat[1],'cc'),squeeze=1)
			
		if self.lat!=None and self.lon!=None :
			# this is user defined selector by passing lat & lon
			
			#final_var = final_var(domain(longitude = self.lon,latitude = self.lat),squeeze=1)
			
			final_var = final_var.subRegion(longitude = (self.lon[0],self.lon[1],'cc'), latitude = (self.lat[0],self.lat[1],'cc'),squeeze=1)
			
			#print self.lat,self.lon,final_var.shape
		# we have to set the id here once again, since the domain selector setting default ids.
		final_var.id = self.variableName
		#return lat_axis,lon_axis,level_axis,final_var,
		#print final_var.getLatitude(),final_var.getLongitude()
		
		return final_var
		
		
		# returning level and extrated multi_
		#return self.level,multi_data_numpy_array
		
	# end of def extract_data_from_grb_file_path(self,grb_file_name,variableName,typeOfLevel,level,**latlonregion):
	
	
	def extract_data_of_a_date(self,variableName,typeOfLevel,Type,date,hour=None,level='all',**latlonregion):
					
		"""
		extract_data_of_a_date : It extracts the multiple data (depends upon the level) and returns in single MV2 array.
		return shape should be like (level,lat,lon)
	       
		Condition : 
	       	   level is optional. level takes default 'all'. if level passed, it must be belongs to the data variable
	       	   hour is must when Type arg should be 'f' (fcst) to select the file name.
	       	   Pass either (lat,lon) or region.
	       	   
	       	   
		Inputs:
		   Type - either 'a' or 'f'
		   variableName,typeOfLevel,level must be belongs to the data file
		   date must be in yyyymmdd string formate
		   key word arg lat,lon or region should be passed
		   
		   
		Outputs:
		   It should return the extracted data as MV2 variable in shape of (level,lat,lon)
		Usage:
	       
		   example 1:
		        extract_data_of_a_date(variableName = "U component of wind",typeOfLevel = "isobaricInhPa",Type = 'a',date = 20100802,level = 850 , lat=(0,40),lon=(60,100))#region = PenIndia )  return data as MV2 variable
		   
		   example 2:
		   	extract_data_of_a_date(variableName = "V component of wind",typeOfLevel = "isobaricInhPa",Type = 'f',date = 20100802,hour = 24, region = PenIndia )  return data as MV2 variable
		   	
		Written by: Arulalan.T

		Date: 09.04.2011
		"""
						
		self.checking_major_parameter_to_extract_data(Type,date,hour)
		# calling Directory_Info's method grib_filename_path
		grb_file_name = self.grib_filename_path(Type,date,hour)
		var = self.extract_data_from_grb_file_path(grb_file_name,variableName,typeOfLevel,level,**latlonregion)
		var.date = date
                return var
	
	# end of def extract_data_of_a_date(self,variableName,typeOfLevel,Type,date,hour=None,level='all',**latlonregion):
	
		
	def _generateTimeAxis(self,days,startdate,skipdays = 1):
	
		"""
		_genTimeAxis : It should generate the time axis with its bounds
		
		Condition : 
		   
	       	   We must pass days as integer and startdata as yyyymmdd formate		       	   
	       	   
		Inputs:
		   No of days as days, startdate which date should set in the time axis units.
		   Skipdays passed then it should genearate the days with that skipdays. Default it takes 1.
		   
		Outputs:
		   It should return time axis with its bounds. its units as ' days since startdate'
		   
		Usage:
	       
		   example 1:
		       >>> t =  _generateTimeAxis(10,'20100525')
		       >>> t
		           id: axis_1
			   Designated a time axis.
			   units:  days since 2010-5-25 0:0:0.0
			   Length: 10
			   First:  0
			   Last:   9
			   Other axis attributes:
			      calendar: gregorian
			      axis: T
			   Python id:  0xa56a22c
		      
		       >>> t.getBounds()
		  	 array([[ 0.,  1.],
			       [ 1.,  2.],
			       [ 2.,  3.],
			       [ 3.,  4.],
			       [ 4.,  5.],
			       [ 5.,  6.],
			       [ 6.,  7.],
			       [ 7.,  8.],
			       [ 8.,  9.],
			       [ 9.,  9.]])
			       
		   example2:
		   	>>> t1=gobj._generateTimeAxis(10,'20100525',2)
			>>> t1
			   id: time
			   Designated a time axis.
			   units:  days since 2010-5-25 0:0:0.0
			   Length: 10
			   First:  0
			   Last:   18
			   Other axis attributes:
			      calendar: gregorian
			      axis: T
			   Python id:  0x9d06eec

			>>> t1.getBounds()
			array([[  0.,   1.],
			       [  2.,   3.],
			       [  4.,   5.],
			       [  6.,   7.],
			       [  8.,   9.],
			       [ 10.,  11.],
			       [ 12.,  13.],
			       [ 14.,  15.],
			       [ 16.,  17.],
			       [ 18.,  19.]])
		     
			    
		      
		   	
		Written by: Arulalan.T

		Date: 09.04.2011
		"""
		
		
		# checking arguments			
		if not isinstance(days,int):
			raise ValueError,' no of days sould be integer only'
		if not isinstance(startdate,str): startdate = str(startdate)
		if not len(startdate) == 8:
			raise ValueError, ' the startdate should be yyyymmdd formate only'
		if isinstance(skipdays,float):
			raise ValueError, ' The passed skipdays should not be float value. It must be an integer'
		#
		# Creating Time Axis for these range of dates
		#
		
		if skipdays == 1:
			# default action 
			lendate = range(0,days)
		# end of if skipdays == 1:
		if skipdays > 1:
			# if skipdays has passed, then we timeAxis should set with proper days from the startdate. So we should generate the correct timeAxis with that skipdays.
			lendate = range(0,days*skipdays,skipdays)
		# end of if skipdays > 1:
		
		time = cdms2.createAxis(lendate)
		time.designateTime()
		# calling Days's methos comptime
		comptime = self.comptime(startdate)
		time.units = 'days since %s' %(str(comptime))
		time.id = 'time'
		# setting time bounds axis daily
		cdutil.setTimeBoundsDaily(time)
		# end of setting time axis properties
		return time
	
	# end of def _generateTimeAxis(self,days,startdate):
	
		
	def extract_data_for_range_of_dates(self,variableName,typeOfLevel,Type,startdate,enddate,skipdays=1,calendar=None,hour=None,level='all',**latlonregion):
		
		"""
		extract_data_for_range_of_dates : It can extract the data for range of dates.
		It extracts the multiple data (depends upon the level and dates) and returns in single array which contains collection of MV2 variable.
		
	       
		Condition : 
		   
	       	   level is optional. level takes default 'all'. if level passed, it must be belongs to the data variable
	       	   hour is must when Type arg should be 'f' (fcst) to select the file name.
	       	   Pass either (lat,lon) or region.
	       	   
	       	   
		Inputs:
		   Type - either 'a' or 'f'
		   variableName,typeOfLevel,level must be belongs to the data file
		   startdate and enddate must be in yyyymmdd string formate. skipdays must be an integer
		   key word arg lat,lon or region should be passed
		   
		   
		Outputs:
		   It should return the single MV2 variable in shape of (time,level,lat,lon). i.e with time axis,level axis, lat axis and lon axis. If level has squeezed while extract the data, then it should return only shape of (time,lat,lon)
		   
		Usage:
	       
		   example 1:
		        extract_data_for_range_of_dates(variableName = "Geopotential Height",typeOfLevel = "isobaricInhPa",Type = 'f', startdate = 20100525, enddate = 20100930,skipdays = 1,calendar = None, hour = 24,level = 'all' ,region = AIR ) #lat=(-90,90),lon=(0,359.5)
		   
			
		  
		Refer :
		  method xdrange(...)
		   	
		Written by: Arulalan.T

		Date: 09.04.2011
		"""
		
		self.checking_major_parameter_to_extract_data(Type,startdate,hour)
		if not enddate== None:
			self.checking_major_parameter_to_extract_data(Type,enddate,hour)
		datavariables = []
		
		# calling Days's method xdrange
		daterange = self.xdrange(startdate,enddate,skipdays,calendar)
		
		# user may pass the shortname of the variable. To get the full name of the variablename, we are calling this function of Collection_Info class here
		# Collection_Info's method _getVariableFromShortName_
		variableName = self._getVariableFromShortName_(variableName)
		
		# extract data for the date which has derived for the range of dates
		for date in daterange:
			# calling Directory_Info's method grib_filename_path
			grb_file_name_date = self.grib_filename_path(Type,date,hour)
			print grb_file_name_date
			var = self.extract_data_from_grb_file_path(grb_file_name_date,variableName,typeOfLevel,level,**latlonregion) 
			var.date = date
			datavariables.append( var )
			
		
		
		# create the time axis  
		timeAxis = self._generateTimeAxis(len(datavariables),startdate,skipdays)
		# get the level,lat,lon axis information
		levelAxis = datavariables[0].getLevel()
		latAxis = datavariables[0].getLatitude()
		lonAxis = datavariables[0].getLongitude()	
		
		
		if levelAxis == None:
			# shape (time,lat,lon)
			VAR = cdms2.createVariable(data = datavariables, axes = [timeAxis,latAxis,lonAxis])
		else:
			# shape (time,level,lat,lon)
			VAR = cdms2.createVariable(data = datavariables, axes = [timeAxis,levelAxis,latAxis,lonAxis])
		
		return VAR
		
	# end of def extract_data_for_range_of_dates(self,variableName,typeOfLevel,Type,startdate,enddate,skipdays=1,calendar=None,hour=None,level='all',**latlonregion):
	
	
	def getData(self,variableName,typeOfLevel,Type,date,hour=None,level='all',**latlonregion):
	
		"""
		getData : It can extract either the data of a single date or range of dates. It depends up on the input of the date argument.
			  Finally it should return MV2 variable.
	       
		Condition : 
		   
		   date is either tuple or string.
	       	   level is optional. level takes default 'all'. if level passed, it must be belongs to the data variable
	       	   hour is must when Type arg should be 'f' (fcst) to select the file name.
	       	   Pass either (lat,lon) or region.
	       	   
	       	   
		Inputs:
		   Type - either 'a' or 'f'
		   variableName,typeOfLevel,level must be belongs to the data file
		   key word arg lat,lon or region should be passed
		   
		   date formate 1:
		   	date = (startdate,enddate,skipdays)
		   	here startdate and enddate must be like cdtime.comptime formate.
		   	skipdays should be an integer
		   
		   	
		   date formate 2:
		   	date = (startdate)
		   	
		   date formate 3:
		   	date = 'startdate' or date = 'date'
		   
		   eg for date input :
		   	date = ('2010-5-25','2010-6-25',2)
		   	date = ('2010-5-1','2010-6-30')
		   	date = ('2010-5-30')
		   	date = '2010-5-30'
		   	
		   	By default skipdays as 1 takes place.
		   	
		   
		Outputs:
		   
		   	If user passed single date in the date argument, then it should return the data of that particular date as a single MV2 variable.
		   	
		   	If user passed start and enddate in the date argument, then it should return the data for the range of dates as a single MV2 variable with time axis.
		   
		
		Usage:
	       
		   example 1:
		        
				   
		Refer :
			method extract_data_for_range_of_dates(...)
		   	method extract_data_of_a_date(...)
		   	
		Written by: Arulalan.T

		Date: 10.05.2011
		"""
		
		endCompTime = None
		skipdays = 1
		
		# user may pass the shortname of the variable. To get the full name of the variablename, we are calling this function of Collection_Info class here
		# Collection_Info's method _getVariableFromShortName_
		variableName = self._getVariableFromShortName_(variableName)
		
		if isinstance(date,tuple):
			startCompTime = date[0] # assign startdate
			if len(date) >= 2:
				endCompTime = date[1] # assign enddate
			# end of if len(date) >= 2:
			
			if len(date) == 3:
				skipdays = int(date[2]) # assign skipdays
			# end of if len(date) >= 3:
									
		elif isinstance(date,str):
			startCompTime = date # assign date
			
		else:
			raise GribAccessTypeError,'date either must be tuple or string \n Read the following docstring \n %s' % (self.getData.__doc__)
			
		# end of if isinstance(date,tuple):
		
		# converting date from comp type into yyyymmdd type according to our NCMRWF2010 model directory structure name
		startdate = self._yyyymmdd_from_comp(startCompTime)
		
		xdrange = False
		if not endCompTime == None:
			enddate = self._yyyymmdd_from_comp(endCompTime)
			xdrange = True
			
		# end of if not enddate == None:
		
		if xdrange:
			# calling range of dates method to extract the data
			VAR = self.extract_data_for_range_of_dates(variableName = variableName,typeOfLevel = typeOfLevel, Type = Type,startdate = startdate,\
							enddate = enddate,skipdays = skipdays,calendar = None,hour = hour,level = level,**latlonregion)
			
		else:
			# calling single date method to extract the data
			VAR = self.extract_data_of_a_date(variableName = variableName,typeOfLevel = typeOfLevel,Type = Type,date = startdate,hour = hour,level = level,**latlonregion)
		
		
		del level
			
		return VAR
		
	# end of def getData(self,variableName,typeOfLevel,Type,date,hour=None,level='all',**latlonregion):
		
	
	
	
	def getDataPartners(self,variableName,typeOfLevel,Type,date,hour=None,level='all',orginData = 0,datePriority = 'o', **latlonregion):
	
		"""
		getDataPartners : It can extract either the orginDate with its partnersData or it can extract only the partnersData without its orginData for a single date or range of dates. It depends up on the input of the orginData, datePriority,date arguments.
			  Finally it should return partnersData and/or orginData   as MV2 variable.
	       
		Condition : 
		   
		   date is either tuple or string.
	       	   level is optional. level takes default 'all'. if level passed, it must be belongs to the data variable
	       	   hour is must when Type arg should be 'f' (fcst) to select the file name.
	       	   hour is must wehn range of date passed, even thogut Type arg should be 'a' (anl), to choose one fcst file along with hour.
	       	   Pass either (lat,lon) or region.
	       	   
	       	   
		Inputs:
		   Type - either 'a' or 'f'
		   variableName,typeOfLevel,level must be belongs to the data file
		   orginData - either 0 or 1. 0 means it shouldnot return the orginData as single MV2 var.
		   			       1 means it should return both the orginData and its partnersData as two seperate MV2 vars.
		   datePriority - either 'o' or 'p'. 'o' means passed date is with respect to orginData. According to this orginData's date, it should return its partnersData.
		   				     'p' means passed date is with respect to partnersData. According to this partnersData's date, it should return its orginData.
		
		   key word arg lat,lon or region should be passed
		   
		   date formate 1:
		   	date = (startdate,enddate)
		   	here startdate and enddate must be like cdtime.comptime formate.
		   		   	
		   date formate 2:
		   	date = (startdate)
		   	
		   date formate 3:
		   	date = 'startdate' or date = 'date'
		   
		   eg for date input :
		      	date = ('2010-5-1','2010-6-30')
		   	date = ('2010-5-30')
		   	date = '2010-5-30'
		   	
		   	By default skipdays as 1 takes place. User cant override till now.
		   	
		   
		Outputs:
		   
		   If user passed single date in the date argument, then it should return the data of that particular date (both orginData & partnersData) as a single MV2 variable.
		   	
		   If user passed start and enddate in the date argument, then it should return the data (both orginData & partnersData) for the range of dates as a single MV2 variable with time axis.
		   
		
		Usage:
	       	   
	       	   Note :  if 'a'(anl) file is orginData means 'f'(fcst) files are its partnersData and vice versa.                        
	       
		   example1:
		       a,b = getDataPartners('U component of wind',typeOfLevel = 'isobaricInhPa',Type = 'a',date = '2010-6-5',hour = None,level = 'all',orginData = 1,datePriority = 'o', lat=(-90,90),lon=(0,359.5)) 
		       a is orginData. i.e. anl. its timeAxis date is '2010-6-5'.
		       b is partnersData. i.e. fcst. its 24 hour fcst date w.r.t orginData is '2010-6-4'. 48 hour is '2010-6-3'. Depends upon the availability of date of fcst files, 
		       it should return the data. In NCMRWF2010 model, it should return maximum of 7 days fcst files.
		       
		       If we will specify any hour in the same eg, that should return only that hour fcst file data instead of returning all the available fcst hours data.
		       
		   example2:
		       a,b = getDataPartners('U component of wind',typeOfLevel = 'isobaricInhPa',Type = 'f',date = '2010-6-5',hour = 24,level = 'all',orginData = 1,datePriority = 'o', lat=(-90,90),lon=(0,359.5)) 
		       a is orginData. i.e. fcst 24 hour. its timeAxis date is '2010-6-5'.
		       b is partnersData. i.e. anl. its anl date w.r.t orginData is '2010-6-6'. 
		    
		   example3:
		       b = getDataPartners('U component of wind',typeOfLevel = 'isobaricInhPa',Type = 'f',date = '2010-6-5',hour = 24,level = 'all',orginData = 0,datePriority = 'o', lat=(-90,90),lon=(0,359.5)) 
		       b is partnersData. i.e. anl. its anl date w.r.t orginData is '2010-6-6'.   No orginData. Because we passed orginData as 0.
		       
		   example4:
		       a,b = getDataPartners('U component of wind',typeOfLevel = 'isobaricInhPa',Type = 'f',date = '2010-6-5',hour = 24,level = 'all',orginData = 1,datePriority = 'p', lat=(-90,90),lon=(0,359.5)) 
		       a is orginData. i.e. fcst 24 hour. its timeAxis date is '2010-6-6'.
		       b is partnersData. i.e. anl. its anl date w.r.t orginData is '2010-6-5'.  we can compare this eg4 with eg2. In this we passed datePriority as 'p'. So the passed
		       date as set to the partnersData and orginData's date has shifted to the next day.
		       
		   example5:
		       a,b = getDataPartners('U component of wind',typeOfLevel = 'isobaricInhPa',Type = 'a',date = ('2010-6-5','2010-6-6'),hour = 24,level = 'all',\
		     										  orginData = 1,datePriority = 'o', lat=(-90,90),lon=(0,359.5)) 
		       
		       Note : Even though we passed 'a' Type, we must choose the hour option to select the fcst file, since we are passing the range of dates.
		       
		       a is orginData. i.e. anl. its timeAxis size is 2. date are '2010-6-5' and '2010-6-6'.
		       b is partnersData. i.e. fcst 24 hour data. its timeAxis size is 2. date w.r.t orginData are '2010-6-4' and '2010-6-5'.  
		       
		       a's '2010-6-5' has partner is b's '2010-6-4'. i.e. orginData(anl) partners is partnersData's (fcst)
		       same concept for the remains day.
		       a's '2010-6-6' has partner is b's '2010-6-5'.
		       
		   example6:
		       a,b = getDataPartners('U component of wind',typeOfLevel = 'isobaricInhPa',Type = 'a',date = ('2010-6-5','2010-6-6'),hour = 24,level = 'all',\
		     										  orginData = 1,datePriority = 'p', lat=(-90,90),lon=(0,359.5)) 
		       
		       Note : Even though we passed 'a' Type, we must choose the hour option to select the fcst file, since we are passing the range of dates.
		       
		       a is orginData. i.e. anl. its timeAxis size is 2. date are '2010-6-6' and '2010-6-7'.
		       b is partnersData. i.e. fcst 24 hour data. its timeAxis size is 2. date w.r.t orginData are '2010-6-5' and '2010-6-6'.  
		       
		       a's '2010-6-6' has partner is b's '2010-6-5'. i.e. orginData(anl) partners is partnersData's (fcst)
		       same concept for the remains day.
		       a's '2010-6-7' has partner is b's '2010-6-6'. we can compare this eg6 with eg5. In this we passed datePriority as 'p'. So the passed
		       date as set to the partnersData and orginData's date has shifted towards the next days.   
		       
				   
		Refer :
			method extract_data_for_range_of_dates(...)
		   	method extract_data_of_a_date(...)
		   	method extract_data_of_partners(...)
		   	
		   	
		Written by: Arulalan.T

		Date: 27.05.2011
		"""
		
		endCompTime = None
		skipdays = 1
		
		# user may pass the shortname of the variable. To get the full name of the variablename, we are calling this function of Collection_Info class here
		# Collection_Info's method _getVariableFromShortName_
		variableName = self._getVariableFromShortName_(variableName)
		
		if isinstance(date,tuple):
			startCompTime = date[0] # assign startdate
			if len(date) >= 2:
				endCompTime = date[1] # assign enddate
			# end of if len(date) >= 2:
			
#			if len(date) == 3:
#				skipdays = int(date[2]) # assign skipdays
#			# end of if len(date) >= 3:
									
		elif isinstance(date,str):
			startCompTime = date # assign date
			
		else:
			raise GribAccessTypeError,'date either must be tuple or string \n Read the following docstring \n %s' % (self.getData.__doc__)
			
		# end of if isinstance(date,tuple):
		
		# converting date from comp type into yyyymmdd type according to our NCMRWF2010 model directory structure name
		orgin_startdate = self._yyyymmdd_from_comp(startCompTime)
		
		xdrange = False
		if not endCompTime == None:
			orgin_enddate = self._yyyymmdd_from_comp(endCompTime)
			xdrange = True
			# enddate has passed. so we need hour to get the partners data
			if hour == None :
				raise GribAccessError, 'You must pass the hour to return the partners data,since you passed the enddate. i.e range of date.'
			
		# end of if not enddate == None:
		
		if not orginData in [0,1]:
			raise GribAccessTypeError,'orginData either 0 or 1.  0 means without orginData. i.e. only partners data. \
			  1 means with orginData. i.e. both orginData and partnersData. Default it takes 0.'
		
			
		if xdrange:	
			# enddate passed
			# find out the partners startdate and enddate
			partner_startdate = self.find_partners(Type = Type, date = orgin_startdate, hour = hour)[1]
			partner_enddate = self.find_partners(Type = Type, date = orgin_enddate, hour = hour)[1]
			
			
			if datePriority == 'p':
				# swaping the orgin date and partners date
				orgin_startdate,partner_startdate = partner_startdate,orgin_startdate
				orgin_enddate,partner_enddate = partner_enddate,orgin_enddate
												
				if orginData:
					# orginData is 1
					comp_partner_startdate = self.comptime(partner_startdate)
					comp_partner_enddate = self.comptime(partner_enddate)
				
					if self._forecastdays_.has_key(hour):
						movedays = self._forecastdays_.get(hour)
					else:
						raise GribAccessError("wrong %d hour has passed as arg, its not belongs to fcst grib file hours\n \
						Choose correct hour\n" % (hour))
					
					# find out the orgin startdate and enddate
					orgin_startdate = self.move_days(comp_partner_startdate.year,comp_partner_startdate.month,comp_partner_startdate.day,movedays)
					orgin_enddate = self.move_days(comp_partner_enddate.year,comp_partner_enddate.month,comp_partner_enddate.day,movedays)
												
			elif datePriority == 'o':
				# default behaviour. so no need to do any actions
				pass
			else:
				raise GribAccessTypeError,"datePriority either 'o' or 'p'. \n 'o' means passed date set to the orginData. \n 'p' means passed date set to the partnersData.\n"
			
			
		
			# calling range of dates method to extract the data
			if orginData:
				# orginData is 1
				# get the orgin data with respect to orgin_startdate and orgin_enddate
				orgin_data = self.extract_data_for_range_of_dates(variableName = variableName,typeOfLevel = typeOfLevel,Type = Type,startdate = orgin_startdate,\
							enddate = orgin_enddate,skipdays = skipdays,calendar = None,hour = hour,level = level,**latlonregion)
				
			# end of if orginData:
			
			# get the orgin's parnter data with respect to partner_startdate and partner_enddate
			partners_data = self.extract_data_for_range_of_dates(variableName = variableName,typeOfLevel = typeOfLevel, Type = Type,startdate = partner_startdate,\
							enddate = partner_enddate,skipdays = skipdays,calendar = None,hour = hour,level = level,**latlonregion)
			
						
			
		else:
			# end date doesnt passed
			# actions for single date
			
			if datePriority == 'o':
				# default behaviour. so no need to do any actions
				# calling single date method to extract the data
				if orginData:
					# orginData is 1
					# get the orgin data with respect to orgin_startdate
					orgin_data = self.extract_data_of_a_date(variableName = variableName,typeOfLevel = typeOfLevel,Type = Type,date = orgin_startdate,hour = hour,level = level,**latlonregion)
				# end of if orginData:
			
				# get the orgin's partner data with respect to orgin_startdate
			 	partners_data = self.extract_data_of_partners(variableName = variableName,typeOfLevel = typeOfLevel,Type = Type,date = orgin_startdate,hour = hour,level = level,**latlonregion)
			
						
			
			elif datePriority == 'p':
				
				if hour == None:
					raise GribAccessError,"you must pass the hour to choose the partners, since you have set datePriority as 'p' "
				
				else:
					# find out the partners startdate 
					partner_startdate = self.find_partners(Type = Type,date = orgin_startdate, hour = hour)[1]
			
					# swaping the orgin date and partners date
					orgin_startdate,partner_startdate = partner_startdate,orgin_startdate
																
					if orginData:
						# orginData is 1
						comp_partner_startdate = self.comptime(partner_startdate)
									
						if self._forecastdays_.has_key(hour):
							movedays = self._forecastdays_.get(hour)
						else:
							raise GribAccessError("wrong %d hour has passed as arg, its not belongs to fcst grib file hours\n \
							Choose correct hour\n" % (hour))
					
						# find out the orgin startdate 
						orgin_startdate = self.move_days(comp_partner_startdate.year,comp_partner_startdate.month,comp_partner_startdate.day,movedays)
				
						# calling single date method to extract the data
			
						# get the orgin data with respect to orgin_startdate
						orgin_data = self.extract_data_of_a_date(variableName = variableName,typeOfLevel = typeOfLevel,Type = Type,date = orgin_startdate,hour = hour,level = level,**latlonregion)
					# end of if orginData:
			
					# get the orgin's partner data with respect to orgin_startdate
				 	partners_data = self.extract_data_of_a_date(variableName = variableName,typeOfLevel = typeOfLevel,Type = Type,date = partner_startdate,hour = hour,level = level,**latlonregion)
					
				# end of if hour == None:			
												
			
			else:
				raise GribAccessTypeError,"datePriority either 'o' or 'p'. \n 'o' means passed date set to the orginData. \n 'p' means passed date set to the partnersData.\n"
			# end of if datePriority == 'o':
		
			
		# end of if xdrange:	
		
		
		if orginData:
			# orginData is 1
			return orgin_data, partners_data
		else:
			# orginData is 0
			return partners_data
			
		
		
	# end of def getDataPartners(self,variableName,typeOfLevel,Type,date,hour=None,level='all',orginData = 0,datePriority = 'o', **latlonregion):
	
	
	
	
		
			
	def extract_data_for_range_of_dates_with_partners(self,variableName,typeOfLevel,Type,startdate,enddate,skipdays=1,calendar=None,hour=None,level='all',**latlonregion):
	
		"""
		extract_data_for_range_of_dates_with_partners : It can extract the data_with_partners for range of dates. 
		It extracts the multiple data (depends upon the level,partners and dates) and returns in single array which contains collection of MV2 variable.
		
	       
		Condition : 
		   
	       	   level is optional. level takes default 'all'. if level passed, it must be belongs to the data variable
	       	   hour is must when Type arg should be 'f' (fcst) to select the file name.
	       	   Pass either (lat,lon) or region.
	       	   
	       	   
		Inputs:
		   Type - either 'a' or 'f'
		   variableName,typeOfLevel,level must be belongs to the data file
		   startdate and enddate must be in yyyymmdd string formate. skipdays must be an integer
		   key word arg lat,lon or region should be passed
		   
		   
		Outputs:
		   It should return the list. It contanins the multiple extracted data as MV2 variable in shape of (time,level,lat,lon). i.e with time axis,level axis, lat axis and lon axis. If level has squeezed while extract the data, then it should return only shape of (time,lat,lon)
		   
		Bug :
		   Here it as major bug. i.e. extract the data with partners for range of concecutive dates. so it make many duplication in same list. Have to enhance it.
		 
		Usage:
	       
		   example 1:
		        extract_data_for_range_of_dates_with_partners(variableName = "Geopotential Height",typeOfLevel = "isobaricInhPa",Type = 'f', startdate = 20100525, enddate = 20100930,skipdays = 1,calendar = None, hour = 24,level = 'all' ,region = AIR ) #lat=(-90,90),lon=(0,359.5)
		        
		Future :
			set time axis
		   
		Refer :
			method extract_data_with_partners(...)
		   	method xdrange(...)
		   	
		Written by: Arulalan.T

		Date: 09.04.2011
		"""
	
		
		self.checking_major_parameter_to_extract_data(Type,startdate,hour)
		if not enddate== None:
			self.checking_major_parameter_to_extract_data(Type,enddate,hour)
		datavariables = []
		
		# calling Days's method xdrange
		daterange = self.xdrange(startdate,enddate,skipdays,calendar)
		for date in daterange:				
			var = self.extract_data_with_partners(variableName,typeOfLevel,Type,date,hour,level,**latlonregion) 
			datavariables.append( var )
		
		'''	
		time = self._generateTimeAxis(len(datavariables),startdate)
		print datavariables[0][0].getLevel()
		level = datavariables[0][0].getLevel()
		lat = datavariables[0][0].getLatitude()
		lon = datavariables[0][0].getLongitude()
		
		
		if level == None:
			# shape (time,lat,lon)
			VAR = cdms2.createVariable(data = datavariables, axes = [time,lat,lon])
		else:
			# shape (time,level,lat,lon)
			VAR = cdms2.createVariable(data = datavariables, axes = [time,level,lat,lon])
		
		return VAR
		'''
		return datavariables
		
		
	# end of def extract_data_for_range_of_dates_with_partners(self,variableName,typeOfLevel,Type,startdate,enddate,skipdays=1,calendar=None,hour=None,level='all',**latlonregion):
		
		
	def extract_data_for_range_of_dates_of_partners(self,variableName,typeOfLevel,Type,startdate,enddate,skipdays=1,calendar=None,hour=None,level='all',**latlonregion):	
		
		"""
		extract_data_for_range_of_dates_of_partners : It can extract the data_of_partners for range of dates. i.e it returns data of only the partners data. not for the passed Type.
		It extracts the multiple data (depends upon the level,partners and dates) and returns in single array which contains collection of MV2 variable.
		
	       
		Condition : 
		   
	       	   level is optional. level takes default 'all'. if level passed, it must be belongs to the data variable
	       	   hour is must when Type arg should be 'f' (fcst) to select the file name.
	       	   Pass either (lat,lon) or region.
	       	   
	       	   
		Inputs:
		   Type - either 'a' or 'f'
		   variableName,typeOfLevel,level must be belongs to the data file
		   startdate and enddate must be in yyyymmdd string formate. skipdays must be an integer
		   key word arg lat,lon or region should be passed
		   
		   
		Outputs:
		   It should return the list. It contanins the multiple extracted data as MV2 variable in shape of (time,level,lat,lon). i.e with time axis,level axis, lat axis and lon axis. If level has squeezed while extract the data, then it should return only shape of (time,lat,lon)
		   
		   It returns only the partners data not along with source of Type data.
		
		Bug :
		   Here it as major bug. i.e. extract the data with partners for range of concecutive dates. so it make many duplication in same list. Have to enhance it.
		 
		   
		Usage:
	       
		   example 1:
		        extract_data_for_range_of_dates_of_partners(variableName = "Geopotential Height",typeOfLevel = "isobaricInhPa", Type = 'f',startdate = 20100525, enddate = 20100930,skipdays = 1,calendar = None, hour = 24,level = 'all' ,region = AIR ) #lat=(-90,90),lon=(0,359.5)
		        
		Future:
			set time axis
		   			 
		Refer :
			method extract_data_of_partners(...)
			method xdrange(...)
		   	
		Written by: Arulalan.T

		Date: 09.04.2011
		"""
		
		self.checking_major_parameter_to_extract_data(Type,startdate,hour)
		if not enddate== None:
			self.checking_major_parameter_to_extract_data(Type,enddate,hour)
		datavariables = []
		
		# calling Days's method xdrange
		daterange = self.xdrange(startdate,enddate,skipdays,calendar)
		for date in daterange:				
			var = self.extract_data_of_partners(variableName,typeOfLevel,Type,date,hour,level,**latlonregion) 
			datavariables.append( var )
		'''
		# create the time axis  
		timeAxis = self._generateTimeAxis(len(datavariables),startdate)
		# get the level,lat,lon axis information
		levelAxis = datavariables[0].getLevel()
		latAxis = datavariables[0].getLatitude()
		lonAxis = datavariables[0].getLongitude()	
		
		
		if levelAxis == None:
			# shape (time,lat,lon)
			VAR = cdms2.createVariable(data = datavariables, axes = [timeAxis,latAxis,lonAxis])
		else:
			# shape (time,level,lat,lon)
			VAR = cdms2.createVariable(data = datavariables, axes = [timeAxis,levelAxis,latAxis,lonAxis])
		
		return VAR
		'''
		return datavariables
		
	# end of def extract_data_for_range_of_dates_of_partners(self,variableName,typeOfLevel,Type,startdate,enddate,skipdays=1,calendar=None,hour=None,level='all',**latlonregion):
		
			
			
	def avg_month_data(self,variableName,typeOfLevel,Type,level,month,year,calendarName=None,hour=None,**latlonregion):
		
		
		"""
		avg_month_data : It returns the average of the given month data ( all days in the month ) for the passed variable options
	       
		Condition : 
	       	   calendarName,level are optional. level takes default 'all' if not pass arg for it.
	       	   hour is must when Type arg should be 'f' (fcst) to select the file name.
	       	   Pass either (lat,lon) or region.
	       	   
	       	   
		Inputs:
		   Type - either 'a' or 'f'
		   variableName,typeOfLevel,level must be belongs to the data file
		   month may be even in 3 char like 'apr' or 'April' or 'aPRiL' or like any month or 4
		   year must be passed as integer
		   calendarName default None, it takes cdtime.DefaultCalendar
		   key word arg lat,lon or region should be passed
		   
		   
		Outputs:
		   It should return the average of the whole month data for the given vars as MV2 variable
		Usage:
	       
		   example:
		       avg_month_data(variableName = "Geopotential Height",typeOfLevel = "isobaricInhPa",Type = 'f',level = 'all', month = 'july',year=2010 , hour = 24,region = AIR ) #lat=(-90,90),lon=(0,359.5)
		   	return dataAvg of one month data as single MV2 variable
		   
		Written by: Arulalan.T

		Date: 29.04.2011
		"""
		# calling Days's method first_last_date_of_month
		firstdate,lastdate = self.first_last_date_of_month(month,year,calendarName)
		
		data = self.extract_data_for_range_of_dates(variableName = variableName,typeOfLevel = typeOfLevel,Type = Type,startdate = firstdate,enddate = lastdate, hour = hour,level = level, **latlonregion)
		#
		#Taking average the data over the time axis. The averager will sum all the day data and divide by the no of days in the time axis.finally it should return the AVG data.
		#
		dataAvg = cdutil.averager(data,axis='t')
		
		return dataAvg
		
	# end of def avg_month_data(self,variableName,typeOfLevel,Type,level,month,year,calendarName=None,hour=None,**latlonregion):
		
		
		
	def analysis_wind_avg_month_data(self,month,year,calendarName=None,level=850):
		
		"""
		analysis_wind_avg_month_data : It returns the average of the given month data ( all days in the month ) for the variable U and V 
	       
		Condition : 
	       	   passing month should be either integer of month or name of the month in string.
	       	   year should be an integer
	       	   calender is optional. It takes default calendar of cdtime
	       	   
		Inputs:
		   month may be even in 3 char like 'apr' or 'April' or 'aPRiL' or like any month or 4
		   year must be passed
		   level default is 850. 
		   
		Outputs:
		   It should return the average of the whole month data for the variables U and V component as MV2 variable
		Usage:
	       
		   example:
		       analysis_wind_avg_month_data('jun',2010) return Uavg and Vavg as MV2 variable
		   
		Written by: Arulalan.T

		Date: 29.04.2011
		"""
		
		UvariableName = "U component of wind"
		VvariableName = "V component of wind"
		typeOfLevel = "isobaricInhPa"
		Type = 'a'
		hour = None
		uAvg = self.avg_month_data(variableName = UvariableName,typeOfLevel = typeOfLevel,Type = Type, level = level, month = month, year = year, calendarName = calendarName, hour = hour, region = 'India1')
		vAvg = self.avg_month_data(variableName = VvariableName,typeOfLevel = typeOfLevel,Type = Type, level = level, month = month, year = year, calendarName = calendarName, hour = hour, region = 'India1' )
		
		return uAvg,vAvg
		
	# end of def analysis_wind_avg_month_data(self,month,year,calendarName=None,level=850):
	
	
	def rainfall_partners_file_path(self,date,hour = None):
		'''
		find the partners of the rainfall's fcst grb file path and return it.
		
		'''
		# calling Directory_Info's method find_partners		
		return self.find_partners('r',date,hour)
		
	#end of def rainfall_partners_file_path(self,date,hour = None):
	
	
	def getRainfallDataPartners(self, date, hour = None, level = 'all',orginData = 1,datePriority = 'o',rainObject = None, **latlonregion):
	
		"""
		getRainfallDataPartners : It returns the rainfall data and its partners data (fcst is the partner of the observation.i.e. rainfall) as MV2 vars
	       
		Condition : 
	       	   startdate is must. enddata is optional one. 
	       	   If both startdate and enddate has passed means, it should return the rainfall data and partnersData within that range.
	       	   
	       	   
		Inputs:
		  
		   orginData - either 0 or 1. 0 means it shouldnot return the orginData as single MV2 var.
		   			       1 means it should return both the orginData and its partnersData as two seperate MV2 vars.
		   datePriority - either 'o' or 'p'. 'o' means passed date is with respect to orginData. According to this orginData's date, it should return its partnersData.
		   				     'p' means passed date is with respect to partnersData. According to this partnersData's date, it should return its orginData.
		
		   key word arg lat,lon or region should be passed
		   By default hour is None and level is 'all'.
		   
		   rainObject is mandatory one when you choosed orginData is 1. You must pass the object of Rainfall_Access class, to access and get the data of obeserved rainfall data.
		   
		   date formate 1:
		   	date = (startdate,enddate)
		   	here startdate and enddate must be like cdtime.comptime formate.
		   		   	
		   date formate 2:
		   	date = (startdate)
		   	
		   date formate 3:
		   	date = 'startdate' or date = 'date'
		   
		   eg for date input :
		      	date = ('2010-5-1','2010-6-30')
		   	date = ('2010-5-30')
		   	date = '2010-5-30'
		   	
		   	By default skipdays as 1 takes place. User cant override till now.
		   	
		   
		Outputs:
		   
		   If user passed single date in the date argument, then it should return the data of that particular date (both orginData & partnersData) as MV2 variable.
		   	
		   If user passed start and enddate in the date argument, then it should return the data (both orginData & partnersData) for the range of dates as MV2 variable with time axis.
		   
		
		Usage:
	       	   
	       	   Note :  if 'r'(observation) file is orginData means 'f'(fcst) files are its partnersData.      
	       
		   example1:
		       a,b = getRainfallDataPartners(date = '2010-6-5',hour = None,level = 'all',orginData = 1,datePriority = 'o', lat=(-90,90),lon=(0,359.5)) 
		       a is orginData. i.e. rainfall observation. its timeAxis date is '2010-6-5'.
		       b is partnersData. i.e. fcst. its 24 hour fcst date w.r.t orginData is '2010-6-4'. 48 hour is '2010-6-3'. Depends upon the availability of date of fcst files, 
		       it should return the data. In NCMRWF2010 model, it should return maximum of 7 days fcst files.
		       
		       If we will specify any hour in the same eg, that should return only that hour fcst file data instead of returning all the available fcst hours data.
		       
		   example2:
		       a,b = getRainfallDataPartners(date = '2010-6-5',hour = 24,level = 'all',orginData = 1,datePriority = 'o', lat=(-90,90),lon=(0,359.5)) 
		       a is orginData. i.e. rainfall observation. its timeAxis date is '2010-6-5'.
		       b is partnersData. i.e. fcst 24 hour. its fcst date w.r.t orginData is '2010-6-6'. 
		    
		   example3:
		       b = getRainfallDataPartners(date = '2010-6-5',hour = 24,level = 'all',orginData = 0,datePriority = 'o', lat=(-90,90),lon=(0,359.5)) 
		       b is partnersData. i.e. fcst. its fcst date w.r.t orginData is '2010-6-6'.   No orginData. Because we passed orginData as 0.
		       
		   example4:
		       a,b = getRainfallDataPartnerss(date = '2010-6-5',hour = 24,level = 'all',orginData = 1,datePriority = 'p', lat=(-90,90),lon=(0,359.5)) 
		       a is orginData. i.e. rainfall observation. its timeAxis date is '2010-6-6'.
		       b is partnersData. i.e. fcst 24 hour. its fcst date w.r.t orginData is '2010-6-5'.  we can compare this eg4 with eg2. 
		       In this we passed datePriority as 'p'. So the passed date as set to the partnersData and orginData's date has shifted to the next day.
		       
		   example5:
		       a,b = getRainfallDataPartners(date = ('2010-6-5','2010-6-6'),hour = 24,level = 'all',orginData = 1,datePriority = 'o', lat=(-90,90),lon=(0,359.5)) 
		       
		       Note : We must choose the hour option to select the fcst file, since we are passing the range of dates.
		       
		       a is orginData. i.e. rainfall observation. its timeAxis size is 2. date are '2010-6-5' and '2010-6-6'.
		       b is partnersData. i.e. fcst 24 hour data. its timeAxis size is 2. date w.r.t orginData are '2010-6-4' and '2010-6-5'.  
		       
		       a's '2010-6-5' has partner is b's '2010-6-4'. i.e. orginData(rainfall observation) partners is partnersData's (fcst)
		       same concept for the remains day.
		       a's '2010-6-6' has partner is b's '2010-6-5'.
		       
		   example6:
		       a,b = getRainfallDataPartners(date = ('2010-6-5','2010-6-6'),hour = 24,level = 'all',orginData = 1,datePriority = 'p', lat=(-90,90),lon=(0,359.5)) 
		       
		       Note : We must choose the hour option to select the fcst file, since we are passing the range of dates.
		       
		       a is orginData. i.e. rainfall observation. its timeAxis size is 2. date are '2010-6-6' and '2010-6-7'.
		       b is partnersData. i.e. fcst 24 hour data. its timeAxis size is 2. date w.r.t orginData are '2010-6-5' and '2010-6-6'.  
		       
		       a's '2010-6-6' has partner is b's '2010-6-5'. i.e. orginData(rainfall observation) partners is partnersData's (fcst)
		       same concept for the remains day.
		       a's '2010-6-7' has partner is b's '2010-6-6'. we can compare this eg6 with eg5. In this we passed datePriority as 'p'. So the passed
		       date as set to the partnersData and orginData's date has shifted towards the next days.   
			   
		Written by: Arulalan.T

		Date: 29.05.2011
		
		"""
		
						
		endCompTime = None
		orgin_enddate = None
		skipdays = 1		
		
		if isinstance(date,tuple):
			startCompTime = date[0] # assign startdate
			if len(date) >= 2:
				orgin_enddate = endCompTime = date[1] # assign enddate
			# end of if len(date) >= 2:
			
			if len(date) == 3:
				skipdays = int(date[2]) # assign skipdays
			# end of if len(date) >= 3:
									
		elif isinstance(date,str):
			startCompTime = date # assign date
			
		else:
			raise GribAccessTypeError,'date either must be tuple or string \n Read the following docstring \n ' 
			
		# end of if isinstance(date,tuple):
			
		
		if not endCompTime == None:			
			# enddate has passed. so we need hour to get the partners data
			if hour == None :
				raise GribAccessError, 'You must pass the hour to return the partners data,since you passed the enddate. i.e range of date.'			
		# end of if not enddate == None:
		
		if not orginData in [0,1]:
			raise GribAccessTypeError,'orginData either 0 or 1.  0 means without orginData. i.e. only partners data. \
			  1 means with orginData. i.e. both orginData and partnersData. Default it takes 0.'
		# end of if not orginData in [0,1]:		
		
		if orginData:
			# orginData is 1
			
			if rainObject == None:
				raise RainfallAccessError('you must pass the instance of Rainfall_Access class in the rainObject argument of this method to access obeserved rainfall data')
			# end of if Rainfall_Access == None:	
		
			if rainObject:
				if not isinstance(rainObject,Rainfall_Access):
					raise RainfallAccessTypeError,' The passed object is not an instance of Rainfall_Access class'
			# end of if rainObject:
			
			if datePriority == 'p':
			
				if self._forecastdays_.has_key(hour):
					movedays = self._forecastdays_.get(hour)
				else:
					raise GribAccessError("wrong %d hour has passed as arg, its not belongs to fcst grib file hours\n \
						Choose correct hour\n" % (hour))
						
				#
				# Finding the Orgin's Shift startdate and enddate
				#
				
				# converting date from comp type into yyyymmdd type according to our NCMRWF2010 model directory structure name
				orgin_startdate = self._yyyymmdd_from_comp(startCompTime)
				# find out the partners startdate
				partner_startdate = self.find_partners(Type = 'r', date = orgin_startdate, hour = hour)[1]
				# swaping the orgin date and partners date
				orgin_startdate,partner_startdate = partner_startdate,orgin_startdate
				# covert to comptime object
				comp_partner_startdate = self.comptime(partner_startdate)
				# find out the orgin startdate 
				orgin_startdate = self.move_days(comp_partner_startdate.year,comp_partner_startdate.month,comp_partner_startdate.day,movedays)
				# covert to comptime object
				orgin_startdate = self.comptime(orgin_startdate)
				# setting time to extract orginData with start date only
				orgin_time = orgin_startdate	
						
				if not endCompTime == None :
					# converting date from comp type into yyyymmdd type according to our NCMRWF2010 model directory structure name
					orgin_enddate = self._yyyymmdd_from_comp(endCompTime)
					# find out the partners enddate
					partner_enddate = self.find_partners(Type = 'r', date = orgin_enddate, hour = hour)[1]
					# swaping the orgin date and partners date				
					orgin_enddate,partner_enddate = partner_enddate,orgin_enddate
					# covert to comptime object
					comp_partner_enddate = self.comptime(partner_enddate)							
					# find out the orgin enddate
					orgin_enddate = self.move_days(comp_partner_enddate.year,\
									comp_partner_enddate.month,comp_partner_enddate.day,movedays)
					# covert to comptime object	
					orgin_enddate = self.comptime(orgin_enddate)
					# setting time to extract orginData with startdate and enddate 	
					orgin_time = (orgin_startdate,orgin_enddate)		
				# end of if not endCompTime == None :
				
															
			elif datePriority == 'o':
				# default behaviour. 
				if orgin_enddate == None:
					# setting time to extract orginData with start date only
					orgin_time = startCompTime				
				else:
					# setting time to extract orginData with startdate and enddate 	
					orgin_time = (startCompTime,endCompTime)
				# end of if orgin_enddate == None:
			
			else:
				raise GribAccessTypeError,"datePriority either 'o' or 'p'. \n 'o' means passed date set to the orginData. \n 'p' means passed date set to the partnersData.\n"
						
			
				
			# calling the rainfall_extract_data_from_xml to extract data by using Rainfall_Access class object.
			rainfall_data = rainObject.rainfall_extract_data_from_xml(orgin_time)
			#
			# Extract the lat,lon info from xmlvar
			#
			latstart = rainfall_data.getLatitude()[0]
			latend = rainfall_data.getLatitude()[-1]
		
			lonstart = rainfall_data.getLongitude()[0]
			lonend = rainfall_data.getLongitude()[-1]	
		
		# end of if orginData:
		
		
		#
		# Find and get the rainfall partners data 
		#
		# calling Grib_Access class's method
		rainfall_partners_fcst_data = self.getDataPartners('Total Precipitation',typeOfLevel = 'surface',Type = 'r',\
		 				date = date,hour = hour,level = level,orginData = 0,datePriority = datePriority, **latlonregion )
		
		
		if orginData:
			# orginData is 1
			return rainfall_data, rainfall_partners_fcst_data 
		else:
			# orginData is 0
			return rainfall_partners_fcst_data 	
		
	# end of def getRainfallDataPartners(self, date, hour = None, level = 'all',datePriority = 'o', **latlonregion):
	
	
		
# end of class Grib_Access(My_Simple,Directory_Info,Collection_Info):


class XmlAccessError(Exception):
	def __init__(self,*args):
		print "\nXmlAccessError Error : "
		for i in args:
			print i
			
class XmlAccessTypeError(XmlAccessError):
	pass 

class Xml_Access:
	
	def __init__(self,xmlPath,xmlVar):
		'assigning to the instance variable'
		self.xmlpath = xmlPath
		self.xmlvar = xmlVar
		
		if not os.path.isfile(self.xmlpath):
			raise XmlAccessError, "the xml file is not exist in the path %s" % (self.xmlpath)
		
		
	def extract_data_from_xml(self,date=None,level = None):
		'''
		Extract the rainfall data from the xml file which has created by the cdscan method (here in the case)
		'''
		
		f = cdms2.open(self.xmlpath)
		
		if not self.xmlvar in f.listvariable():
			raise XmlAccessError("the xml file %s doesnt have the passed xmlvar %s .\
				Choose correct var from the available vars here " % (self.xmlpath,self.xmlvar), f.listvariable() )
		
					
		if date == None :
			VAR = f(self.xmlvar,level = level)
		# end of if date == None :
		
		else:
			if isinstance(date,tuple):
				startCompTime = date[0] # assign startdate
				time = (startCompTime)
				if len(date) >= 2:
					endCompTime = date[1] # assign enddate
					time = (startCompTime,endCompTime)
				# end of if len(date) >= 2:
				
				if len(date) == 3:
					skipdays = int(date[2]) # assign skipdays
					time = (startCompTime,endCompTime,skipdays)
				# end of if len(date) >= 3:
									
			elif isinstance(date,str):
				startCompTime = date # assign date
				time = (startCompTime)
			
			else:
				raise XmlAccessTypeError,'date %s either must be tuple or string \n' % (str(date))
			
			# end of if isinstance(date,tuple):
						
			VAR = f(self.xmlvar,time = time,level = level)
			
		# end of if date == None :	
					
		return VAR
		
	#end of def extract_data_from_xml(self,xml,xmlvar,date=None,level = None):

# end of class Xml_Access:



class RainfallAccessError(Exception):
	def __init__(self,*args):
		print "\nRainfallAccessError Error : "
		for i in args:
			print i
		
class RainfallAccessStringError(RainfallAccessError):
	pass
class RainfallAccessIntegerError(RainfallAccessError):
	pass
	
class RainfallAccessTypeError(RainfallAccessError):
	pass
	

class Rainfall_Access(Xml_Access):
	' Rainfall access methods along with Grib_Access properties ...'

	def __init__(self,xmlPath,xmlVar):
		
		"""
		Rainfall_Access.__init__ : It returns the instance of the Rainfall_Access class.
	       
		Condition : 
	       	   xmlPath and xmlVar are mandatory.
	       	          	   
		Inputs:
		  xmlPath is absolute one. This xml should be created by cdscan command.
		  xmlVar should be one of the variables of the passed xmlPath.
		  
		Usage:
		  Assigning to the instance variable for Xml_Access class 
		  xml is the absolute path of the xml which has created by cdscan
		  xmlvar is the variable name which same as in the xml 
		
		Written by: Arulalan.T

		Date: 29.05.2011
		
		"""
		  
		# initializing the Xml_Access's __init__ method members
		Xml_Access.__init__(self,xmlPath,xmlVar)	
		
	# end of def __init__(self,xmlPath,xmlVar):
				
		
	def rainfall_extract_data_from_xml(self,date=None,level = None):
		'''
		Extract the rainfall data from the xml file which has created by the cdscan method (here in the case)
		'''
		data = self.extract_data_from_xml(date = date,level = level)
		return data
		
	#end of def rainfall_extract_data_from_xml(self,xml,var,date=None):
		
# end of class Rainfall_Access(Xml_Access):
	
	
			
			
#myinfo = Directory_Info('NCMRWF2010')
#print myinfo.do_while("Enter any no",['1','2','3'],mytype=int)

#day = Days()
#a = day.xdrange(20110407,20120410,1,cdtime.NoLeapCalendar)






#a=myinfo.find_partners('f','20100525',72)
#b=myinfo.find_partners('a','20100601')

#print myinfo.grib_filename_path('a','20100525')
#print myinfo.grib_filename_path('f','20100525',24)
# temp comment started

#print myinfo.move_days(2011,04,03,-200) 




#print gobj.rainfall_partners_file_path(20100820)
#rainfall_data, rainfall_partners_fcst_data = gobj.rainfall_data_and_fcst_partners('/mnt/ncmrw-data-2010/rainfall/rainfall.xml','pobs',20100820,hour=144)#,20100821)#,hour=48)
#global_grb_data = gobj.extract_data_for_range_of_dates(Type = 'f',variableName = "Geopotential Height",typeOfLevel = "isobaricInhPa", startdate = 20100525, enddate = 20100930,skipdays = 1,calendar = None, hour = 24,level = 'all' ,region = AIR ) #lat=(-90,90),lon=(0,359.5)

#global_grb_data = gobj.extract_data_with_partners(Type = 'a',variableName = "Geopotential Height",typeOfLevel = "isobaricInhPa",date = 20100625,hour = 24,level = 'all' ,region = AIR ) #lat=(-90,90),lon=(0,359.5)

#global_grb_data = gobj.extract_data_of_a_date(Type = 'f',variableName = "Geopotential Height",typeOfLevel = "isobaricInhPa",date = 20100525,hour = 24,level = 'all' ,region = 'AIR' ) #lat=(-90,90),lon=(0,359.5)

#uglobal_grb_data = gobj.extract_data_of_a_date(Type = 'a',variableName = "U component of wind",typeOfLevel = "isobaricInhPa",date = 20100802,hour = 24,level = 850 , lat=(0,40),lon=(60,100))#region = PenIndia ) #lat=(-90,90),lon=(0,359.5)

#vglobal_grb_data = gobj.extract_data_of_a_date(Type = 'a',variableName = "V component of wind",typeOfLevel = "isobaricInhPa",date = 20100802,hour = 24,level = 850 , lat=(0,40),lon=(60,100)) #region = PenIndia ) #

#global_grb_data = cdms2.createVariable(data=final_var, axes=[level_axis,lat_axis,lon_axis],id="Geopotential Height")

#uglobal_grb_data = gobj.extract_data_for_range_of_dates(Type = 'a',variableName = "U component of wind",typeOfLevel = "isobaricInhPa",startdate = 20100601,enddate = 20100603, hour = 24,level = 850 , lat=(0,40),lon=(60,100))#region = PenIndia ) #lat=(-90,90),lon=(0,359.5)

#vglobal_grb_data = gobj.extract_data_for_range_of_dates(Type = 'a',variableName = "V component of wind",typeOfLevel = "isobaricInhPa",startdate = 20100601,enddate = 20100630, hour = 24,level = 850 , lat=(0,40),lon=(60,100)) #region = PenIndia ) #

# for UV plot code for one month


#U,V = gobj.analysis_wind_avg_month_data('june',2010)
'''
uvar = U[::4,::4]
vvar = V[::4,::4]
uvar.id = " U V component of wind "
vvar.id = " U V component of wind "


latfull={-90:'90S', -85:'85S', -80:'80S', -75:'75S', -70:'70S', -65:'65S', -60:'60S',
		   -55:'55S', -50:'50S', -45:'45S', -40:'40S', -35:'35S', -30:'30S', -25:'25S',
		   -20:'20S', -15:'15S', -10:'10S', -5:'5S',0:'EQ', 5:'5N', 10:'10N', 15:'15N',
		    20:'20N', 25:'25N', 30:'30N', 35:'35N', 40:'40N', 45:'45N', 50:'50N',
		    55:'55N', 60:'60N', 65:'65N', 70:'70N', 75:'75N', 80:'80N', 85:'85N', 90:'90N' } 


lonfull={0:'0E',5:'5E',10:'10E',15:'15E',20:'20E',25:'25E',30:'30E',35:'35E',40:'40E',45:'45E',
		   	50:'50E',55:'55E',60:'60E',65:'65E',70:'70E',75:'75E',80:'80E',85:'85E',90:'90E',
		   95:'95E',100:'100E',105:'105E',110:'110E',115:'115E',120:'120E',125:'125E',130:'130E',135:'135E',
		   140:'140E',145:'145E',150:'150E',155:'155E',160:'160E',160:'160E',165:'165E',170:'170E',
		   175:'175E',180:'180E',185:'185E',190:'190E',195:'195E',200:'200E',205:'205E',210:'210E', 
		   215:'215E', 220:'220E', 225:'225E', 230:'230E', 235:'235E', 240:'240E', 245:'245E',
		   250:'250E', 255:'255E', 260:'260E', 265:'265E', 270:'270E', 275:'275E', 280:'280E',
		   285:'285E', 290:'290E', 295:'295E', 300:'300E', 305:'305E', 310:'310E', 315:'315E',
		   320:'320E', 325:'325E', 330:'330E', 335:'335E', 340:'340E', 345:'345E', 350:'350E', 355:'355E'				
			
		 }
		 
lat5={-20:'20S', -15:'15S', -10:'10S', -5:'5S',0:'EQ', 5:'5N', 10:'10N', 15:'15N',
		    20:'20N', 25:'25N', 30:'30N', 35:'35N', 40:'40N', 45:'45N', 50:'50N',
		    55:'55N', 60:'60N' } 


lon5={20:'20E',30:'30E',40:'40E',50:'50E',60:'60E',70:'70E',80:'80E',90:'90E',
		   100:'100E',110:'110E',120:'120E',130:'130E',140:'140E'			
		 }
		 
		 
import vcs
v = vcs.init()
# vector properties
#vc = v.getvector('quick')
vc=v.createvector('new')   

vc.projection='linear'              # Can only be 'linear'

vc.xticlabels1=lon5
vc.xticlabels2=''
#vc.xticlabels(lon5, lon5)         # Will set them both
#vc.xmtics1=''
vc.xmtics2=''
#vc.xmtics(lon5, lon5)             # Will set them both
vc.yticlabels1=lat5
vc.yticlabels2=''
#vc.yticlabels(lat5, lat5)         # Will set them both
#vc.ymtics1=''
vc.ymtics2=''
#vc.ymtics(lat5, lat5)             # Will set them both
vc.datawc_y1=-20.0
vc.datawc_y2=60.0
vc.datawc_x1=20.0#-180.0
vc.datawc_x2=140.0#180.0
#vc.datawc(-90, 90, -180, 180)       # Will set them all
xaxisconvert='linear'
yaxisconvert='linear'

vc.linewidth = 1
vc.type = 0
vc.scale = 2.0 # scaling the vector's scaling length
#vc.linecolor = 16 # 16 to 255
vc.reference = 20.0  # reference only pointing the -> angle with respect to ... in the vector plot we can see in the left bottom of the vcs to indicate. depends upon this, vectors should change. it should be float only. 50 doesnt work. 50.0 only ll display the vectors in vcs

# 20.0 for 2deg intervals
vc.reference = 20.0 
	 
		 
v.plot(uvar,vvar,vc,continents=6,name="UV Componenet of Wind",units="Monthly Avg of Aug 2010")#,ratio='autot')


'''
