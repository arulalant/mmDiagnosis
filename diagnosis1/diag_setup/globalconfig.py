"""
.. module:: modeldata_climatologydata_filespath
   :synopsis: Using this module we can read the
          'modeldata_climatologydata_filespath.txt' file and get the
           information of model names, model paths, climatolgy names,
           climatolgy paths, processfilesPath and plotsgraphsPath as
           variables and objects.

   :usage: Using this script, we can access all the paths and names as
           namedtuples and variables by importing this module into another
           module.

   :condition: User must set the 'modeldata_climatologydata_filespath.txt'
           in the 'setup' directory. The paths must be exists which are all
           set inside the text file. The (modelname, modelxml) and
           (climatologyname, climatologyoriginal, climatologyregrid)
           must be in same order and it must endswith the number.

.. moduleauthor:: Arulalan.T <arulalant@gmail.com>

   Date : 18.08.2011

"""
import os
import re
from collections import namedtuple


# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__setupDir__ = os.path.dirname(__file__)

# uvcdat installed absolute path
uvcdat = ''
logpath = ''
archivepath = ''
ftppath = ''
plotceofanlsince = None
plotceoftinterval = 10
plotexcludehour = []
# initiazing the namedtuples for model and climatology...
# need to change this namedtuple path as xpath or xmlpath here only.
# Inside the scripts has updated already
model = namedtuple('model', 'count name dpath path hour extension')
climatology = namedtuple('climatology', 'count name year path dfile mfile')
obsrain = namedtuple('obsrain', 'count name path xml regrid')
obsvar = namedtuple('obsvar', 'count name path year')
# initiazing an empty arrays for models and climatologies contains many
# model and climatology namedtuples ...
models = []
climatologies = []
obsrainfalls = []
observations = []
# initiazing local vars
modelnamecount = None
climatologynamecount = None
rainfallXmlName = None
obsRain = obsrain(None, None, None, None, 'no')
obsVar = obsvar(None, None, None, None)
# initiazing the seasons dictionary var
seasons = {}
if __setupDir__ == '':
    __setupDir__ = '.'

