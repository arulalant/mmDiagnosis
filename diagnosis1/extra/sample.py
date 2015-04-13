import diagnosisutils.xml_data_access as x
import diagnosisutils.timeutils as t
import diagnosisutils.regions as r
import cdms2
o = x.GribXmlAccess('/home/dileep/z/Model_data/ECMWF_Europe/ECMWF_xml')

o.rainfallXmlPath = '/home/dileep/NCMRWF_out/processed_files/ECMWF/Regrid/ObsRain/NCMRWF/rainfall_regrided.xml'
o.rainfallXmlVar = 'pobs'
o.rainfallModel = 'ECMWF'
#d = o.getData('tpratesfc', 'f', ('2010-6-1', '2010-6-3'), '48', 850, region = India, squeeze = 1)

##,lon = (20,140,'cc'),lat = (-20,60,'cc'))
##fu = cdms2.open('/NCMRWF/climatology/Levels/uwnd.day.ltm.nc')

d = o.getData('tpratesfc', 'f', '2010-6-1', '48','all', squeeze = 1, lon = (60,100,'cob'),lat = (0., 40,'cob'))

print d
##o.closeXmlObjs()
#modeldataset = o['ugrdprs', 'a']
## get the timeAxis of modeldata set and correct its bounds
#modeltime = o._correctTimeAxis(modeldataset.getTime())
# get the fully available months
#availableMonths = o.getTimeAxisFullMonths(modeltime)
#print d.listall()
#fu = cdms2.open('/NCMRWF/climatology/Levels/uwnd.day.ltm.nc')

#print d(India).getLatitude()[:],d(India).getLongitude()[:]
#myd  = o.getData('ugrdprs', 'a', ('2010-6-1', '2010-6-3'), level = 850, region = r.India, squeeze = 1)
#test = o['ugrdprs','f',48]
#ori, dp = o.getDataPartners('absvprs', 'a', ('2010-6-1'),
#             hour=24, level='all', orginData = 1, datePriority = 'o')

#t = timeutils.Time()
#myt = t.generateTimeAxis(10,'2010-5-1')

#t = o.getMonthAvgData(var = 'ugrdprs', Type = 'f', hour = '24', level = 850, \
#                                                month = 'june', year = 2010)
 
#o = xml_data_access.GribXmlAccess('/home/dileep/z/Model_data/CMA_China/CMA_xml')

#o.rainfallXmlPath = '/home/dileep/z/NCMRWF/Monsoon_2010/rainfall/regrid/CMA/rainfall_regrided.xml'
#o.rainfallXmlVar ='pobs'
#o.rainfallModel = 'T254'
#o.rainfallXmlPath = '/NCMRWF/ncmrwf-data-2010/rainfall/uvrainfall.xml'
#o.rainfallXmlVar ='pobs'
#

#r,p = o.getRainfallDataPartners(date = ('2010-6-10'), hour = 24, level = 'all',
#                  orginData = 1,datePriority = 'o',region = r.India, squeeze=1)
