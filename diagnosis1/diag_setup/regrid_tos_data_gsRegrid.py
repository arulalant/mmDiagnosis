"""
## This program reads the  Models data from Curvelinear grid ##
## and rewrites it into a rectelinear grid ##
"""

import cdms2, numpy, cdutil, MV2, vcs, sys, os, string
#from regrid2 import Regridder
from cdms2 import gsRegrid 
from CMIP5_ENSO_ProcessDict import *

# Testing with one data 
# infile one is to extract a required sample destination grid grid
#

print '\t\t\tReading infile1 !'
infile1 = cdms2.open('/home/rajeev/work/data/cmip5/CanESM2/historical/tos/r1i1p1/tos_Omon_CanESM2_historical_r1i1p1_185001-200512.nc')
start_time = infile1.getAxis('time').asComponentTime()[0]
end_time = infile1.getAxis('time').asComponentTime()[1]
VAR1 = infile1('tos', squeeze = 1, time=(start_time, end_time))
#
# Get the destination grid.
#
dst_grd = VAR1.getGrid()
#
# print grid1.info()
#
EXP_LIST = ['historical']
VAR_LIST = ['tos']
MODEL_LIST = ['CCSM4']
#RUN_LIST.remove('r4i1p1')
#RUN_LIST = ['r3i1p1']

for VAR in VAR_LIST:
    #
    print 'Processing Variable ', VAR
    #
    for EXP in EXP_LIST:
        #
        print '\tExperiment ', EXP
        #
        for MODEL in MODEL_LIST:
            #
            print '\t\tProcessing Model ', MODEL
	    #
            for RUN in RUN_LIST:
                #
                print '\t\t\tRun ', RUN
                #
                # Get the data directory & filename for the specified VAR, EXP, MODEL & RUN
                #
                indir = create_raw_data_dir_name(MODEL,  EXP, VAR, RUN)
                infile = create_raw_data_xmlfile_name(MODEL,  EXP, VAR, RUN)
                #
                # If the file does not exist, raise a warning message and move on......
                #
                if (not indir) or (not infile):
                    print '\t\t\tFile does not exist! Skipping!'
                else:
                    #
                    f = cdms2.open(indir + infile)
		    data_list = []
		    TARGET_DIR = indir
		    outfile = string.joinfields([VAR, EXP, MODEL, RUN], '_') + '_rewritted' '.nc'
		    TIME = f.getAxis('time').asComponentTime()
		    for t in TIME:
		   	VAR2 = f(VAR, time=(t, t), squeeze=1)
			#
			# Get the source grid
			#
			src_grd = VAR2.getGrid()
			#src_bounds = src_grd.getBounds()
			#

			##########   Regridding ##################

			# Getting the source and Destination Co-ordinates and the Mask
			#
			src_y = src_grd.getLatitude().getValue()
			src_x = src_grd.getLongitude().getValue()
			dst_y = dst_grd.getLatitude().getValue()
			dst_x = dst_grd.getLongitude().getValue()
			#
			# Geting Mask
			#
			bool_mask = MV2.masked_greater_equal(VAR2, 1.e+20)
			condition = MV2.getmask(bool_mask)
			mask = MV2.where(condition, 0, 1)
			newmask = numpy.array(mask,dtype = numpy.int32)
			#
			# Defining the regrid function
			#
			rg = gsRegrid.Regrid([src_y, src_x], [dst_y, dst_x], mkCyclic = False) # src_bounds = src_bounds)
			rg.setValidMask(newmask)
			rg.computeWeights(nitermax= 10, tolpos= 1.e-1)
			#
			# Creating the dummy destination data for Regridding 
			#
			src_coords = rg.getSrcGrid()
			dst_coords = rg.getDstGrid()
			print 'src_coords[0].shape = ', src_coords[0].shape
			print 'dst_coords[0].shape = ', dst_coords[0].shape
			dst_data = numpy.zeros( dst_coords[0].shape, numpy.float32)
			#
			# Regird
			#
			rg.apply(VAR2, dst_data)
			#
			data_list.append(dst_data)
			del(dst_data)
			del(VAR2)
			print 'end of loop ', t
			# 
		    # end of for t in TIME  
		    # Creating the MV's
		    var = MV2.array(data_list)
		    del(data_list)
		    lat = dst_grd.getLatitude()
		    lon = dst_grd.getLongitude()
		    t = range(len(var.getAxis(0)))
		    time = cdms2.createAxis(t)
		    time.designateTime() 
		    time.id='time'
		    time.units = 'months since' + str(TIME[0])
		    var.setAxis(0, time )
		    var.setAxis(1, lat)
		    var.setAxis(2, lon)
		    var.id = VAR
		    var.comment1 = MODEL
		    var.units = 'K'
		    var.long_name = 'Sea Surface Temperature'
		    fout = cdms2.open(TARGET_DIR + outfile, 'w')
		    fout.write(var)
       		    fout.close()
		    del(var)
		# end of if (not indir) or (not infile):
	    # end for RUN in RUN_LIST
	# end of for MODEL in MODEL_LIST:
    # end of for MODEL in MODEL_LIST:
#end of for VAR in VAR_LIST:





