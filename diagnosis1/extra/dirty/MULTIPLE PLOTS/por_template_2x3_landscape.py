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
leftOfTop_lscp.scale(0.36, axis='x')#, font=10)
leftOfTop_lscp.scale(1.4, axis='y')

# Adjesting the position of figure
leftOfTop_lscp.move(-0.07, 'y')
leftOfTop_lscp.move(-0.15, 'x')

# member = source
leftOfTop_lscp.source.priority = 1
leftOfTop_lscp.source.x = 0.7
leftOfTop_lscp.source.y = 1.0767
leftOfTop_lscp.source.texttable = tt
leftOfTop_lscp.source.textorientation = to_dc

# member = title
leftOfTop_lscp.title.priority = 1
leftOfTop_lscp.title.x = 0.05
leftOfTop_lscp.title.y = .99
leftOfTop_lscp.title.texttable = tt
leftOfTop_lscp.title.textorientation = to_d

# member = units
leftOfTop_lscp.units.priority = 1
leftOfTop_lscp.units.x = 0.65
leftOfTop_lscp.units.y = 1.26384
leftOfTop_lscp.units.texttable = tt
leftOfTop_lscp.units.textorientation = to_br

# member = xtic1
leftOfTop_lscp.xtic1.priority = 1
leftOfTop_lscp.xtic1.y1 = 0.62
leftOfTop_lscp.xtic1.y2 = 0.61
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
leftOfTop_lscp.xlabel1.y = 0.59
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

##########--------------midOfTop_lscp--------------###########
# The template  'midOfTop_lscp' is for gettig plot on  top mid of 
# the landscape template 
midOfTop_lscp =x.createtemplate('midOfTop_lscp','por_topof3')

# adjesting the length & width ratio
midOfTop_lscp.scale(0.36, axis='x')
midOfTop_lscp.scale(1.4, axis='y')

# Adjesting the position of figure
midOfTop_lscp.move(-0.07, 'y')
midOfTop_lscp.move(0.18, 'x')


# member = source
midOfTop_lscp.source.priority = 1
midOfTop_lscp.source.x = 0.7
midOfTop_lscp.source.y = 1.0767
midOfTop_lscp.source.texttable = tt
midOfTop_lscp.source.textorientation = to_dc

# member = title
midOfTop_lscp.title.priority = 1
midOfTop_lscp.title.x = 0.38
midOfTop_lscp.title.y = .99
midOfTop_lscp.title.texttable = tt
midOfTop_lscp.title.textorientation = to_d

# member = units
midOfTop_lscp.units.priority = 1
midOfTop_lscp.units.x = 0.65
midOfTop_lscp.units.y = 1.26384
midOfTop_lscp.units.texttable = tt
midOfTop_lscp.units.textorientation = to_br


# member = xvalue
midOfTop_lscp.xvalue.priority = 1
midOfTop_lscp.xvalue.x = 0.2
midOfTop_lscp.xvalue.y = 0.6
midOfTop_lscp.xvalue.texttable = tt
midOfTop_lscp.xvalue.textorientation = to_d

# member = xtic1
midOfTop_lscp.xtic1.priority = 0


# adj X tic...................................
# member = xtic2
midOfTop_lscp.xtic2.priority = 1
midOfTop_lscp.xtic2.y1 = 0.62
midOfTop_lscp.xtic2.y2 = 0.61
midOfTop_lscp.xtic2.line = ls

# member = ytic1
midOfTop_lscp.ytic1.priority = 0
midOfTop_lscp.ytic1.x1 = 0.19
midOfTop_lscp.ytic1.x2 = 0.2
midOfTop_lscp.ytic1.line = ls
## Adjusing Y tic------------------------
# member = ytic2
midOfTop_lscp.ytic2.priority = 1
midOfTop_lscp.ytic2.x1 = 0.38
midOfTop_lscp.ytic2.x2 = 0.37
midOfTop_lscp.ytic2.line = ls

