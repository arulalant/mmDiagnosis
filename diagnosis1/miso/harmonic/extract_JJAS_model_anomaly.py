import os
import sys
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
diagDir = os.path.abspath(os.path.join(__curDir__, '../..'))
# adding the previous diagnosisutils path to python path
sys.path.append(diagDir)
from diag_setup.globalconfig import climatologies, models, processfilesPath, logpath
from diag_setup.logsetup import createLog
import diag_setup.netcdf_settings
from extract_JJAS_obs_anomaly import extractJJAS

# create log object to written into logfile
logfile = __file__.split('.py')[0] + '.log'
log = createLog(__file__, os.path.join(logpath, logfile))

print os.path.join(logpath, logfile)


if __name__ == '__main__':

    for climatology in climatologies:
        if not (climatology.dfile and climatolgy.name.lower() == 'miso'):
            print "In configure.txt climpartialdayfile \
                    not mentioned or its not miso. \
                    So can not compute daily anomaly."
            continue
        # end of if not climatology.dfile and obs.path and ...:
        for model in models:

            dailyAnlAnomalyPath = os.path.join(processfilesPath,
               'Anomaly', 'Unfiltered', model.name, climatology.name, 'Daily')

            jjasAnlAnomalyPath = os.path.join(processfilesPath,
               'Anomaly', 'Unfiltered', model.name, climatology.name, 'JJAS')

            if not os.path.isdir(jjasAnlAnomalyPath):
                os.makedirs(jjasAnlAnomalyPath)
                log.info("Path has created %s" % jjasAnlAnomalyPath)
            # end of if not os.path.isdir(jjasAnlAnomalyPath):
            # calling the genDailyAnomalyDirs function to do process
            # passing our own directory path and do model data regrid
            # w.r.t climatology.
            log.info("JJAS Extract Anomaly for the model '%s' has started" % model.name)
            # extract JJAS
            extractJJAS(dailyAnlAnomalyPath, jjasAnlAnomalyPath, log=log)
            log.info("Anomaly for the model '%s' has finished" % model.name)
        # end of if climatology.dfile and obs.filename:
    # end of for climatology in climatologies:

    print "Done! Creation of JJAS Anomaly netCdf Files"
# end of if __name__ == '__main__':



