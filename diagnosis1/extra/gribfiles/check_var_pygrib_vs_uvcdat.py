'''
Usage :

Using this script we can compare the variable data which are extracted by
pygrib (return as MV2) and cdms2.open xml (return as MV2)

Numpy array comparision take place

Author : Arulalan.T
Date : 05.07.2011
'''

import sys, os
import numpy
# getting the absolute path of the previous directory
previousDir = os.path.abspath(os.path.join(os.getcwd(), '..'))
# adding the previous path to python path
sys.path.append(previousDir)
# importing xml_data_acces.py from previous directory diagnosisutils module
import diagnosisutils.xml_data_access as xml_data_access
# getting the absolute path of the pre previous directory
prePreviousDir = os.path.abspath(os.path.join(previousDir, '..'))
# adding the pre previous path to python path
sys.path.append(prePreviousDir)
# importing data_acces.py from previous directory pygrib-code package
import pygrib_code.data_access as data_access

del sys

gobj = data_access.Grib_Access(dataPath = '/NCMRWF/ncmrwf-data-2010',
                                    modelName = 'NCMRWF2010')


data_pygrib = gobj.getData(variableName = "Geopotential Height",
                                 typeOfLevel = "isobaricInhPa", Type = 'a',
                                 date = ('2010-6-20'),
                                 hour = 24, level = 'all',
                                 lat=(-90, 90), lon=(0, 359.5))

print data_pygrib.shape
anl_xml_path = '/NCMRWF/all_xml'
xobj = xml_data_access.GribXmlAccess(anl_xml_path)

data_uvcdat = xobj.getData('hgtprs', Type = 'a', date = ('2010-6-20'), level = 'all', squeeze = 1)
print data_uvcdat.shape
# get the value alone
#data_pygrib = data_pygrib.getValue()
#data_uvcdat = data_uvcdat.getValue()

if data_pygrib.shape != data_uvcdat.shape:
    raise ValueError, 'The shapes of var are different'

# simple inbuilt method to numpy array eq compare
if numpy.array_equal(data_pygrib, data_uvcdat):
    print "The passed two variables are row wise same. So both are same data"
else:
    print "The passed two variables are not same. So it is diff data var"


# our explicit way to check each row wise element compare
for level in zip(data_pygrib, data_uvcdat):
    for i in range(len(level[0])):
        if not all(level[0][i] == level[1][i]):
            raise ValueError, "The passed two variables are not same. So it is diff data var"
#        else:
#            print "passing"

print "The passed two variables are row wise same. So both are same data \n"
print "Done"

# list comprehension to check each row wise element compare
comp = [True for level in zip(data_pygrib, data_uvcdat) for i in range(len(level[0])) if all(level[0][i] == level[1][i])]
latlen = data_uvcdat.shape[1]

if len(comp) == latlen:
    print "The passed two variables are row wise same. So both are same data"
else:
    print "The passed two variables are not same. So it is diff data var"
