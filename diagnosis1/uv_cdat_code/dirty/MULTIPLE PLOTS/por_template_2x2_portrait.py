import cdms2
import cdutil
import numpy
import numpy.ma
import vcs
import os
import sys
# Getting the path 
paths = os.getcwd()

# Initialising VCS
x = vcs.init()
x.portrait()


# Defining the text type

tt=x.createtexttable('new', 'std')
tt.font=1
tt.expansion=150
tt.priority=1

# Defining the text height & orientation 
to_d=x.createtextorientation('new', 'default')
to_d.height=30
to_d.angle=0

to_dc=x.gettextorientation('defcentup')
to_bc=x.createtextorientation('new_bc', 'botcenter')
to_bc.height=32
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


##########--------------leftOfTop_portrait--------------###########

# The template  ''leftOfTop_portrait' is for gettig plot on  left top corner of 
# the portrait template 
leftOfTop_prt =x.createtemplate('leftOfTop_prt','por_topof3')
# adjesting the length & width ratio
leftOfTop_prt.scale(0.62, axis='x')#, font=10)
leftOfTop_prt.scale(1.54, axis='y')

# Adjesting the position of figure
leftOfTop_prt.move(-0.115, 'y')
leftOfTop_prt.move(-0.13, 'x')

# member = source
leftOfTop_prt.source.priority = 1
leftOfTop_prt.source.x = 0.7
leftOfTop_prt.source.y = 1.0767
leftOfTop_prt.source.texttable = tt
leftOfTop_prt.source.textorientation = to_dc

# member = title
leftOfTop_prt.title.priority = 1
leftOfTop_prt.title.x = 0.08
leftOfTop_prt.title.y = .98
leftOfTop_prt.title.texttable = tt
leftOfTop_prt.title.textorientation = to_d

# member = units
leftOfTop_prt.units.priority = 1
leftOfTop_prt.units.x = 0.65
leftOfTop_prt.units.y = 1.26384
leftOfTop_prt.units.texttable = tt
leftOfTop_prt.units.textorientation = to_br

# member = xtic1
leftOfTop_prt.xtic1.priority = 1
leftOfTop_prt.xtic1.y1 = 0.575
leftOfTop_prt.xtic1.y2 = 0.565
leftOfTop_prt.xtic1.line = ls
# adj X tic...................................
# member = xtic2
leftOfTop_prt.xtic2.priority = 0
leftOfTop_prt.xtic2.y1 = 0.62
leftOfTop_prt.xtic2.y2 = 0.61
leftOfTop_prt.xtic2.line = ls

# member = ytic1
leftOfTop_prt.ytic1.priority = 0
leftOfTop_prt.ytic1.x1 = 0.2
leftOfTop_prt.ytic1.x2 = 0.19
leftOfTop_prt.ytic1.line = ls
## Adjusing Y tic------------------------
# member = ytic2
leftOfTop_prt.ytic2.priority = 1
leftOfTop_prt.ytic2.x1 = 0.07
leftOfTop_prt.ytic2.x2 = 0.055
leftOfTop_prt.ytic2.line = ls

# member = xlabel1
leftOfTop_prt.xlabel1.priority = 1
leftOfTop_prt.xlabel1.y = 0.55
leftOfTop_prt.xlabel1.texttable = tt
leftOfTop_prt.xlabel1.textorientation = to_bc

# member = xlabel2
leftOfTop_prt.xlabel2.priority = 0
leftOfTop_prt.xlabel2.y = 0
leftOfTop_prt.xlabel2.texttable = tt
leftOfTop_prt.xlabel2.textorientation = to_d
# adj Y label----------------------------------
# member = ylabel1
leftOfTop_prt.ylabel1.priority = 1
leftOfTop_prt.ylabel1.x = 0.009
leftOfTop_prt.ylabel1.texttable = tt
leftOfTop_prt.ylabel1.textorientation = to_d

# member = ylabel2
leftOfTop_prt.ylabel2.priority = 0
leftOfTop_prt.ylabel2.x = 0
leftOfTop_prt.ylabel2.texttable = tt
leftOfTop_prt.ylabel2.textorientation = to_d


#------Setting Legend------#
leftOfTop_prt.legend.priority = 0
leftOfTop_prt.legend.y1=.64
leftOfTop_prt.legend.texttable=tt
leftOfTop_prt.legend.x1=0.22
leftOfTop_prt.legend.y2=0.63
leftOfTop_prt.legend.x2=0.83
leftOfTop_prt.legend.textorientation = to_d




