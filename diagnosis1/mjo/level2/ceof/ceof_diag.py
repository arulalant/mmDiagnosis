import numpy
import cdms2
import cdutil
import pickle
import os, sys
from eof2 import MultipleEof
from regrid2 import Horizontal
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__levelDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__levelDir__, '../../..'))
# adding the previous path to python path
sys.path.append(previousDir)
from uv_cdat_code.diagnosisutils.timeutils import TimeUtility
from uv_cdat_code.diagnosisutils.xml_data_access import GribXmlAccess
from diag_setup.globalconfig import processfilesPath, logpath, plotceofanlsince
from diag_setup.varsdict import variables
from diag_setup.logsetup import createLog
import diag_setup.netcdf_settings


timeobj = TimeUtility()
xmlobj = GribXmlAccess('.')
_overWrite = True

# create log object to written into logfile
logfile = __file__.split('.py')[0] + '.log'
log = createLog(__file__, os.path.join(logpath, logfile))


def getZonalNormStd(data):
    """
    data - pass filtered data
    Return : normalized data and std of the meridionally averaged data.
        Once we averaged over latitude, then it will become zonal data.
    """
    # todo : correct the commented, docstr line for meridionally, zonally
    # meridionally averaged data (averaged over latitude axis)
    # weight='weighted' is default option that will generate the area weights
    meridional_avg = cdutil.averager(data, axis='y')(squeeze=1) #, weight='weighted')
    # make memory free
    del data
    # averaged over time axis
    time_avg = cdutil.averager(meridional_avg, axis='t', weight='equal')(squeeze=1)
    # get the std
    std_avg = numpy.sqrt(meridional_avg.asma().var())
    # get the normalize the data
    normal_data = (meridional_avg - time_avg) / std_avg
     # make memory free
    del meridional_avg, time_avg
    # return normal_data and std_avg data
    return normal_data, std_avg
# end of def getZonalNormStd(data):


