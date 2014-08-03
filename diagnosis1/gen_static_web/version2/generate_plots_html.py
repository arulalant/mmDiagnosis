"""
.. module:: generate_plots_html.py
   :synopsis: It should create the static html page by walk through the
              directories strucure of the 'plotsgraphsPath' which is given in
              the 'configure.txt' file.
              The root directories name will be treated as radio buttons and
              its sub directories name will be treated as select boxes.

              Finally once it should reach the least directory which contains
              the plots (image files), that should be represented within a
              table by giving image link.

              Also the generating html has imported the 'diagnosis.css' and
              'diagnosis.js' stylesheets to work properly.

              At last the html will be saved as 'index.html'

Version : 0.2a

Needed Package : html.py 1.16 or above. http://pypi.python.org/pypi/html

Written by: Arulalan.T

Date: 18.01.2012

"""

import os
import sys
from html import HTML
import json
# getting the absolute path of the previous directory
previousDir = os.path.abspath(os.path.join(os.getcwd(), '../..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diag_setup.globalconfig import plotsgraphsPath as filespath, staticWebPath
from diag_setup.short_names_abb import shortNamesAbb
from uv_cdat_code.diagnosisutils.timeutils import TimeUtility

# create time utility object
timobj = TimeUtility()

# created index object from HTML() class which should create open & close tags
html = HTML('html')
head = html.head()
title = head.title('Model Diagnosis')
css = head.link(rel="stylesheet", type="text/css", href="css/diagnosis.css")
#jq = head.script(type="text/javascript", src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js")
jq = head.script(type="text/javascript", src="js/jquery-1.7.min.js")
jq.text("")
js = head.script(type="text/javascript", src="js/diagnosis.js")
js.text("")
# created body tag
body = html.body()
b = body.div(name = 'body', klass = 'bodyCls')
load = body.p(id="loading", style = 'display:inline')
load.text("Loading . . .")
b.br
heading = b.div(name = 'heading', klass = 'headingCls')
heading.h1('Model Diagnosis Plots')


form = b.form()
txt = form.div(id = "txtdiv")
txt.p("Choose a model")
# sphinx documentation link
docdiv = form.div(name = 'docdiv')
doclink = docdiv.a(id = 'docdivid', href = 'doc/index.html', target = '_blank', klass = '')
doclink.text("Documentation")
#form.input(id = "go", type = "button", name = "go", value = "Go", style = "visibility:hidden")
span = form.span(id = "modelSpan")
form.br

globalDict = {'model': {}}

# The level and threshold primary values are added in the below list.
# these levels only should display in the table by default. The remaining 
# levels should be hidden under the 'More' link inside the table.
primaryList = [0.0, 0.1, 200.0, 850.0, "AIR", "CIndia"]

directoryStructure = os.walk(filespath)
for rootdir, sub, files in directoryStructure:

    # Sorting the directories
    sub.sort()

    for dirname in sub:
        if dirname.startswith('.') or dirname == 'CSV':
            sub.remove(dirname)  # don't visit hidden directories

    root = rootdir.split(filespath)[1].split('/')
    lenroot = len(root)


    if lenroot == 2:
        # Getting the Model names directory
        model = root[-1]
        globalDict['model'][model] = {}
        # Set the model names as radio selections
        span.input(type = "radio", name = "model", id = model, klass = "model", value = model)
        span.text(model)
        procdiv = None

    elif lenroot == 3:
        # Getting the process names directory
        process = root[-1]

        modeldic = globalDict['model'][model]
        modeldic[process] = []

        processid = model + '_' + process

        # Set the process name as input buttons
        if root[lenroot - 2] == model and (not procdiv):
            procdiv = form.div(id = model + "Id", name = "processdiv", klass = model + "Cls" + ' ' + "modelCls")
            procdiv.p("Type of plot", id = "P" + model + "_Select", klass = "Pprocess leftTag", style = "display:none")
            proselect = procdiv.select(name = "process", id = model + "_Select", klass = "selectCls", style = "display:none")
            proselect.option(value = "", selected = "selected")
            proselect.text("Select type of plot")

        proselect.option(value = process)
        if process == 'FcstSysErr':
            proselect.text('Forecast Systematic Error')
        elif process == 'Mean':
            proselect.text('Mean Analysis')
        elif process == 'StatiScore':
            proselect.text('Statistical Score')
        else:
            proselect.text(process)
        yeardiv = None

    elif lenroot == 4:
        # Getting the year directory
        year = root[-1]
        yearid = processid + '_' + year

        yeardic = {year : {}}
        modeldic[process].append(yeardic)

    elif lenroot == 5:
        # Getting Month or Season directory
        monseason = root[-1]
        yeardic[year][monseason] = []

        # get the total no of months/seasons
        totalMonthCount = len(sub)
        regionhrselect = None
        # Sorting the directories by month wise/ season wise order
        if sub:
            # replace the unordered directories list into month/season wise
            # ordered directories list
            sub[:] = timobj._sortMonths(sub)
        msselect = None

    elif lenroot == 6:
        # Getting months or season directories
        msname = root[-1]
        #msnameid = monseasonid + '_' + msname
        msnameid = yearid + '_' + msname

        msnamedic = {}
        yeardic[year][monseason].append(msnamedic)
        msnamedic[msname] = []

        # default plotselect
        if 'Region' in sub:
            plotselecttxt = 'Hour/Region'
        else:
            plotselecttxt = 'Hour'


        gotHr = False
        avlHoursCount = 0
        totalPlotCount = 0
        plotdivflag = True

        for dirname in sub:
            if dirname.isdigit(): avlHoursCount += 1
        plotselect = None

    elif lenroot == 7:
        # Getting plot or hour name directories
        plothr = root[-1]

        plothrdic = {}
        msnamedic[msname].append(plothrdic)
        plothrdic[plothr] = []
        plotdic = None

        plothrid = msnameid + '_' + plothr

        if plothr.isdigit():
            latestHour = plothr
            totalPlotCount = len(sub)
            visitedPlotCount = 0
            gotHr = True
        latestPlotHr = None
        gotPlotHr = False
        gotRegion = False
        plotdivFlag = False
        if plothr == 'Region':
            #regionhrselect.text('By Region')
            gotRegion = True
        elif plothr == 'CSV':
            pass
        plotHrid = yearid + '_' + msname + "_Select"
        tablePlotId = plotHrid

    elif lenroot == 8:
        # Getting plot name directories
        plot = root[-1]

        plotdic = {}
        plothrdic[plothr].append(plotdic)
        plotdic[plot] = None

    else:
        pass

    if files:

        tablediv = None
        imgfiledict = {}
        imgfiledict['primary'] = {}
        imgfiledict['secondary'] = {}
        #print files
        
        for imgfile in files:
            extension = imgfile.split('.')[-1].lower()
            if not extension in ['png', 'jpg', 'jpeg', 'svg', 'gif']:
                print "Found extension of file is not image type", imgfile
                continue
            else:
                # To make table index & imgfile in order, store the values into dict
                num = imgfile.split('_')[-4]
                
                try:
                    # float string only falls here. Not char sting.
                    key = float(num)                    
                except ValueError:
                    # combination of no and char or only char falls here.
                    if num.endswith('hPa'):
                        level = num.split('hPa')[0]
                        key = float(level)
                        num = level + ' hPa'                    
                    else:
                        key = num
                            
                if key in primaryList:                    
                    imgfiledict['primary'][key] = (num,  imgfile)
                else:                    
                    imgfiledict['secondary'][key] = (num,  imgfile)
                
        # end of for loop
        imgfiledict['path'] = rootdir
        
        if plotdic:
            if plot.islower(): 
                plot = plot.upper()
            print plot
            if plot in shortNamesAbb:
                abb = shortNamesAbb.get(plot)
                print abb
            else:
                abb = plot 
            imgfiledict['title'] = abb 
            plotdic[plot] = imgfiledict
        else:
            if plot.islower(): 
                plot = plot.upper()
            if plot in shortNamesAbb:
                abb = shortNamesAbb.get(plot)
            else:
                abb = plot 
            imgfiledict['title'] = abb 
            plothrdic[plothr] = imgfiledict



prev = form.div(id = 'preview', klass = 'previewCls')
prev.img(src="css/dummy.png", width = "80", height = "180")

foot = b.div(id = 'footDiv')
foot.text('')

#print html
index = open(staticWebPath + '/index.html', 'w')
index.write(str(html))
index.close()

jsonfile = open(staticWebPath + '/js/diagnosis.json', 'w')
json.dump(globalDict, jsonfile, indent = 2, sort_keys = True)
jsonfile.close()


print "Created index.html in the path ", staticWebPath
print "Created diagnosis.json in the path ", staticWebPath + "/js"
