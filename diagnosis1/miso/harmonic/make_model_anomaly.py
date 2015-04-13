import os
import sys
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
diagDir = os.path.abspath(os.path.join(__curDir__, '../..'))
# adding the previous diagnosisutils path to python path
sys.path.append(diagDir)
from diagnosis.compute_daily_anomaly import genDailyAnomalyDirs
from diag_setup.globalconfig import observations, climatologies, models, processfilesPath, logpath
from diag_setup.logsetup import createLog
import diag_setup.netcdf_settings

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
#                # generate the climatology regrid path which has already
#                # created
#                climRegridPath = os.path.join(processfilesPath,
#                    model.name, 'Regrid', 'Climatology', climatology.name)
            climatologyPath = os.path.join(climatology.path, 'Daily')
            dailyAnlAnomalyPath = os.path.join(processfilesPath,
               'Anomaly', 'Unfiltered', model.name, climatology.name, 'Daily')

            if not os.path.isdir(dailyAnlAnomalyPath):
                os.makedirs(dailyAnlAnomalyPath)
                log.info("Path has created %s" % dailyAnlAnomalyPath)
            # end of if not os.path.isdir(dailyAnlAnomalyPath):
            # calling the genDailyAnomalyDirs function to do process
            # passing our own directory path and do model data regrid
            # w.r.t climatology.
            log.info("Anomaly for the model '%s' has started" % model.name)
            
            # make harmonic climatolgy file name 
            cdfile = climatology.dfile.split('.')
            cdfile = '.'.join(cdfile.insert(-1, 'harmonic'))
    
            genDailyAnomalyDirs(model.name, model.path, model.hour,
                    climatologyPath, cdfile, climatology.year,
                    anopath=dailyAnlAnomalyPath, dregrid=True, log=log)
            log.info("Anomaly for the model '%s' has finished" % model.name)
        # end of if climatology.dfile and obs.filename:
    # end of for climatology in climatologies:

    print "Done! Creation of Daily Anomaly netCdf Files"
# end of if __name__ == '__main__':



