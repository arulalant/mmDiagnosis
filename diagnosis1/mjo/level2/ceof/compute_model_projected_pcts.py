import os
import sys
import time
import cdms2
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
diagDir = os.path.abspath(os.path.join(__curDir__, '../../..'))
# adding the previous diagnosisutils path to python path
sys.path.append(diagDir)
from diag_setup.globalconfig import models, climatologies, logpath, plotexcludehour
from diag_setup.logsetup import createLog
from ceof_diag import makeProjectedPcts

# create log object to written into logfile
logfile = __file__.split('.py')[0] + '.log'
log = createLog(__file__, os.path.join(logpath, logfile))


if __name__ == '__main__':

    # Creating the projected pcts nc files for the models anomaly and its
    # forecast hours datasets.
    # To reach that path, , we need to pass the suffixpath as
    # [modelName, ClimatologyName, Year, 'Daily'] in the kwarg.

    # get the current year
    year = time.localtime().tm_year
    log.info("It will try to compute projected pcts only to the current year %d. \
           If you need to loop through all the available years in the \
           models anomaly path means, insert your code here.", year)
    obs_years = (1979, 2005)

    # Right now we are not doing regrid the anomaly here.
    # We already done regrid the model data into 2.5x2.5 resoltution 
    # while doing anomaly itself.
    doregrid = False
    if doregrid:
        grid_file = 'olr.sample.2.5x2.5.grid.nc'
        grid_var = grid_file.split('.')[0]
        gf = cdms2.open(grid_file)
        # get the grid
        obs_grid = gf[grid_var].getGrid()
    else:
        obs_grid = None
    # end of if doregrid:
    for climatology in climatologies:
        for model in models:
            log.info("Compute Projected PCTS has started for the model '%s'", model.name)
            modelPathList = [model.name, climatology.name, str(year), 'Daily']
            makeProjectedPcts('Anomaly', 'Filtered',
                  suffixpath=modelPathList, year=obs_years,
                         seasons=['mjjas'], overwrite=True,
                         log=log, mname=model.name, exclude=plotexcludehour, ogrid=obs_grid)
            log.info("Compute Projected PCTS has finished for the model '%s'", model.name)
        # end of for model in models:
    # end of for climatology in climatologies:
    #gf.close()
# end of if __name__ == '__main__':



