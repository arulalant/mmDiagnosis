import os
import sys
# getting the absolute path of the previous directory
previousDir = os.path.abspath(os.path.join(os.getcwd(), '..'))
# adding the previous path to python path
sys.path.append(previousDir)
# import xml_data_acces.py from previous directory diagnosisutils
from diagnosisutils.xml_data_access import GribXmlAccess
from globalconfig import models
from varsdict import variables


def getFirstLastDate(xmlpath, mvar, Type='a', hour=None):
    """
    26.08.2013
    """

    xmlobj = GribXmlAccess(xmlpath)
    timeAxis = xmlobj[mvar, Type, hour].getTime()
    comtime = timeAxis.asComponentTime()
    return (comtime[0], comtime[-1])
# end of def getFirstLastDate(xmlpath, mvar, Type='a', hour=None):


def getModelVarFirstLastDate(var, model, mtype, hour=None):
    """
    var : primary variable looking in variables.
          It takes short_var from varsdict.
    26.08.2013
    """

    mpath = model.path
    totvar = variables.get(model.name)

    if var in totvar:
        anl_hour = totvar[var].anl_hour
        if anl_hour:
            # anl hour is exists. So it's type is fcst.
            # But virtually consider it as analysis.
            mtype = 'f'
            hour = anl_hour
        # end of if anl_hour:
    else:
        var = totvar.keys()[0]
    # end of if var in totvar:
    mvar = totvar[var].model_var
    return getFirstLastDate(mpath, mvar, mtype, hour)
# end of def getModelVarFirstLastDate():


def getModelAnlFirstLastDate(var='olr', mname=None):
    """
    var : primary variable looking in variables.
          It takes short_var from varsdict.
    26.08.2013
    """

    if len(models) > 1:
        if mname:
            for m in models:
                if m.name == mname:
                    model = m
                    break
            # end of for m in models:
        else:
            raise ValueError("You must pass the model name to access \
                                     getFirstLastDate of xml_status")
    else:
        model = models[0]
    # end of if len(models) > 1:
    return getModelVarFirstLastDate(var, model, mtype='a')
# end of def getModelAnlFirstLastDate():


def isModelVarsLatestDateSame(dtype='anl', hour=None, mname=None):
    """

    dtype : anl | fcst
    hour : fcst hour. By default None

    Return : True if all vars of model 'anl' or 'fcst' files latest
             date are same. Otherwise False.
             None if problem has occured in xml files

    Date : 18.09.2013

    """

    if len(models) > 1:
        if mname:
            for m in models:
                if m.name == mname:
                    model = m
                    break
            # end of for m in models:
        else:
            raise ValueError("You must pass the model name to access \
                                     getFirstLastDate of xml_status")
    else:
        model = models[0]
    # end of if len(models) > 1:
    mpath = model.path
    totvar = variables.get(model.name)

    all_vars_last_date = set([])
    for short_var in totvar:
        mvar = totvar[short_var].model_var
        anl_hour = totvar[short_var].anl_hour
        if dtype in ['anl', 'a']:
            if anl_hour:
                mtype = 'f'
                hour = anl_hour
            else:
                mtype = 'a'
        elif dtype in ['fcst', 'f']:
            mtype = 'f'
        # end of if dtype in ['anl', 'a']:
        ldate = getFirstLastDate(mpath, mvar, Type=mtype, hour=hour)[-1]
        all_vars_last_date.add(str(ldate))
    # end of for short_var in totvar:

    if len(all_vars_last_date) == 1:
        return True
    elif len(all_vars_last_date) == 0:
        # problem while getting last date from model xml file
        return None
    else:
        return False
    # end of if len(all_vars_last_date) == 1:
# end of def isModelVarsLatestDateSame(dtype='anl', hour=None, mname=None):





















