import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import cdms2


def format_date(x, pos=None):
    '''
    Get the appropriate the index of the time axis (x-axis). And get its
    corresponding component time object. Convert that into needed string.
    '''
    if x in dtime:
        position = dtime.index(x)
        date = str(dCompTime[position]).split(' ')[0]
    else:
        date = ''
    return date

# initialize the plot
fig = plt.figure()
ax = fig.add_subplot(111)

# get the correlation data
f = cdms2.open('./24/ugrdprs_T254_2010_daily_f24hr_anomaly_correlation.nc')
data = f('ugrdprs', time = ('2010-6-1', '2010-6-30'))

# get the time axis of the correlation as list and as component time
dtime = list(data.getTime())
dCompTime = data.getTime().asComponentTime()

# plot the correlation
ax.plot(dtime, data, '.-', label = '24 Hr')

# set the properties of the plot
plt.xlabel('Time')
plt.ylabel('Correlation')
plt.title('T254 Anomaly Correlation')
plt.legend(('24 Hr',))

# change the x-axis label by calling the 'format_date' function
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
fig.autofmt_xdate()
plt.show()

# save it as img
fig.savefig("correlation.png", dpi=(640/8))
