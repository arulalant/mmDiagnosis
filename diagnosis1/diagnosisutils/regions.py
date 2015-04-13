import cdutil.region as region

# selector regions variables
PGlobal = PartialGlobal = region.domain(longitude=(0, 360, 'cc'), latitude=(-50, 50, 'cc')) # (0-360 E) & (50 S-50 N)
CIndia = region.domain(longitude=(67, 73, 'cc'), latitude=(20, 22, 'cc'))
#region.domain(longitude=(67, 90, 'cc'), latitude=(20, 28, 'cc'))
#CentralIndiaRegion = region.domain(longitude=(73, 90, 'cc'), latitude=(22, 28, 'cc')) # (73-90 E) & (22-28 N)
PenIndia = PeninsularIndiaRegion = region.domain(longitude=(74, 85, 'cc'), latitude=(7, 21, 'cc')) # (74-85 E) & (7-21 N)
WcstIndia = WestCoastRegionOfIndia = region.domain(longitude=(70, 78, 'cc'), latitude=(10, 20, 'cc')) # (70-78 E) & (10-20 N)
AIR = AllIndiaRegion = region.domain(longitude=(67, 100, 'cc'), latitude=(7, 37, 'cc')) # (67-100 E) & (7-37 N)
India1 = region.domain(longitude=(20, 140, 'cc'), latitude=(-20, 60, 'cc')) # (20-140 E) & (20 S - 60 N)
India2 = region.domain(longitude=(40, 120, 'cc'), latitude=(-10, 40, 'cc')) # (40-120 E) & (10 S - 40 N)
India3 = region.domain(longitude=(20, 140, 'cc'), latitude=(-10, 50, 'cc')) # (20-140 E) & (10 S - 50 N)
India = region.domain(longitude=(60, 100, 'cc'), latitude=(0, 40, 'cc')) # (60-100 E) & (Eq, 40 N)
#NWIndia = region.domain(longitude=(67, 73, 'cc'), latitude=(20, 22, 'cc'))
#CI+NWIndia=region.domain(longitude=(67, 90, 'cc'), latitude=(20, 28, 'cc'))


Northern_hemisphere = region.domain(longitude=(-180, 180, 'cc'), latitude=(20, 90, 'cc'))
Southern_hemisphere = region.domain(longitude=(-180, 180, 'cc'), latitude=(-90, -20, 'cc'))
North_America = region.domain(longitude=(-145, -60, 'cc'), latitude=(25, 60, 'cc'))
South_America = region.domain(longitude=(-120, 0, 'cc'), latitude=(-60, 20, 'cc'))
Europe = region.domain(longitude=(-10, 28, 'cc'), latitude=(25, 70, 'cc'))
Asia = region.domain(longitude=(50, 180, 'cc'), latitude=(0, 80, 'cc'))#-->ECMWF my bound
#Asia = region.domain(longitude=(60, 145, 'cc'), latitude=(25, 65, 'cc'))#-->ECMWF original
Australia = region.domain(longitude=(90, 180, 'cc'), latitude=(-55, -10, 'cc'))
Africa = region.domain(longitude=(-40, 80, 'cc'), latitude=(-40, 40, 'cc'))
Tropic = region.domain(longitude=(90, 180, 'cc'), latitude=(-20, 20, 'cc'))

# define region -1, i.e extend lat, lon by 1 degree in both directions.
# It may help to extract region while doing regrid.
# CIndia_1 = CIndia - 1.
PGlobal_1 = PartialGlobal_1 = region.domain(longitude=(0, 360, 'cc'), latitude=(-51, 51, 'cc'))
CIndia_1 = region.domain(longitude=(66, 74, 'cc'), latitude=(19, 23, 'cc'))
PenIndia_1 = PeninsularIndiaRegion_1 = region.domain(longitude=(73, 86, 'cc'), latitude=(6, 22, 'cc'))
WcstIndia_1 = WestCoastRegionOfIndia_1 = region.domain(longitude=(69, 79, 'cc'), latitude=(9, 21, 'cc'))
AIR_1 = AllIndiaRegion_1 = region.domain(longitude=(66, 101, 'cc'), latitude=(6, 38, 'cc'))
India1_1 = region.domain(longitude=(19, 141, 'cc'), latitude=(-19, 61, 'cc'))
India2_1 = region.domain(longitude=(39, 121, 'cc'), latitude=(-9, 41, 'cc'))
India3_1 = region.domain(longitude=(19, 141, 'cc'), latitude=(-9, 51, 'cc'))
India_1 = region.domain(longitude=(59, 101, 'cc'), latitude=(-1, 41, 'cc'))

