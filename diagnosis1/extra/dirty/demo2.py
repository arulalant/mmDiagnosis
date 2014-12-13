import xml_data_access
xmlobj = xml_data_access.GribXmlAccess('/NCMRWF/all_xml')
anl, fcst = xmlobj.getDataPartners(var = 'ugrdprs', Type = 'a',
                    date = ('2010-6-5'), hour = 24, level = 'all',
                    orginData = 1, datePriority = 'o',
                    lat=(0, 40), lon=(60, 100))

print 'anl time ', anl.getTime().asComponentTime()
print 'fcst time ', fcst.getTime().asComponentTime()
