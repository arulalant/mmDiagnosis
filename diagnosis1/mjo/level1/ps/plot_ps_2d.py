# Importing Modules
import os
import sys
import cdms2
import vcs
__curDir__ = os.path.dirname(__file__)
diagDir = os.path.abspath(os.path.join(__curDir__, '../../..'))
# adding the previous diagnosisutils path to python path
sys.path.append(diagDir)
from diag_setup.globalconfig import processfilesPath, plotsgraphsPath


seasondic = {'sum': 'Summer', 'win': 'Winter', 'all': 'All'}


def plotPowerSpectrum2D(data, outfile, season,
                         title='Equatorial Space Time Spectra',
                         xname='Frequency (cycles/day)', yname='Wavenumber',
                         pdf=0, png=1, **kwarg):

    bg = kwarg.get('bg', 1)
    x = kwarg.get('x', None)
    if x is None:
        x = vcs.init()
    # end of if x is None:
    x.clear()
    isotmp = x.getisofill('quick')
    # we have to set the colormap as AMIP to get the below colorcode.
    x.setcolormap("AMIP")

    if season in ['sum', 'Summer', 'win', 'Winter']:
        # summer and winter
        isotmp.levels = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8]
    elif season in ['all', 'annual', 'All']:
        ## annual year
        isotmp.levels = [0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8, 25.6]
    # end of if season in ['sum', 'win']:

    # set the colors to fill it.
    isotmp.fillareacolors = [48, 45, 27, 14, 34, 33, 32, 21, 10, 247]

    isotmp.ext_1 = 'y'
    isotmp.ext_2 = 'y'
    if 'genPS2DTemplate' in x.listelements('template'):
        # get the 'genPS2DTemplate' template object from temporary memory of vcs
        # template
        gentemp = x.gettemplate('genPS2DTemplate')
    else:
        gentemp = x.createtemplate('genPS2DTemplate', 'ASD')
        gentemp.mean.priority = 0
        gentemp.min.priority = 0
        gentemp.max.priority = 0
        gentemp.dataname.priority = 0
        gentemp.units.priority = 0
        gentemp.crdate.priority = 0
        gentemp.crtime.priority = 0
        gentemp.tvalue.priority = 0
        gentemp.tname.priority = 0
        gentemp.tunits.priority = 0
        gentemp.comment1.priority = 0
        gentemp.comment2.priority = 0
        gentemp.comment3.priority = 0
        gentemp.comment4.priority = 0
        gentemp.source.priority = 0
        gentemp.zvalue.priority = 0
        gentemp.xtic2.priority = 0
        gentemp.xmintic2.priority = 0
        gentemp.ytic2.priority = 0
        gentemp.ymintic2.priority = 0
        gentemp.ylabel2.priority = 0
        gentemp.xlabel2.priority = 0
        gentemp.yvalue.priority = 0
        gentemp.xvalue.priority = 0

        gentemp.xname.priority = 1
        gentemp.yname.priority = 1
        gentemp.xname.x = .5
        gentemp.xname.y = .22
        gentemp.yname.x = .03
        gentemp.yname.y = .55

        gentemp.title.priority = 1
        gentemp.title.x = .5
        gentemp.title.y = .92

        to1 = x.createtextorientation('to1', 'centerup')
        to1.height = 24
        to1.angle = 0

        to2 = x.createtextorientation('to2', 'centerup')
        to2.height = 16
        to2.angle = 0

        to3 = x.createtextorientation('to3', 'centerup')
        to3.height = 16
        to3.angle = 90

        gentemp.title.textorientation = to1
        gentemp.xname.textorientation = to2
        gentemp.yname.textorientation = to3
        
        # saving the 'genPS2DTemplate' into temporary python memory
        x.set('template', 'genPS2DTemplate')
    # end of if 'genPS2DTemplate' in x.listelements('template'):
    
    x.plot(data, isotmp, gentemp, title=title, xname=xname, yname=yname, bg=bg)
    x.flush()
    if pdf:
        x.pdf(outfile + '.pdf')
    if png:
        x.png(outfile + '.png')
    x.clear()
# end of def plotPowerSpectrum2D(data, outfile, season, ...):


def doPlotPS2D(rawOrAnomaly, filteredOrNot, year,
                    seasons=['sum', 'win', 'all'], pdf=0, png=1):
    """

    Written By : Arulalan.T

    Date : 22.07.2013

    """
    v = vcs.init()
    if isinstance(year, int):
        yearDir = str(year)
    elif isinstance(year, tuple):
        yearDir = str(year[0]) + '_' + str(year[1])

    inpath = os.path.join(processfilesPath, 'Level1', 'WaveNumber',
                          rawOrAnomaly, filteredOrNot, yearDir)

    for subName in os.listdir(inpath):
        anopath = os.path.join(inpath, subName)
        opath = os.path.join(plotsgraphsPath, 'Level1', 'PowerSpectrum2D',
                                rawOrAnomaly, filteredOrNot, yearDir)
        for seasonName in os.listdir(anopath):
            wvpath = os.path.join(anopath, seasonName)
            for wavefile in os.listdir(wvpath):
                varName = wavefile.split('.')[0].split('_')[0]
                wvfile = os.path.join(wvpath, wavefile)

                outpath = os.path.join(opath, subName, varName, seasonName)
                if not os.path.isdir(outpath):
                    os.makedirs(outpath)
                    print "Path has created ", outpath
                # end of if not os.path.isdir(outpath):

                title = 'Equatorial Space Time Spectra - %s %s %s %s %s' % (varName.upper(),
                                                 seasonName, subName, yearDir, filteredOrNot)

                outfile = '%s_%s_%s_%s_%s_%s_ps2d' % (varName, seasonName, subName,
                        yearDir, filteredOrNot, rawOrAnomaly)
                imgpath = os.path.join(outpath, outfile)
                if pdf:
                    imgpath_ext = imgpath + '.pdf'
                else:
                    imgpath_ext = imgpath + '.png'
                # end of if pdf:
                if os.path.isfile(imgpath_ext):
                    print "The image file already exists in the path ", imgpath
                    print "So skipping summerVariance"
                else:
                    f = cdms2.open(wvfile)
                    data = f(varName)  # latitude=(0,8),longitude=(-0.05,0.05))
                    # options to extract needed portion # wavenumber=(0,8), frequency=(-0.05,0.05))
                    f.close()
                    plotPowerSpectrum2D(data, imgpath, seasonName, title, pdf=pdf, png=png, x=v)
                    print "Plotted power spectrum 2d", imgpath
                    # make memory free
                    del data
                # end of if os.path.isfile(imgpath_ext):
            # end of for season in seasons:
        # end of for anofile in os.listdir(anopath):
    # end of for subName in os.listdir(inpath):
# end of def doPlotPS2D(rawOrAnomaly, filteredOrNot, year, ...):


if __name__ == '__main__':

    year = (1979, 2005)
    doPlotPS2D('Anomaly', 'Unfiltered', year)
    year = 2005
    doPlotPS2D('Anomaly', 'Unfiltered', year)

# end of if __name__ == '__main__':


