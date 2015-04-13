import cdms2, sys, numpy

# Determine the (lat, lon) and (j, i) coordinates of a model on an
# curvilinear grid CLOSEST to a given (lat_search, lon_search) coordinate

# Extracted from deep_ocean/get_TS_cmip5.py
# J-Y Peterschmitt - LSCE - France
datapath = 'zos_Omon_ACCESS1-0_rcp45_r1i1p1.xml'
v_name = 'zos'
dp_lat = int(raw_input("Enter the latitude you looking for : "))
dp_lon = int(raw_input("Enter the longitude you looking for : "))

f_input = cdms2.open(datapath, 'r')
# Get one time slice of the model data at the specified depth,
# with the longitudes centered on the data point
v_slice = f_input(v_name, time=slice(1), squeeze=1)

# Get the latitudes and the longitudes
# (note, we get rid of the metadata and keep only the array values)
if 'lat' not in f_input.listvariables():
    print '        *          NO "lat" variable! This file is probably on a regular grid...'
    f_input.close()
    sys.exit()

lat_slab = f_input('lat').data
lon_slab = f_input('lon').data
(nb_j, nb_i) = lat_slab.shape

# Compute the distance between model points and the data point
# Method #1
delta_lat = lat_slab - dp_lat
delta_lon1 = numpy.absolute(lon_slab - dp_lon)
delta_lon2 = numpy.absolute(delta_lon1 - 360)
delta_lon = numpy.minimum(delta_lon1, delta_lon2)
dp_dist1 = numpy.sqrt(delta_lat * delta_lat + delta_lon * delta_lon)

# Create a masked variable from dp_dist and the original variable
dp_dist1_var = cdms2.createVariable(dp_dist1, mask=v_slice.mask)

# Compute the distance between model points and the data point
# Method #2
# All the points on the sphere (radius = 1) are projected in a 3D
# geocentric referential, and we then compute the distance between
# 2 points along a straight line (through the sphere)
conv_rad = numpy.pi / 180.
x_slab = numpy.cos(conv_rad * lat_slab) * numpy.cos(conv_rad * lon_slab)
y_slab = numpy.cos(conv_rad * lat_slab) * numpy.sin(conv_rad * lon_slab)
z_slab = numpy.sin(conv_rad * lat_slab)
dp_x = numpy.cos(conv_rad * dp_lat) * numpy.cos(conv_rad * dp_lon)
dp_y = numpy.cos(conv_rad * dp_lat) * numpy.sin(conv_rad * dp_lon)
dp_z = numpy.sin(conv_rad * dp_lat)
dp_dist2 = numpy.sqrt((x_slab - dp_x) * (x_slab - dp_x) +
                      (y_slab - dp_y) * (y_slab - dp_y) +
                      (z_slab - dp_z) * (z_slab - dp_z))
dp_dist2_var = cdms2.createVariable(dp_dist2, mask=v_slice.mask)

# Get the indices of the minimum value, to get the
# coordinates of the model point closest to the data point
dist1_min_idx = numpy.ma.argmin(dp_dist1_var)
dist2_min_idx = numpy.ma.argmin(dp_dist2_var)
#if dist1_min_idx <> dist2_min_idx:

if dist1_min_idx < dist2_min_idx:
    dist_type = 1
elif dist1_min_idx > dist2_min_idx:
    dist_type = 2
else:
    print '        * Warning! We do not find exactly the same closest model point'
    print '        *          with the different distance types'
    print '        * dist1, dist2 =', dist1_min_idx, dist2_min_idx
    print '        * We still use the selected distance type',
    print '        1. Use distance b/w the points - Method'
    print '        2. All the points on the sphere  - Method'
    dist_type = int(raw_input("Enter you choice : "))

# Compute the indices of the closest point, based on
# the specified distance computation scheme
if dist_type == 1:
    print 'Using distance b/w the points - Method'
    dist_min_idx = dist1_min_idx
    dp_dist_var_selected = dp_dist1_var
elif dist_type == 2:
    print 'Using all the points on the sphere  - Method'
    dist_min_idx = dist2_min_idx
    dp_dist_var_selected = dp_dist2_var
else:
    raise 'Distance method not implemented:', dist_type

j_min_idx = dist_min_idx / nb_i
i_min_idx = dist_min_idx % nb_i

dist_value = dp_dist_var_selected[j_min_idx, i_min_idx]
dd = {}
lat_closest = lat_slab[j_min_idx, i_min_idx]
lon_closest = lon_slab[j_min_idx, i_min_idx]
dd['j_min_idx'] = j_min_idx
dd['i_min_idx'] = i_min_idx
dd['lat_val'] = lat_closest
dd['lon_val'] = lon_closest
d_lat = abs(dp_lat - lat_closest)
d_lon1 = abs(lon_closest - dp_lon)
d_lon2 = abs(d_lon1 - 360)
d_lon = min(d_lon1, d_lon2)
value = v_slice[j_min_idx, i_min_idx]
print '      Model grid size: (lat x lon) = %i x %i' % (nb_j, nb_i)
#print '        Closest model depth (k) = %8.2f (%2i)  (delta = %8.2f)' % \
#      (depth_select_val, depth_select_idx, d_depth)
print '        Closest model point: lat (j) = %8.3f (%3i) (delta = %8.3f)  -  lon (i) = %8.3f (%3i) (delta = %8.3f)' % \
      (lat_closest, j_min_idx, d_lat, lon_closest, i_min_idx, d_lon)
print ' The value is = %r for the given lat = %r and lon = %r ' % (value, dp_lat, dp_lon)

#>>> f_input('zos', time=slice(1), j=(136), i=(339), squeeze=1)
#0.91628397
#>>> zzz = f_input('zos', j=(136), i=(339), squeeze=1)
#>>> zzz.shape
#(1140,)



