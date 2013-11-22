import os
import numpy 
import vcs


lat5 = {-90: '90S', -85: '85S', -80: '80S', -75: '75S',
         -70: '70S', -65: '65S', -60: '60S', -55: '55S', -50: '50S',
         -45: '45S', -40: '40S', -35: '35S', -30: '30S', -25: '25S',
         -20: '20S', -15: '15S', -10: '10S', -5: '5S', 0: 'EQ', 5: '5N',
          10: '10N', 15: '15N', 20: '20N', 25: '25N', 30: '30N',
          35: '35N', 40: '40N', 45: '45N', 50: '50N', 55: '55N',
          60: '60N', 65: '65N', 70: '70N', 75: '75N', 80: '80N',
          85: '85N', 90: '90N'}

lon5 = {0: '0E', 5: '5E', 10: '10E', 15: '15E', 20: '20E',
        25: '25E', 30: '30E', 35: '35E', 40: '40E', 45: '45E', 50: '50E',
        55: '55E', 60: '60E', 65: '65E', 70: '70E', 75: '75E', 80: '80E',
        85: '85E', 90: '90E', 95: '95E', 100: '100E', 105: '105E',
        110: '110E', 115: '115E', 120: '120E', 125: '125E', 130: '130E',
        135: '135E', 140: '140E', 145: '145E', 150: '150E', 155: '155E',
        160: '160E', 165: '165E', 170: '170E', 175: '175E',
        180: '180E', 185: '185E', 190: '190E', 195: '195E', 200: '200E',
        205: '205E', 210: '210E', 215: '215E', 220: '220E', 225: '225E',
        230: '230E', 235: '235E', 240: '240E', 245: '245E', 250: '250E',
        255: '255E', 260: '260E', 265: '265E', 270: '270E', 275: '275E',
        280: '280E', 285: '285E', 290: '290E', 295: '295E', 300: '300E',
        305: '305E', 310: '310E', 315: '315E', 320: '320E', 325: '325E',
        330: '330E', 335: '335E', 340: '340E', 345: '345E', 350: '350E',
        355: '355E'}

lat10 = {-90: '90S', -80: '80S', -70: '70S', -60: '60S', -50: '50S',
         -40: '40S', -30: '30S', -20: '20S', -10: '10S', 0: 'EQ', 10: '10N',
         20: '20N', 30: '30N', 40: '40N', 50: '50N', 60: '60N', 70: '70N',
         80: '80N', 90: '90N'}

lon10 = {0: '0E', 10: '10E', 20: '20E', 30: '30E', 40: '40E', 50: '50E',
        60: '60E', 70: '70E', 80: '80E', 90: '90E', 100: '100E', 110: '110E',
        120: '120E', 130: '130E', 140: '140E', 150: '150E', 160: '160E',
        170: '170E', 180: '180E', 190: '190E', 200: '200E',
        210: '210E', 220: '220E', 230: '230E', 240: '240E', 250: '250E',
        260: '260E', 270: '270E', 280: '280E', 290: '290E', 300: '300E',
        310: '310E', 320: '320E', 330: '330E', 340: '340E', 350: '350E',
        359: '359E'}

lon60 = {0: '0E', 60: '60E', 120: '120E', 180: '180E', 240: '240E',
         300: '300E', 359: '359E'}

lat60 = {-90: '90S', -30: '30S', 0: 'EQ', 30: '30N', 90: '90N'}

x = None


def getLatLonLabel(latlabel='lat5', lonlabel='lat5'):

    if latlabel == 'lat5':
        # setting latitude as 5 degree interval
        latlabel = lat5
    elif latlabel == 'lat10':
        # setting latitude as 10 degree interval
        latlabel = lat10
    elif latlabel == 'lat60':
        # setting latitude as 10 degree interval
        latlabel = lat60
    else:
        pass

    if lonlabel == 'lon5':
        # setting longitude as 5 degree interval
        lonlabel = lon5
    elif lonlabel == 'lon10':
        # setting longitude as 10 degree interval
        lonlabel = lon10
    elif lonlabel == 'lon60':
        # setting longitude as 10 degree interval
        lonlabel = lon60
    else:
        pass
    return latlabel, lonlabel
# end of getLatLonLabel(latlabel='lat5', lonlabel='lat5'):

def checkLatLonLabel(template, latlabel, lonlabel):

    # resetting lat,lon values back to the vctemp once the vctemp's lat,lon
    # differs from the arg lat,lon
    lenlat = len(template.yticlabels1)
    lenlon = len(template.xticlabels1)
    if lenlat != len(lat5) and latlabel == 'lat5':
        template.yticlabels1 = lat5
    elif lenlat != len(lat10) and latlabel == 'lat10':
        template.yticlabels1 = lat10
    elif lenlat != len(lat60) and latlabel == 'lat60':
        template.yticlabels1 = lat60
    else:
        pass

    if lenlon != len(lon5) and lonlabel == 'lon5':
        template.xticlabels1 = lon5
    elif lenlon != len(lon10) and lonlabel == 'lon10':
        template.xticlabels1 = lon10
    elif lenlon != len(lon60) and lonlabel == 'lon60':
        template.xticlabels1 = lon60
    else:
        pass
    return template
