# This scipt will generate the ctl and idx files of the grib1 (<2) data
import os
import sys
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__diagnosisDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__diagnosisDir__, '..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diag_setup.globalconfig import models, logpath
from diag_setup.logsetup import createLog

# create log object to written into logfile
logfile = __file__.split('.py')[0] + '.log'
log = createLog(__file__, os.path.join(logpath, logfile))


def createCtlIdxFiles(path, grib2ctl='grib2ctl.pl', gribmap='gribmap'):
    """
    Inputs :
        grib2ctl : Executable path of grib2ctl.pl script. By default it
                   takes grib2ctl.pl.
        gribmap : Executable path of gribmap. By default it takes
                  gribmap.

                  So in your bash environment if you set these two as
                  either alias or exported those path, then it will
                  works as it is.

    Written By : Arulalan.T

    """

    if path.endswith('*'):
        path = path[:-1]
    for root, sub, files in os.walk(path):
        print root
        os.chdir(root)
        log.info("Changed pwd into %s", root)
        for f in files:
            log.info("created %s.ctl file", f)
            if f.endswith('anl'):
                # Do need full to create ctl,idx files for the analysis files
                # -ts1dy is for setting 1day time stamp in ctl file
                os.system("%s %s -ts1dy > %s.ctl " % (grib2ctl, f, f))
                os.system("%s -i %s.ctl" % (gribmap, f))
                #print os.system("ls")
            else:
                try:
                    if (f.split('.')[2]).startswith(('grbf', 'sfluxgrbf')) and \
                        not f.endswith('.idx') and not f.endswith('.ctl'):
                        # Do need full to create ctl,idx
                        # files for the fcst files
                        # -ts1dy is for setting 1day time stamp in ctl file
                        # we no need to pass -verf option for fcst file, since
                        # it cdat cant read the data
                        os.system("%s %s -ts1dy > %s.ctl " % (grib2ctl, f, f))
                        os.system("%s -i %s.ctl -0 " % (gribmap, f))
                except:
                    #continue
                    pass
        # end of for f in files:
    # end of for root, sub, files in os.walk(path):
    log.info("Done")
# end of def createCtlIdxFiles(path, ...):


def createCtlIdxFilesOf(date, dpath, prefix='gdas.', grib2ctl='/usr/local/bin/grib2ctl',
                    gribmap='/usr/local/bin/gribmap'):
    """
    dpath - model.dpath
    """
    date_dir = prefix + date
    if dpath.endswith('*'):
        dpath = dpath[:-1]
    model_date_path = os.path.join(dpath, date_dir)
    print model_date_path
    createCtlIdxFiles(model_date_path, grib2ctl=grib2ctl, gribmap=gribmap)
# end of def createCtlIdxFilesOf(date, prefix='gdas'):


if __name__ == '__main__':

    for model in models:
        # pass model.dpath (data path, not the xml path)
        createCtlIdxFiles(model.dpath, grib2ctl='/usr/local/bin/grib2ctl',
            gribmap='/usr/local/bin/gribmap')
    # end of for model in models:
# end of if __name__ == '__main__':


