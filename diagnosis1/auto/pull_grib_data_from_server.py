import os
import sys
import time
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.abspath(os.path.dirname(__file__))
previousDir = os.path.abspath(os.path.join(__curDir__, '..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diag_setup.globalconfig import logpath
from diag_setup.logsetup import createLog
from ping import sleepIfPingHostDown


# create log object to written into logfile
logfile = __file__.split('.py')[0] + '.log'
log = createLog(__file__, os.path.join(logpath, logfile))


def pullDataOf(date, sshuser='kuldeep', sshserver='ncmr0102', sshpass=None,
        frompath='/scratch/ncmrtmp/kuldeep/2014/GFS/data/1p0',
        topath='/data/kuldeep/Model_Data/GFS/1p0/',
        dprefix='gdas.', fprefix='gdas1.t00z.grb',
        files=['anl', 'f24', 'f48', 'f72', 'f96', 'f120', 'f144', 'f168']):
    
    # sleep at most 100 min. check every 10 min interval ping host.
    # if host is down for 100 min, then quit the program
    sleepIfPingHostDown(sshserver)
    year = date[:4]
    date_dir = dprefix + date
    frompath = os.path.join(frompath, date_dir)
    if topath.endswith('*'):
        topath = topath[:-1]
    # end of if topath.endswith('*'):
    topath = os.path.join(topath, date_dir)
    if not os.path.exists(topath):
        log.info("created path %s", topath)
        os.makedirs(topath)
    # end of if not os.path.exists(topath):

    for gribfile in files:
        gribfile = fprefix + gribfile
        rfilepath = os.path.join(frompath, gribfile)
        cmd = "scp -r %s@%s:%s %s" % (sshuser, sshserver, rfilepath, topath)
        log.info("Executing SCP cmd '%s'", cmd)
        os.system(cmd)
        time.sleep(5)
        if os.path.isfile(os.path.join(topath, gribfile)):
            log.info("Successfully copied file from %s to %s", rfilepath, topath)
        else:
            log.error("Couldn't scp file from %s to %s", rfilepath, topath)
    # end of for gribfile in files:
# end of def pullData(date,...):


def pullOlrDataOf(date, frompath='/scratch/ncmrtmp/kuldeep/2014/GFS/olr/1p0',
                        topath='/data/kuldeep/Model_Data/GFS/1p0/',
                        fprefix='gdas1.t00z.sfluxgrb', files=['f01']):

    pullDataOf(date, frompath=frompath, topath=topath, fprefix=fprefix, files=files)
# end of def pullOlrDataOf(date, ...):










