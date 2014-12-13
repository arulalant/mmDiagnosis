try:
	from cdutil.region import *

	# selector regions variables
	CIndia = CentralIndiaRegion = domain(longitude = (73,90),latitude = (22,28) ) # (73-90 E) & (22-28 N)
	PenIndia = PeninsularIndiaRegion = domain(longitude = (74,85),latitude = (7,21) ) # (74-85 E) & (7-21 N)
	WcstIndia = WestCoastRegionOfIndia = domain(longitude = (70,78),latitude = (10,20) ) # (70-78 E) & (10-20 N)
	AIR = AllIndiaRegion = domain(longitude = (67,100),latitude = (7,37) ) # (67-100 E) & (7-37 N)
	India1 = domain(longitude = (20,140,'cc'),latitude = (-20,60,'cc') ) # (20-140 E) & (20 S - 60 N)
	India2 = domain(longitude = (40,120),latitude = (-10,40) ) # (40-120 E) & (10 S - 40 N)
	
except:
	import sys
	print  "you have to run this 'region.py' module under CDAT. We need to import cdutil.region for making our own region variables\n"
	sys.exit()

