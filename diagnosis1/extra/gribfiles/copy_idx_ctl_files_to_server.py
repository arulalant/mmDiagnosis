"""
 This scipt will copy the ctl and idx files of the grib2 data of 
 NCMRWF 2010 data from the local_path to the server_path...

 reason is, some time generating ctl,idx files in the server from the local 
 machines script, takes too much time...
"""
import os

server_path = '/home/arulalan/y/NCMRWF/Monsoon_2010'
local_path = '/NCMRWF/ncmrwf-data-2010/'
walk = os.walk(local_path)
for root, sub, files in walk:
    #print root
    os.chdir(root)
    subpath = root.split('/')[-1]
    #print subpath 
    for f in files:
        #print f
        if f.endswith('.idx') or f.endswith('.ctl'):
            os.system("cp %s/%s %s/%s" % (root, f, server_path, subpath))
            #print "cp %s/%s %s/%s" % (root, f, server_path, subpath)
