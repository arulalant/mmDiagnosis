import xml_data_access
import regions
xmlobj = xml_data_access.GribXmlAccess('/NCMRWF/all_xml')
xmlobj.rainfallXmlPath = '/NCMRWF/ncmrwf-data-2010/rainfall/uvrainfall.xml'
xmlobj.rainfallXmlVar = 'pobs'
xmlobj.rainfallModel = 'T254'

anl, fcst = xmlobj.getRainfallDataPartners(date = ('2010-6-5'),
                         hour = 24, level = 'all', orginData = 1,
                         datePriority = 'o', region = regions.India)

print 'anl time ', anl.id, anl.getTime().asComponentTime()
print 'fcst time', fcst.id, fcst.getTime().asComponentTime()
