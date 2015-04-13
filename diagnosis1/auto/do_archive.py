"""
This script will do copy of plots & log files into archive path
and make it as tarball.
Written By : Arulalan.T
Date : 20.08.2013

"""
import os
import sys
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__curDir__, '..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diagnosisutils.timeutils import TimeUtility
from diag_setup.globalconfig import plotsgraphsPath, logpath, archivepath
from diag_setup.xml_status import getModelAnlFirstLastDate
from diag_setup.logsetup import createLog


timeobj = TimeUtility()
# create log object to written into logfile
logfile = __file__.split('.py')[0] + '.log'
log = createLog(__file__, os.path.join(logpath, logfile))


def doCopy(inpath, outpath, matchdir):
    """
    20.08.2013
    """

    if not os.path.isdir(outpath):
        os.makedirs(outpath)
    for root, sub, files in os.walk(inpath):
        if root.endswith(matchdir):
            cmd = "cp -r %s/* %s/" % (root, outpath)
            os.system(cmd)
            log.info("Copied folders/files from %s/* into %s", root, outpath)
        # end of if root.endswith(matchdir):
    # end of for root, sub, files in os.walk(inpath):
# end of def doCopy(inpath, outpath, matchdir, dname):


if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        # pass date as command line argument to create archive file name.
        currentDate = sys.argv[1]
    else:
        # get the first and lastest date of xml analysis timeAxis
        anlFirstLastDate = getModelAnlFirstLastDate()

        # conver the component time object into yyyymmdd string format
        currentDate = timeobj.comp2timestr(anlFirstLastDate[-1], returnHour='no')
        cyear = str(anlFirstLastDate[-1].year)
    # end of if len(sys.argv) > 1:
    
    # model name should be created as first directory
    # inside the currentDate of the archivepath.
    # todo : need to be automated when multi model comes in/out.
    modelname = 'GFS'
    prefix = 'mjo'
    outname = prefix + '_' + currentDate
    # outpath of plots inside the archive path
    outpath = os.path.join(archivepath, outname, modelname, 'Plots')
    log.info("Copy the Plots from %s into %s", plotsgraphsPath, outpath)
    # make copy of plots into archive path
    doCopy(plotsgraphsPath, outpath, currentDate)

    # get the log files from current directory which are created in this
    # same path by wrongly instead of logpath
    if not __curDir__: __curDir__ = '.'
    logfiles = [f for f in os.listdir(__curDir__) if f.endswith('.log')]
    if logfiles:
        # copy all log files of current directory into logpath
        os.system("cp -r %s/*.log %s" % (__curDir__, logpath))
    # outpath of latest logs inside the archive path
    outpath = os.path.join(archivepath, outname, modelname, 'Logs')
    log.info("Copy the Logs from %s into %s", logpath, outpath)
    # make copy of latest logs into archive path
    doCopy(logpath, outpath, 'Latest')

    # outpath of currentDate inside the same logpath
    outpath = os.path.join(logpath, '..', currentDate)
    # make copy of latest logs into currentDate inside the same logpath
    log.info("Copy the Latest Logs into %s folder", outpath)
    doCopy(logpath, outpath, 'Latest')

    currentDir = os.getcwd()
    os.chdir(archivepath)
    tarfile = outname + '.tar.gz'
    if os.path.exists(tarfile):
        log.warning("Removed old tar file %s for the same date", tarfile)
        os.remove(tarfile)
    # end of if os.path.exists(tarfile):
    cfiles = [f for f in os.listdir('.') if f.endswith('.tar.gz')]
    if cfiles:
        log.info("moved old tarbal into previous directory of %s", archivepath)
        os.system("mv *.tar.gz ../")
    # end of if os.listdir('.'):

    # create the tarbal of currentDate directory in archivepath
    os.system("tar -cf  %s.tar  %s" % (outname, outname))
    # In ubuntu
    os.system("gzip %s.tar" % outname)
    log.info("Created tarball file %s/%s.tar.gz", archivepath, outname)
    # remove the directory in archivepath
    os.system("rm -rf %s" % outname)
    log.info("Removed directory %s/%s", archivepath, outname)

    if os.listdir(logpath):
        # removed the *.log, *.txt files from logpath
        lpath = os.path.join(logpath, '*')
        os.system("rm -rf %s/*" % lpath)
    # end of if os.listdir(logpath):
    # back to original path
    os.chdir(currentDir)
# end of if __name__ == '__main__':






