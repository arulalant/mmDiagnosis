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

Version : 0.1a

Needed Package : html.py 1.16 or above. http://pypi.python.org/pypi/html

Written by: Arulalan.T

Date: 16.11.2011

"""

import os
import sys
from html import HTML
# getting the absolute path of the previous directory
previousDir = os.path.abspath(os.path.join(os.getcwd(), '../..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diag_setup.globalconfig import plotsgraphsPath as filespath, staticWebPath
from uv_cdat_code.diagnosisutils.timeutils import TimeUtility

# create time utility object
timobj = TimeUtility()

# created index object from HTML() class which should create open & close tags
html = HTML('html')
head = html.head()
title = head.title('Model Diagnosis')
css = head.link(rel="stylesheet", type="text/css", href="css/diagnosis.css")
jq = head.script(type="text/javascript", src="js/jquery-1.7.min.js")
jq.text("")
js = head.script(type="text/javascript", src="js/diagnosis.js")
js.text("")
# created body tag
body = html.body()
b = body.div(name = 'body', klass = 'bodyCls')
b.br
heading = b.div(name = 'heading', klass = 'headingCls')
heading.h1('Model Diagnosis Plots')


flag = True
count = 3
form = b.form()
txt = form.div(id = "txtdiv")
txt.p("Choose a model")
# sphinx documentation link
docdiv = form.div(name = 'docdiv')
doclink = docdiv.a(id = 'docdivid', href = 'doc/index.html', target = '_blank', klass = '')
doclink.text("Documentation")
form.input(id = "go", type = "button", name = "go", value = "Go", style = "visibility:hidden")
span = form.span(id = "modelSpan")
form.br

directoryStructure = os.walk(filespath)
for rootdir, sub, files in directoryStructure:

    # Sorting the directories
    sub.sort()

    for dirname in sub:
        if dirname.startswith('.'):
            sub.remove(dirname)  # don't visit hidden directories

    root = rootdir.split(filespath)[1].split('/')
    lenroot = len(root)

    if lenroot == 2:
        # Getting the Model names directory
        model = root[lenroot - 1]
        # Set the model names as radio selections
        span.input(type = "radio", name = "model", id = model, klass = "model", value = model)
        span.text(model)
        procdiv = None

    elif lenroot == 3:
        # Getting the process names directory
        process = root[lenroot - 1]
        processid = model + '_' + process

        # Set the process name as input buttons
        if root[lenroot - 2] == model and (not procdiv):
            procdiv = form.div(name = "processdiv", klass = model + "Cls" + ' ' + "modelCls")
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
        year = root[lenroot - 1]
        yearid = processid + '_' + year
        # Add the yeardiv
        if root[lenroot - 2] == process and (not yeardiv):
            yeardiv = procdiv.div(klass = processid + 'Cls' + ' ' + model + "_SelectCls")
            yeardiv.p("Year", id = "P" + processid + "_Select", klass = "Pyear leftTag", style = "display:none")
            yearselect = yeardiv.select(name = "year", id = processid + "_Select", klass = "selectCls", style = "display:none")
            yearselect.option(value = "", selected = "selected")
            yearselect.text("Select year")
        yearselect.option(value = year)
        yearselect.text(year)
        msselect = None

        # default msselect
        if len(sub) > 1:
            if ('Month' and 'Season') in sub:
                msselecttxt = 'Month/Season'
        else:
            msselecttxt = sub[0]

    elif lenroot == 5:
        # Getting Month or Season directory
        monseason = root[lenroot -1]
        monseasonid = yearid + '_' + monseason
        # Add the monseason div
        monseasondiv = yeardiv.div(name = "monseasondiv", klass = yearid + 'Cls')
        monseasondiv.text("")

        # Sorting the directories by month wise/ season wise order
        if sub:
            # replace the unordered directories list into month/season wise
            # ordered directories list
            sub[:] = timobj._sortMonths(sub)

    elif lenroot == 6:
        # Getting months or season directories
        msname = root[lenroot - 1]
        #msnameid = monseasonid + '_' + msname
        msnameid = yearid + '_' + msname
        # Set the month/season name as input buttons
        if root[lenroot - 3] == year and (not msselect):
            msnamediv = monseasondiv.div(name = "msname", klass = yearid + 'Cls', title = monseason)
            msnamediv.p("Time period", id = "P" + yearid + "_Select", klass = "Pmonseason leftTag", style = "display:none")
            msselect = msnamediv.select(name = "monseason", id = yearid + "_Select", klass = "selectCls", style = "display:none")
            msselect.option(value = "", selected = "selected")
            msselect.text("Select " + msselecttxt)
        msselect.option(value = msname)
        msselect.text(msname)
        plothrselect = None
        # default plotselect
        if 'Region' in sub:
            plotselecttxt = 'Hour/Region'
        else:
            plotselecttxt = 'Hour'

        # Sorting the directories by numerical order (combination of int & str)
        if sub and sub[0].isdigit():
            subdirdic = {}
            for dirname in sub:
                if dirname.isdigit():
                    key = int(dirname)
                else:
                    key = dirname
                subdirdic[key] = dirname
            newsub = []
            keys = subdirdic.keys()
            keys.sort()
            for dirname in keys:
                newsub.append(subdirdic.get(dirname))
            # replace the unordered directories list into hour/region wise ordered directories list
            sub[:] = newsub

    elif lenroot == 7:
        # Getting plot or hour name directories
        plothr = root[lenroot -1]
        plothrid = msnameid + '_' + plothr
        # Set the plot/hour name as input buttons
        if root[lenroot - 2] == msname and (not plothrselect):
            plotHrid = yearid + '_' + msname + "_Select"
            tablePlotId = plotHrid
            if files:
                plothrdiv = msnamediv.div(name = "plothr", klass = msnameid + 'Cls' + ' ' + yearid + "_SelectCls")
                plothrdiv.p("Plot", id = "P" + plotHrid, klass = "Pplot1 leftTag", style = "display:none")
                plothrselect = plothrdiv.select(name = "plot", id = plotHrid, klass = "selectCls", style = "display:none")
                plothrselect.option(value = "", selected = "selected")
                plothrselect.text("Select Plot")
                # assinging plotdiv to create tablediv
                plotdiv = plothrdiv
            else:
                plothrdiv = msnamediv.div(name = "plothr", klass = msnameid + 'Cls' + ' ' + yearid + "_SelectCls")
                plothrdiv.p("Forecast " + plotselecttxt, id = "P" + plotHrid, klass = "Pregionhr leftTag", style = "display:none")
                plothrselect = plothrdiv.select(name = "regionhr", id = plotHrid, klass = "selectCls", style = "display:none")
                plothrselect.option(value = "", selected = "selected")

                plothrselect.text("Select " + plotselecttxt)
        plothrselect.option(value = plothr)
        if plothr == 'Region':
            plothrselect.text('By Region')
        else:
            plothrselect.text(plothr)
        plotselect = None

    elif lenroot == 8:
        # Getting plot name directories
        plot = root[lenroot -1]
        plotid = plothrid + plot
        # Set the plot name as input buttons
        if root[lenroot - 2] in [plot, plothr] and (not plotselect):
            # creating plotdiv to create tablediv
            plotdiv = plothrdiv.div(name = "plot", klass = plothrid + 'Cls' + ' ' + plotHrid + 'Cls')
            tablePlotId = plothrid + "_Select"
            plotdiv.p("Plot", id = "P" + tablePlotId, klass = "Pplot2 leftTag", style = "display:none")
            plotselect = plotdiv.select(name = "plot", id = tablePlotId, klass = "selectCls", style = "display:none")
            plotselect.option(value = "", selected = "selected")
            plotselect.text("Select Plot")
        plotselect.option(value = plot)
        plotselect.text(plot)

    else:
        pass

    if files:
        tablediv = None
        imgfiledict = {}
        #print files
        for imgfile in files:
            extension = imgfile.split('.')[-1].lower()
            if not extension in ['png', 'jpg', 'jpeg', 'svg', 'gif']:
                print "Found extension of file is not image type", imgfile
                continue
            else:
                # To make table index & imgfile in order, store the values into dict
                num = imgfile.split('_')[-4]
                if num.isdigit():
                    key = float(num)
                elif num.endswith('hPa'):
                    level = num.split('hPa')[0]
                    key = float(level)
                    num = level + ' ' + 'hPa'
                else:
                    key = num
                imgfiledict[key] = (num, imgfile)
        # Sorting the table index
        imgOrder = imgfiledict.keys()
        imgOrder.sort()
        for index in imgOrder:
            column1, imgfile = imgfiledict.get(index)
            imgstr = imgfile.split('_')
            column2 = imgstr[1]
            if imgstr[-4].endswith('hPa'):
                thead1 = 'Level'
            else:
                thead1 = imgstr[-3].capitalize()

            if column2.startswith('D') and column2[1].isdigit():
                # Need to add column2 in the table
                #print "getting D"
                #raw_input()
                pass
            else:
                column2 = None

            if root[lenroot - 1] in [plot, plothr] and (not tablediv):
                plotname = root[lenroot - 1]
                if plothr.isdigit() or plothr == 'Region':
                    tableid = plothrid + "_" + plotname + "_Table"
                else:
                    tableid = plothrid + "_Table"

                tablediv = plotdiv.div(id = tableid, name = "plottable",
                                 klass = 'tableCls ' + tablePlotId + 'Cls',
                                 style = "display:none")

                table = tablediv.table(border = "1", id = tableid)
                trow = table.tr()
                trow.th(thead1)

                if column2:
                    trow.th(plotname + ' ' + column2 + " Day Plots")
                else:
                    trow.th(plotname + " Plots")
                #print "creating table header"
            else:
                tbrow = table.tr()
                tbrow.td(column1)
                data = tbrow.td()
                imglink = rootdir + '/' + imgfile
                link = data.a(href = imglink, target = '_blank', klass = 'imgCls')
                # Make image preview (thumbnail)
                #link.img(src = imglink, width = '180', height = '180')
                # Make text link only
                link.text(imgfile)
        # end of for imgfile in files:
    # end of if files:
# end of for rootdir, sub, files in os.walk(filespath):

prev = form.div(id = 'preview', klass = 'previewCls')
prev.img(src="css/dummy.png", width = "80", height = "180")

#print html
index = open(staticWebPath + '/index.html', 'w')
index.write(str(html))
index.close()
print "Created index.html in the path ", staticWebPath
