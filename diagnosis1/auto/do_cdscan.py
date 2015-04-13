import os
import sys
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__diagnosisDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__diagnosisDir__, '..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diag_setup.globalconfig import uvcdat, models, logpath
from diag_setup.logsetup import createLog
from cdscan_update import updateCdmlFile

# create log object to written into logfile
logfile = __file__.split('.py')[0] + '.log'
log = createLog(__file__, os.path.join(logpath, logfile))


def doCdscan(xmlpath, inpath, extension='nc',
           parameters=['anl', '24', '48', '72', '96', '120', '144', '168'],
                                                                  **kwarg):

    """

    Written By : Arulalan.T

    Date : 19.08.2013

    """

    cdscan = kwarg.get('cdscan', None)
    if not cdscan:
        raise ValueError("cdscan keyword arg is must")
    # end of if not cdscan:
    # get the relative path of the inpath w.r.t xmlpath
    relativeInpath = os.path.relpath(inpath, xmlpath)
    curpath = os.getcwd()
    # change the working directory into xmlpath
    os.chdir(xmlpath)

    for hr in parameters:
        if hr.isalpha():
            name = ['all', hr, extension]
        elif hr.isdigit():
            name = ['all', 'fcst', hr + 'hr', extension]
        outxml = '_'.join(name) + '.xml'
        xmlfilepath = os.path.join(xmlpath, outxml)
        # relative file specfication
        infile = '*' + hr + '.' + extension
        # still its relative path only.
        infilepath = '/'. join([relativeInpath, infile])
        # cdscan command
        cmd = ' '.join([cdscan, '-x', outxml, '-q', infilepath])

        if os.path.exists(xmlfilepath):
            # remove the existing xml file.
            log.info("%s has removed before doing cdscan", xmlfilepath)
            os.remove(xmlfilepath)
        # end of if os.path.exists(xmlfilepath):

        # execute cmd. Use Popen, so we can get the error as string...
        os.system(cmd)

        if os.path.exists(xmlfilepath):
            log.info("%s has created successfully by cdscan", xmlfilepath)
        else:
            log.info("Got Problem : Couldn't create %s by cdscan", xmlfilepath)
        # end of if os.path.exists(xmlfilepath):
    # end of for hr in parameters:

    # back to previous working directory
    os.chdir(curpath)
# end of def doCdscan(...):


def updateCdscanXmlFiles(date, xmlpath, dpath, extension='nc',
           dprefix='gdas.', fprefix='gdas1.t00z.grb', fprefix01='gdas1.t00z.sfluxgrbf',
           parameters=['anl', '24', '48', '72', '96', '120', '144', '168']):

    """

    Written By : Arulalan.T

    Date : 09.10.2013

    """

    date_dir = os.path.join(dpath, dprefix + date)
    # get the relative path of the inpath(date_dir) w.r.t xmlpath
    relativeInpath = os.path.relpath(date_dir, xmlpath)
    curpath = os.getcwd()
    # change the working directory into xmlpath
    os.chdir(xmlpath)

    for hr in parameters:        
        if hr.isalpha():
            # anl xml partial name
            name = ['all', hr, extension]   
            fprefix_file = fprefix         
        elif hr.isalnum():
            # fcst xml partial name
            name = ['all', 'fcst', hr + 'hr', extension]
            if hr.endswith(('01')):
                fprefix_file = fprefix01
            else:
                fprefix_file = fprefix + 'f'           
            # end of if hr.endswith(('01')):
        # end of if hr.isalpha():
        outxml = '_'.join(name) + '.xml'

        xmlfilepath = os.path.join(xmlpath, outxml)
        # relative file specfication
        infile = fprefix_file + hr + '.' + extension
        # still its relative path only.
        infilepath = '/'. join([relativeInpath, infile])

        if os.path.exists(xmlfilepath):
            updateCdmlFile(infilepath, outxml)  #xmlfilepath  check this ..
        else:
            # remove the existing xml file.
            log.info("%s doesnot exist. So can not update the xml file", xmlfilepath)
            os.remove(xmlfilepath)
        # end of if os.path.exists(xmlfilepath):

        if os.path.exists(xmlfilepath):
            log.info("%s has created successfully by cdscanUpdate", xmlfilepath)
        else:
            log.info("Got Problem : Couldn't create %s by cdscanUpdate", xmlfilepath)
        # end of if os.path.exists(xmlfilepath):
    # end of for hr in parameters:

    # back to previous working directory
    os.chdir(curpath)
# end of def updateCdscanXmlFiles(...):


if __name__ == '__main__':

    if uvcdat.endswith(('python', 'cdat', 'vcdat', 'uvcdat')):
        uvcdat_bin_list = uvcdat.split('/')[:-1]
        uvcdat_bin = os.path.join('/', *uvcdat_bin_list)
    else:
        # uvcdat.endswith('bin')
        uvcdat_bin = uvcdat
    cdscan = os.path.join(uvcdat_bin, 'cdscan')

    for model in models:
        anl_fcst = ['anl'] + model.hour
        doCdscan(xmlpath=model.path, inpath=model.dpath,
            extension=model.extension, parameters=anl_fcst, cdscan=cdscan)
    # end of for model in models:

# end of if __name__ == '__main__':




