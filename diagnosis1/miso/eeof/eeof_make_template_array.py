"""
Make template  array
written By: Rajappan
"""
import  vcs

tp=vcs.init()
tp.portrait()


def make_template_array(tp, Nrows, Ncols, xgap, ygap, Left_Margin, Right_Margin, Top_Margin, Bot_Margin ):
    tt=tp.createtexttable('new', 'std')
    tt.font=1

    #tt.expansion=150
    tt.priority=1
    
    tt_11=tp.createtexttable('new1', 'std')
    tt_11.font=6

    #tt_11.expansion=150
    tt_11.priority=1
    
	# Create text orientation
    tt1=tp.createtextorientation('new1', 'centerup')
    tt1.height=11
    tt1.angle=0
#	tt1.halign = 'center'
	
    tt2=tp.createtextorientation('new2', 'centerup')
    tt2.height=7
    tt2.angle=0
    
    tt3=tp.createtextorientation('new3', 'centerup')
    tt3.height=9
    tt3.angle=0
    
    tt4=tp.createtextorientation('new43', 'centerup')
    tt4.height=9
    tt4.angle=-90
	#
    template_array = []
	#, 'ASD')
    x=  (1 - Left_Margin -((Ncols-1) * xgap) - Right_Margin )/(Ncols)
#    print 'x =', x
    y = (1- Top_Margin -((Nrows-1) * ygap) - Bot_Margin )/Nrows
#    print 'y =', y 
    for i in range(Nrows):	
    	for j in range(Ncols):
            jstring = str(j)
            istring = str(i)
            xmove = Left_Margin + ((j+1)-1)*(x+xgap)
            ymove = 0.6-(Top_Margin + ((i+1)-1) * (y+ygap))
            template=tp.createtemplate('new'+ jstring + istring)
		
			#******************template**************#
			#template.ratio = 
            template.move(xmove, axis = 'x')
            template.move(ymove, axis = 'y')	
            template.scale(x, axis ='x')  
            template.scale(y, axis = 'y')	
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
            if ( i == 0 and j == 0):
                template.legend.priority = 0
                template.legend.y1=0.030
                template.legend.texttable=tt
                template.legend.x1=0.10
                template.legend.y2=0.038
                template.legend.x2=0.9
                template.legend.textorientation = tt1
                
                template.title.priority = 1
                template.title.x=0.50
                template.title.y = 0.99
                template.title.texttable=tt
                template.title.textorientation=tt3
                
                template.comment4.priority = 1
                template.comment4.texttable = tt_11
                template.comment4.textorientation = tt1
                template.comment4.x = 0.91
                template.comment4.y = 0.05
                
            else:
                template.legend.priority = 0
                template.title.priority = 0
            template.comment1.priority = 1
            template.comment1.texttable = tt
            template.comment1.textorientation = tt1
            template.comment1.x = xmove+x-0.03
            template.comment1.y = ymove+y+0.18
            
            template.comment2.priority = 1
            template.comment2.texttable = tt
            template.comment2.textorientation = tt4
            template.comment2.x = xmove+x-0.33
            template.comment2.y = ymove+y+0.08
            
            template.comment3.priority = 1
            template.comment3.texttable = tt
            template.comment3.textorientation = tt1
            template.comment3.x = 0.70#xmove+x-0.1
            template.comment3.y = 0.97#ymove+y+0.21
            
            
            template.units.priority = 0
            template.xtic1.priority = 1
            template.xtic2.priority = 0
            template.ytic1.priority = 1
            template.ytic1.height = 0
            template.ytic2.priority = 0
			#template.ytic2.expansion = 300
			#template.ytic2.x1 = xmove+x+0.02
			#template.ytic2.x2 = xmove+x
			
			#template.xlabel1.priority = 0
            if (i==Nrows-1):
                template.xlabel1.priority = 1
                template.xlabel1.textorientation = tt2
                template.xlabel1.y=0.11
                
                template.xname.priority = 1
                template.xname.textorientation = tt1
                template.xname.y= 0.08
			#elif(i== Nrows-2 and j == Ncols-1):
			#	template.xlabel1.priority = 1
			#	template.xlabel1.textorientation = tt1
            else:
                template.xlabel1.priority = 0
            template.ylabel1.priority = 1
            template.ylabel1.x=0.52
            template.ylabel1.textorientation = tt2
            template.xlabel2.priority = 0
            if (j == Ncols-1):
                template.ylabel1.priority = 1
                template.ylabel1.x=0.13
                template.ylabel1.textorientation = tt2
                
			#elif(j== Ncols-2 and i == Nrows-1):
			#	template.ylabel2.priority = 1
			#	template.ylabel2.textorientation = tt2
            else:
                
                template.ylabel2.priority = 0
            template_array.append(template)
			#template.script('template.scr')
		# end of i in
	#end of j in
	
    return template_array