def genCeofVars(infiles, outfile, eobjf=True, lat=(-15, 15, 'cob'),
                                     NEOF=4, season='all', **kwarg):
    """
    genCeofVars : generate the combined eof variables as listed below.

    Input :-

    infiles : List of tuples contains variable generic name, actual varible
              name (say model varName), data path. So ceof input files list
              contains the tuples which contains the above three information.

              For eg : ceof(olr, u200, u850)
              infiles = [('olr', 'olrv', 'olr.ctl'),
                         ('u200', 'u200v', 'u200.ctl'),
                         ('u850', 'u850v', 'u850.ctl')]

    outfile : output nc file path. All the supported output varibles of ceof
              will be stored in this nc file. This nc file will be opened in
              append mode.

    eobjf : eof obj file store. If True, the eofobj of ceof will be stored
            as binary ('*.pkl') file in the outfile path directory,
            using pickle module.

    lat : latitude to extract the data of the input file.
          By default it takes as (-15, 15, 'cob').

    NEOF : no of eof or no of mode. By default it takes 4.

    season : It could be 'all', 'sum', 'win'. Not a list.
         all : through out the year data from all the available years
         sum : only summer data will be extracted from all the available years
         win : only winter data will be extracted from all the available years

    Output : The follwing output varibles from 1 to 5 will be stored/append
             into outfile along with individual varName, season
             (where ever needed).
        1. Std of each zonal normalized varibles
        2. Percentage explained by ceof input variables
        3. variance accounted for ceof of each input variables
        4. eof variable of each input variables
        5. PC time series, Normalized PC time Series (for 'all' season only)
        6. Store the eofobj (into .pkl file) [optional]

    Written By : Dileep.K, Arulalan.T

    Date :

    Updated : 11.05.2013

    """

    eofobj_endname = kwarg.get('eofobj_endname', None)
    year = kwarg.get('year', None)
    vnames = []
    variableNames = []
    normals = []
    variances = []
    out = cdms2.open(outfile, 'a')

    for name, varName, infile in infiles:
        print "Collecting data %s for season %s" % (name, season)
        if season == 'all':
            f = cdms2.open(infile)
            if year:
                period = timeobj._getYearFirstLast(year)
                data = f(varName, time=period, latitude=lat)
            else:
                data = f(varName, latitude=lat)
            # end of if year:
            f.close()
        elif season == 'sum':
            data = timeobj.getSummerData(varName, infile, latitude=lat, **kwarg)
        elif season == 'win':
            data = timeobj.getWinterData(varName, infile, latitude=lat, **kwarg)
        else:
            raise ValueError("arg 'season' must be either 'all/sum/win' only")
        # end of if season == 'all':
        print "Calculating Zonal Normalized data & its Std, variance"
        # get the normalized data & std of meridionally averaged data
        normal, std = getZonalNormStd(data)
        # make memory free
        del data

        # append the normalize data into normals list
        normals.append(normal)
        # append the variance data into variances list
        variance = normal.asma().var()
        variances.append(variance)

        # set std meta data attributes
        std = cdms2.createVariable(std)
        std.id = '_'.join(['std', name, season])
        std.comments = ''
        out.write(std)

        # store the input variable generic name
        vnames.append(name)
        variableNames.append(name)
        # make memory free
        del normal, std, variance
    # end of for name, varName, infile in infiles:

    print "Calculating multiple eof"
    # get the eofobj by passing multiple normalized varibles of meridionally
    # averaged data. eg(norm_olr, norm_u200, norm_850)
    eofobj = MultipleEof(*normals, weights=None)

    if eobjf:
        variableNames.sort()
        # generate the eofobj binary file name and its path
        path = os.path.dirname(outfile)
        eofobj_filename = ['eofobj', 'level2', 'ceof'] + variableNames + [season]
        eofobj_filename = '_'.join(eofobj_filename)
        if eofobj_endname: eofobj_filename += '_' + eofobj_endname
        eofobj_filename += '.pkl'
        eofobj_fpath = os.path.join(path, eofobj_filename)
        # store the eofobj into binary file using pickle module
        objf = open(eofobj_fpath, 'wb')
        pickle.dump(eofobj, objf, 2)
        comment = ''
        pickle.dump(comment, objf, 2)
        objf.close()
        print "Saved the ceof object into file", eofobj_fpath
    # end of if eobjf:

    # generate the eof for each input variables
    eof_vars = eofobj.eofs(neofs=NEOF, eofscaling=2)

    for eof_var, name in zip(eof_vars, vnames):
        # set eof variable name with season and write into nc file
        eof_var.id = '_'.join(['eof', name, season])
        eof_var.comments = ''
        out.write(eof_var)
    # end of for eof_var in zip(eof_vars, vnames):

    # make memory free
    del eof_vars

    # Percentage explained by ceof input variables
    per_exp = eofobj.varianceFraction(neigs=NEOF) * 100
    per_exp.id = '_'.join(['per_exp', 'ceof', season])
    per_exp.comments = ''
    out.write(per_exp)

    # make memory free
    del per_exp

    # construct variable for no of input varibles and NEOF
    cvar = numpy.zeros((len(variances), NEOF))
    for i in range(NEOF):
        reCFileds = eofobj.reconstructedField(i + 1)
        j = 0
        for reCField, variance in zip(reCFileds, variances):
            cvar[j][i] = reCField.asma().var() / variance
            j += 1
        # end of for reCField, var in reCFileds, variances:
    # end of for i in range(NEOF):

    # variance axis start from 1 (mode=1,2,3, ... NEOF+1)
    vaxis = cdms2.createAxis(range(1, NEOF + 1), id='vaxis')
    for j in range(len(variances)):
        var_acc = (cvar[j].copy())
        var_acc[1:] = cvar[j][1:] - cvar[j][:-1]
        # variance accounted for ceof input variable
        var_acc = var_acc * 100
        # set variance accounted variable meta data attributes
        var_acc = cdms2.createVariable(var_acc)
        var_acc.id = '_'.join(['var_acc', vnames[j], season])
        var_acc.setAxis(0, vaxis)
        var_acc.comments = ''
        # write the variance accounted variable into nc file.
        out.write(var_acc)
        # make memory free
        del var_acc
    # end of for j in range(len(variances)):

    if season == 'all':
        # PC Time Series Computation For The Purpose Of
        # Computing Amplitude And Phases
        # Computating pcts only for the all season.

        # get the pcs of ceof input variables
        pcs = eofobj.pcs(pcscaling=0, npcs=NEOF)
        pctime = pcs.getTime()

        for i in range(NEOF):
            # extract the pcs 0, 1, 2, 3,...,NEOF-1.
            pcs_i = pcs[::, i]
            pcs_i.id = 'pcs' + str(i+1)
            pcs_i.comments = ''
            # do the normalized pcs 0, 1, 2, 3,...,NEOF-1.
            norm_pcs_i = (pcs_i - pcs_i.mean()) / numpy.sqrt(pcs_i.var())
            norm_pcs_i = cdms2.createVariable(norm_pcs_i)
            norm_pcs_i.id = 'norm_pcs' + str(i+1)
            norm_pcs_i.setAxis(0, pctime)
            norm_pcs_i.comments = ''
            # write the pcs, normalize pcs 0, 1, 2, 3,...,NEOF-1 into nc file.
            out.write(pcs_i)
            out.write(norm_pcs_i)
        # end of for i in range(NEOF):

        # make memory free
        del pcs
    # end of if season == 'all':
    out.close()
    # make memory free
    del eofobj
    print "Stored all the ceof variables into nc file", outfile