leftOfTop_prt.dataname.priority = 0
leftOfTop_prt.crdate.priority = 0
leftOfTop_prt.crtime.priority = 0
leftOfTop_prt.function.priority = 0
leftOfTop_prt.logicalmask.priority = 0
leftOfTop_prt.transformation.priority = 0
leftOfTop_prt.comment1.priority = 0
leftOfTop_prt.comment2.priority = 0
leftOfTop_prt.comment3.priority = 0
leftOfTop_prt.comment4.priority = 0
leftOfTop_prt.xname.priority = 0
leftOfTop_prt.yname.priority = 0
leftOfTop_prt.zname.priority = 0
leftOfTop_prt.tname.priority = 0
leftOfTop_prt.xunits.priority = 0
leftOfTop_prt.yunits.priority = 0
leftOfTop_prt.zunits.priority = 0
leftOfTop_prt.tunits.priority = 0
leftOfTop_prt.xvalue.priority = 0
leftOfTop_prt.yvalue.priority = 0
leftOfTop_prt.zvalue.priority = 0
leftOfTop_prt.tvalue.priority = 0
leftOfTop_prt.mean.priority = 0
leftOfTop_prt.min.priority = 0
leftOfTop_prt.max.priority = 0
#prt---stands for portrait
leftOfTop_prt.script('leftOfTop_prt.scr') 
sys.path.append(paths + '/'+'leftOfTop_prt.scr')


################
##########--------------rightOfTop_prt--------------###########

# The template  'rightOfTop_prt' is for gettig plot on  right top corner of 
# the portrait template 

rightOfTop_prt =x.createtemplate('rightOfTop_prt', 'por_topof3')

rightOfTop_prt.dataname.priority = 0
rightOfTop_prt.crdate.priority = 0
rightOfTop_prt.crtime.priority = 0
rightOfTop_prt.function.priority = 0
rightOfTop_prt.logicalmask.priority = 0
rightOfTop_prt.transformation.priority = 0
rightOfTop_prt.comment1.priority = 0
rightOfTop_prt.comment2.priority = 0
rightOfTop_prt.comment3.priority = 0
rightOfTop_prt.comment4.priority = 0
rightOfTop_prt.xname.priority = 0
rightOfTop_prt.yname.priority = 0
rightOfTop_prt.zname.priority = 0
rightOfTop_prt.tname.priority = 0
rightOfTop_prt.xunits.priority = 0
rightOfTop_prt.yunits.priority = 0
rightOfTop_prt.zunits.priority = 0
rightOfTop_prt.tunits.priority = 0
rightOfTop_prt.xvalue.priority = 0
rightOfTop_prt.yvalue.priority = 0
rightOfTop_prt.zvalue.priority = 0
rightOfTop_prt.tvalue.priority = 0
rightOfTop_prt.mean.priority = 0
rightOfTop_prt.min.priority = 0
rightOfTop_prt.max.priority = 0


# adjesting the length & width ratio
rightOfTop_prt.scale(0.62, axis='x')#, font=10)
rightOfTop_prt.scale(1.54, axis='y')

# Adjesting the position of figure
rightOfTop_prt.move(-0.115, 'y')
rightOfTop_prt.move(0.38, 'x')


# member = source
rightOfTop_prt.source.priority = 1
rightOfTop_prt.source.x = 0.7
rightOfTop_prt.source.y = 1.0767
rightOfTop_prt.source.texttable = tt
rightOfTop_prt.source.textorientation = to_dc

# member = title
rightOfTop_prt.title.priority = 1
rightOfTop_prt.title.x = 0.59
rightOfTop_prt.title.y = .98
rightOfTop_prt.title.texttable = tt
rightOfTop_prt.title.textorientation = to_d

# member = units
rightOfTop_prt.units.priority = 0
rightOfTop_prt.units.x = 0.65
rightOfTop_prt.units.y = 1.26384
rightOfTop_prt.units.texttable = tt
rightOfTop_prt.units.textorientation = to_br




# member = xtic1
rightOfTop_prt.xtic1.priority = 0
rightOfTop_prt.xtic1.y1 = 0.68
rightOfTop_prt.xtic1.y2 = 0.69
rightOfTop_prt.xtic1.x1 = 0.70
rightOfTop_prt.xtic1.x2 = 0.69
rightOfTop_prt.xtic1.line = ls