# end of checkLatLonLabel():

def genTemplate(xscale=0, yscale=0, xmove=0, ymove=0):

    global x
    if not (x and isinstance(x, vcs.Canvas.Canvas)):
        # initializing vcs
        x = vcs.init()
        
        
#        x.portrait()
        # auto update vcs
        x.mode = 1
        print "one time initializing of vcs obj x"

    if 'genTemplate' in x.listelements('template'):
        # get the 'genTemplate' template object from temporary memory of vcs
        # template
        gentemp = x.gettemplate('genTemplate')
    else:
        # creating 'genTemplate' object
        tt = x.createtexttable('new', 'std')
        tt.font = 1
        tt.priority = 1

        to = x.createtextorientation('new', 'centerup')
        to.height = 17
        to.angle = 0

        l = x.createline('new', 'thick')
        l.type = ['solid']
        l.width = 3
        # create copy of ASD template
        gentemp = x.createtemplate('genTemplate', 'ASD')

        gentemp.title.priority = 1
        gentemp.title.x = 0.50
        gentemp.title.y = 0.88
        gentemp.title.texttable = tt
        gentemp.title.textorientation = to
        gentemp.min.priority = 0    # off min value
        gentemp.mean.priority = 0   # off mean value
        gentemp.max.priority = 0    # off max value
        gentemp.dataname.priority = 0  # off the variable id

        gentemp.legend_type = 'VCS'
        gentemp.legend.priority = 1
        
        gentemp.legend.x1 = 0.9
        gentemp.legend.y1 = 0.06
        gentemp.legend.x2 = 0.1
        gentemp.legend.y2 = 0.1


#        gentemp.legend.x1 = 0.9
#        gentemp.legend.y1 = 0.06
#        gentemp.legend.x2 = 0.1
#        gentemp.legend.y2 = 0.1
        gentemp.legend.texttable = tt
        #gentemp.legend.textorientation = to

        gentemp.xname.priority = 0  # off the longitude string in x axis
        gentemp.yname.priority = 0  # off the latitude string in y axis
        gentemp.units.priority = 0  # off the units value

        if xscale:
            gentemp.scale(xscale, axis = 'x')
        if yscale:
            gentemp.scale(yscale, axis = 'y')
        if xmove:
            gentemp.move(xmove, 'x')
        if ymove:
            gentemp.move(ymove, 'y')
        gentemp.scalefont(2.4)

        # saving the 'genTemplate' into temporary python memory
        x.set('template', 'genTemplate')

    # return the genTemplate object
    return gentemp
# end of def genTemplate():

def genVector(reference, scale, latlabel='lat5', lonlabel='lon5'):

    global x
    if not (x and isinstance(x, vcs.Canvas.Canvas)):
        # initializing vcs
        x = vcs.init()
        # auto update vcs
        x.mode = 1
        print "one time initializing of vcs obj x"

    if not isinstance(reference, float):
        # converting reference point into float
        reference = float(reference)

    if 'genVector' in x.listelements('vector'):
        # get the 'vctemp' template object from temporary memory
        # of vcs template
        vctemp = x.getvector('genVector')
    else:
        # get the lat,lon label according to the passed string
        latlabel, lonlabel = getLatLonLabel(latlabel, lonlabel)
        # create copy of new vector template to vctemp template
        vctemp = x.createvector('genVector')
        # set vector properties
        vctemp.projection = 'linear'
        vctemp.alignment = 'head'
        vctemp.xticlabels1 = lonlabel       # set bottom longitude values
        vctemp.xticlabels2 = ''             # set top longitude values
        vctemp.yticlabels1 = latlabel       # set left latitude values
        vctemp.yticlabels2 = ''             # set right latitude values
        vctemp.scale = scale           # scaling the vector's scaling length
        #vctemp.linecolor = 16         # 16 to 255
        vctemp.reference = reference   # 20.0 for 2deg intervals
        # save this 'vctemp' vector template object into temporary vcs
        # template memory
        x.set('vector', 'genVector')
    # end of if 'vctemp' in x.listelements('vector'):
    if (vctemp.scale != scale or vctemp.reference != reference):
        # setting vector scale, reference if user passed
        vctemp.scale = scale
        vctemp.reference = reference
    # checking the lat,lon label and reset if needed
    vctemp = checkLatLonLabel(vctemp, latlabel, lonlabel)
    # return the genVector object
    return vctemp
# end of def genVector():