# end of def genCeofVars(infiles, outfile, ...):


def genProjectedPcts(infiles, outfile, eofobj, lat=(-15, 15, 'cob'),
                                      NEOF=4, season='mjjas', **kwarg):
    """

    KWargs:
        ogrid : if grid has passed then data will be regridded before
                normalize it w.r.t passed grid resoltution. By default it
                takes None.

        dtype : dtype should be either 'anl', or fcst hours.
                if both season and dtype has passed then, according to dtype
                season time will be calculated using xmlobj.findPartners()
                method. By default it takes 'Analysis'.
                i.e. period from 01-05-yyyy to 30-9-yyyy for the 'mjjas' season.
                If dtype will be '24' means then period will be from 30-04-yyyy
                to 29-09-yyyy. Likewise user can pass fcst hour.

    Date : 08.08.2013
    """

    year = kwarg.get('year', None)
    ogrid = kwarg.get('ogrid', None)
    dtype = kwarg.get('dtype', 'Analysis')
    vnames = []
    normals = []
    regridfn = None

    for name, varName, infile in infiles:
        print "Collecting data %s for season %s" % (name, season)
        if season == 'all':
            f = cdms2.open(infile)
            if year:
                period = timeobj._getYearFirstLast(year)
                data = f(varName, time=period, latitude=lat)
            else:
                data = f(varName, latitude=lat)
            # end of if year:
            f.close()
        elif season == 'sum':
            data = timeobj.getSummerData(varName, infile, latitude=lat, **kwarg)
        elif season == 'win':
            data = timeobj.getWinterData(varName, infile, latitude=lat, **kwarg)
        elif season.upper() == 'MJJAS':
            # get the latest comptime of analysis data.
            f = cdms2.open(infile)
            anlLatestDate = f[varName].getTime().asComponentTime()[-1]
            if dtype in ['anl', 'Analysis']:       
