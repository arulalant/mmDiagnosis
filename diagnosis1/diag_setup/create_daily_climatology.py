"""
.. module:: create climatology files
   :synopsis: Using this module we can create the climatology
              nc files for all the models/observations dataset.

   :detailed: It will create climatology for obeservation or models
              (analysis only, not the forecasts days)

   :todo: If we need to create forecast hours climatology, then in the code we
          need to get the forecast hours files from the xmlobj itself and
          just loop through it by calling the function createClimatology.

.. moduleauthor:: Arulalan.T <arulalant@gmail.com>

   Date : 13.08.2013

"""
import os
import sys
from climatology_utils import dailyClimatology, monthlyClimatology
from varsdict import variables
from globalconfig import models, observations, climatologies
# getting the absolute path of the previous directory
previousDir = os.path.abspath(os.path.join(os.getcwd(), '..'))
# adding the previous path to python path
sys.path.append(previousDir)
# import xml_data_acces.py from previous directory uv_cdat_code.diagnosisutils
import uv_cdat_code.diagnosisutils.xml_data_access as xml_data_access


def doClimatology(modelname, modelPath, climPath,
                    climPartialFileName, **kwarg):
    """

    KWargs:
        climatologyType : 'daily' | 'monthly'
                      'daily' means it will calculate daily climatology.
                      For this user can pass extra kwarg 'leap' is 0 | 1.
                      'monthly' means it will calculate monthly climatology
                      even though user passed daily model/observation data.

        Type : 'a' | 'o' | 'f'
        hour : If Type is 'f' then appropriate forecast hour has to pass.
        leap : True | False. For the daily climatology leap day need or not.

    Written By : Arulalan.T

    Date : 13.08.2013
    """

    climatologyType = kwarg.get('climatologyType', None)
    if not climatologyType:
        raise ValueError("Please pass kwarg 'climatologyType' as 'daily' | 'monthly'")
    Type = kwarg.get('Type', 'a')
    hour = kwarg.get('hour', None)
    leap = kwarg.get('leap', True)
    xmlobj = xml_data_access.GribXmlAccess(modelPath)
    toalvars = variables.get(modelname)
    climPath = os.path.join(climPath, climatologyType.capitalize())
    if not os.path.isdir(climPath):
        os.makedirs(climPath)
        print "The path has created", climPath
    # end of if not os.path.isdir(climPath):

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

        if not cvar:
            print "clim '%s' var name is empty string in 'vars.txt' file. \
                    So skipping climatology regid process for '%s' model \
                    variable name" % (cvar, mvar)
            continue
        # end of if not cvar:
        # get the xml file absolute path
        xmlFilePath = xmlobj.getXmlPath(Type, hour)
        # generate the climatology file name
        climatology_file = cvar + climPartialFileName
        climFilePath = os.path.join(climPath, climatology_file)
        # creating the regridded climatology file
        if os.path.isfile(climFilePath):
            os.remove(climFilePath)
            print "Already exists the regridded file. So removed it"
        # end of if os.path.isfile(climFilePath):
        print "\n climatology process takes place for '%s' variable" % mvar
        # call the below function to create the climatology in optimized manner
        if climatologyType == 'daily':
            dailyClimatology(mvar, xmlFilePath, climFilePath,
                                     ovar=cvar, leapday=leap)
        elif climatologyType == 'monthly':
            monthlyClimatology(mvar, xmlFilePath, climFilePath,
                                       memory='low', ovar=cvar)
        else:
            raise ValueError("arg climatologyType '%s' not either 'daily' \
                                nor 'monthly'" % climatologyType)
        # end of if climatologyType == 'daily':
    # end of for globalvar in toalvars.itervalues():
# end of def doClimatology(...):


def doClimatology_wrt(dType='model', **kwarg):
    """
    doClimatology_wrt : do climatology regid with respect to what ?

    Inputs :
        dType - It takes either 'model' or 'observation'.
                If model (by default) has passed, then it will do
                climatologies of models dataset.
                if observation has passed, then it will do
                climatologies of observations dataset.
    KWargs:
        climatologyType : 'daily' | 'monthly'
                      'daily' means it will calculate daily climatology.
                      For this user can pass extra kwarg 'leap' is 0 | 1.
                      'monthly' means it will calculate monthly climatology
                      even though user passed daily model/observation data.

        leap - True | False. It will create leap day in climatology if true

    """

    if dType in ['model']:
        mod_obs_list = models
        dtype = 'a'  # 'anl'
    elif dType in ['observation', 'obs']:
        mod_obs_list = observations
        dtype = 'o'  # 'obs'

    if len(mod_obs_list) == len(climatologies) == 1:
        print "Obtained one %s and one climatology" % dType
    elif len(mod_obs_list) == len(climatologies):
        print "Obtained %d %ss and climatologies" % len(mod_obs_list, dType)
    else:
        print "Obtained %d %ss and %d climatologies" % (len(mod_obs_list), dType, len(climatologies))

    for model in mod_obs_list:
        for climatology in climatologies:
            if model.count == climatology.count:
                if climatology.mfile:
                    # do monthly climatology
                    print "Monthly climatology takes place"
                    # calling the climatology regrid function to do process
                    doClimatology(model.name, model.path, climatology.path,
                                    climatology.mfile, Type=dtype, **kwarg)
                if climatology.dfile:
                    # do daily climatology
                    print "Daily climatology takes place"
                    # calling the climatology regrid function to do process
                    doClimatology(model.name, model.path, climatology.path,
                                    climatology.dfile, Type=dtype, **kwarg)
            else:
                pass
                # climatology configuration and model data configuration
                # are not equal in the text file
                # handle this case, in diff manner. The same loop should works.
                # But need to check all the cases.
            # end of if model.count == climatology.count:
        # end of for climatology in climatologies:
    # end of for model in models:
# end of def doClimatology_wrt(...):


if __name__ == '__main__':

#    doClimatology_wrt(dType='model', climatologyType='monthly')
    doClimatology_wrt(dType='observation', climatologyType='daily', leap=True)
# end of if __name__ == '__main__':