def genIsoLine(levels=None, colorlist=None, latlabel='lat5', lonlabel='lon5'):

    global x
    if not (x and isinstance(x, vcs.Canvas.Canvas)):
        # initializing vcs
        x = vcs.init()
        # auto update vcs
        x.mode = 1
        print "one time initializing of vcs obj x"

    if 'genIsoLine' in x.listelements('isoline'):
        # get the 'genIsoLine' template object from temporary memory of vcs
        # isoline template
        isolinetemp = x.getisoline('genIsoLine')
    else:
        # get the lat,lon label according to the passed string
        latlabel, lonlabel = getLatLonLabel(latlabel, lonlabel)

        isolinetemp = x.createisoline('genIsoLine', 'ASD')
        isolinetemp.line = ['solid']
        isolinetemp.linewidths = [1.0]
        isolinetemp.label = 'y'
        isolinetemp.xticlabels1 = lonlabel   # set bottom longitude values
        isolinetemp.xticlabels2 = ''         # set top longitude values
        isolinetemp.yticlabels1 = latlabel   # set left latitude values
        isolinetemp.yticlabels2 = ''             # set right latitude values

        if levels:
            # setting isoline levels if user passed
            isolinetemp.levels = levels
        if colorlist:
            # setting isoline colors if user passed
            isolinetemp.linecolors = colorlist
        # saving the 'genIsoLine' into temporary python memory
        x.set('isoline', 'genIsoLine')
    # make isotypelevels for checking purpose, i.e. check the already created
    # template levels and user passed levels are same or not
    isotypelevels = [[lev, 0] for lev in levels]
    if (isolinetemp.levels != isotypelevels or isolinetemp.linecolors != colorlist):
        # setting isoline levels, colorlist if user passed
        isolinetemp.levels = levels
        isolinetemp.linecolors = colorlist
    # checking the lat,lon label and reset if needed
    isolinetemp = checkLatLonLabel(isolinetemp, latlabel, lonlabel)
    # return the genIsoLine object
    return isolinetemp
# end of def genIsoLine(levels=None, colorlist=None):

def genIsoFill(levels=None, colorlist=None, latlabel='lat5', lonlabel='lon5'):

    global x
    if not (x and isinstance(x, vcs.Canvas.Canvas)):
        # initializing vcs
        x = vcs.init()
        # auto update vcs
        x.mode = 1
        print "one time initializing of vcs obj x"

    if 'genIsoFill' in x.listelements('isofill'):
        # get the 'genIsoFill' template object from temporary memory of vcs
        # isoline template
        isofilltemp = x.getisofill('genIsoFill')
    else:
        # get the lat,lon label according to the passed string
        latlabel, lonlabel = getLatLonLabel(latlabel, lonlabel)

        isofilltemp = x.createisofill('genIsoFill', 'quick')
        isofilltemp.line = ['solid']
        isofilltemp.linewidths = [1.0]
        isofilltemp.label = 'y'
        isofilltemp.xticlabels1 = lonlabel   # set bottom longitude values
        isofilltemp.xticlabels2 = ''         # set top longitude values
        isofilltemp.yticlabels1 = latlabel   # set left latitude values
        isofilltemp.yticlabels2 = ''         # set right latitude values
        if levels:
            # setting isofill levels if user passed
            isofilltemp.levels = levels
            # enable the extensions of legend
            isofilltemp.ext_1 = 'y'         # setting ext in legend after
            isofilltemp.ext_2 = 'y'         # setting levels only
        if colorlist:
            # setting isofill colors if user passed
            isofilltemp.fillareacolors = colorlist

        # saving the 'genIsoFill' into temporary python memory
        x.set('isofill', 'genIsoFill')
    # make isotypelevels for checking purpose, i.e. check the already created
    # template levels and user passed levels are same or not
    isotypelevels = [[lev, 0] for lev in levels]
    if (isofilltemp.levels != isotypelevels or isofilltemp.fillareacolors != colorlist):
        # setting isofill levels, colorlist if user passed
        isofilltemp.levels = levels
        isofilltemp.fillareacolors = colorlist
        # enable the extensions of legend
        isofilltemp.ext_1 = 'y' # setting ext in legend after setting levels only
        isofilltemp.ext_2 = 'y' # if levels changed means again need to set ext
    # checking the lat,lon label and reset if needed
    isofilltemp = checkLatLonLabel(isofilltemp, latlabel, lonlabel)
    # return the genIsoFill object
    return isofilltemp
# end of def genIsoFill(levels=None, colorlist=None):