#                if plotceofanlsince:
#                    sday = int(plotceofanlsince[4:6])
#                    smon = int(plotceofanlsince[6:8])
#                else:
                sday = 1
                smon = 5
                # end of if plotceofanlsince:
                #               eday = 30
                #               emon = 9
                eday = anlLatestDate.day
                emon = anlLatestDate.month
            elif dtype in ['Merged']:    
                # get the start & end date of merged   
                anlStartDate = f[varName].getTime().asComponentTime()[0]
                sday = anlStartDate.day
                smon = anlStartDate.month
                eday = anlLatestDate.day
                emon = anlLatestDate.month
            elif dtype.isdigit():
                # find fcst hour partner data w.r.t analysis date as 0001-05-01
                # as start of the season
                #                    #'0001-05-01'
                pStartDate = xmlobj.findPartners('a', plotceofanlsince, int(dtype))
                sday = pStartDate.day
                smon = pStartDate.month
                # find fcst hour partner data w.r.t analysis date as 0001-09-30
                # as end of the season
                #                    #'0001-09-30'
                # Use the analysis latest date to get its partner's latest date.
                pEndDate = xmlobj.findPartners('a', anlLatestDate, int(dtype))
                eday = pEndDate.day
                emon = pEndDate.month      
            else:
                pass
            # extract seasonal data
            data = timeobj.getSeasonalData(varName, infile, sday, smon,
                                     eday, emon, latitude=lat, **kwarg)
        else:
            raise ValueError("arg 'season' must be either 'all/sum/win' only")
        # end of if season == 'all':
        log.info("Calculating Zonal Normalized data & its Std, variance")

        if ogrid and regridfn is None:
            regridfn = Horizontal(data.getGrid(), ogrid)
        # end of if ogrid and regridfn is None:
        log.info("Doing Regridding the model data w.r.t observation grid")
        if ogrid:
            # do regrid the data w.r.t observed resoltution to project over it.
            data = regridfn(data)
        # get the normalized data & std of meridionally averaged data
        normal, std = getZonalNormStd(data)
        # make memory free
        del data
        # append the normalize data into normals list
        normals.append(normal)
        # store the input variable generic name
        vnames.append(name)
        # make memory free
        del normal, std
    # end of for name, varName, infile in infiles:
    log.info("applying projected fileds")
    proj_field = eofobj.projectField(*normals, neofs=NEOF)(squeeze=1)
    # make memory free
    del normals

    out = cdms2.open(outfile, 'w')
    pctime = proj_field.getTime()
    for i in range(NEOF):
        # extract the pcs 0, 1, 2, 3,...,NEOF-1.
        pcs_i = proj_field[::, i]
        pcs_i.id = 'pcs' + str(i+1)
        pcs_i.long_name = 'projected pc time series'
        pcs_i.comments = '' #'NCMRWF T254 model pseudo projected ceof%s pcts. The first projected pcts is given by proj_pcts1=proj_field[::, 0]' % str(tuple(vnames))
        # do the normalized pcs 0, 1, 2, 3,...,NEOF-1.
        norm_pcs_i = (pcs_i - pcs_i.mean()) / numpy.sqrt(pcs_i.var())
        norm_pcs_i = cdms2.createVariable(norm_pcs_i)
        norm_pcs_i.id = 'norm_pcs' + str(i+1)
        norm_pcs_i.setAxis(0, pctime)
        norm_pcs_i.long_name = 'projected normalized pc time series'
        norm_pcs_i.comments = '' #'NCMRWF T254 model pseudo projected ceof%s Normalized pcts. The first normalized projected pcts is given by nomproj_pcts1=normalized_proj_field[::, 0]' % str(tuple(vnames))
        # write the pcs, normalize pcs 0, 1, 2, 3,...,NEOF-1 into nc file.
        out.write(pcs_i)
        out.write(norm_pcs_i)
    # end of for i in range(NEOF):
    # make memory free
    del proj_field

    out.close()
    log.info("Project pcts has written into nc file %s", outfile)
# end of def genProjectedPcts(eofobj, *data, **kwarg):


