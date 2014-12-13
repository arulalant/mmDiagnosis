import os
import sys
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
diagDir = os.path.abspath(os.path.join(__curDir__, '../..'))
# adding the previous diagnosisutils path to python path
sys.path.append(diagDir)
from diagnosisutils.timeutils import TimeUtility
from diag_setup.globalconfig import observations, climatologies, processfilesPath, logpath
from diag_setup.logsetup import createLog
import diag_setup.netcdf_settings

# create log object to written into logfile
logfile = __file__.split('.py')[0] + '.log'
log = createLog(__file__, os.path.join(logpath, logfile))

print os.path.join(logpath, logfile)

# create timeutils object
tobj = timeutils.TimeUtility()

def extractJJAS(inpath, outpath, log):

    for fname in os.listdir(inpath):
        if fname.endswith('.nc'):
            varName = fname.split('.')[0]
            infpath = os.path.join(inpath, fname)
            log.info('Extract JJAS anomaly has started for file %s' % infpath)
            # extrat JJAS data
            JJAS_data = tobj.getSeasonalData(varName, infpath, 1, 6, 30, 9)
            # write JJAS anomaly
            outfpath = os.path.join(outpath, fname)
            outf = cdms2.open(outfpath, 'w')
            outf.write(JJAS_data)
            outf.close()
            log.info('Extracted JJAS anomaly has written into file %s' % outfpath)
        # end of if fname.endswith('.nc'):
    # end of for fname in os.listdir(inpath):
# end of def extractJJAS(inpath, outpath, log):



if __name__ == '__main__':

    for climatology in climatologies:
        if not (climatology.dfile and climatolgy.name.lower() == 'miso'):
            print "In configure.txt climpartialdayfile \
                    not mentioned or its not miso. \
                    So can not compute daily anomaly."
            continue
        # end of if not climatology.dfile and obs.path and ...:
        for obs in observations:
            if not obs.name == 'GPCP':
                log.info('obs.name "%s" is not GPCP. So skip it' % obs.name)
                continue
            # end of if not obs.name == 'GPCP':
            
            dailyAnlAnomalyPath = os.path.join(processfilesPath,
               'Anomaly', 'Unfiltered', obs.name, climatology.name, 'Daily')

            jjasAnlAnomalyPath = os.path.join(processfilesPath,
               'Anomaly', 'Unfiltered', obs.name, climatology.name, 'JJAS')

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