Northern_hemisphere_1 = region.domain(longitude=(-180, 180, 'cc'), latitude=(19, 91, 'cc'))
Southern_hemisphere_1 = region.domain(longitude=(-180, 180, 'cc'), latitude=(-90, -21, 'cc'))
North_America_1 = region.domain(longitude=(-144, -61, 'cc'), latitude=(24, 61, 'cc'))
South_America_1 = region.domain(longitude=(-119, 1, 'cc'), latitude=(-59, 21, 'cc'))
Europe_1 = region.domain(longitude=(-9, 29, 'cc'), latitude=(24, 71, 'cc'))
Asia_1 = region.domain(longitude=(49, 180, 'cc'), latitude=(-1, 81, 'cc'))#-->ECMWF my bound
#Asia_1 = region.domain(longitude=(59, 146, 'cc'), latitude=(24, 66, 'cc'))#-->ECMWF original
Australia_1 = region.domain(longitude=(89, 180, 'cc'), latitude=(-54, -11, 'cc'))
Africa_1 = region.domain(longitude=(-39, 81, 'cc'), latitude=(-39, 41, 'cc'))
Tropic_1 = region.domain(longitude=(89, 180, 'cc'), latitude=(-19, 21, 'cc'))


# For alok singh/power spectrum project region domains
# Indian Ocean
IO = region.domain(longitude=(75, 100, 'ccb'), latitude=(-10, 5, 'ccb'))
# Western Pacific
WP = region.domain(longitude=(115, 140, 'ccb'), latitude=(10, 25, 'ccb'))
# Bay of bengal
BB = region.domain(longitude=(80, 100, 'ccb'), latitude=(10, 20, 'ccb'))
# Maritime Continents
MC = region.domain(longitude=(115.,145.,'ccb'), latitude=(-17.5, -2.5,'ccb'))

# collections of all selector regions
regions = {
    'PGlobal': PGlobal,
    'PGlobal_1': PGlobal_1,
    'CIndia': CIndia,
    'CIndia_1': CIndia_1,
    'PenIndia': PenIndia,
    'PenIndia_1': PenIndia_1,
    'WcstIndia': WcstIndia,
    'WcstIndia_1': WcstIndia_1,
    'AIR': AIR,
    'AIR_1': AIR_1,
    'India1': India1,
    'India1_1': India1_1,
    'India2': India2,
    'India2_1': India2_1,
    'India3': India3,
    'India3_1': India3_1,
    'India': India,
    'India_1': India_1,
    'Asia': Asia,
    'Asia_1': Asia_1,
    'Northern_hemisphere': Northern_hemisphere,
    'Northern_hemisphere_1': Northern_hemisphere_1,
    'Southern_hemisphere': Southern_hemisphere,
    'Southern_hemisphere_1': Southern_hemisphere_1,
    'North_America': North_America,
    'North_America_1': North_America_1,
    'South_America': South_America,
    'South_America_1': South_America_1,
    'Europe': Europe,
    'Europe_1': Europe_1,
    'Australia': Australia,
    'Australia_1': Australia_1,
    'Africa': Africa,
    'Africa_1': Africa_1,
    'Tropic': Tropic,
    'Tropic_1': Tropic_1,
    'IO': IO,
    'WP': WP,
    'BB': BB,
    'MC': MC}

# end of regions