def makeGenCeofVars(rawOrAnomaly='Anomaly', filteredOrNot='Filtered',
                            seasons=['all', 'sum', 'win'], **kwarg):
    """
    Written By : Arulalan.T

    Date : 22.07.2013

    """

    year = kwarg.get('year', None)
    if not year:
        raise ValueError("You must pass year to find the path of directory structure")
    if isinstance(year, int):
        yearDir = str(year)
    elif isinstance(year, tuple):
        yearDir = str(year[0]) + '_' + str(year[1])

    seasondic = {'sum': 'Summer', 'win': 'Winter', 'all': 'All'}
    # CAUTION : This is the correct order of variables to do ceof.
    # If order has changed, then it produces with multiplied by -1 in eofs
    # and pcs1. ('olr', 'u200', 'u850') is the correct order to do MJO works.
    # If 'precipitation' has passed instead of 'olr', then just replace the
    # olr position. Add that code here.
    correctOrderVars = ['olr', 'u200', 'u850']
    inpath = os.path.join(processfilesPath, rawOrAnomaly, filteredOrNot)
    opath = os.path.join(processfilesPath, 'Level2', 'Ceof', rawOrAnomaly,
                                         filteredOrNot, yearDir)
    for subName in os.listdir(inpath):
        anopath = os.path.join(inpath, subName)
        anofiles = [anofile for anofile in os.listdir(anopath)
                             if not anofile.endswith('5x5.nc')]
        file_input = [None] * len(anofiles)
        for afile in anofiles:
            varName = afile.split('_')[0]
            apath = os.path.join(anopath, afile)
            if varName in correctOrderVars:
                idx = correctOrderVars.index(varName)
            else:
                idx = anofiles.index(afile)
            # end of if varName in correctOrderVars:
            file_input[idx] = (varName, varName, apath)
        # end of for afile in anofiles:

        ceofobj_fileendname = '%s_%s_%s_%s' % (yearDir, rawOrAnomaly,
                                             filteredOrNot, subName)
        for sea in seasons:
            seasonName = seasondic.get(sea, 'season')
            outpath = os.path.join(opath, subName, seasonName)
            if not os.path.isdir(outpath):
                os.makedirs(outpath)
                print "The path has created ", outpath
            # end of if not os.path.isdir(outpath):
            print "Doing Combined Eof For", seasonName, yearDir
            # creating individual nc files for each season, since
            # we cant overwrite the timeaxis in same nc file.
            outfile = 'ceof_vars_%s_%s_%s_%s_%s.nc' % (seasonName,
                   yearDir, rawOrAnomaly, filteredOrNot, subName)
            file_output = os.path.join(outpath, outfile)
            genCeofVars(file_input, file_output, season=sea,
                  eofobj_endname=ceofobj_fileendname, **kwarg)
        # end of for sea in seasons:
    # end of for subName in os.listdir(inpath):
# end of def makeGenCeofVars(rawOrAnomaly='Anomaly', ...):