# adj X tic...................................
# member = xtic2
rightOfTop_prt.xtic2.priority = 1
rightOfTop_prt.xtic2.y1 = 0.575
rightOfTop_prt.xtic2.y2 = 0.565
rightOfTop_prt.xtic2.line = ls

# member = ytic1
rightOfTop_prt.ytic1.priority = 0
rightOfTop_prt.ytic1.x1 = 0.19
rightOfTop_prt.ytic1.x2 = 0.2
rightOfTop_prt.ytic1.line = ls
## Adjusing Y tic------------------------
# member = ytic2
rightOfTop_prt.ytic2.priority = 1
rightOfTop_prt.ytic2.x1 = 0.58
rightOfTop_prt.ytic2.x2 = 0.565
rightOfTop_prt.ytic2.line = ls

# member = xlabel1
rightOfTop_prt.xlabel1.priority = 1
rightOfTop_prt.xlabel1.y = 0.55

rightOfTop_prt.xlabel1.texttable = tt
rightOfTop_prt.xlabel1.textorientation = to_bc


# adj Y label----------------------------------
# member = ylabel1
rightOfTop_prt.ylabel1.priority = 1
rightOfTop_prt.ylabel1.x = 0.520
rightOfTop_prt.ylabel1.texttable = tt
rightOfTop_prt.ylabel1.textorientation = to_d

#------Setting Legend------#
rightOfTop_prt.legend.priority = 0



rightOfTop_prt.script('rightOfTop_prt.scr')
sys.path.append(paths + '/'+ 'rightOfTop_prt.scr')
##########--------------leftOfBot_prt--------------###########
# The template  'leftOfBot_prt' is for gettig plot on  left bottom corner of 
# the landscape template 

leftOfBot_prt =x.createtemplate('leftOfBot_prt','por_midof3')



# adjesting the length & width ratio
leftOfBot_prt.scale(0.62, axis='x')#, font=10)
leftOfBot_prt.scale(1.54, axis='y')

# Adjesting the position of figure
leftOfBot_prt.move(-0.26, 'y')
leftOfBot_prt.move(-0.13, 'x')

# member = source
leftOfBot_prt.source.priority = 1
leftOfBot_prt.source.x = 0.7
leftOfBot_prt.source.y = 1.0767
leftOfBot_prt.source.texttable = tt
leftOfBot_prt.source.textorientation = to_dc

# member = title
leftOfBot_prt.title.priority = 1
leftOfBot_prt.title.x = 0.08
leftOfBot_prt.title.y = .52
leftOfBot_prt.title.texttable = tt
leftOfBot_prt.title.textorientation = to_d

# member = units
leftOfBot_prt.units.priority = 1
leftOfBot_prt.units.x = 0.65
leftOfBot_prt.units.y = 1.26384
leftOfBot_prt.units.texttable = tt
leftOfBot_prt.units.textorientation = to_br

# member = xtic1
leftOfBot_prt.xtic1.priority = 0
leftOfBot_prt.xtic1.y1 = 0.68
leftOfBot_prt.xtic1.y2 = 0.69
leftOfBot_prt.xtic1.x1 = 0.70
leftOfBot_prt.xtic1.x2 = 0.69
leftOfBot_prt.xtic1.line = ls
# adj X tic...................................
# member = xtic2
leftOfBot_prt.xtic2.priority = 1
leftOfBot_prt.xtic2.y1 = 0.12
leftOfBot_prt.xtic2.y2 = 0.108
leftOfBot_prt.xtic2.line = ls

# member = ytic1
leftOfBot_prt.ytic1.priority = 0
leftOfBot_prt.ytic1.x1 = 0.19
leftOfBot_prt.ytic1.x2 = 0.2
leftOfBot_prt.ytic1.line = ls
## Adjusing Y tic------------------------
# member = ytic2
leftOfBot_prt.ytic2.priority = 1
leftOfBot_prt.ytic2.x1 = 0.07
leftOfBot_prt.ytic2.x2 = 0.055
leftOfBot_prt.ytic2.line = ls

# member = xlabel1
leftOfBot_prt.xlabel1.priority = 1
leftOfBot_prt.xlabel1.y = 0.085
leftOfBot_prt.xlabel1.texttable = tt
leftOfBot_prt.xlabel1.textorientation = to_bc

# member = xlabel2
leftOfBot_prt.xlabel2.priority = 0