# member = xlabel1
midOfTop_lscp.xlabel1.priority = 1
midOfTop_lscp.xlabel1.y = 0.59
midOfTop_lscp.xlabel1.texttable = tt
midOfTop_lscp.xlabel1.textorientation = to_bc

# member = xlabel2
midOfTop_lscp.xlabel2.priority = 0

# adj Y label----------------------------------
# member = ylabel1
midOfTop_lscp.ylabel1.priority = 1
midOfTop_lscp.ylabel1.x = 0.342
midOfTop_lscp.ylabel1.texttable = tt
midOfTop_lscp.ylabel1.textorientation = to_d

#------Setting Legend------#
midOfTop_lscp.legend.priority = 0
midOfTop_lscp.legend.y1=.64
midOfTop_lscp.legend.texttable=tt
midOfTop_lscp.legend.x1=0.22
midOfTop_lscp.legend.y2=0.63
midOfTop_lscp.legend.x2=0.83
midOfTop_lscp.legend.textorientation = to_d

midOfTop_lscp.script('midOfTop_lscp.scr') 
sys.path.append(paths + '/'+ 'midOfTop_lscp.scr') 

##########--------------rightOfTop_lscp--------------###########

# The template  'rightOfTop_lscp' is for gettig plot on  right top corner of 
# the landscape template 

rightOfTop_lscp =x.createtemplate('rightOfTop_lscp', 'por_topof3')

# adjesting the length & width ratio
rightOfTop_lscp.scale(0.36, axis='x')#, font=10)
rightOfTop_lscp.scale(1.4, axis='y')

# Adjesting the position of figure
rightOfTop_lscp.move(-0.07, 'y')
rightOfTop_lscp.move(0.51, 'x')


# member = source
rightOfTop_lscp.source.priority = 1
rightOfTop_lscp.source.x = 0.7
rightOfTop_lscp.source.y = 1.0767
rightOfTop_lscp.source.texttable = tt
rightOfTop_lscp.source.textorientation = to_dc

# member = title
rightOfTop_lscp.title.priority = 1
rightOfTop_lscp.title.x = 0.71
rightOfTop_lscp.title.y = .99
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
rightOfTop_lscp.xtic1.y1 = 0.68
rightOfTop_lscp.xtic1.y2 = 0.69
rightOfTop_lscp.xtic1.x1 = 0.70
rightOfTop_lscp.xtic1.x2 = 0.69
rightOfTop_lscp.xtic1.line = ls

# adj X tic...................................
# member = xtic2
rightOfTop_lscp.xtic2.priority = 1
rightOfTop_lscp.xtic2.y1 = 0.62
rightOfTop_lscp.xtic2.y2 = 0.61
rightOfTop_lscp.xtic2.line = ls

# member = ytic1
rightOfTop_lscp.ytic1.priority = 0
rightOfTop_lscp.ytic1.x1 = 0.19
rightOfTop_lscp.ytic1.x2 = 0.2
rightOfTop_lscp.ytic1.line = ls
## Adjusing Y tic------------------------
# member = ytic2
rightOfTop_lscp.ytic2.priority = 1
rightOfTop_lscp.ytic2.x1 = 0.71
rightOfTop_lscp.ytic2.x2 = 0.70
rightOfTop_lscp.ytic2.line = ls

# member = xlabel1
rightOfTop_lscp.xlabel1.priority = 1
rightOfTop_lscp.xlabel1.y = 0.6
rightOfTop_lscp.xlabel1.x = 0.7
rightOfTop_lscp.xlabel1.texttable = tt
rightOfTop_lscp.xlabel1.textorientation = to_bc


# adj Y label----------------------------------
# member = ylabel1
rightOfTop_lscp.ylabel1.priority = 1
rightOfTop_lscp.ylabel1.x = 0.67
rightOfTop_lscp.ylabel1.texttable = tt
rightOfTop_lscp.ylabel1.textorientation = to_d

#------Setting Legend------#
rightOfTop_lscp.legend.priority = 0
rightOfTop_lscp.legend.y1=.64
rightOfTop_lscp.legend.texttable=tt
rightOfTop_lscp.legend.x1=0.22
rightOfTop_lscp.legend.y2=0.63
rightOfTop_lscp.legend.x2=0.83
rightOfTop_lscp.legend.textorientation = to_d

