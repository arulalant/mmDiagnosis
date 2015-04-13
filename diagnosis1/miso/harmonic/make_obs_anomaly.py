import os
import sys
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
diagDir = os.path.abspath(os.path.join(__curDir__, '../../'))
# adding the previous diagnosisutils path to python path
sys.path.append(diagDir)
from diagnosis.compute_daily_anomaly import genDailyAnomalyFiles
from diag_setup.globalconfig import observations, climatologies, processfilesPath
import diag_setup.netcdf_settings


if __name__ == '__main__':

    for obs in observations:
        if not obs.name == 'GPCP':
            log.info('obs.name "%s" is not GPCP. So skip it' % obs.name)
            continue
        # end of if not obs.name == 'GPCP':
        for climatology in climatologies:
            if climatology.dfile and obs.path and climatolgy.name.lower() == 'miso':
                # daily climatolgy path
                climatologyPath = os.path.join(climatology.path, 'Daily')
                # anomaly path will be created
                dailyAnlAnomalyPath = os.path.join(processfilesPath,
                      'Anomaly', 'Unfiltered', climatology.name, 'Daily')

                if not os.path.isdir(dailyAnlAnomalyPath):
                    os.makedirs(dailyAnlAnomalyPath)
                    print "Path has created ", dailyAnlAnomalyPath
                # end of if not os.path.isdir(dailyAnlAnomalyPath):
                # calling below fn to create daily anomaly for observations
                Type = 'o'  # obs type
                # make harmonic climatolgy file name 
                cdfile = climatology.dfile.split('.')
                cdfile = '.'.join(cdfile.insert(-1, 'harmonic'))
                genDailyAnomalyFiles(dailyAnlAnomalyPath, Type, None, obs.year,
                    climatologyPath, cdfile, climatology.year,
                    modelName=obs.name, modelXmlPath=obs.path)

            else:
                print "In configure.txt obs xmlPath and climpartialdayfile \
                        not mentioned or its not miso. So can not compute daily anomaly."
            # end of if climatology.dfile and obs.filename:
        # end of for climatology in climatologies:
    # end of for obs in observations:
    print "Done! Creation of Daily Anomaly netCdf Files"
# end of if __name__ == '__main__':



