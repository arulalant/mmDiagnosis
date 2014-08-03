"""
Make template  array
written By: Rajappan
Updated By : Dileep.K, Arulalan.T
updated : 28.07.2013

"""

import  vcs


def make_template_array(Nrows, Ncols, xgap, ygap, Left_Margin,
                        Right_Margin, Top_Margin, Bot_Margin, **kwarg):

    x = kwarg.get('x', None)
    if x is None:
        print "vcs init from eof_make_template_array"
        x = vcs.init()
        x.landscape()
        x.mode = 1
    # end of if x is None:

    if 'eof' in x.listelements('texttable'):
        tt = x.gettexttable('eof')
    else:
        tt = x.createtexttable('eof', 'std')
        tt.font = 1
        tt.priority = 1

    # Create text orientation
    if 'eof13' in x.listelements('textorientation'):
        tt1 = x.gettextorientation('eof13')
    else:
        tt1 = x.createtextorientation('eof13', 'centerup')
        tt1.height = 13
        tt1.angle = 0

    if 'eof17' in x.listelements('textorientation'):
        tt2 = x.gettextorientation('eof17')
    else:
        tt2 = x.createtextorientation('eof17', 'centerup')
        tt2.height = 17
        tt2.angle = 0
    # storing templates into array
    template_array = []
    xval = (1 - Left_Margin - ((Ncols-1) * xgap) - Right_Margin)/(Ncols)
    yval = (1 - Top_Margin - ((Nrows-1) * ygap) - Bot_Margin)/Nrows
    for i in range(Nrows):
        for j in range(Ncols):
            jstring = str(j)
            istring = str(i)
            templateName = 'eof'+ istring + jstring
            if templateName in x.listelements('template'):
                template = x.gettemplate(templateName)
            else:
                xmove = Left_Margin + ((j+1)-1) * (xval+xgap)
                ymove = 0.5-(Top_Margin + ((i+1)-1) * (yval+ygap))

                template = x.createtemplate(templateName)

                #******************template**************#
                template.move(xmove, axis='x')
                template.move(ymove, axis='y')
                template.scale(xval, axis='x')
                template.scale(yval, axis='y')
                template.file.priority = 0
                template.xvalue.priority = 0
                template.yvalue.priority = 0
                template.zvalue.priority = 0
                template.data.priority = 1
                template.mean.priority = 0
                template.max.priority = 0
                template.min.priority = 0
                template.file.priority = 0
                template.function.priority = 0
                template.logicalmask.priority = 0
                template.transformation.priority = 0
                template.crtime.priority = 0
                template.crdate.priority = 0
                template.dataname.priority = 0
                template.comment2.priority = 0
                template.comment3.priority = 0
                template.comment4.priority = 0
                template.crtime.priority = 0
                template.crdate.priority = 0
                template.tunits.priority = 0
                template.zunits.priority = 0
                template.yunits.priority = 0
                template.xunits.priority = 0
                template.tunits.priority = 0
                template.zunits.priority = 0
                template.yunits.priority = 0
                template.xunits.priority = 0
                template.source.priority = 0
                template.tvalue.priority = 0
                template.xname.priority = 0
                template.yname.priority = 0
                template.xtic2.priority=0
                template.ytic2.priority=0
                if (i == 0 and j == 0):
                    template.legend.priority = 1
                    template.legend.y1 = 0.06
                    template.legend.texttable = tt
                    template.legend.x1 = 0.12
                    template.legend.y2 = 0.045
                    template.legend.x2 = 0.9
                    template.legend.textorientation = tt1

                    template.title.priority = 1
                    template.title.x = 0.50
                    template.title.y = 0.98
                    template.title.texttable = tt
                    template.title.textorientation = tt2
                else:
                    template.legend.priority = 0
                    template.title.priority = 0
                template.comment1.priority = 1
                template.comment1.texttable = tt
                template.comment1.textorientation = tt1
                template.comment1.x = xmove + xval - 0.77
                template.comment1.y = ymove + yval + 0.15
                template.units.priority = 0
                template.xtic1.priority = 0
                template.xtic2.priority = 0
                template.ytic1.priority = 1
                template.ytic1.height = 0
                template.ytic2.priority = 0

                if (i==Nrows-1):
                    template.xlabel1.priority = 1
                    template.xlabel1.y = 0.115
                    template.xlabel1.textorientation = tt1
                    template.xtic1.priority = 1
                else:
                    template.xlabel1.priority = 0
                    template.xtic1.priority = 0
                template.ylabel1.priority = 0
                template.xlabel2.priority = 0
                if (j == Ncols-1):
                    template.ylabel1.priority = 1
                    template.ylabel1.x = 0.04
                    template.ylabel1.textorientation = tt1
                else:
                    template.ylabel2.priority = 0

                # saving these templates into temporary python vcs memory.
                x.set('template', templateName)
            # end of if templateName in x.listelements('template'):
            # append the template to the list
            template_array.append(template)
        # end of for j in range(Ncols):
    # end of for i in range(Nrows):
    return  template_array
# end of def make_template_array(Nrows, Ncols, xgap, ...):




