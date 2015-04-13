"""
This do_model_lfilter.py script will create filtered data for the available
variables for all the models of analysis and all forecast hours datasets.
"""
import os
import sys
import time
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
diagDir = os.path.abspath(os.path.join(__curDir__, '../../..'))
# adding the previous diagnosisutils path to python path
sys.path.append(diagDir)
from diag_setup.globalconfig import models, climatologies, logpath
from diag_setup.logsetup import createLog
from do_obs_lfilter import applyLanczosFilter

# create log object to written into logfile
logfile = __file__.split('.py')[0] + '.log'
log = createLog(__file__, os.path.join(logpath, logfile))

if __name__ == '__main__':

    # applying the lancoz filter to the models anomaly datasets.
    # for the models anomaly, we need to pass the suffixpath as
    # [modelName, ClimatologyName, Year, 'Daily'] in the kwarg.

    # get the current year
    year = time.localtime().tm_year
    log.info("It will try to apply lfilter only to the current year %d. \
           If you need to loop through all the available years in the \
           models anomaly path means, insert your code here.", year)

    for climatology in climatologies:
        for model in models:
            log.info("The Lanczos Filter has started for the model '%s'", model.name)
            modelPathList = [model.name, climatology.name, str(year), 'Daily']
            applyLanczosFilter('Anomaly', 'Unfiltered',
                    suffixpath=modelPathList, overwrite=True, log=log)
            log.info("The Lanczos Filter has finished for the model '%s'", model.name)
        # end of for model in models:
    # end of for climatology in climatologies:
# end of if __name__ == '__main__':



