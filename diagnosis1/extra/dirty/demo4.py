import xml_data_access
import regions
import numpy
import plots 
import por_template_1x2_landscape as template_1x2

xmlobj = xml_data_access.GribXmlAccess('/NCMRWF/all_xml')
xmlobj.rainfallXmlPath = '/NCMRWF/ncmrwf-data-2010/rainfall/uvrainfall.xml'
xmlobj.rainfallXmlVar = 'pobs'
xmlobj.rainfallModel = 'T254'

anl, fcst = xmlobj.getRainfallDataPartners(date = ('2010-6-5'),
                         hour = 24, level = 'all', orginData = 1,
                         datePriority = 'o', region = regions.India)

print 'anl time ', anl.id, anl.getTime().asComponentTime()
print 'fcst time', fcst.id, fcst.getTime().asComponentTime()

anl_array = numpy.array(anl)
anl_max = int(numpy.amax(anl_array))
anl_min = int(numpy.amin(anl_array))

diff = (anl_max - anl_min)/10
anl_level = range(anl_min, anl_max, diff)
anl_colors = (246, 255, 252, 253, 254, 251, 140, 5, 171, 248, 249, 242, 239)
isoFillTemplate = plots.genIsoFill(levels = anl_level, colorlist = anl_colors)

X = template_1x2.x

X.plot(anl, template_1x2.leftOfTop_lscp, isoFillTemplate, title = 'Obs Rainfall on 2010-6-5', continents = 1,)# bg = 1)
X.plot(fcst, template_1x2.rightOfTop_lscp, isoFillTemplate, title = 'Fcst Rainfall on 2010-6-5', continents = 1, )#bg = 1)

X.png('demo_1x2_rainfall.png')


