import xml_data_access
import regions
xmlobj = xml_data_access.GribXmlAccess('/NCMRWF/all_xml')

u = xmlobj.getData('ugrdprs', 'a', ('2010-6-1', '2010-6-3'), level = 850,)
#                                               lat=(0, 40), lon=(60, 100))
#                                                  region = regions.India))

print 'u info ', u.info()