def vectorPlot(u, v, name, path=None, reference=20.0, scale=1, interval=1,
                            svg=1, png=0, latlabel='lat5', lonlabel='lon5',
                                                         style='portrait'):
    """
    :func:`vectorPlot`: Plotting the vector with some default preferences.

    Input : u - u variable
            v - v variable
            name - name to plot on the top of the vcs
            path - path to save as the image file.
            reference - vector reference. Default it takes 20.0 (i.e 2 degree)
            scale - scaling of the arrow mark in vector plot
            interval - slicing the data to reduce the density (noise)
                       in the vector plot, with respect to the interval.
                       Default it takes 1. (i.e. doesnot affect the u & v)
            svg - to save image as svg
            png - to save image as png

    Condition : u must be 'u variable' and v must be 'v variable'.
                name must pass to set the name on the vector vcs
                path is not passed means, it takes current workig directory
                reference must be float.
                interval not be 0.

    Usage : using this function, user can plot the vector.

            user can control the reference point of the vector, and scale
            length of the arrow marks in plot.

            Also can control the u and v data shape by interval.

            filename should be generated from the 'name' passed by the user,
            just replacing the space into underscore '_'.

            if svg and png passed 1, the image will be saved with these
            extensions in the filename.

    Written By : Arulalan.T

    Date : 26.07.2011

    """

    global x
    if not (x and isinstance(x, vcs.Canvas.Canvas)):
        # initializing vcs
        x = vcs.init()
        # auto update vcs
        x.mode = 1
        print "one time initializing of vcs obj x"
    if style == 'portrait':
        x.portrait()
        gentemp = genTemplate(xscale = 0, yscale = 0, xmove = 0.02, ymove = -0.075)
    elif style == 'landscape':
        x.landscape()
        
        gentemp = genTemplate(xscale = 1, yscale = 0.7, xmove = 0.02, ymove = 0.1)
    else:
        raise ValueError("style must be either portrait or landscape")
    # slicing the data to reduce the density (noise) in the vector plot
    u = u[::interval, ::interval]
    v = v[::interval, ::interval]
    windSpeed = (u**2 + v**2)**0.5
#    gentemp = genTemplate(xscale = 0, yscale = 0, xmove = 0.02, ymove = -0.075)   
    genvector = genVector(reference, scale, latlabel, lonlabel)
    ws_lev = [2, 4, 6]
    ws_clr = [240, 245, 249, 242]
    isofilltemp = genIsoFill(ws_lev, ws_clr, latlabel, lonlabel)
    # plotting vector in background

    x.plot(windSpeed, isofilltemp, gentemp, title = None, bg=1)
    x.plot(u, v, genvector, gentemp, title = name, bg = 1)
    filename = name.replace(' ', '_')

    if not path:
        # get the current workig directory
        path = os.getcwd()
    if not os.path.isdir(path):
        raise RuntimeError("The passed path doesnot exists to store the \
                            vector plots")
    if not path.endswith('/'):
        path += '/'
    if svg:
        x.svg(path + filename + '.svg')
        print "plotted and saved the %s%s.svg" % (path, filename)
    if png:
        x.png(path + filename + '.png')
        print "plotted and saved the %s%s.png" % (path, filename)
    if not (svg or png):
        raise RuntimeError("Can not set both svg, png options are zero/None.\
                            Enable any one to store the vectorPlot")
    # clear the vcs object
    x.clear()
# end of def vectorPlot(...):

def isoLinePlot(var, levels, colorlist, name, path=None, svg=1, png=0,
                        latlabel='lat5', lonlabel='lon5', style='portrait'):

    global x
    if not (x and isinstance(x, vcs.Canvas.Canvas)):
        # initializing vcs
        x = vcs.init()
        # auto update vcs
        x.mode = 1
        print "one time initializing of vcs obj x"
    if style == 'portrait':
        x.portrait()
    elif style == 'landscape':
        x.landscape()
    else:
        raise ValueError("style must be either portrait or landscape")

    gentemp = genTemplate(xmove = 0.02, ymove = -0.075)

    gentemp.legend.priority = 0 # off the legend
    isolinetemp = genIsoLine(levels, colorlist, latlabel, lonlabel)
    x.plot(var, isolinetemp, gentemp, title = name, bg = 0)
    filename = name.replace(' ', '_')

    if not path:
        # get the current workig directory
        path = os.getcwd()
    if not os.path.isdir(path):
        raise RuntimeError("The passed path doesnot exists to store the \
                            vector plots")
    if not path.endswith('/'):
        path += '/'
    if svg:
        x.svg(path + filename + '.svg')
        print "plotted and saved the %s%s.svg" % (path, filename)
    if png:
        x.png(path + filename + '.png')
        print "plotted and saved the %s%s.png" % (path, filename)
    if not (svg or png):
        raise RuntimeError("Can not set both svg, png options are zero/None.\
                            Enable any one to store the isoLinePlot")
    # clear the vcs object
    x.clear()
# end of def isoLinePlot(...):