rightOfTop_lscp.script('rightOfTop_lscp.scr')
sys.path.append(paths + '/'+ 'rightOfTop_lscp.scr')

##########--------------leftOfBot_lscp--------------###########
# The template  'leftOfBot_lscp' is for gettig plot on  left bottom corner of 
# the landscape template 

leftOfBot_lscp =x.createtemplate('leftOfBot_lscp','por_midof3')



# adjesting the length & width ratio
leftOfBot_lscp.scale(0.36, axis='x')#, font=10)
leftOfBot_lscp.scale(1.4, axis='y')

# Adjesting the position of figure
leftOfBot_lscp.move(-0.25, 'y')
leftOfBot_lscp.move(-0.15, 'x')

# member = source
leftOfBot_lscp.source.priority = 1
leftOfBot_lscp.source.x = 0.7
leftOfBot_lscp.source.y = 1.0767
leftOfBot_lscp.source.texttable = tt
leftOfBot_lscp.source.textorientation = to_dc

# member = title
leftOfBot_lscp.title.priority = 1
leftOfBot_lscp.title.x = 0.05
leftOfBot_lscp.title.y = .50
leftOfBot_lscp.title.texttable = tt
leftOfBot_lscp.title.textorientation = to_d

# member = units
leftOfBot_lscp.units.priority = 1
leftOfBot_lscp.units.x = 0.65
leftOfBot_lscp.units.y = 1.26384
leftOfBot_lscp.units.texttable = tt
leftOfBot_lscp.units.textorientation = to_br

# member = xtic1
leftOfBot_lscp.xtic1.priority = 0
leftOfBot_lscp.xtic1.y1 = 0.68
leftOfBot_lscp.xtic1.y2 = 0.69
leftOfBot_lscp.xtic1.x1 = 0.70
leftOfBot_lscp.xtic1.x2 = 0.69
leftOfBot_lscp.xtic1.line = ls
# adj X tic...................................
# member = xtic2
leftOfBot_lscp.xtic2.priority = 1
leftOfBot_lscp.xtic2.y1 = 0.13
leftOfBot_lscp.xtic2.y2 = 0.115
leftOfBot_lscp.xtic2.line = ls

# member = ytic1
leftOfBot_lscp.ytic1.priority = 0
leftOfBot_lscp.ytic1.x1 = 0.19
leftOfBot_lscp.ytic1.x2 = 0.2
leftOfBot_lscp.ytic1.line = ls
## Adjusing Y tic------------------------
# member = ytic2
leftOfBot_lscp.ytic2.priority = 1
leftOfBot_lscp.ytic2.x1 = 0.035
leftOfBot_lscp.ytic2.x2 = 0.04
leftOfBot_lscp.ytic2.line = ls

# member = xlabel1
leftOfBot_lscp.xlabel1.priority = 1
leftOfBot_lscp.xlabel1.y = 0.11
leftOfBot_lscp.xlabel1.x = 0.7
leftOfBot_lscp.xlabel1.texttable = tt
leftOfBot_lscp.xlabel1.textorientation = to_bc

# member = xlabel2
leftOfBot_lscp.xlabel2.priority = 0
leftOfBot_lscp.xlabel2.y = 0
leftOfBot_lscp.xlabel2.texttable = tt
leftOfBot_lscp.xlabel2.textorientation = to_d
# adj Y label----------------------------------
# member = ylabel1
leftOfBot_lscp.ylabel1.priority = 1
leftOfBot_lscp.ylabel1.x = 0.01
leftOfBot_lscp.ylabel1.texttable = tt
leftOfBot_lscp.ylabel1.textorientation = to_d

# member = ylabel2
leftOfBot_lscp.ylabel2.priority = 0
leftOfBot_lscp.ylabel2.x = 0
leftOfBot_lscp.ylabel2.texttable = tt
leftOfBot_lscp.ylabel2.textorientation = to_d


