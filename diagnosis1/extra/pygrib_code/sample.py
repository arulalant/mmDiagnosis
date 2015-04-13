#from data_access import *
import data_access 
import cdtime


gobj = data_access.Grib_Access(dataPath = '/NCMRWF/ncmrwf-data-2010',modelName = 'NCMRWF2010')
f24gribpath = '/NCMRWF/ncmrwf-data-2010/gdas.20100525/gdas1.t00z.grbf24'
# open the grib file
gobj.open_grib_file(f24gribpath)
# get all its variableName and typeOfLevel
gobj.get_all_vars()
grib_vars_leveltypes = gobj.all_vars_leveltypes


# opening one grib file with absolute path
#gobj.open_grib_file('gdas.20100625/gdas1.t00z.grbf24')
# listing all the available variablenames
#gobj.listVariable()
#gobj.listShortVars()
#x= gobj.comptime('20110504')
#y= gobj._yyyymmdd_from_comp(x)

#print gobj.find_partners('f','20100525',24)

#dirinfo = data_access.Directory_Info()
#dataPath = '/NCMRWF/ncmrwf-data-2010'
#modelName = 'NCMRWF2010'
#acess = False
#access = dirinfo._set_dataPath_modelName_(dataPath, modelName)
#print dirinfo.find_partners('f','20100525',24)

#ran = gobj.xdrange(20110407,20110410,1,None,'c')

#ran1 = gobj.xdrange(cdtime.comptime(2011,04,10),cdtime.comptime(2011,04,7),-1,None,'c')
#print gobj.move_days(2011,04,03,-200) 


#a=gobj.find_partners('f','20100525',72)
#b=gobj.find_partners('a','20100601')

#print gobj.grib_filename_path('a','20100525')

#print gobj.grib_filename_path('f','20100525',24)


#print gobj.rainfall_partners_file_path(20100820)

#gobj.open_grib_file('/mnt/ncmrw-data-2010/gdas.20100525/gdas1.t00z.grbanl')
#gobj.listVariable()
#gobj.listShortVars()
#single_data = gobj.getData(variableName = "va",typeOfLevel = "isobaricInhPa",Type = 'a',date = '2010-6-25',hour = 24,level = 'all' ,region = 'AIR' ) #lat=(-90,90),lon=(0,359.5)

#range_data = gobj.getData(variableName = "Geopotential Height",typeOfLevel = "isobaricInhPa",Type = 'a',date = ('2010-6-20','2010-6-30',2),hour = 24,level = 750 ,region = 'AIR' ) #lat=(-90,90),lon=(0,359.5)


#global_grb_data = gobj.extract_data_with_partners(variableName = "Geopotential Height",typeOfLevel = "isobaricInhPa",Type = 'a',date = 20100625,hour = 24,level = 'all' ,region = 'AIR' ) #lat=(-90,90),lon=(0,359.5)

#partner_only = gobj.extract_data_of_partners(variableName = "Geopotential Height",typeOfLevel = "isobaricInhPa",Type = 'f', date = 20100525, hour = 24,level = 'all' ,region = 'AIR' ) #lat=(-90,90),lon=(0,359.5)
		   

#global_grb_data = gobj.extract_data_of_a_date(variableName = "Geopotential Height",typeOfLevel = "isobaricInhPa",Type = 'f',date = 20100525,hour = 24,level = 'all' ,lat=(0.0,40.0),lon=(60.0,100.0))

#uglobal_grb_data_range = gobj.extract_data_for_range_of_dates(variableName = "U component of wind",typeOfLevel = "isobaricInhPa",Type = 'a',startdate = 20100601,enddate = 20100603, hour = 24,level = 850 , lat=(0,40),lon=(60,100))#region = 'PenIndia' ) #lat=(-90,90),lon=(0,359.5)

#vglobal_grb_data_range = gobj.extract_data_for_range_of_dates(variableName = "V component of wind",typeOfLevel = "isobaricInhPa",Type = 'a',startdate = 20100601,enddate = 20100630, hour = 24,level = 850 , lat=(0,40),lon=(60,100)) #region = 'PenIndia' ) #

#uglobal_grb_data = gobj.extract_data_of_a_date(variableName = "U component of wind",typeOfLevel = "isobaricInhPa",Type = 'a',date = 20100802,hour = 24,level = 850 , lat=(0,40),lon=(60,100))#region = 'PenIndia' ) #lat=(-90,90),lon=(0,359.5)

#vglobal_grb_data = gobj.extract_data_of_a_date(variableName = "V component of wind",typeOfLevel = "isobaricInhPa",Type = 'a',date = 20100802,hour = 24,level = 850 , lat=(0,40),lon=(60,100)) #region = 'PenIndia' ) #

#data_with_partners_range = gobj.extract_data_for_range_of_dates_with_partners(variableName = "Geopotential Height",typeOfLevel = "isobaricInhPa",Type = 'f', startdate = 20100525, enddate = 20100527,skipdays = 1,calendar = None, hour = 24,level = 'all' ,region = 'AIR' ) #lat=(-90,90),lon=(0,359.5)
		   
		
#partners_data_range = gobj.extract_data_for_range_of_dates_of_partners(variableName = "Geopotential Height",typeOfLevel = "isobaricInhPa",Type = 'f', startdate = 20100525, enddate = 20100527,skipdays = 1,calendar = None, hour = 24,level = 'all' ,region = 'AIR' ) #lat=(-90,90),lon=(0,359.5)
		   		

#rainfall_data, rainfall_partners_fcst_data = gobj.rainfall_data_and_fcst_partners('/mnt/ncmrw-data-2010/rainfall/rainfall.xml','pobs',20100820,hour=144)#,20100821)#,hour=48)


#avg = gobj.avg_month_data(variableName = "Geopotential Height",typeOfLevel = "isobaricInhPa",Type = 'f',level = 'all', month = 'july',year=2010 , hour = 24,region = 'AIR' ) #lat=(-90,90),lon=(0,359.5)

#UV plot code for one month
#U,V = gobj.analysis_wind_avg_month_data('aug',2010)





