import  cdms2, os, sys
__curDir__ = os.path.dirname(__file__)
diagDir = os.path.abspath(os.path.join(__curDir__, '../../mjo/level2/phase3d'))
# adding the previous diagnosisutils path to python path
sys.path.append(diagDir)
from phase3d import miso_phase3d

# plotting MJO Phase diagrams
f = cdms2.open('PC-Time-Series-I_and_II_Rainfall.nc')

# Summer Data Extraction
#pc1 = f('pct1', time=('1997-1-1', '2008-12-31'))
#npc1 = (pc1 - pc1.mean()) / pc1.std()
#npc1 *= -1
#print pc1.shape
#npc1 = npc1(time=('2000-6-1', '2000-9-30'))
#npc1.id = 'Normalized PC1'
#print npc1.shape
#pc2 = f('pct2', time=('1997-1-1', '2008-12-31'))
#npc2 = (pc2 - pc2.mean()) / pc2.std()
#npc2 *= -1

#npc2 = npc2(time=('2000-6-1', '2000-9-30'))
#npc2.id = 'Normalized PC2'

year = '2000'
pc1 = f('pct1', time=(year+'-6-1', year+'-9-30'))
npc1 = (pc1 - pc1.mean()) / pc1.std()
#npc1 *= -1
print pc1.shape
npc1.id = 'Normalized PC1'
print npc1.shape
pc2 = f('pct2', time=(year+'-6-1', year+'-9-30'))
npc2 = (pc2 - pc2.mean()) / pc2.std()
npc2 *= -1
npc2.id = 'Normalized PC2'


# plotting MJO Phase diagrams
f1 = cdms2.open('Amplitude_Phase_PCTS-I_and_II_Rainfall.nc')
phase_start = f1('amppha', time=year+'-6-1')(amp_pha=1)(squeeze=1)
phase_start = int(phase_start)
# summer mjo phase plotting
# here sxyphase is 3 for this ('1979-5-1', '1979-10-31') time season only.
# this is just demonstration that we can pass sxyphase purpose only.
x = miso_phase3d(npc1, npc2, sxyphase=None, #pposition1=None, 
            plocation='out', mintick=4, stitle1='GPCP Precip - year '+year) #,
#x = miso_phase3d(npc1, npc2, sxyphase=3, pposition1=None, plocation='in',
#                                      mintick=0, pdirection='anticlock')

outfilepath = os.path.abspath('miso_phase3d_'+year)
x.eps(outfilepath)
# $ epstopdf *.eps  # this cmd will convert eps to pdf with HD
os.system("epstopdf %s.eps" % outfilepath)
# remove eps file 
#os.remove(outfilepath)

## only single red color plot of summer
#x = mjo_phase3d(npc1, npc2, sxyphase=3, colors=['red'], pposition1=None,
#                      plocation='in', mintick=0, pdirection='anticlock')

#x.ps('mjo_phase2d_summer_red')
## make memory free
#del x, npc1, npc2

## Winter Data Extraction
#npc1 = f('norm_pcs1', time=('1979-11-1', '1980-4-30'))
#npc1.id = 'Normalized PC1'
#npc2 = f('norm_pcs2', time=('1979-11-1', '1980-4-30'))
#npc2.id = 'Normalized PC2'
## winter mjo phase plotting
## this is generic function call demonstration. For MJO we can make sxyphase 
## as None and using default argument to the pposition1 as 5.
#x = mjo_phase3d(npc1, npc2, sxyphase=None, plocation='out', mintick=4)
#x.ps('mjo_phase2d_winter')
#f.close()

## only single red color plot of winter
#x = mjo_phase3d(npc1, npc2, sxyphase=None, colors='red', plocation='out', mintick=4)
#x.ps('mjo_phase2d_winter_red')
## make memory free
#del x, npc1, npc2


## plotting MISO Phase diagrams
#f = cdms2.open('miso_phases.nc')
#xdata = f('miso1')
#xdata.id = 'MISO1'
#ydata = f('miso2')
#ydata.id = 'MISO2'

#x = miso_phase3d(xdata, ydata, sxyphase=None, plocation='out', mintick=4)
#x.ps('miso_phase2d_monsoon')
#f.close()
## make memory free
#del x, xdata, ydata



