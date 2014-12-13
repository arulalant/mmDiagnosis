import data_access
import pytest
import cdtime

days = data_access.Days()

class TestDays:
	''' Testing for Days class '''

	# comptime method testing start
	
	def test_comptime_StringInput(self):
		''' Testing for comptime generation form string date input '''
		comp = cdtime.comptime(2011,5,21)
		# passing string input to the days.comptime function
		assert comp == days.comptime('20110521')
	# end of def test_comptime_StringInput(self):
	
	def test_comptime_IntegerInput(self):
		''' Testing for comptime generation form integer date input '''
		comp = cdtime.comptime(2011,05,21)
		# passing integer input to the days.comptime function
		assert comp == days.comptime(20110521)
	# end of def test_comptime_IntegerInput(self):
		
	def test_comptime_BadStringInput(self):
		''' Testing for bad sting input to the comptime '''
		# it should raise the following error
		pytest.raises(data_access.DaysStringError,days.comptime,'2011521')
	# end of def test_comptime_BadStringInput(self):
		
	# comptime method testing end


	# _yyyymmdd_from_comp method start
	
	def test_yyyymmdd_from_comp_CdtimeInput(self):
		''' Testing for _yyyymmdd_from_comp generation from comptime object input '''
				
		assert days._yyyymmdd_from_comp(cdtime.comptime(2011,5,21)) == '20110521'
	# end of def test_yyyymmdd_from_comp_CdtimeInput(self):
	
	def test_yyyymmdd_from_comp_StringInput(self):
		''' Testing for _yyyymmdd_from_comp generation from comptime object string formate input '''
		
		assert days._yyyymmdd_from_comp('2011-5-21 0:0:0.0') == '20110521' 
	# end of def test_yyyymmdd_from_comp_StringInput(self):
		
	# _yyyymmdd_from_comp method end	
		
		
	# first_last_date_of_month method start
	def test_first_last_date_of_month_IntegerInput(self):
		'''  Testing for first_last_date_of_month(4,2010) returns '20100401' and '20100430' in yyyymmdd string formate '''
	
		startdate = '20100401'
		enddate = '20100430'
		assert days.first_last_date_of_month(4,2010) == (startdate,enddate)
	# end of def test_first_last_date_of_month_IntegerInput(self):
		
	def test_first_last_date_of_month_StringInput(self):
		'''  Testing for first_last_date_of_month('may',2010) returns '20100501' and '20100531' in yyyymmdd string formate '''
	
		startdate = '20100501'
		enddate = '20100531'
		assert days.first_last_date_of_month('may',2010) == (startdate,enddate)
	# end of def test_first_last_date_of_month_StringInput(self):
	
	def test_first_last_date_of_month_CdtimeCalendarInput(self):
		'''  Testing for cdtime.calendar optional argument '''
	
		startdate = '20120201'
		enddate = '20120228' # Note 2012 is leap year.  even though its end up with 28th, if we choose cdtime.NoLeapCalendar as calendar optional argument
		assert days.first_last_date_of_month('feb',2012,cdtime.NoLeapCalendar) == (startdate,enddate)
	# end of def test_first_last_date_of_month_CdtimeCalendarInput(self):		
		
	def test_first_last_date_of_month_BadStringInputMonth(self):	
		'''  Testing for bad string input for month argument '''	
		
		pytest.raises(data_access.DaysError,days.first_last_date_of_month,'MOy',2010)
	# end of def test_first_last_date_of_month_BadStringInputMonth(self):	
	
	def test_first_last_date_of_month_BadInegerInputMonth(self):
		'''  Testing for bad range input for month argument '''
		
		pytest.raises(data_access.DaysIntegerError,days.first_last_date_of_month,13,2010)
		pytest.raises(data_access.DaysIntegerError,days.first_last_date_of_month,0,2010)
	# end of def test_first_last_date_of_month_BadInegerInputMonth(self):
		
		
	def test_first_last_date_of_month_BadStringInputYear(self):
		'''  Testing for bad string input for year argument '''
		
		pytest.raises(data_access.DaysIntegerError,days.first_last_date_of_month,'May','2010')
	# end of def test_first_last_date_of_month_BadStringInputYear(self):
		
	def test_first_last_date_of_month_BadTypeInputMonth(self):
		'''  Testing for bad type input for month argument '''
		
		pytest.raises(data_access.DaysTypeError,days.first_last_date_of_month,1.1,'2010')
	# end of def test_first_last_date_of_month_BadTypeInputMonth(self):
	
	
	# first_last_date_of_month method end
		
		
	# move_days method start 
	def test_move_days_tomorrow(self):
		''' Testing for move_days with positive integer movedays'''		
		tomorrow = '20110605'
		assert tomorrow == days.move_days(2011,06,04,1)	
	# end of def test_move_days_tomorrow(self):	
		
	def test_move_days_yesterday(self):
		''' Testing for move_days with positive negative movedays'''	
		yesterday = '20110603'
		assert yesterday == days.move_days(2011,06,04,-1)
	# end of def test_move_days_yesterday(self):
		
	def test_move_days_calendar(self):
		''' Testing for move_days with calendar'''
		# On 2012 year, feb have 29 days. But it should return only march 1st as its next day of 28th feb, since we have passed cdtime.NoLeapCalendar arg.	
		tomorrow = '20120301'
		assert tomorrow == days.move_days(2012,02,28,1,cdtime.NoLeapCalendar)
	# end of def test_move_days_calendar(self):			
	
	def test_move_days_BadIntegerInput(self):
		''' Testing for bad integer input '''	
		pytest.raises(data_access.DaysIntegerError,days.move_days,'2011',06,04,-1)
	# end of def test_move_days_BadIntegerInput(self):
		
	# move_days method end
	
	
	# xdrange method start
	def test_xdrange_StringDateInput(self):
		''' Testing for xdrange string date input '''
		gen = days.xdrange('20110610','20110612')
		checkdates = ['20110610','20110611','20110612']
		count = 0
		for date in gen:
			assert date == checkdates[count]
			count = count + 1
		# end of for date in gen:
	# end of def test_xdrange_StringDateInput(self):
			
	def test_xdrange_StringDateSkipInput(self):
		''' Testing for xdrange string date with skipdays input '''
		gen = days.xdrange('20110610','20110615',2)
		checkdates = ['20110610','20110612','20110614']
		count = 0
		for date in gen:
			assert date == checkdates[count]
			count = count + 1
		# end of for date in gen:	
	# end of def test_xdrange_StringDateSkipInput(self):
	
	def test_xdrange_CdtimeCompDateInput_StringDateOutput(self):
		''' Testing for xdrange string date with skipdays input '''
		gen = days.xdrange(startdate = cdtime.comptime(2011,6,10),enddate = cdtime.comptime(2011,6,14), stepdays = 2, returnType = 's')
		checkdates = ['20110610','20110612','20110614']		
		count = 0
		for date in gen:
			assert date == checkdates[count]
			count = count + 1
		# end of for date in gen:
	# end of def test_xdrange_CdtimeCompDateInput_StringDateOutput(self):
	
	def test_xdrange_CdtimeCompDateInput_CdtimeCompDateOutput(self):
		''' Testing for xdrange string date with skipdays input '''
		gen = days.xdrange(startdate = cdtime.comptime(2011,6,10),enddate = cdtime.comptime(2011,6,14), stepdays = 2, returnType = 'c')
		checkdates = []
		checkdates.append(cdtime.comptime(2011,6,10))
		checkdates.append(cdtime.comptime(2011,6,12))
		checkdates.append(cdtime.comptime(2011,6,14))
		count = 0
		for date in gen:
			assert date == checkdates[count]
			count = count + 1
		# end of for date in gen:
	# end of def test_xdrange_CdtimeCompDateInput_CdtimeCompDateOutput(self):
	
		
	def test_xdrange_StringDate_CalendarInput_CdtimeCompDateOutput(self):
		''' Testing for xdrange string date with skipdays input '''
		gen = days.xdrange(startdate = '20120226',enddate = '20120301', calendarName = cdtime.NoLeapCalendar,returnType = 'c')
		checkdates = []
		checkdates.append(cdtime.comptime(2012,2,26))
		checkdates.append(cdtime.comptime(2012,2,27))
		checkdates.append(cdtime.comptime(2012,2,28))
		# 2012,2,29 not included, because we are passing NoLeapCalendar option
		checkdates.append(cdtime.comptime(2012,3,1))
		
		count = 0
		for date in gen:
			assert date == checkdates[count]
			count = count + 1
		# end of for date in gen:
	# end of def test_xdrange_StringDate_CalendarInput_CdtimeCompDateOutput(self):
		
	def xdrange_generator_error_raiser(self,gen):
		''' local method to extract the genearator variable, to check the raise errors '''		
		for i in gen:
			# here we will get rasie error if the gen has genearated by passing some wrong inputs to that generator method  
			print i
		# end of for i in gen:	
	# end of def xdrange_generator_error_raiser(self,gen):
		
	def test_xdrange_BadDateInput(self):
		''' Testing for xdrange for bad lenght string input '''
		
		gen = days.xdrange(2011640001,2011650001)
		# calling local method to raise proper error by pass the above genearator object
		pytest.raises(data_access.DaysStringError,self.xdrange_generator_error_raiser,gen)
	# end of def test_xdrange_BadDateInput(self):
		
	def test_xdrange_BadStepDaysInput(self):
		''' Testing for xdrange for bad lenght string input '''
		
		gen = days.xdrange(20110604,20110606,1.5)
		# calling local method to raise proper error by pass the above genearator object
		pytest.raises(data_access.DaysIntegerError,self.xdrange_generator_error_raiser,gen)
	# end of def test_xdrange_BadStepDaysInput(self):
		
	def test_xdrange_BadCalendarInput(self):
		''' Testing for xdrange for bad calendarName input '''
		
		gen = days.xdrange(20110604,20110606,1,'mycalendar')
		# calling local method to raise proper error by pass the above genearator object
		pytest.raises(data_access.DaysError,self.xdrange_generator_error_raiser,gen)
	# end of def test_xdrange_BadCalendarInput(self):
		
	def test_xdrange_BadReturnTypeInput(self):
		''' Testing for xdrange for bad returnType input '''
		
		gen = days.xdrange(20110604,20110606,1,returnType = 'a')
		# calling local method to raise proper error by pass the above genearator object
		pytest.raises(data_access.DaysTypeError,self.xdrange_generator_error_raiser,gen)
	# end of def test_xdrange_BadReturnTypeInput(self):
		
	def test_xdrange_BadStartDateInput(self):
		''' Testing for xdrange for bad startdate input . i.e. startdate must be lower than the enddate. But for testing \
		    we are going to give lower startdate than enddate to raise error '''
		
		gen = days.xdrange(2011-4-10,2011-4-7)
		# calling local method to raise proper error by pass the above genearator object
		pytest.raises(data_access.DaysError,self.xdrange_generator_error_raiser,gen)
	# end of def test_xdrange_BadStartDateInput(self):
		
	def test_xdrange_BadSameDateInput(self):
		''' Testing for xdrange for bad startdate and enddate input both are same date. so it should raise error  '''
		
		gen = days.xdrange(2011-4-10,2011-4-10)
		# calling local method to raise proper error by pass the above genearator object
		pytest.raises(data_access.DaysError,self.xdrange_generator_error_raiser,gen)
	# end of def test_xdrange_BadSameDateInput(self):
	
	
	# xdrange method end 
		
		
		
