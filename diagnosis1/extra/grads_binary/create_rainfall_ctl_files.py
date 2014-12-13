import os

path = '/NCMRWF/ncmrwf_2011/rainfall/'
os.chdir(path)

months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']

ctl_file_content_part1 = '''
*             ddmmyy
options big_endian
undef -9999
title ncm fcst pptn mm/day
XDEF 41 LINEAR    60.0000  1.0000
YDEF 41 LINEAR     0.0000   1.0000
zdef   1 levels 1000
'''

ctl_file_content_part2 = '''
vars     1
pobs   00 99  pcp fcst
endvars
'''


filepath = 'dset  ^' #obs_03z010610_day00.bin

list_of_files = os.listdir('.')

list_of_bin_files = [ files for files in list_of_files if files.endswith('trm') ]


for bin_file in list_of_bin_files:    
	filename = bin_file.split('trm')[0]
	day = filename.split('obs_03z')[1]
	day = day.split('_')[0]
	date = day[:2]
	month = day[2:4]
	print date,month
	# defining time variable dynamically setting the date and month from the filename itself.
	time = 'tdef  1 linear %s%s2011 1dy' % ( date,months[int(month)-1])
	filename += 'ctl'
	# create the new ctl file
	ctl_file = open(filename,'w')
	print bin_file
	ctl_first_line = filepath + bin_file
	content = ctl_first_line + ctl_file_content_part1 + time + ctl_file_content_part2
	ctl_file.write(content)
	ctl_file.close()
	# closing the above ctl file
	print 'created file : %s ' % (filename)	

list_of_files = os.listdir('.')

list_of_ctl_files = [files for files in list_of_files if files.endswith('ctl') ]
list_of_ctl_files.sort()
print list_of_ctl_files
# creating file which contains all the ctl files in sorted order
ctl_files_name = open('all_ctl_files.txt','w')
for name in list_of_ctl_files:
	ctl_files_name.write(name+"\n")
	
ctl_files_name.close()