fpathdir = os.path.join(__setupDir__,  'configure.txt')
fileobj = open(fpathdir, 'r')
for line in fileobj.readlines():
    if line.startswith('#'):
        # comment line in the text file. skip this line
        continue
    if line.find('#') != -1:
        # comment inline. removing commented parts inline
        line = line.split('#')[0]
    # removing whitespace fully
    line = re.sub(r'\s', '', line)
    line = line.strip().split('=')
    var = line[0].lower()
    # collecting needed name
    if var.startswith('modelname'):
        modelname = line[1]
        modelnamecount = line[0][-1]
        if not modelnamecount.isdigit():
            raise ValueError("modelname '%s' must endswith the number" % line[0])

    # collecting needed hour
    if var.startswith('modelhour'):
        modelhour = line[1].split(',')
        modelhour = [hr for hr in modelhour if hr != '']
        modelhourcount = line[0][-1]
        if not modelhourcount.isdigit():
            raise ValueError("modelhour '%s' must endswith the number" % line[0])

    # collecting model original data path
    if var.startswith('modeldatapath'):
        modeldatapath = line[1]
        modeldatapathcount = line[0][-1]
        if not modeldatapathcount.isdigit():
            raise ValueError("modeldatapath '%s' must endswith the number" % line[0])

    # collecting model file extension
    if var.startswith('modelfileext'):
        modeldatafile_ext = line[1]
        modelextcount = line[0][-1]
        if not modelextcount.isdigit():
            raise ValueError("modelfileext '%s' must endswith the number" % line[0])

    # collecting needed path
    if var.startswith('modelxmlpath'):
        modelxmlpath = line[1]
        modelxmlcount = line[0][-1]
        if not modelxmlcount.isdigit():
            raise ValueError("modelxml '%s' must endswith the number" % line[0])
        if modelnamecount == modelxmlcount == modelhourcount == modeldatapathcount == modelextcount:
            # storing the count, modelname, modeldatapath, modelxmlpath, modelhour in to the model namedtuple
            modeltemp = model(modelnamecount, modelname, modeldatapath,
                               modelxmlpath, modelhour, modeldatafile_ext)
            # storing the updated modeltemp variable into list
            models.append(modeltemp)
            # removing the modeltemp from memory
            del modeltemp
        else:
            raise ValueError('In path text file modelname, modelpath must \
                                be in order with suffix of the model number')
        if modeldatapath.endswith('*'):
            model_data_path = modeldatapath[:-1]
        else:
            model_data_path = modeldatapath
        if not os.path.exists(model_data_path):
            raise ValueError('The model%s data path %s does not exists'
                                % (modelnamecount, model_data_path))
        if not os.path.exists(modelxmlpath):
            raise ValueError('The model%s path %s does not exists'
                                        % (modelnamecount, modelxmlpath))

    elif var.startswith('climatologyname'):
        climatologyname = line[1]
        climatologynamecount = line[0][-1]
        if not climatologynamecount.isdigit():
            raise ValueError("climatologyname '%s' must endswith the number" % line[0])

    elif var.startswith('climatologyyear'):
        climatologyyear = int(line[1])
        climatologyyearcount = line[0][-1]
        if not climatologyyearcount.isdigit():
            raise ValueError("climatologyname '%s' must endswith the number" % line[0])

    elif var.startswith('climatologypath'):
        climatologypath = line[1]
        climatologypathcount = line[0][-1]
        if not climatologypathcount.isdigit():
            raise ValueError("climatologypath '%s' must endswith the number" % line[0])
        if not os.path.exists(climatologypath):
            raise ValueError('The climatology path does not exists %s'
                                 % climatologypath)

    elif var.startswith('climpartialdayfile'):
        climpartialdayfile = line[1]
        if climpartialdayfile in ['', 'None']:
            climpartialdayfile = None
        climpartialdayfilecount = line[0][-1]
        if not climpartialdayfilecount.isdigit():
            raise ValueError("climpartialdayfile '%s' must endswith the number" % line[0])

    elif var.startswith('climpartialmonfile'):
        climpartialmonfile = line[1]
        if climpartialmonfile in ['', 'None']:
            climpartialmonfile = None
        climpartialmonfilecount = line[0][-1]
        if not climpartialmonfilecount.isdigit():
            raise ValueError("climpartialmonfile '%s' must endswith the number" % line[0])
        if climatologynamecount == climatologypathcount == climatologyyearcount == climpartialdayfilecount == climpartialmonfilecount:
            # storing the count, climatologyname, climatologyyear, path, climpartialfile into the climatology namedtuple
            climtemp = climatology(climatologynamecount, climatologyname,
                                   climatologyyear, climatologypath,
                                   climpartialdayfile, climpartialmonfile)
            # storing the updated climtemp variable into the list
            climatologies.append(climtemp)
            # removing the climtemp from memory
            del climtemp
        else:
            raise ValueError('In path text file climatologyname, \
                   climatologyyear, climatologypath and climpartialfile must \
                   be in order with suffix of the model number')

    elif var.startswith('processfiles'):
        processfilesPath = line[1]
        if not os.path.exists(processfilesPath):
            raise ValueError('The process files path does not exists %s'
                                 % processfilesPath)

    elif var.startswith('plotsgraphs'):
        plotsgraphsPath = line[1]
        if not os.path.exists(processfilesPath):
            raise ValueError('The plots graphs path does not exists %s'
                                 % processfilesPath)

    elif var.startswith('plotlevel'):
        plotLevel = line[1].split(',')
        if not plotLevel:
            raise ValueError('The plotlevel values cant be an empty')
        if plotLevel[0] == 'all':
            plotLevel = 'all'
        else:
            plotLevel = [lev for lev in plotLevel if lev!= '']    
    
    elif var.startswith('plotexcludehour'):
        hours = line[1].split(',')
        plotexcludehour = [hr for hr in hours if hr != '']        

    elif var.startswith('climpartialfilename') or var.startswith('climatolgypartialfilename'):
        climPartialFileName = line[1]

    elif var.startswith('season') or var.endswith('season'):
        if var.startswith('season_'):
            seasonName = var.split('season_')[1]
        elif var.endswith('_season'):
            seasonName = var.split('_season')[0]
        else:
            raise ValueError("season %s is not startswith 'season_'or endswith '_season' " % var)
        # get the season's months and convert everything into lower
        monthlist = [month.lower() for month in line[1].split(',')]
        # store inside dictionary as list
        seasons[seasonName] = monthlist

    #### added obsvar
    elif var.startswith('obsname'):
        obsname = line[1]
        obsnamecount = line[0][-1]
        if not obsnamecount.isdigit():
            raise ValueError("obsname '%s' must endswith the number" % line[0])

    elif var.startswith('obsxml'):
        # get the observed xml path
        obsPath = line[1]
        obsxmlcount = line[0][-1]
        if not os.path.exists(obsPath):
            raise ValueError('The observation xml path does not\
                                exists %s' % obsPath)
        if not obsxmlcount.isdigit():
            raise ValueError("obsxml '%s' must endswith the number" % line[0])

    elif var.startswith('obsyear'):
        # get the observed xml path
        obsYear = line[1]
        obsyearcount = line[0][-1]
        if not obsyearcount.isdigit():
            raise ValueError("obsyear '%s' must endswith the number" % line[0])

        if obsnamecount == obsxmlcount == obsyearcount:
            # update the count, name, path, year into the obsVar namedtuple
            obstemp = obsVar._replace(count=obsnamecount,
                            name=obsname, path=obsPath, year=obsYear)
            # storing the updated obstemp variable into the list
            observations.append(obstemp)
            # removing the obsvartemp from memory
            del obstemp
        else:
            raise ValueError('In path text file obsname, \
                             obsxml and obsyear must \
                             be in order with suffix of the obs number')
    #### end of added obsvar

    elif var.startswith('obsrainname'):
        rainfallname = line[1]
        rainfallnamecount = line[0][-1]
        if not rainfallnamecount.isdigit():
            raise ValueError("obsrainname '%s' must endswith the number" % line[0])
        # make the copy of path count into xml count
        rainfallxmlcount = line[0][-1]
        # set the xml as None, it will help to update obsRain even user not passed obsrainfallxml
        rainfallXmlName = None

    elif var.startswith('obsrainpath'):
        # get the observed rainfall orginal path
        rainfallPath = line[1]
        rainfallpathcount = line[0][-1]
        if not os.path.exists(rainfallPath):
            raise ValueError('The observation rainfall path does not\
                                exists %s' % rainfallPath)
        if not rainfallpathcount.isdigit():
            raise ValueError("obsrainfallpath '%s' must endswith the number" % line[0])

    elif var.startswith('obsrainxml'):
        # set the rainfallXmlName to create this xml while regrid or use it
        # if not doing regrid to generate the xml filepath.
        rainfallXmlName = line[1]
        rainfallxmlcount = line[0][-1]
        if not rainfallxmlcount.isdigit():
            raise ValueError("obsrainfallxml '%s' must endswith the number" % line[0])

    elif var.startswith('obsrainregrid'):
        # get the observed rainfall regridded path to regrid & other future purposes
        rainfallRegrid = line[1].lower()
        rainfallregridcount = line[0][-1]
        if not rainfallRegrid in ['yes', 'no']:
            raise ValueError('The observation rainfall regrid must be either \
                               yes or no only %s' % rainfallRegrid)
        if not rainfallregridcount.isdigit():
            raise ValueError("obsrainfallregrid '%s' must endswith the number" % line[0])

        if rainfallnamecount == rainfallpathcount == rainfallxmlcount == rainfallregridcount:
            # update the count, rainfallpath, rainfallxml, path, rainfallregrid into the obsRain namedtuple
            obsraintemp = obsRain._replace(count = rainfallnamecount,
                            name = rainfallname, path = rainfallPath,
                            xml = rainfallXmlName, regrid = rainfallRegrid)
            # storing the updated obsraintemp variable into the list
            obsrainfalls.append(obsraintemp)
            # removing the obsraintemp from memory
            del obsraintemp
        else:
            raise ValueError('In path text file obsrainfallpath, \
                             obsrainfallxml, and obsrainfallregrid must \
                             be in order with suffix of the model number')

    elif var.startswith('threshold'):
        # get the rainfall threshold values
        threshold = line[1].split(',')
        threshold = [float(th) for th in threshold if th != '']

    elif var.startswith('region'):
        # get the rainfall threshold values
        region = line[1].split(',')
        region = [r for r in region if r != '']

    elif var.startswith('html'):
        # get the html path to make static web page
        staticWebPath = line[1]
        if not os.path.exists(staticWebPath):
            raise ValueError('The html path does not exists %s to set \
                                static web page' % staticWebPath)
    elif var.startswith('uvcdat'):
        # get the uvcdat installed system path
        uvcdat = line[1]
        if not os.path.exists(uvcdat):
            raise ValueError('The uvcdat path does not exists' % uvcdat)

    elif var.startswith('logpath'):
        # get the logpath
        logpath = line[1]
        if not os.path.exists(logpath):
            raise ValueError('The log path does not exists' % logpath)

    elif var.startswith('archivepath'):
        # get the logpath
        archivepath = line[1]
        if not os.path.exists(archivepath):
            raise ValueError('The archive path does not exists' % archivepath)
    
    elif var.startswith('ftppath'):
        # get the ftppath public path 
        ftppath = line[1]
        
    elif var.lower() == 'plotceofanlsince':
        # get the plot ceof anl since date
        plotceofanlsince = line[1]

    elif var.lower() == 'plotceoftinterval':
        # get the plot ceof time interval in the x-axis to plot the dates.
        plotceoftinterval = int(line[1])
        
    else:
        # unneccessary contents
        pass
# end of for i in pathfile.readlines():
fileobj.close()





