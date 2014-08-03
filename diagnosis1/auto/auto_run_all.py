#!/usr/local/uvcdat/1.3.1/bin/python
"""
This script will do run all the scripts. It will do daily tasks such as
0.regrid_data_in_server 1.pull data,
2. generate ctl, idx files, 3.do_cdscan, 4.mjo_model_run,
5.do_archive, 6.copy_archive2public_ftp

Written By : Arulalan.T
Date : 03.09.2013
Updated : 31.05.2014

"""
import os
import sys
import time
import cdtime
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.abspath(os.path.dirname(__file__))
previousDir = os.path.abspath(os.path.join(__curDir__, '..'))
# adding the previous path to python path
sys.path.append(previousDir)
from generate_idx_ctl_files_grib1 import createCtlIdxFilesOf
from pull_grib_data_from_server import pullDataOf, pullOlrDataOf
from regrid_model_data_in_server import regridOf, regridOlrOf
from uv_cdat_code.diagnosisutils.timeutils import TimeUtility
from diag_setup.xml_status import getModelVarFirstLastDate, \
                        getModelAnlFirstLastDate, isModelVarsLatestDateSame
from diag_setup.globalconfig import uvcdat, models, logpath, plotexcludehour
from diag_setup.logsetup import createLog
from do_cdscan import updateCdscanXmlFiles



timeobj = TimeUtility()
# create log object to written into logfile
logfile = __file__.split('.py')[0] + '.log'
log = createLog(__file__, os.path.join(logpath, logfile))


def notifyme(msg, sec=5):
    os.system('notify-send "%s" -t %d000' % (msg, sec))
    time.sleep(sec)
    log.info(msg)
# end of def notifyme(msg, sec):


def _exitIfFalse(status, msg):
    if status:
        # status is Ok. So just return.
        return
    # end of if status:
    # Status got failure
    notifyme(msg, sec=10)
    msg = "Got Problem : So going to quit the auto_run script!"
    notifyme(msg, sec=10)
    sys.exit()
# end of def _exitIfFalse(status, msg):


def runDailyRoutineJobs(date, cdscanupdate=True, fullcdscan=False):
    """
    date - inpute directory name (endswith)
    cdscanupdate - Enable do only update the cdscanned xml/cdml files
                   of date directory input files. Takes True | False
    fullcdscan - Enable run complete cdscan and created cdml/xml files
                 freshly. Takes True | False

    """

    logtxtfile = os.path.join(logpath, 'auto_run_all_log.txt')
    if os.path.exists(logtxtfile):
        # remove the existing file. Otherwise it will keep on
        # append to the previous log file itself
        os.remove(logtxtfile)
    # end of if os.path.exists(logtxtfile):

    for model in models:
        # make desktop notification to the user
        msg = "Regriding data in server for %s" % date
        notifyme(msg)
        # do regrid the model data in the server
        regridOf(date)
        regridOlrOf(date)

        #print "2 min sleeping has started"
        time.sleep(10)
        #print "2 min sleeping was over"
        print "Now doing scp"

        # make desktop notification to the user
        msg = "Pulling data from server for %s" % date
        notifyme(msg)
        # pull/copy data of current 'date' from server to local
        pullDataOf(date, topath=model.dpath)
        pullOlrDataOf(date, topath=model.dpath)

        if model.dpath.endswith('*'):
            mdpath = model.dpath[:-1]
        else:
            mdpath = model.dpath
        # end of if model.dpath.endswith('*'):
        
        # checks either all files are pulled from the server
        checkdir = os.path.join(mdpath, 'gdas.'+date)
        if os.path.exists(checkdir):
            if not len(os.listdir(checkdir)) >= 9:
                # 1 anl, 1 f01, 7 fcst hr files, total 9 files
                # should be exists.
                # make desktop notification to the user
                msg = "Problem in scp copying files on %s" % date
                _exitIfFalse(False, msg)
            # end of if not len(os.listdir(checkdir)) >= 9:
        else:
            msg = "Problem, the directory as 'gdas.%s' doesnot exists in %s " % (date, mdpath)
            _exitIfFalse(False, msg)
        # end of if os.path.exists(checkdir):

        # make desktop notification to the user
        msg = "Creating ctl, idx files for %s" % date
        notifyme(msg)
        # create the ctl files for the newly copied date data directory alone
        print "Creating ctl idx files", date
        createCtlIdxFilesOf(date, dpath=model.dpath)

        if cdscanupdate:
            # make desktop notification to the user
            msg = "Updating Cdscanned Xml files for %s" % date
            notifyme(msg)
            # update the cdscanned xml with newly copied date data directory file/s alone
            print "Updating Cdscanned Xml files for", date
            anl_fcst = ['anl'] + model.hour
            updateCdscanXmlFiles(date, xmlpath=model.path, dpath=mdpath,
                             extension=model.extension, parameters=anl_fcst)
        # end of if cdscanupdate:
    # end of for model in models:

    if fullcdscan:
        # Doing cdscan stuff for fresh/full
        script = 'do_cdscan.py'
        # make desktop notification to the user
        msg = "Started MJO Works-%s for %s" % (script, date)
        notifyme(msg)
        scriptpath = os.path.join(__curDir__, script)
        print "Executing script", scriptpath
        cmd = "%s %s  >> %s" % (uvcdat, scriptpath, logtxtfile)
        log.info(cmd)
        os.system(cmd)
    # end of if fullcdscan:

    # get the passed date as comptime
    dateCompFmt = timeobj.timestr2comp(date)
    for model in models:
        # Multi model check the status of model vars latest date are same
        # or not for both analysis and fcst hours.
        # If status is false, then it will exit the program immediately
        status = isModelVarsLatestDateSame('anl', mname=model.name)
        msg = "Got Problem : Model %s analysis %s Vars Latest Date is not same" % (model.name, date)
        _exitIfFalse(status, msg)
        # check either model analysis latest date is same as argument date or not... 
