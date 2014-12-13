"""
.. module:: regrid_climatology_files
   :synopsis: Using this module we can create the regridded climatolgy
              nc files for all the months.

   :detailed: This script should read the climatolgy data variables and regrid
              it w.r.t the model data variables. It should create individual
              nc files for each variables climatolgy regridded data.

              Most importantly it shoule do the vertical level regrid and
              horizontal level (both lat, lon) regrid w.r.t the model data
              resolution.

.. moduleauthor:: Arulalan.T <arulalant@gmail.com>

   Date : 17.08.2011

"""
import os
import sys
import cdms2
from regrid2 import Horizontal
from varsdict import variables
from globalconfig import models, observations, climatologies, processfilesPath
import netcdf_settings
from gendir import createDirsIfNotExists
# getting the absolute path of the previous directory
previousDir = os.path.abspath(os.path.join(os.getcwd(), '..'))
# adding the previous path to python path
sys.path.append(previousDir)
# import xml_data_acces.py from previous directory uv_cdat_code.diagnosisutils
import uv_cdat_code.diagnosisutils.xml_data_access as xml_data_access


__Debug__ = False


def createRegriddedClimatology(modelname, modelPath, climoriginalPath,
                         climRegridPath, climPartialFileName, **kwarg):

    Type = kwarg.get('Type', 'a')
    hour = kwarg.get('hour', None)
    xmlobj = xml_data_access.GribXmlAccess(modelPath)
    toalvars = variables.get(modelname)
    for globalvar in toalvars.itervalues():
        # get the model and clim var name from the namedtuple object
        if Type in ['a', 'anl', 'f', 'fcst']:
            mvar = globalvar.model_var
        elif Type in ['o', 'obs']:
            mvar = globalvar.obs_var
        else:
            mvar = globalvar.model_var
        # end of if Type in ['a', 'anl', 'f', 'fcst']:
        cvar = globalvar.clim_var
        # get the model variable level
        mlevel = globalvar.model_level
        if not cvar:
            print "clim '%s' var name is empty string in 'vars.txt' file. \
                    So skipping climatology regid process for '%s' model \
                    variable name" % (cvar, mvar)
            continue
        # end of if not cvar:
        print "\n Regriding process takes place for '%s' variable" % cvar
        # get the model data of the first date of its timeAxis
        modeldata = xmlobj.getData(mvar, Type, date=slice(1), hour=hour)
        # get the model data grid
        modelgrid = modeldata.getGrid()
        # generate the climatology file name
        climatology_file = cvar + climPartialFileName
        climRegridFilePath = os.path.join(climRegridPath, climatology_file)
        cfile = cdms2.open(os.path.join(climoriginalPath, climatology_file))

        # creating the regridded climatology file
        if os.path.isfile(climRegridFilePath):
            os.remove(climRegridFilePath)
            print "Already exists the regridded file. So removed it"
        rcfile = cdms2.open(climRegridFilePath, 'a')
        # get the climatology data
        climatologyvar = cfile[cvar]
        # get the climatology data grid
        climatologygrid = climatologyvar.getGrid()
        #
        # Regridding the climatology data
        # Creating the horizontal lat,lon regrid
        # Note that 'climatlogygrid' is the source and 'modelgrid' is the target
        regridfunc = Horizontal(climatologygrid, modelgrid)
        climlevelaxis = climatologyvar.getLevel()
        modellevelaxis = modeldata.getLevel()

        if mlevel is not None:
            if climlevelaxis:
                climatology_levels = climlevelaxis[:]
            if modellevelaxis:
                model_levels = modellevelaxis[:]

            if modellevelaxis and climlevelaxis:
                if min(climatology_levels) <= min(model_levels):
                    if max(climatology_levels) <= max(model_levels):
                        if __Debug__:
                            print "The min and max of both model and climatolgy levels \
                                equal or less than the model levels. \
                                So level regridding takes place"
                    else:
                        raise RuntimeError("The max level of model is greater\
                                           than the max level of climatology")
                else:
                    raise RuntimeError("The min level of model is less \
                                            than the min level of climatology")
            # end of if modellevelaxis and climlevelaxis:
        # end of if mlevel is not None:

        climatologytime = climatologyvar.getTime().asComponentTime()
        for day in climatologytime:
            climatology_day_data = cfile(cvar, time = day, squeeze=0)
            if mlevel is not None:
                if modellevelaxis and climlevelaxis:
                    #
                    # Doing vertical pressure level regrid
                    #
                    climatology_level_regridded = climatology_day_data.pressureRegrid(modellevelaxis)
                    if __Debug__:
                        print "The Date : ", day
                        print "before level regridded"
                        print climatology_day_data.shape
                        print "Levels : ", climatology_day_data.getLevel()[:]
                        print "after level regridded"
                        print climatology_level_regridded.shape
                        print "Levels : ", climatology_level_regridded.getLevel()[:]
                # end of if modellevelaxis and climlevelaxis:
            # end of if mlevel is not None:

            # apply regridfunc to climatology data
            if modellevelaxis and climlevelaxis:
                climatology_latlon_regridded = regridfunc(climatology_level_regridded)
                # free memory
                del climatology_level_regridded
            else:
                climatology_latlon_regridded = regridfunc(climatology_day_data)
            # end of if modellevelaxis and climlevelaxis:
            if __Debug__:
                print "after latlon regrid"
                print climatology_latlon_regridded.shape
                print "Latitude : ", climatology_latlon_regridded.getLatitude()[:]
                print "Longitude : ", climatology_latlon_regridded.getLongitude()[:]
            # write the regridded (level, lat, lon) climatology data into nc file
            rcfile.write(climatology_latlon_regridded)
            # free memory
            del climatology_latlon_regridded
        # end of for day in climatologytime:
        print "Created Regridded file ", climRegridFilePath
        rcfile.close()
        cfile.close()
    # end of for globalvar in toalvars.itervalues():