def isoFillPlot(var, levels, colorlist, name, path=None, svg=1, png=0,
                         latlabel='lat5', lonlabel='lon5', style='portrait'):

    global x
    if not (x and isinstance(x, vcs.Canvas.Canvas)):
        # initializing vcs
        x = vcs.init()
        # auto update vcs
        x.mode = 1
        print "one time initializing of vcs obj x"
    if style == 'portrait':
        x.portrait()
        gentemp = genTemplate(xscale = 0.98, yscale = 1.2,
                          xmove = 0.02, ymove = -0.075)
    elif style == 'landscape':
        x.landscape()
        gentemp.legend.priority = 1
        gentemp.legend.x1 = 0.9
        gentemp.legend.y1 = 0.06
        gentemp.legend.x2 = 0.1
        gentemp.legend.y2 = 0.1

        gentemp = genTemplate(xscale = 0.98, yscale = 0.9,
                          xmove = 0.02, ymove = -0.075)
    else:
        raise ValueError("style must be either portrait or landscape")
        
    
    #gentemp.legend.priority = 1 # on the legend
    isofilltemp = genIsoFill(levels, colorlist, latlabel, lonlabel)
    x.plot(var, isofilltemp, gentemp, title = name, continents =6, bg = 1)
    filename = name.replace(' ', '_')

    if not path:
        # get the current workig directory
        path = os.getcwd()
    if not os.path.isdir(path):
        raise RuntimeError("The passed path doesnot exists to store the \
                            vector plots")
    if not path.endswith('/'):
        path += '/'
    if svg:
        x.svg(path + filename + '.svg')
        print "plotted and saved the %s%s.svg" % (path, filename)
    if png:
        x.png(path + filename + '.png')
        print "plotted and saved the %s%s.png" % (path, filename)
    if not (svg or png):
        raise RuntimeError("Can not set both svg, png options are zero/None.\
                            Enable any one to store the isoFillPlot")
    # clear the vcs object
    x.clear()
# end of def isoFillPlot(...):

def isoFillLinePlot(var, levels, colorlist, name, path=None, svg=1, png=0,
                         latlabel='lat5', lonlabel='lon5', style='portrait'):

    global x
    if not (x and isinstance(x, vcs.Canvas.Canvas)):
        # initializing vcs
        x = vcs.init()
        # auto update vcs
        x.mode = 1
        print "one time initializing of vcs obj x"
    if style == 'portrait':
        x.portrait()
    elif style == 'landscape':
        x.landscape()
        
    else:
        raise ValueError("style must be either portrait or landscape")
    gentemp = genTemplate(xmove = 0.02, ymove = -0.075)

    gentemp.legend.priority = 1 # on the legend
   
    isofilltemp = genIsoFill(levels, colorlist, latlabel, lonlabel)
    isolinetemp = genIsoLine(levels, colorlist, latlabel, lonlabel)
    x.plot(var, isofilltemp, gentemp, title = name, bg = 0)
    gentemp.legend.priority = 0 # off the legend
    x.plot(var, isolinetemp, gentemp, title = name, bg = 0)
    filename = name.replace(' ', '_')

    if not path:
        # get the current workig directory
        path = os.getcwd()
    if not os.path.isdir(path):
        raise RuntimeError("The passed path doesnot exists to store the \
                            vector plots")
    if not path.endswith('/'):
        path += '/'
    if svg:
        x.svg(path + filename + '.svg')
        print "plotted and saved the %s%s.svg" % (path, filename)
    if png:
        x.png(path + filename + '.png')
        print "plotted and saved the %s%s.png" % (path, filename)
    if not (svg or png):
        raise RuntimeError("Can not set both svg, png options are zero/None.\
                            Enable any one to store the isoFillLinePlot")
    # clear the vcs object
    x.clear()
# end of def isoFillPlot(...):

def tyTemplate(xscale=0, yscale=0, xmove=0, ymove=0, scalefont=0, minor=False):

    global x
    if not (x and isinstance(x, vcs.Canvas.Canvas)):
        # initializing vcs
        x = vcs.init()        
