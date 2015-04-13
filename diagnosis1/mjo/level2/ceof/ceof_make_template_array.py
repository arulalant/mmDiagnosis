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
    # end of if x is None:
    x.portrait()
    x.mode = 1
    
    if 'ceof' in x.listelements('texttable'):
        tt = x.gettexttable('ceof')
    else:
        tt = x.createtexttable('ceof', 'std')
        tt.font = 3
        tt.priority = 1

    # Create text orientation
    if 'ceof8' in x.listelements('textorientation'):
        tt1 = x.gettextorientation('ceof8')
    else:
        tt1 = x.createtextorientation('ceof8', 'centerup')
        tt1.height = 8
        tt1.angle = 0

    if 'ceof15' in x.listelements('textorientation'):
        tt2 = x.gettextorientation('ceof15')
    else:
        tt2 = x.createtextorientation('ceof15', 'centerup')
        tt2.height = 15
        tt2.angle = 0

    if 'ceof12' in x.listelements('textorientation'):
        tt3 = x.gettextorientation('ceof12')
    else:
        tt3 = x.createtextorientation('ceof12', 'centerup')
        tt3.height = 12
        tt3.angle = 0

    if 'ceof12_90' in x.listelements('textorientation'):
        tt4 = x.gettextorientation('ceof12_90')
    else:
        tt4 = x.createtextorientation('ceof12_90', 'centerup')
        tt4.height = 12
        tt4.angle = -90

    # storing templates into array
    template_array = []
    xval = (1 - Left_Margin -((Ncols-1) * xgap) - Right_Margin)/(Ncols)
    yval = (1- Top_Margin -((Nrows-1) * ygap) - Bot_Margin)/Nrows
    for i in range(Nrows):
        for j in range(Ncols):
            jstring = str(j)
            istring = str(i)
            templateName = 'ceof' + istring + jstring
            if templateName in x.listelements('template'):
                template = x.gettemplate(templateName)
            else:
                xmove = Left_Margin + ((j+1)-1)*(xval+xgap)
                ymove = 0.5 -(Top_Margin + ((i+1)-1) * (yval+ygap))
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
                template.xtic2.priority=0
                template.ytic2.priority=0
                if (i == 0 and j == 0):
                    template.legend.priority = 1
                    template.legend.y1=0.06
                    template.legend.texttable=tt
                    template.legend.x1=0.12
                    template.legend.y2=0.045
                    template.legend.x2=0.9
                    template.legend.textorientation = tt1

                    template.title.priority = 1
                    template.title.x=0.50
                    template.title.y = 0.93
                    template.title.texttable=tt
                    template.title.textorientation=tt2
                else:
                    template.legend.priority = 0
                    template.title.priority = 0
                template.comment1.priority = 1
                template.comment1.texttable = tt
                template.comment1.textorientation = tt3
                template.comment1.x = xmove + xval - 0.60
                template.comment1.y = ymove + yval + 0.12

                template.comment2.priority = 1
                template.comment2.texttable = tt
                template.comment2.textorientation = tt1
                template.comment2.x = xmove + xval - 0.40
                template.comment2.y = ymove + yval - 0.21

                template.comment3.priority = 1
                template.comment3.texttable = tt
                template.comment3.textorientation = tt3
                template.comment3.x = xmove + xval - 0.40
                template.comment3.y = ymove + yval - 0.18

                template.xname.priority = 0
                template.xname.texttable = tt
                template.xname.textorientation = tt3

                template.yname.priority = 0
                template.yname.texttable = tt
                template.yname.textorientation = tt4
                template.units.priority = 0
                template.xtic1.priority = 1
                template.xtic2.priority = 0
                template.ytic1.priority = 1
                template.ytic1.height = 0
                template.ytic2.priority = 0

                if (i==Nrows-1):
                    template.xlabel1.priority = 1
                    template.xlabel1.textorientation = tt1
                    template.xlabel1.texttable = tt
                else:
                    template.xlabel1.priority = 1
                    template.xlabel1.textorientation = tt1
                    template.xlabel1.texttable = tt
                template.ylabel1.priority = 0
                template.xlabel2.priority = 0
                if (j == Ncols-1):
                    template.ylabel1.priority = 1
                    template.ylabel1.x=0.125
                    template.ylabel1.textorientation = tt1
                    template.ylabel1.texttable = tt
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