# end of class TestDays:


dirinfo = data_access.Directory_Info()
# here we are setting the data path to test all upcoming tests
dataPath = '/NCMRWF/ncmrwf-data-2010'
modelName = 'NCMRWF2010'
acess = False
access = dirinfo._set_dataPath_modelName_(dataPath, modelName)



class Test_Directory_Info:
	''' Testing for Directory_Info class '''
	pytestmark = pytest.mark.skipif("not access")
	# i.e., skip all the tests in this class if access is false
	
	# _set_dataPath_modelName_ method start 
	
	def test_set_dataPath_modelName_BadDataPathInput(self):
		''' Testing for _set_dataPath_modelName_ for bad datapath Input  '''
		
		pytest.raises(data_access.DirectoryInfoError,dirinfo._set_dataPath_modelName_,'/home/home','NCMRWF2010')
	# end of def test_set_dataPath_modelName_BadDataPathInput(self):
		
	def test_set_dataPath_modelName_BadModelNameInput(self):
		''' Testing for _set_dataPath_modelName_ for bad modelname Input  '''
		
		pytest.raises(data_access.DirectoryInfoError,dirinfo._set_dataPath_modelName_,'/mnt','mymodelname')
	# end of def test_set_dataPath_modelName_BadModelNameInput(self):
	
	# _set_dataPath_modelName_ method endCompTime
	
	
	# grib_filename_path method start 	
	
	def test_grib_filename_path_Input(self):
		''' Testing for passing anl file generating '''   
		
		result = False
		filename = dirinfo.grib_filename_path('a','20100525')
		if filename.find('20100525'):
			result = True 
		# end of if
		assert result == True 
	# end of def test_grib_filename_path_anlInput(self):
	
	def test_grib_filename_path_NoInput(self):
		''' Testing for calling method without any arguments '''
	
		pytest.raises(data_access.DirectoryInfoError,dirinfo.grib_filename_path,None,None)
	# end of def test_grib_filename_path_NoInput(self):
	
	def test_grib_filename_path_BadTypeInput(self):
		''' Testing for bad type input '''
					
		pytest.raises(data_access.DirectoryInfoError,dirinfo.grib_filename_path,'','20100525')
	# end of def test_grib_filename_path_BadTypeInput(self):
	
	def test_grib_filename_path_NoHourBadInput(self):
		''' Testing for no hour input, when Type is 'f', hour is must '''
	
		pytest.raises(data_access.DirectoryInfoError,dirinfo.grib_filename_path,'f','20100525')
	# end of def test_grib_filename_path_NoHourBadInput(self):
	
	def test_grib_filename_path_BadDateInput(self):
		''' Testing for bad date input '''
		
		pytest.raises(data_access.DirectoryInfoStringError,dirinfo.grib_filename_path,'a',2010525)
	# end of def test_grib_filename_path_BadDateInput(self):
	
	# grib_filename_path method end 
	
	# find_partners method start 
	
	def test_find_partners_Anl24HourInput(self):
		''' Testing for find_partners for anl of 24 hour '''
		# calling the _set_dataPath_modelName_ method to set dataPath and modelName once again, since we called so many times for testing.
		# so it may set the wring path and wrong modelName. To set correct dataPath & modelName, we are calling the same method here
		dirinfo._set_dataPath_modelName_(dataPath, modelName)
		assert dirinfo.find_partners('a','20100625',24)[1] ==  '20100624'
	# end of def test_find_partners_Anl24HourInput(self):
	
	def test_find_partners_Fcst24HourInput(self):
		''' Testing for find_partners for fcst of 24 hour '''
		assert dirinfo.find_partners('f','20100625',24)[1] ==  '20100626'
	# end of def test_find_partners_Fcst24HourInput(self):
	
	def test_find_partners_AnlAllHourOutput(self):
		''' Testing for find_partners for anl all hours output '''
		dates = dirinfo.find_partners('a','20100601')
		result = ['20100525', '20100526', '20100527', '20100528', '20100529', '20100530', '20100531']

		check = [ i[1] for i in dates.values() ]
		check.sort()		
		assert result == check 
	# end of def test_find_partners_AnlAllHourOutput(self):
		
	def test_find_partners_CdtimeCompDateInput(self):
		''' Testing for find_partners for fcst of 24 hour '''
		
		compdate = cdtime.comptime(2010,6,25)
		assert dirinfo.find_partners('f',compdate,24)[1] ==  '20100626'
	# end of def test_find_partners_CdtimeCompDateInput(self):
	
	def test_find_partners_BadDateInput(self):
		''' Testing for bad date length input '''
		
		pytest.raises(data_access.DirectoryInfoStringError, dirinfo.find_partners,'f','201006250',24)
	# end of def test_find_partners_BadDateInput(self):
	
	def test_find_partners_NoneHourInput(self):
		''' Testing for none hour input, when hour is must for fcst '''
		pytest.raises(data_access.DirectoryInfoError, dirinfo.find_partners, 'f', '2010-6-25', None)
	# end of def test_find_partners_NoneHourInput(self):
	
	def test_find_partners_BadHourInput(self):
		''' Testing for bad hour input '''
		pytest.raises(data_access.DirectoryInfoError, dirinfo.find_partners, 'f', '2010-6-25', 0.6)
		pytest.raises(data_access.DirectoryInfoError, dirinfo.find_partners, 'a', '2010-6-25', 0.5)
	# end of def test_find_partners_BadHourInput(self):
	
	# find_partners method end 
	
# end of class Test_Directory_Info:

	
		
		
		
		
		
		
		
	
	
	