#        # !!!! CMT on 31.05.2014.. Why should passed arg date match with current day date ?
#        latestAnlDate = getModelVarFirstLastDate('olr', model, mtype='a')[-1]
#        cmpresult = cdtime.compare(dateCompFmt, latestAnlDate)
#        if cmpresult != 0:
#            # dates are not same. So quit this script.
#            msg = "Got Problem : After cdscanned model %s latest anl date \
#                    is not same as current date '%s'" % (model.name, date)
#            _exitIfFalse(False, msg)
#        # end of if cmpresult != 0:

        for hr in model.hour:
            if not hr in plotexcludehour:
                # check model fcst vars dates are same or not
                status = isModelVarsLatestDateSame('fcst', hr, mname=model.name)
                msg = "Got Problem : Model %s fcst %s hr %s \
                       Vars Latest Date is not same" % (model.name, str(hr), date)
                _exitIfFalse(status, msg)
 #               # check either model fcst latest date is same as argument date or not
 #               latestFcstDate = getModelVarFirstLastDate('olr', model, mtype='a')[-1]
 #               cmpresult = cdtime.compare(dateCompFmt, latestFcstDate)
 #               if cmpresult != 0:
 #                   # dates are not same. So quit this script.
 #                   msg = "Got Problem : After cdscanned model %s latest fcst %s date \
 #                           is not same as current date '%s'" % (model.name, hr, date)
 #                   _exitIfFalse(False, msg)
                # end of if cmpresult != 0:
            # end of if not hr in plotexcludehour:
        # end of for hr in model.hour:
    # end of for model in models:

    scripts = ['mjo_model_run.py', 'do_archive.py', 
               'copy_archive2public_ftp.py', 'sendemail/sendreport2mails.py']
    for script in scripts:
        # make desktop notification to the user
        msg = "Started MJO Works-%s for %s" % (script, date)
        notifyme(msg)

        scriptpath = os.path.join(__curDir__, script)
        print "Executing script", scriptpath
        
        if script.endswith('do_archive.py'):
            cmd = "%s %s '%s' >> %s" % (uvcdat, scriptpath, date, logtxtfile)
        else:    
            cmd = "%s %s  >> %s" % (uvcdat, scriptpath, logtxtfile)
        # end of if script.endswith('do_archive.py'):
        
        log.info(cmd)

# Disabled the logfile copy to mail body txt file.
#       
#        if script.endswith('sendreport2mails.py'):
#            sendemailpath = os.path.join(__curDir__, 'sendemail')
#            # copying logtxt into body of auto email.
#            os.system('cp %s %s/body' % (logtxtfile, sendemailpath))
#        # end of if script.endswith('sendreport2mails.py'): 
        
        
        os.system(cmd)
    # end of for script in scripts:
# end of def runDailyRoutineJobs():


if __name__ == '__main__':

    # get the first and lastest date of xml analysis timeAxis
    anlFirstLastDate = getModelAnlFirstLastDate('olr')
    anlLastDate = anlFirstLastDate[-1]
    currentSysDate = time.strftime('%Y-%m-%d')
    # convert the component time object into yyyymmdd string format
    currentSysDate = timeobj.timestr2comp(currentSysDate)
    cmpresult = cdtime.compare(anlLastDate, currentSysDate)
    # get the next day to the latest date of xml analysis timeAxis
    nextDay = timeobj.moveTime(anlLastDate.year, anlLastDate.month,
                                anlLastDate.day, 1, returnType='s')

    thisDir = os.getcwd()
    os.chdir(__curDir__)
    count = 0

    pathstatus = os.path.exists(logpath)
    while not pathstatus:
        # make desktop notification to the user
        msg = "Please plug-in your external hdd 'segate_1tb'"
        notifyme(msg, sec=20)
        pathstatus = os.path.exists(logpath)
        time.sleep(5)
        count += 1
        if count == 10:
            msg = "You didn't plug ur external hdd. So going to quit script"
            notifyme(msg, sec=30)
            sys.exit()
        # end of if count == 10:
    # end of while not pathstatus:

    # Here the count purpose is to limit the no of days to attain
    # the current date
    count = 0
    while (cmpresult == -1 and count < 100):
        # make desktop notification to the user
        msg = "Started MJO Works for %s" % nextDay
        notifyme(msg)
        # call the below function to run all the scripts
        runDailyRoutineJobs(nextDay)
        # get the latest date of xml analysis timeAxis
        # after all the above update has done.
        anlLastDate = getModelAnlFirstLastDate('olr')[-1]      
        # get the next day to the latest date of xml analysis timeAxis
        nextDay = timeobj.moveTime(anlLastDate.year, anlLastDate.month,
                                    anlLastDate.day, 1, returnType='s')
        # if xml last timeAxis is < then current system date then
        # it will continue the loop. Else break the loop.
        cmpresult = cdtime.compare(anlLastDate, currentSysDate)
        count += 1
    # end of while cmpresult and count < 100:
    os.chdir(thisDir)
    # make desktop notification to the user
    msg = "Done! MJO Work is update to date %s" % nextDay
    notifyme(msg, sec=10)
# end of if __name__ == '__main__':