#------Setting Legend------#
leftOfBot_lscp.legend.priority = 0
leftOfBot_lscp.legend.y1=.64
leftOfBot_lscp.legend.texttable=tt
leftOfBot_lscp.legend.x1=0.22
leftOfBot_lscp.legend.y2=0.63
leftOfBot_lscp.legend.x2=0.83
leftOfBot_lscp.legend.textorientation = to_d





leftOfBot_lscp.script('leftOfBot_lscp.scr')
sys.path.append(paths + '/'+ 'leftOfBot_lscp.scr')
##########--------------midOfBot_lscp--------------###########
# The template  'midOfBot_lscp' is for gettig plot on  mid bottom of 
# the landscape template 

midOfBot_lscp =x.createtemplate('midOfBot_lscp','por_midof3')

# adjesting the length & width ratio
midOfBot_lscp.scale(0.36, axis='x')#, font=10)
midOfBot_lscp.scale(1.4, axis='y')

# Adjesting the position of figure
midOfBot_lscp.move(-0.25, 'y')
midOfBot_lscp.move(0.18, 'x')


# member = source
midOfBot_lscp.source.priority = 1
midOfBot_lscp.source.x = 0.7
midOfBot_lscp.source.y = 1.0767
midOfBot_lscp.source.texttable = tt
midOfBot_lscp.source.textorientation = to_dc

# member = title
midOfBot_lscp.title.priority = 1
midOfBot_lscp.title.x = 0.38
midOfBot_lscp.title.y = .50
midOfBot_lscp.title.texttable = tt
midOfBot_lscp.title.textorientation = to_d

# member = units
midOfBot_lscp.units.priority = 1
midOfBot_lscp.units.x = 0.65
midOfBot_lscp.units.y = 1.26384
midOfBot_lscp.units.texttable = tt
midOfBot_lscp.units.textorientation = to_br


# member = xvalue
midOfBot_lscp.xvalue.priority = 1
midOfBot_lscp.xvalue.x = 0.2
midOfBot_lscp.xvalue.y = 0.6
midOfBot_lscp.xvalue.texttable = tt
midOfBot_lscp.xvalue.textorientation = to_d

# member = xtic1
midOfBot_lscp.xtic1.priority = 0
midOfBot_lscp.xtic1.y1 = 0.68
midOfBot_lscp.xtic1.y2 = 0.69
midOfBot_lscp.xtic1.x1 = 0.70
midOfBot_lscp.xtic1.x2 = 0.69
midOfBot_lscp.xtic1.line = ls

# adj X tic...................................
# member = xtic2
midOfBot_lscp.xtic2.priority = 1
midOfBot_lscp.xtic2.y1 = 0.13
midOfBot_lscp.xtic2.y2 = 0.115
midOfBot_lscp.xtic2.line = ls

# member = ytic1
midOfBot_lscp.ytic1.priority = 0
midOfBot_lscp.ytic1.x1 = 0.19
midOfBot_lscp.ytic1.x2 = 0.2
midOfBot_lscp.ytic1.line = ls
## Adjusing Y tic------------------------
# member = ytic2
midOfBot_lscp.ytic2.priority = 1
midOfBot_lscp.ytic2.x1 = 0.38
midOfBot_lscp.ytic2.x2 = 0.37
midOfBot_lscp.ytic2.line = ls

# member = xlabel1
midOfBot_lscp.xlabel1.priority = 1
midOfBot_lscp.xlabel1.y = 0.11
midOfBot_lscp.xlabel1.x = 0.7
midOfBot_lscp.xlabel1.texttable = tt
midOfBot_lscp.xlabel1.textorientation = to_bc

# member = xlabel2
midOfBot_lscp.xlabel2.priority = 0
midOfBot_lscp.xlabel2.y = 0
midOfBot_lscp.xlabel2.texttable = tt
midOfBot_lscp.xlabel2.textorientation = to_d
# adj Y label----------------------------------
# member = ylabel1
midOfBot_lscp.ylabel1.priority = 1
midOfBot_lscp.ylabel1.x = 0.342
midOfBot_lscp.ylabel1.texttable = tt
midOfBot_lscp.ylabel1.textorientation = to_d