#        x.portrait()
        # auto update vcs
        x.mode = 1
        print "one time initializing of vcs obj x"

    if 'tyTemplate' in x.listelements('template'):
        # get the 'tyTemplate' template object from temporary memory of vcs
        # template
        tytemp = x.gettemplate('tyTemplate')
    else:
        # creating 'tyTemplate' object with customized properties
        # create the text table 
        tt = x.createtexttable('tytt', 'std')
        tt.font = 1
        tt.priority = 1
        tt.color = 'black'
        # create text orientation for long strings
        to = x.createtextorientation('tyto', 'centerup')
        to.height = 30
        to.angle = 0
        to.halign = 'center'
        # create the text orientation for x axis standard deviation labels 
        xlto = x.createtextorientation('tyxlto', 'centerup')
        xlto.height = 20
        xlto.angle = 0
        xlto.halign = 'center'
        # create the text orientation for y axis standard deviation labels 
        ylto = x.createtextorientation('tyylto', 'centerup')
        ylto.height = 20
        ylto.angle = 0
        ylto.halign = 'right'  
        
        # create copy of deftaylor template
        tytemp = x.createtemplate('tyTemplate', source="deftaylor")
        
        #Sets the correlation major line
        l = x.createline()
        l.type = 'solid'
        l.width = 1
        l.color = [241] # black
        tytemp.ytic2.x1 = tytemp.data.x1
        tytemp.ytic2.line = l
        
        #Sets standard dev major line
        l = x.createline()
        l.type = 'solid'
        l.width = 1
        l.color = [241] # black
        tytemp.xtic2.line = l
        tytemp.xtic2.priority = 1  
        
        if minor:
            #Sets the correlation minor line
            l = x.createline()
            l.type = 'dot'
            l.width = 1
            l.color = [252] # grey
            tytemp.ymintic2.x1 = tytemp.data.x1
            tytemp.ymintic2.line = l
            
            #Sets the std minor line
            l = x.createline()
            l.type = 'dot'
            l.width = 1
            l.color = [252] # grey
            tytemp.xmintic2.line = l
            tytemp.xmintic2.priority = 1              

        #Sets the outer lines (x,y standard deviation & correlation) properties
        l = x.createline()
        l.type = 'solid'
        l.width = 3
        l.color = [241] # black
        tytemp.line1.line = l
        tytemp.line3.line = l
        tytemp.line4.line = l
        
        #Sets the reference line properties. i.e truth(obs) standard deviation
        l = x.createline()
        l.type = 'solid'
        l.width = 2
        l.color = [242] # red
        tytemp.line2.line = l

        tytemp.title.priority = 1
        tytemp.title.x = 0.50
        #tytemp.title.y = 0
        tytemp.title.texttable = tt
        tytemp.title.textorientation = to
        tytemp.min.priority = 0    # off min value
        tytemp.mean.priority = 0   # off mean value
        tytemp.max.priority = 0    # off max value
        tytemp.dataname.priority = 0  # off the variable id

        # Set the xname (Standard Deviation) text font, size
        tytemp.xname.texttable = tt
        tytemp.xname.textorientation = to
        # Set the yname (Correlation) text font, size
        tytemp.yname.texttable = tt        
        tytemp.yname.textorientation = to
        
        #Sets the xlabels (numbers) text font, size
        # i.e x axis standard deviation
        tytemp.xlabel1.texttable = tt 
        tytemp.xlabel1.textorientation = xlto
        tytemp.xlabel2.texttable = tt 
        tytemp.xlabel2.textorientation = xlto
        # Sets the ylabels (numbers) text font, size.
        # i.e y axis standard deviation & circle correlation axis labels
        tytemp.ylabel1.texttable = tt 
        tytemp.ylabel1.textorientation = ylto
        tytemp.ylabel2.texttable = tt 
        tytemp.ylabel2.textorientation = ylto
        

        if xscale:
            tytemp.scale(xscale, axis = 'x')
        if yscale:
            tytemp.scale(yscale, axis = 'y')
        if xmove:
            tytemp.move(xmove, 'x')
        if ymove:
            tytemp.move(ymove, 'y')
        if scalefont:
            tytemp.scalefont(scalefont)
        #tytemp.moveto(0.0,0.01) 
        # saving the 'tyTemplate' into temporary python memory
        x.set('template', 'tyTemplate')

    # return the tytemp object
    return tytemp
# end of def tyTemplate():

def genTaylor(reference, colors=None, symbols=None, maxvalue=None, quadrans=1):

    global x
    if not (x and isinstance(x, vcs.Canvas.Canvas)):
        # initializing vcs
        x = vcs.init()
        # auto update vcs
        x.mode = 1
        print "one time initializing of vcs obj x"


    if 'genTaylor' in x.listelements('taylordiagram'):
        tytemp = x.gettaylordiagram('genTaylor')
    else:
        tytemp = x.createtaylordiagram('genTaylor')
        # setting the color to the rms error/deviaton isolines.        
        tytemp.skillColor = 'green'
    # set taylordiagram properties
    
    # setting the truth dotted reference std value 
    tytemp.referencevalue = reference
    if colors:
        # setting the colors
        tytemp.Marker.color = colors
    if symbols:
        # setting the symbols
        tytemp.Marker.symbol= symbols
    if maxvalue:
        # set the max value in std        
        tytemp.max = maxvalue
    # set the quadrans
    tytemp.quadrans = quadrans
    
    if False:
        # this block should do, change the x-axis std labels as 
        # alternative to the y-axis labels. 
        # But in future, we are going to remove this block, since 
        # we are going to keep both x-y axis std labels are same.
        
        # make the skip value either 1, or 2, or 3 or so on ., 
        skip = 1 if maxvalue <=10 else (maxvalue/10)+1 
        # generate & set the x-axis standard deviation labels
        mjrstd1 = vcs.mklabels(numpy.arange(0.5, maxvalue + 2, skip))
        tytemp.xticlabels1 = mjrstd1
        # generate & set the y-axis standard deviation labels
        mjrstd2 = vcs.mklabels(range(0, maxvalue + 1, skip))
        tytemp.yticlabels1 = mjrstd2
   
    # return the genTaylor object
    return tytemp
# end of def genTaylor():

def _plotMarker(x, mx, my, mtype, mcolor, msize=5, plotbg=0):
    """
    x : vcs init object 
    plot the marker in x, with passed arguemts.
    """
    mk = x.createmarker()
    mk.x = [mx] 
    mk.y = [my]
    mk.color = [mcolor]
    mk.size = [msize if msize else 5]
    mk.type = [mtype]
    x.plot(mk, bg = plotbg)
    return 
        