# adj Y label----------------------------------
# member = ylabel1
leftOfBot_prt.ylabel1.priority = 1
leftOfBot_prt.ylabel1.x = 0.009
leftOfBot_prt.ylabel1.texttable = tt
leftOfBot_prt.ylabel1.textorientation = to_d

# member = ylabel2
leftOfBot_prt.ylabel2.priority = 0
leftOfBot_prt.ylabel2.x = 0
leftOfBot_prt.ylabel2.texttable = tt
leftOfBot_prt.ylabel2.textorientation = to_d


#------Setting Legend------#
leftOfBot_prt.legend.priority = 0
leftOfBot_prt.legend.y1=.64
leftOfBot_prt.legend.texttable=tt
leftOfBot_prt.legend.x1=0.22
leftOfBot_prt.legend.y2=0.63
leftOfBot_prt.legend.x2=0.83
leftOfBot_prt.legend.textorientation = to_d


leftOfBot_prt.script('leftOfBot_prt.scr')
sys.path.append(paths + '/'+ 'leftOfBot_prt.scr')

###########--------------rightOfBot_prt--------------###########
# The template  'rightOfBot_prt' is for gettig plot on  right bottom corner of 
# the portrait template 

rightOfBot_prt =x.createtemplate('rightOfBot_prt', 'por_botof3')

# adjesting the length & width ratio
rightOfBot_prt.scale(.62, axis='x')#, font=10)
rightOfBot_prt.scale(1.54, axis='y')

# Adjesting the position of figure
rightOfBot_prt.move(0.065, 'y')
rightOfBot_prt.move(0.38, 'x')


# member = source
rightOfBot_prt.source.priority = 1
rightOfBot_prt.source.x = 0.7
rightOfBot_prt.source.y = 1.0767
rightOfBot_prt.source.texttable = tt
rightOfBot_prt.source.textorientation = to_dc

# member = title
rightOfBot_prt.title.priority = 1
rightOfBot_prt.title.x = 0.59
rightOfBot_prt.title.y = 0.52
rightOfBot_prt.title.texttable = tt
rightOfBot_prt.title.textorientation = to_d

# member = units
rightOfBot_prt.units.priority = 0
rightOfBot_prt.units.x = 0.65
rightOfBot_prt.units.y = 1.26384
rightOfBot_prt.units.texttable = tt
rightOfBot_prt.units.textorientation = to_br


# member = xtic1
rightOfBot_prt.xtic1.priority = 0
rightOfBot_prt.xtic1.y1 = 0.68
rightOfBot_prt.xtic1.y2 = 0.69
rightOfBot_prt.xtic1.x1 = 0.70
rightOfBot_prt.xtic1.x2 = 0.69
rightOfBot_prt.xtic1.line = ls

# adj X tic...................................
# member = xtic2
rightOfBot_prt.xtic2.priority = 1
rightOfBot_prt.xtic2.y1 = 0.12
rightOfBot_prt.xtic2.y2 = 0.108
rightOfBot_prt.xtic2.line = ls

# member = ytic1
rightOfBot_prt.ytic1.priority = 0

## Adjusing Y tic------------------------
# member = ytic2
rightOfBot_prt.ytic2.priority = 1
rightOfBot_prt.ytic2.x1 = 0.58
rightOfBot_prt.ytic2.x2 = 0.565
rightOfBot_prt.ytic2.line = ls

# member = xlabel1
rightOfBot_prt.xlabel1.priority = 1
rightOfBot_prt.xlabel1.y = 0.085
rightOfBot_prt.xlabel1.texttable = tt
rightOfBot_prt.xlabel1.textorientation = to_bc


# adj Y label----------------------------------
# member = ylabel1
rightOfBot_prt.ylabel1.priority = 1
rightOfBot_prt.ylabel1.x = 0.520
rightOfBot_prt.ylabel1.texttable = tt
rightOfBot_prt.ylabel1.textorientation = to_d

rightOfBot_prt.legend.priority = 1
rightOfBot_prt.legend.y1=0.03
rightOfBot_prt.legend.x1=0.12
rightOfBot_prt.legend.y2=0.04
rightOfBot_prt.legend.x2=0.91
rightOfBot_prt.legend.textorientation = to_d
rightOfBot_prt.legend.texttable=tt

rightOfBot_prt.script('rightOfBot_prt.scr')
sys.path.append(paths + '/'+ 'rightOfBot_prt.scr') 


