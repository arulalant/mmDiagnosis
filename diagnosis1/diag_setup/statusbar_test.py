from genutil import statusbar
prevall=0
previ=0
prevj=0
prevtxt=0
ni=100
nj=20
# status in tk gui
for i in range(ni):
    previ=statusbar(float(i)/ni,prev=previ,tk=1)
    for j in range(nj):
        prevj=statusbar(float(j)/nj,prev=prevj,tk=1)
        prevall=statusbar([float(i)/ni,float(j)/nj],prev=prevall,tk=1,title='Test')
        prevtxt=statusbar(float(j)/nj,prev=prevtxt,tk=1,title='Test')
    
#### Status in terminal
prev=0
for I in range(1000):
    prev=statusbar(I,total=1000, title='Status:',prev=prev)
print
# The final above empty print outside the loop is necessary 
# to endup with proper terminal '$' at its original position