def makeProjectedPcts(rawOrAnomaly='Anomaly', filteredOrNot='Filtered',
                            seasons=['mjjas'], obsname='MJO', **kwarg):
    """
    
    KWarg:
        exclude : exclude hours. If some hours list has passed then those 
              model hours will be omitted. eg : 01 hour.
              Note : it will omit those exclude model hours directory.
              So for the remaining model anl, fcst hours only calculated the
              projected pcts.
              
    Written By : Arulalan.T

    Date : 08.08.2013

    """

    year = kwarg.get('year', None)
    mname = kwarg.get('mname', None)
    exclude = kwarg.get('exclude', [])
    if not year:
        raise ValueError("You must pass year to find the path of directory structure")
    if isinstance(year, int):
        yearDir = str(year)
    elif isinstance(year, tuple):
        yearDir = str(year[0]) + '_' + str(year[1])

    seasondic = {'sum': 'Summer', 'win': 'Winter', 'all': 'All', 'mjjas': 'MJJAS'}
    # CAUTION : This is the correct order of variables to do ceof.
    # If order has changed, then it produces with multiplied by -1 in eofs
    # and pcs1. ('olr', 'u200', 'u850') is the correct order to do MJO works.
    # If 'precipitation' has passed instead of 'olr', then just replace the
    # olr position. Add that code here.
    correctOrderVars = ['olr', 'u200', 'u850']
    eofobjfilepath = kwarg.get('eofobjfpath', None)
    suffixPath = kwarg.get('suffixpath', None)
    overwrite = kwarg.get('overwrite', False)
    arglog = kwarg.get('log', None)
    if arglog is not None:
        log = arglog
    # end of if arglog is not None:
    if overwrite: _overWrite = True
    inpath = os.path.join(processfilesPath, rawOrAnomaly, filteredOrNot)
    if suffixPath:
        if isinstance(suffixPath, list):
            suffixPath = '/'.join(suffixPath)
        inpath = os.path.join(inpath, suffixPath)
        if not os.path.isdir(inpath):
            log.error("The path doesnot exists '%s'", inpath)
            raise ValueError("The path doesnot exists '%s'" % inpath)
    # end of if suffixPath:

    if not eofobjfilepath:
        eofobjpath = os.path.join(processfilesPath, 'Level2', 'Ceof',
                         rawOrAnomaly, filteredOrNot, yearDir, obsname, 'All')
        pklfiles = [fname for fname in os.listdir(eofobjpath)
                                    if fname.endswith('.pkl')]
        if len(pklfiles) == 1:
             eoffilename = pklfiles[0]
        elif len(pklfiles) > 1:
            print "Found more *.pkl files in ", eofobjpath
            print "So trying with default pickle one"
            eoffilename = 'eofobj_level2_ceof_olr_u200_u850_all_1979_2005_Anomaly_Filtered_MJO.pkl'
        # end of if len(pklfiles) == 1:
        eofobjfilepath = os.path.join(eofobjpath, eoffilename)
    # end of if not eofobjfilepath:

    objf = open(eofobjfilepath, 'rb')
    eofobj = pickle.load(objf)
    objf.close()
    log.info("eofobj is loaded from '%s' binary file", eofobjfilepath)
    totvar = variables.get(mname)
    
    fcstdirs = os.listdir(inpath)
    # remove the unwanted directories to be used to do projected pcts
    for ex in exclude:
        if ex in fcstdirs:
            print "Omitted directory '%s' without doing projected pcts", ex
            fcstdirs.remove(ex)
        # end of if ex in fcstdirs:
    # end of for ex in exclude:
    # sort the directories of fcst hours in string
    fcstdirs = timeobj._sortFcstHours(fcstdirs)
    for anl_fcst in fcstdirs:
        anopath = os.path.join(inpath, anl_fcst)
        anofiles = [anofile for anofile in os.listdir(anopath)
                     if anofile.endswith('.nc')
                     if not (anofile.endswith('5x5.nc') or
                     anofile.startswith(('projected_pcts', 'amppha')))]

        file_input = []
        # get the anomaly files in correctOrderVars list.
        # model dataset should be same order of observation dataset order
        # to compute projected pcts. Otherwise it will produce wrong result
        for name in correctOrderVars:
            mvar = totvar.get(name).model_var
            mlev = totvar.get(name).model_level
            for afile in anofiles:
                afile_list = afile.split('_')
                varName = afile_list[0]
                if varName != mvar:
                    continue
                # end of if varName != mvar:
                if mlev:
                    if str(int(mlev)) != afile_list[1]:
                        continue
                # end of if mlev:
                apath = os.path.join(anopath, afile)
                file_input.append((name, varName, apath))
            # end of  for afile in anofiles:
        # end of for name in correctOrderVars:

        if len(correctOrderVars) != len(anofiles):
            for afile in anofiles:
                file_input.append((varName, varName, apath))
            # end of for afile in anofiles:
        # end of if len(correctOrderVars) != len(anofiles):

        for sea in seasons:
            seasonName = seasondic.get(sea, 'season')
            # creating individual nc files for each season, since
            # we cant overwrite the timeaxis in same nc file.
            outfile = 'projected_pcts_%s_%s_%s_%s.nc' % (seasonName,
                               rawOrAnomaly, filteredOrNot, anl_fcst)
            file_output = os.path.join(anopath, outfile)
            if os.path.isfile(file_output) and not _overWrite:
                log.warning("The file %s is exist already. \
                       So skipping projected pcts to this", file_output)
                continue
            # end of if os.path.isfile(file_output) ...:
            log.info("Calculating projected pcts for the %s for %s", anopath, anl_fcst)
            print "Calculating projected pcts for the %s for %s" % (anopath, anl_fcst)
            ### Note here we overwrite the year
            kwarg['year'] = None
            genProjectedPcts(file_input, file_output, eofobj, season=sea, dtype=anl_fcst, **kwarg)
        # end of for sea in seasons:
    # end of for anl_fcst in fcstdirs:
# end of def makeProjectedPcts(rawOrAnomaly='Anomaly', ...):


if __name__ == '__main__':

    year = (1979, 2005)
    makeGenCeofVars('Anomaly', 'Filtered',  year=year)

    year = 2005
    makeGenCeofVars('Anomaly', 'Filtered',  year=year, cyclic=True)

# end of if __name__ == '__main__':

