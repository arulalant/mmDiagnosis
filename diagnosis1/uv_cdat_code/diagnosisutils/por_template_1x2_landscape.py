import cdms2
import cdutil
import numpy
import numpy.ma
import vcs
import os
import sys
# Getting the path 
paths=os.getcwd()

# Initialising VCS
x = vcs.init()
#x.portrait()
x.landscape()

# Defining the text type

tt=x.createtexttable('new', 'std')
tt.font=1
tt.expansion=150
tt.priority=1

# Defining the text height & orientation 
to_d=x.createtextorientation('new', 'default')
to_d.height=27
to_d.angle=0

to_dc=x.gettextorientation( 'defcentup')
to_bc=x.createtextorientation('new_bc', 'botcenter')
to_bc.height=27
to_bc.angle=0

to_bl=x.gettextorientation( 'botleft')
#to_bl.height=30
#to_bl.angle=0 



to_7r=x.gettextorientation( '7right')
#to_7r.height=30
#to_7r.angle=0 

to_7c=x.gettextorientation( '7center')
#to_7c.height=30
#to_7c.angle=0 


to_br=x.gettextorientation( 'botright')


to_7rcc=x.gettextorientation( '7rcc')
#to_7rcc.height=30
#to_7rcc.angle=0 


# Defining the properties of lines
ls=x.getline('std')
#ls.type=['solid']
#ls.width=2

ld=x.getline('default')
#ld.type=['solid']
#ld.width=2

##########--------------leftOfTop_lscp--------------###########

# The template  ''leftOfTop_lscp' is for gettig plot on  left top corner of 
# the landscape template 
leftOfTop_lscp =x.createtemplate('leftOfTop_lscp','por_topof3')
# adjesting the length & width ratio
leftOfTop_lscp.scale(0.6, axis='x')#, font=10)
leftOfTop_lscp.scale(2.6, axis='y')

# Adjesting the position of figure
leftOfTop_lscp.move(-0.5, 'y')
leftOfTop_lscp.move(-0.15, 'x')

# member = source
leftOfTop_lscp.source.priority = 1
leftOfTop_lscp.source.x = 0.7
leftOfTop_lscp.source.y = 1.0767
leftOfTop_lscp.source.texttable = tt
leftOfTop_lscp.source.textorientation = to_dc

# member = title
leftOfTop_lscp.title.priority = 1
leftOfTop_lscp.title.x = 0.11
leftOfTop_lscp.title.y = .86
leftOfTop_lscp.title.texttable = tt
leftOfTop_lscp.title.textorientation = to_d

# member = units
leftOfTop_lscp.units.priority = 0
leftOfTop_lscp.units.x = 0.65
leftOfTop_lscp.units.y = 1.26384
leftOfTop_lscp.units.texttable = tt
leftOfTop_lscp.units.textorientation = to_br

# member = xtic1
leftOfTop_lscp.xtic1.priority = 1
leftOfTop_lscp.xtic1.y1 = 0.175
leftOfTop_lscp.xtic1.y2 = 0.19
leftOfTop_lscp.xtic1.line = ls
# adj X tic...................................
# member = xtic2
leftOfTop_lscp.xtic2.priority = 0
leftOfTop_lscp.xtic2.y1 = 0.62
leftOfTop_lscp.xtic2.y2 = 0.61
leftOfTop_lscp.xtic2.line = ls

# member = ytic1
leftOfTop_lscp.ytic1.priority = 0
leftOfTop_lscp.ytic1.x1 = 0.2
leftOfTop_lscp.ytic1.x2 = 0.19
leftOfTop_lscp.ytic1.line = ls
## Adjusing Y tic------------------------
# member = ytic2
leftOfTop_lscp.ytic2.priority = 1
leftOfTop_lscp.ytic2.x1 = 0.05
leftOfTop_lscp.ytic2.x2 = 0.04
leftOfTop_lscp.ytic2.line = ls

# member = xlabel1
leftOfTop_lscp.xlabel1.priority = 1
leftOfTop_lscp.xlabel1.y = 0.16
leftOfTop_lscp.xlabel1.texttable = tt
leftOfTop_lscp.xlabel1.textorientation = to_bc