class reference_std_dev (float):
    """
    This class implements the type: standard deviation of a reference variable.
    It is just a float value with one method that will be used in the computation of
    a test variable RMS.
    """
    # < Function compute_RMS_function>=                                       

    def compute_RMS_function (self, s, R):
        """
        Function compute_RMS_function
        -----------------------------

        Compute and return the centered-pattern RMS of a test variable
        from its standard-deviation and correlation.

        Input:
            self:   reference-variable standard deviation
            s:      test variable standard deviation
            R:      test-variable correlation with reference variable
        """

        RMS_2 = self*self + s*s - 2*self*s*R
        # Compute square root
        return RMS_2** 0.5


def tylorPlot(data, reference, name, path=None, colors=[], symbols=[], 
                maxvalue=None, legendstrings=[], lcolors=[], lsymbols=[],
                markersize=[], svg=1, png=0, 
                style='landscape', plotbg=0, legendpos='topright', rms='yes'):


    global x
    if not (x and isinstance(x, vcs.Canvas.Canvas)):
        # initializing vcs
        x = vcs.init()
        # auto update vcs
        x.mode = 1
        print "one time initializing of vcs obj x"
    x.clear()
    if style == 'portrait':
        x.portrait()
        # generate the template for tylor (customized)
        tytemp = tyTemplate(xscale = 1, yscale = 1, xmove = 0.0, ymove = 0.0)
    elif style == 'landscape':
        x.landscape()
        # generate the template for tylor (customized)    
        tytemp = tyTemplate(xscale = 1, yscale = 1, xmove = 0, ymove = 0.0, scalefont = 1.4) #ymove = -0.2, 
    else:
        raise ValueError("style must be either portrait or landscape")
    
    if not legendstrings:
        raise ValueError("pass legendstrings arg ")
    
    # find out either correlations have -ve value. If yes, then make the 
    # quadrans has 2 else 1.
    correlations = data.transpose()[1]
    mincorr = min(correlations) 
    
    if mincorr < 0:
        quadrans = 2
        legendpos = 'bottomcenter'
        # swtich off the left most labels, tic, mintics of std.
        tytemp.ylabel1.priority = 0
        tytemp.ytic1.priority = 0
        tytemp.ymintic1.priority = 0
    else:
        quadrans = 1
        legendpos = 'topright'
        # swtich on the left most labels, tic, mintics of std.
        tytemp.ylabel1.priority = 1
        tytemp.ytic1.priority = 1
        tytemp.ymintic1.priority = 1
    # generate/get the taylor template
    gentylor = genTaylor(reference, colors, symbols, maxvalue, quadrans)    
    # plot the data with taylot template with values.
    # Here we just passing the defaultSkillFunction method as skill argument,
    # to plot the rms error isolines.    
    
    if rms in ['yes', 'y', 1, True]:
        # Determine Centered-pattern RMS as skill score function
        # Make a specific data-type off reference std dev value
        reference = reference_std_dev(reference)

        # Compute max_RMS: RMS for point at top left diagram corner
        # where std_dev = scale and correlation = 0.
        max_RMS = reference.compute_RMS_function (maxvalue, 0.)

        # Determine the displayed levels for the skill score
        RMS_levels = vcs.mkscale (0., max_RMS)
        gentylor.skillValues = RMS_levels[1:] # do not include the leading value wich is 0.

        # Plot the diagram with Centered-pattern RMS as skill score
        x.plot (data, gentylor, tytemp, skill = reference.compute_RMS_function,
                 title = name,  bg = plotbg)
    else:
        # Plot the diagram
        x.plot (data, gentylor, tytemp, title = name,  bg = plotbg)
   
    ##
    # Additional (legend) plots
    ##
    
    # over write the colors & symbols if user passed legend marker symbols 
    # and/or legend marker colors.
    colors = lcolors if lcolors else colors
    symbols = lsymbols if lsymbols else symbols
    
    colors_count = len(colors)
    symbols_count = len(symbols) 
    
    # create the text template to add the legend strings   
    strcount = len(legendstrings)
    xgap = 0
    ygap = 0
    
    if legendpos == 'topright':
        strX = 0.8 
        strY = 0.8
        ygap = 0.03        
        # generate the Strings X axis positions.
        sX = [strX] * strcount
        # generate the Strings Y axis positions.
        sY = list(numpy.arange(strY, strY-(ygap * strcount), -ygap))
        #create the markers template to add the legend marker
        mX = [strX - 0.02] * strcount        
        mY = sY 
        # create the legend (rectangle) box at top right corner
        lx1 = 0.75 
        lx2 = 0.9 
        ly1 = 0.83
        # increase the legend height dynamically w.r.t no of strings in the legend 
        ly2 = ly1 - (ygap * strcount) - ygap
        
    elif legendpos == 'bottomcenter':
        strX = 0.3 
        strY = 0.08
        xgap = 0.1        
        
        if strcount <=6:
            # generate the Strings X axis positions.
            sX = list(numpy.arange(strX, strX+(xgap * strcount), xgap))
            # generate the Strings Y axis positions.            
            sY = [strY] * strcount
            #create the markers template to add the legend marker
            mX = [strX - 0.02] * strcount
            mY = sY
            # create the legend (rectangle) box at bottom center 
            ly1 = 0.11
            ly2 = 0.05 
            lx1 = 0.25
            # increase the legend width dynamically w.r.t no of strings in the legend 
            lx2 = lx1 + (xgap * strcount) + (xgap / 4)
            
        elif strcount <=12:
            # generate the Strings X axis positions. 
            # take only the first 6 x pos 
            sX = list(numpy.arange(strX, strX+(xgap * 6), xgap))[:6]            
            # repeate the from the 6 x pos 
            sX += sX[: strcount-6]            
            # generate the Strings Y axis positions.
            sY = [strY] * 6 + [strY - 0.03] * (strcount - 6)    
            #create the markers template to add the legend marker
            mX = list(numpy.array(sX) - 0.02)            
            mY = sY
            # create the legend (rectangle) box at bottom center 
            ly1 = 0.11
            ly2 = 0.03 
            lx1 = 0.25
            # increase the legend width dynamically w.r.t 6 strings in the legend 
            # i.e. 6 strings printed in first line, the remaning string will 
            # be in the second line of the legend
            lx2 = lx1 + (xgap * 6) + (xgap / 4)
            
        elif strcount <=16:
            # generate the Strings X axis positions. 
            # take only the first 8 x pos 
            strX = strX - 0.07
            sX = list(numpy.arange(strX, strX+(xgap * 8), xgap))[:8]            
            # repeate the from the 8 x pos 
            sX += sX[: strcount-8]            
            # generate the Strings Y axis positions.
            sY = [strY] * 8 + [strY - 0.03] * (strcount - 8)    
            #create the markers template to add the legend marker
            mX = list(numpy.array(sX) - 0.02)            
            mY = sY
            # create the legend (rectangle) box at bottom center 
            ly1 = 0.11
            ly2 = 0.03 
            lx1 = 0.18
            # increase the legend width dynamically w.r.t 8 strings in the legend 
            # i.e. 8 strings printed in first line, the remaning string will 
            # be in the second line of the legend
            lx2 = lx1 + (xgap * 8) + (xgap / 4)
            
    txt = x.createtext()
    txt.x = sX
    txt.y = sY
    txt.color = 241
    txt.string = legendstrings
    txt.height = 25
    txt.font = 1
    # plotting the strings 
    x.plot(txt, bg = plotbg)
    
   
    # default marker size. common for all the markers.
    defmarkersize = 5
         
    # plots the multiple markers with different attibutes inside legend box.
    if colors_count > symbols_count:
        # plot same color, different types of symbols 
        for color in colors:  
            msize = markersize.pop(0) if markersize else defmarkersize
            mx = mX.pop(0)
            my = mY.pop(0)
            _plotMarker(x, mx, my, symbols[0], color, round(msize))   
    elif colors_count < symbols_count:
        # plot different colors, same type of symbol
        for symbol in symbols:            
            msize = markersize.pop(0) if markersize else defmarkersize
            mx = mX.pop(0)
            my = mY.pop(0)
            _plotMarker(x, mx, my, symbol, colors[0], round(msize))            
    else:
        # colors_count == symbols_count:
        # plot different colors & different types of symbols 
        for color, symbol in zip(colors, symbols):            
            msize = markersize.pop(0) if markersize else defmarkersize 
            mx = mX.pop(0)
            my = mY.pop(0)                         
            _plotMarker(x, mx, my, symbol, color, round(msize))            
    
    
    ln = x.createline()
    ln.x = [lx1, lx2, lx2, lx1, lx1]       # x line positions
    ln.y = [ly1, ly1, ly2, ly2, ly1]       # y line positions
    ln.width = 3                      
    ln.color = 241 
    ln.type = 'solid' 
    # plot the legend                        
    x.plot(ln, bg = plotbg)
    
    ###
    ## End of plotting
    ###

    # save the plot 
    filename = name.replace(' ', '_')

    if not path:
        # get the current workig directory
        path = os.getcwd()
    if not os.path.isdir(path):
        raise RuntimeError("The passed path doesnot exists to store the \
                            vector plots")
    if not path.endswith('/'):
        path += '/'
    if svg:
        x.svg(path + filename + '.svg')
        print "plotted and saved the %s%s.svg" % (path, filename)
    if png:
        x.png(path + filename + '.png')
        print "plotted and saved the %s%s.png" % (path, filename)
    if not (svg or png):
        raise RuntimeError("Can not set both svg, png options are zero/None.\
                            Enable any one to store the vectorPlot")
    # clear the vcs object
    x.clear()
    # 
    
# end of def tylorPlot(...):
