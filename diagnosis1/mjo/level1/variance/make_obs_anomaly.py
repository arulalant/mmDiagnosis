import os
import sys
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
diagDir = os.path.abspath(os.path.join(__curDir__, '../../..'))
# adding the previous diagnosisutils path to python path
sys.path.append(diagDir)
from diagnosis.compute_daily_anomaly import genDailyAnomalyFiles
from diag_setup.globalconfig import observations, climatologies, processfilesPath
import diag_setup.netcdf_settings


if __name__ == '__main__':

    for obs in observations:
        for climatology in climatologies:
            if climatology.dfile and obs.path:
                # daily climatolgy path
                climatologyPath = os.path.join(climatology.path, 'Daily')
                # anomaly path will be created
                dailyAnlAnomalyPath = os.path.join(processfilesPath,
                      'Anomaly', 'Unfiltered', climatology.name)

                if not os.path.isdir(dailyAnlAnomalyPath):
                    os.makedirs(dailyAnlAnomalyPath)
                    print "Path has created ", dailyAnlAnomalyPath
                # end of if not os.path.isdir(dailyAnlAnomalyPath):
                # calling below fn to create daily anomaly for observations
                Type = 'o'  # obs type
                genDailyAnomalyFiles(dailyAnlAnomalyPath, Type, None, obs.year,
                    climatologyPath, climatology.dfile, climatology.year,
                    modelName=obs.name, modelXmlPath=obs.path)

            else:
                print "In configure.txt obs xmlPath and climpartialdayfile \
                        not mentioned. So can not compute daily anomaly."
            # end of if climatology.dfile and obs.filename:
        # end of for climatology in climatologies:
    # end of for obs in observations:
    print "Done! Creation of Daily Anomaly netCdf Files"
# end of if __name__ == '__main__':



