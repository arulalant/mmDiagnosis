import os
import sys
import cdms2
import vcs
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
mDir = os.path.abspath(os.path.join(__curDir__, '../../..'))
# adding the previous path to python path
sys.path.append(mDir)
import diag_setup.netcdf_settings
previousDir = os.path.abspath(os.path.join(__curDir__, 'WK'))
# adding the previous path to python path
sys.path.append(previousDir)
# importing WK & WKPlot from this local module/directory named as WK.
# Once uvcdat updates the above local module/directory named as WK into
# its own repo, then we can remove the above two lines where
# os.path.join(__curDir__, 'WK') path is added to python system path.
import WK
from WKPlot import WKPlot

# intialize the global variables
v = vcs.init()
WP = WKPlot(x=v)
WP.x.scriptrun(os.path.join(__curDir__, "WK/colormap.scr"))
WP.x.setcolormap("rainbow")
bg = 0


def genWKVars(data, outpath, outfile, segment=96, overlap=60, **kwarg):
    """
    data - model anomaly

    output - It produces the following 6 variables & will be written
             into outfile.
                1. power
                2. power_S  # symmetric power
                3. power_A  # anti-symmetric power
                4. background
                5. power_S_bg  # symmetric power / background
                6. power_A_bg  # anti-symmetric power / background

    outfile - user has to pass the outfile name with .nc file extension.
              This outfile name will be updated along with no of days in
              segment and no of days overlap. Finally it will return the
              new nc file name with its outpath.

    Return - outfile path (outfile name has modified here)


    Written By : Arulalan.T

    Updated : 24.06.2013

    """
    compresstime = kwarg.get('compresstime', True)
    smooth = kwarg.get('smooth', False)
    W = WK.WK(number_of_days=segment, shift=overlap)
    ## Process the data, i.e compute spectral wave number and frequencies
    print "computeing spectral wave number and frequencies"
    power = W.process(data)
    # make memory free
    del data

    outfile, ext = outfile.split('.')
    outfile = '_'.join([outfile, str(segment), 'segment',
                                str(overlap), 'overlap'])
    outfile = '.'.join([outfile, ext])
    outfile = os.path.join(outpath, outfile)

    comment = '%d-day segment, %d-day overlapping' % (segment, overlap)

    f = cdms2.open(outfile, 'w')
    power.id = 'power'
    power.comment = comment
    # write power into nc file
    f.write(power)

    print "Spliting between Sym and ASym components"
    # Split between Sym and ASym components
    # Averages over time if compresstime is True (default)
    S, A = W.split(power, compresstime=compresstime, smooth=smooth)
    # make memory free
    del power
    S.comment = comment
    A.comment = comment
    # write S & A into nc file
    f.write(S)  # by default S id is power_S
    f.write(A)  # by default A id is power_A

    print "Generating background data"
    background = W.background(S, A)
    background.id = 'background'
    background.comment = comment
    # write background into nc file
    f.write(background)

    sid = S.id
    aid = A.id
    S /= background
    A /= background
    # make memory free
    del background

    S.id = sid + '_bg'
    A.id = aid + '_bg'
    # write power_S_bg, power_A_bg into nc file
    f.write(S)
    f.write(A)
    # close the file
    f.close()
    print "Written all the vars into", outfile
    # return the modified outfile name along with its path.
    return outfile
# end of def genWKVars(data, outpath, outfile, segment=96, overlap=60):


def plotWKPowers(infile, outpath, outfile='Powers', png=0, pdf=1):
    """
    figure1 : plotting power_S & power_A
    """

    global WP, v, bg

    f = cdms2.open(infile)
    S = f('power_S')
    A = f('power_A')
    f.close()
    print 'Powers'
    WP.plot_figure1(S, A, bg=bg)
    #v.show()
    outfile = os.path.join(outpath, outfile)
    if pdf: v.pdf(outfile + '.pdf')
    if png: v.pdf(outfile + '.png')

    WP.x.clear()
# end of def plotWKPowers(infile, outpath, ...):


def plotWKBackground(infile, outpath, outfile='background',
                                lmin=-1, lmax=2, png=0, pdf=1):
    """
    figure2 : plotting background
    """

    global WP, v, bg

    f = cdms2.open(infile)
    background = f('background')
    f.close()
    print 'background'
    WP.plot_figure2(background, min=lmin, max=lmax, bg=bg)
    #v.show()
    outfile = os.path.join(outpath, outfile)
    if pdf: v.pdf(outfile + '.pdf')
    if png: v.pdf(outfile + '.png')

    WP.x.clear()
# end of def plotWKBackground(infile, outpath, ...):


def plotWK_Sym_ASym(infile, outpath, outfile='Sym_ASym', lmin=1., lmax=2.1,
               ptitle='Wheeler Kiladis Diagram', comment_1='',
               comment_2='Variable (Data) : , Period : JJAS', png=0, pdf=1):

    """
    figure3 : plotting power_S_bg & power_A_bg

    lmin : legend min user can pass even +ve value or -ve value
    lmax : legend max must be +ve value

    ptitile : Plot title

    comment_1 : If comment_1 is '' or None, then comment will be extracted
                from power_S_bg variable (while generating this variable
                using funciton genWKVars, the comment has set to all the
                variables as like '96-day segment, 60-day overlapping'.
                The parameters days will be set w.r.t input of that funciton).

    comment_2 : By default it is 'Variable (Data) : , Period : JJAS'.
                User can change it as follows
                eg : 'Variable (Data) : OLR (NCMRWF), Period : JJAS 2010'

                Both comment_1 & comment_2 can be changed by user.
    """

    global WP, v, bg

    f = cdms2.open(infile)
    S = f('power_S_bg')
    A = f('power_A_bg')
    f.close()
    # overwrite the S, A ids to plot
    S.id = 'Symmetric'
    A.id = 'Anti-symmetric'
    print 'Plotting 3'

    if not comment_1:
        # take comment from S or A variable
        comment_1 = S.comment
    # end of if not comment_1:

    # actual min should be -ve & max should be +ve. say min=-0.1, max=2.2.
    # I changed this in the WK module, to plot the legend from +ve min to
    # +ve max.
    WP.plot_figure3(S, A, min=lmin, max=lmax, delta_isofill=.1,
                    delta_isoline=1,
                    days_lines=(80, 30, 20, 15, 10, 7, 5, 4, 3, 2),
                    H=[12., 25., 50.], title=ptitle,
                    comment1=comment_1, comment2=comment_2, bg=bg)

    #v.show()
    outfile = os.path.join(outpath, outfile)
    if pdf: v.pdf(outfile + '.pdf')
    if png: v.pdf(outfile + '.png')

    WP.x.clear()
    print "Plot saved into ", outfile
# end of def plotWK_Sym_ASym(infile, outpath, ...):