# end of def createRegriddedClimatology(...):


def doClimRegrid_wrt(dType='model'):
    """
    doClimRegrid_wrt : do climatology regid with respect to what ?

    Inputs :
        dType - It takes either 'model' or 'observation'.
                If model (by default) has passed, then it will do
                climatologies regrid w.r.t models.
                if observation has passed, then it will do
                climatologies regrid w.r.t observations.


    """

    if dType in ['model']:
        mod_obs_list = models
#        dtype = 'a'  # 'anl'
        dtype = 'f'
        hour = 24
    elif dType in ['observation', 'obs']:
        mod_obs_list = observations
        dtype = 'o'  # 'obs'

    if len(mod_obs_list) == len(climatologies) == 1:
        print "Obtained one %s and one climatolgy" % dType
    elif len(mod_obs_list) == len(climatologies):
        print "Obtained %d %ss and climatologies" % len(mod_obs_list, dType)
    else:
        print "Obtained %d %ss and %d climatologies" % (len(mod_obs_list), dType, len(climatologies))

    for model in mod_obs_list:
        for climatology in climatologies:
            if model.count == climatology.count:
                # creating climatology directory w.r.t climatology name in the
                # processfilesPath, modelname, Regrid, Climatology directory.
                climatologyRegridPath = createDirsIfNotExists(processfilesPath,
                                        [model.name, 'Regrid', 'Climatology',
                                                            climatology.name])

                if climatology.mfile:
                    # add suffix to the original climatolgy path
                    climatologyPath = os.path.join(climatology.path, 'Monthly')
                    print "Note : Appened suffix 'Monthly' in climatolgy \
                        original path. Make sure that you already added", climatology.path
                    print "So new access path of original climatology files is", climatologyPath
                    # do monthly climatolgy regrid
                    print "Monthly regridding takes place"
                    # calling the climatolgy regrid function to do process
                    createRegriddedClimatology(model.name, model.path,
                                           climatologyPath,
                                           climatologyRegridPath,
                                           climatology.mfile, Type=dtype)
                if climatology.dfile:
                    # add suffix to the original climatolgy path
                    climatologyPath = os.path.join(climatology.path, 'Daily')
                    print "Note : Appened suffix 'Daily' in climatolgy \
                        original path. Make sure that you already added", climatology.path
                    print "So new access path of original climatology files is", climatologyPath
                    # do daily climatolgy regrid
                    print "Daily regridding takes place"
                    if climatolgy.name.lower() == 'miso':
                        cdfile = climatology.dfile
                        cdfile = cdfile.split('.')
                        cdfile = '.'.join(cdfile.insert(-1, 'harmonic'))
                    else:
                        cdfile = climatology.dfile
                    # end of if climatolgy.name.lower() == 'miso':
                    
                    # calling the climatolgy regrid function to do process
                    createRegriddedClimatology(model.name, model.path,
                                           climatologyPath,
                                           climatologyRegridPath,
                                           cdfile, Type=dtype, hour=hour)
            else:
                pass
                # climatolgy configuration and model data configuration are not equal in the text file
                # handle this case, in diff manner. The same loop should works.
                # But need to check all the cases.
            # end of if model.count == climatolgy.count:
        # end of for climatolgy in climatologies:
    # end of for model in models:
# end of def doClimRegrid_wrt_Model():


if __name__ == '__main__':

    doClimRegrid_wrt(dType='model')
#    doClimRegrid_wrt(dType='observation')