#------Setting Legend------#
midOfBot_lscp.legend.priority = 1
midOfBot_lscp.legend.y1=.049
midOfBot_lscp.legend.texttable=tt
midOfBot_lscp.legend.x1=0.20
midOfBot_lscp.legend.y2=0.035
midOfBot_lscp.legend.x2=0.81
midOfBot_lscp.legend.textorientation = to_d  

midOfBot_lscp.script('midOfBot_lscp.scr')
sys.path.append(paths + '/'+ 'midOfBot_lscp.scr')  

##########--------------rightOfBot_lscp--------------###########
# The template  'rightOfBot_lscp' is for gettig plot on  right bottom corner of 
# the landscape template 

rightOfBot_lscp =x.createtemplate('rightOfBot_lscp', 'por_botof3')

# adjesting the length & width ratio
rightOfBot_lscp.scale(.36, axis='x')#, font=10)
rightOfBot_lscp.scale(1.4, axis='y')

# Adjesting the position of figure
rightOfBot_lscp.move(0.07, 'y')
rightOfBot_lscp.move(0.51, 'x')


# member = source
rightOfBot_lscp.source.priority = 1
rightOfBot_lscp.source.x = 0.7
rightOfBot_lscp.source.y = 1.0767
rightOfBot_lscp.source.texttable = tt
rightOfBot_lscp.source.textorientation = to_dc

# member = title
rightOfBot_lscp.title.priority = 1
rightOfBot_lscp.title.x = 0.71
rightOfBot_lscp.title.y = 0.50
rightOfBot_lscp.title.texttable = tt
rightOfBot_lscp.title.textorientation = to_d

# member = units
rightOfBot_lscp.units.priority = 0
rightOfBot_lscp.units.x = 0.65
rightOfBot_lscp.units.y = 1.26384
rightOfBot_lscp.units.texttable = tt
rightOfBot_lscp.units.textorientation = to_br


# member = xtic1
rightOfBot_lscp.xtic1.priority = 0
rightOfBot_lscp.xtic1.y1 = 0.68
rightOfBot_lscp.xtic1.y2 = 0.69
rightOfBot_lscp.xtic1.x1 = 0.70
rightOfBot_lscp.xtic1.x2 = 0.69
rightOfBot_lscp.xtic1.line = ls

# adj X tic...................................
# member = xtic2
rightOfBot_lscp.xtic2.priority = 1
rightOfBot_lscp.xtic2.y1 = 0.13
rightOfBot_lscp.xtic2.y2 = 0.115
rightOfBot_lscp.xtic2.line = ls

# member = ytic1
rightOfBot_lscp.ytic1.priority = 0
rightOfBot_lscp.ytic1.x1 = 0.19
rightOfBot_lscp.ytic1.x2 = 0.2
rightOfBot_lscp.ytic1.line = ls
## Adjusing Y tic------------------------
# member = ytic2
rightOfBot_lscp.ytic2.priority = 1
rightOfBot_lscp.ytic2.x1 = 0.71
rightOfBot_lscp.ytic2.x2 = 0.70
rightOfBot_lscp.ytic2.line = ls

# member = xlabel1
rightOfBot_lscp.xlabel1.priority = 1
rightOfBot_lscp.xlabel1.y = 0.11
rightOfBot_lscp.xlabel1.x = 0.7
rightOfBot_lscp.xlabel1.texttable = tt
rightOfBot_lscp.xlabel1.textorientation = to_bc


# adj Y label----------------------------------
# member = ylabel1
rightOfBot_lscp.ylabel1.priority = 1
rightOfBot_lscp.ylabel1.x = 0.67
rightOfBot_lscp.ylabel1.texttable = tt
rightOfBot_lscp.ylabel1.textorientation = to_d

rightOfBot_lscp.legend.priority = 0

rightOfBot_lscp.script('rightOfBot_lscp.scr')
sys.path.append(paths + '/'+ 'rightOfBot_lscp.scr') 
 