# member = xlabel2
leftOfTop_lscp.xlabel2.priority = 0
leftOfTop_lscp.xlabel2.y = 0
leftOfTop_lscp.xlabel2.texttable = tt
leftOfTop_lscp.xlabel2.textorientation = to_d
# adj Y label----------------------------------
# member = ylabel1
leftOfTop_lscp.ylabel1.priority = 1
leftOfTop_lscp.ylabel1.x = 0.015
leftOfTop_lscp.ylabel1.texttable = tt
leftOfTop_lscp.ylabel1.textorientation = to_d

# member = ylabel2
leftOfTop_lscp.ylabel2.priority = 0
leftOfTop_lscp.ylabel2.x = 0
leftOfTop_lscp.ylabel2.texttable = tt
leftOfTop_lscp.ylabel2.textorientation = to_d


#------Setting Legend------#
leftOfTop_lscp.legend.priority = 0
leftOfTop_lscp.legend.y1=.64
leftOfTop_lscp.legend.texttable=tt
leftOfTop_lscp.legend.x1=0.22
leftOfTop_lscp.legend.y2=0.63
leftOfTop_lscp.legend.x2=0.83
leftOfTop_lscp.legend.textorientation = to_d
#ls---stands for Landscape
leftOfTop_lscp.script('leftOfTop_lscp.scr') 
sys.path.append(paths + '/'+'leftOfTop_lscp.scr')
###########################################################

# The template  'rightOfTop_lscp' is for gettig plot on  right top corner of 
# the landscape template 

rightOfTop_lscp =x.createtemplate('rightOfTop_lscp', 'por_topof3')

# adjesting the length & width ratio
rightOfTop_lscp.scale(0.6, axis='x')#, font=10)
rightOfTop_lscp.scale(2.6, axis='y')

# Adjesting the position of figure
rightOfTop_lscp.move(-0.5, 'y')
rightOfTop_lscp.move(0.35, 'x')


# member = source
rightOfTop_lscp.source.priority = 1
rightOfTop_lscp.source.x = 0.7
rightOfTop_lscp.source.y = 1.0767
rightOfTop_lscp.source.texttable = tt
rightOfTop_lscp.source.textorientation = to_dc

# member = title
rightOfTop_lscp.title.priority = 1
rightOfTop_lscp.title.x = 0.63
rightOfTop_lscp.title.y = .86
rightOfTop_lscp.title.texttable = tt
rightOfTop_lscp.title.textorientation = to_d

# member = units
rightOfTop_lscp.units.priority = 0
rightOfTop_lscp.units.x = 0.65
rightOfTop_lscp.units.y = 1.26384
rightOfTop_lscp.units.texttable = tt
rightOfTop_lscp.units.textorientation = to_br




# member = xtic1
rightOfTop_lscp.xtic1.priority = 0


# adj X tic...................................
# member = xtic2
rightOfTop_lscp.xtic2.priority = 1
rightOfTop_lscp.xtic2.y1 = 0.175
rightOfTop_lscp.xtic2.y2 = 0.19
rightOfTop_lscp.xtic2.line = ls

# member = ytic1
rightOfTop_lscp.ytic1.priority = 0

## Adjusing Y tic------------------------
# member = ytic2
rightOfTop_lscp.ytic2.priority = 1
rightOfTop_lscp.ytic2.x1 = 0.55
rightOfTop_lscp.ytic2.x2 = 0.54
rightOfTop_lscp.ytic2.line = ls

# member = xlabel1
rightOfTop_lscp.xlabel1.priority = 1
rightOfTop_lscp.xlabel1.y = 0.16
rightOfTop_lscp.xlabel1.texttable = tt
rightOfTop_lscp.xlabel1.textorientation = to_bc


# adj Y label----------------------------------
# member = ylabel1
rightOfTop_lscp.ylabel1.priority = 1
rightOfTop_lscp.ylabel1.x = 0.52
rightOfTop_lscp.ylabel1.texttable = tt
rightOfTop_lscp.ylabel1.textorientation = to_d

#------Setting Legend------#

rightOfTop_lscp.legend.priority = 1
rightOfTop_lscp.legend.y1=.05
rightOfTop_lscp.legend.texttable=tt
rightOfTop_lscp.legend.x1=0.20
rightOfTop_lscp.legend.y2=0.035
rightOfTop_lscp.legend.x2=0.81
rightOfTop_lscp.legend.textorientation = to_d  

rightOfTop_lscp.script('rightOfTop_lscp.scr')
sys.path.append(paths + '/'+ 'rightOfTop_lscp.scr')
###########

