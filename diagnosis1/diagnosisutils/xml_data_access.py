"""
.. module:: xml_data_access
   :synopsis: A useful module for grib data access through the xml which has
              created by cdscan
.. moduleauthor:: Arulalan.T <arulalant@gmail.com>

"""
import os
import sys
import re
import cdms2
import cdtime
import cdutil
from timeutils import TimeUtility
# setting the absolute path of the previous to previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__diagnosisutilDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__diagnosisutilDir__, '../..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diag_setup.varsdict import variables


class _XmlAccessError(Exception):

    def __init__(self, *args):
        print "\nXmlAccessError Error : "
        for i in args:
            print i


class _XmlAccessTypeError(_XmlAccessError):
    pass


class _XmlAccessInputError(_XmlAccessError):
    pass


class _RainfallAccessError(_XmlAccessError):
    pass


class _RainfallAccessTypeError(_XmlAccessError):
    pass


class XmlAccess(TimeUtility):

    def __init__(self, xmlPath):
        """
        XmlAccess.__init__ : It returns the instance of this XmlAccess class.

        Condition :
                  xmlPath is mandatory.

        Inputs :
          xmlPath is absolute one. This xml should be created by cdscan cmd.

        Usage:
          Assigning to the instance variable for Xml_Access class object

        Written by: Arulalan.T

        Date: 29.05.2011

        """
        self.xmlpath = xmlPath
        if not os.path.isfile(self.xmlpath):
            raise _XmlAccessError("the xml file is not exist \
                        in the path %s" % (self.xmlpath))
        self.xmlobj = cdms2.open(self.xmlpath)
        # initializing the TimeUtility class __init__ attributes
        TimeUtility.__init__(self)
    # end of def __init__(self,xmlPath):

    def __getitem__(self, var):
        """
        Get the variable as <class 'cdms2.variable.DatasetVariable'>
        """
        return self.xmlobj[var]
    # end of def __getitem__(self, var):

    def listvariable(self):
        """
        Returns the listvariable of cdms2 open object method result
        """
        return self.xmlobj.listvariable()
    # end of def listvariable(self):

    def close(self):
        """
        Close the xml file object which is opened by cdms2, while creating
        an instance to this class.
        """
        self.xmlobj.close()
    # end of def close(self):

    def getXmlData(self, var, date=None, level='all', **latlonregion):
        """
        :func:`getXmlData`: Extract the data from the xml file which has
                            created by the cdscan command
        Inputs : var is mandatory.
                 if we passed date,level then it should return var accordingly
                 By default level takes 'all' levels.
                 Pass either (lat,lon) or region keyword arg

        Written by : Arulalan.T

        Date : 29.05.2011

        """
        if not var in self.xmlobj.listvariable():
            raise _XmlAccessError("the xml file %s doesnt have the passed \
                    xmlvar %s.Choose correct var from the available vars \
                  here" % (self.xmlpath, var), self.xmlobj.listvariable())
        # make copy level
        lev = level
        # make free memory
        del level
        if lev == 'all':
            lev = None

        if lev is not None:
            all_levels = self.xmlobj[var].getLevel()[:]
            if not lev in all_levels:
                raise _XmlAccessInputError("the passed level %s is not \
                    present in the levelAxis. Choose one from the \
                    following levels %s" % (str(lev), str(all_levels)))

        # get the squeeze option from user.
        # squeeze must be keyword argument only
        if 'squeeze' in latlonregion:
            squeezeVal = latlonregion.get('squeeze')
            if squeezeVal not in [0, 1]:
                raise _XmlAccessError("squeeze option must be either 0 or 1\
                                                    by default it takes 0")
        else:
            # default squeeze setting
            squeezeVal = 0

        if (('lat' or 'lon' or 'latitude' or 'longitude') in latlonregion
                                            and 'region' in latlonregion):
            # find out if user passed (lat or lon) and region
            raise _XmlAccessError("Pass either region or lat,lon \
                                  key word arguments. Do not pass all ")
        # initializing lat,lon,region variables
        lat, lon, regionVar = None, None, None
        if ('lat' or 'latitude') in latlonregion:
            if 'lat' in latlonregion:
                lat = latlonregion.get('lat')
            elif 'latitude' in latlonregion:
                lat = latlonregion.get('latitude')

        if ('lon' or 'longitude') in latlonregion:
            if 'lon' in latlonregion:
                lon = latlonregion.get('lon')
            elif 'longitude' in latlonregion:
                lon = latlonregion.get('longitude')

        if 'region' in latlonregion:
            # calling the region dictionary from the regions module
            regionVar = latlonregion.get('region')

        if date == None:
            if lat and lon:
                # extract the partial data w.r.t passed lat & lon
                if lev:
                    # extract paticular level only
                    VAR = self.xmlobj(var, level = lev, longitude = lon,
                                       latitude = lat, squeeze = squeezeVal)
                else:
                    # extract all the levels
                    VAR = self.xmlobj(var, longitude = lon, latitude = lat,
                                                        squeeze = squeezeVal)
            elif regionVar:
                # extract the partial data w.r.t passed region variable
                if lev:
                    VAR = self.xmlobj(var, regionVar, level = lev,
                                              squeeze = squeezeVal)
                else:
                    VAR = self.xmlobj(var, regionVar, squeeze = squeezeVal)
            else:
                # extract the whole (available lat,lon & time) variable
                if lev:
                    VAR = self.xmlobj(var, level = lev, squeeze = squeezeVal)
                else:
                    VAR = self.xmlobj(var, squeeze = squeezeVal)

        else:
            all_dates_DTGT = self.xmlobj[var].getTime().asDTGTime()[:]
            all_dates_COMP = self.xmlobj[var].getTime().asComponentTime()[:]
            if isinstance(date, str):
                if self.comppattern.match(date):
                    # checking date and retain date as same as passed by user
                    tmpdate = self.comp2timestr(date)
                    if not tmpdate in all_dates_DTGT:
                        raise _XmlAccessInputError("The passed date %s is not\
                            in the timeAxis. Choose one date from here %s" %
                                           (str(date), str(all_dates_COMP)))
                elif self.ymdpattern.match(date):
                    # checking date and change date as component object
                    date = self.timestr2comp(date)
                    if not date in all_dates_COMP:
                        raise _XmlAccessInputError("The passed date %s is not\
                            in the timeAxis. Choose one date from here %s" %
                                            (str(date), str(all_dates_DTGT)))
                else:
                    raise _XmlAccessInputError("date must be either yyyymmdd \
                               yyymmddhh or  or cdtime.comptime object/string\
                                                               formate only ")
            elif isinstance(date, tuple):
                startdate = date[0]
                enddate = date[1]
                # startdate checking begins
                if (str(type(startdate)) == "<type 'comptime'>"):
                    # component time object passed
                    pass
                elif self.comppattern.match(startdate):
                    # checking start date
                    startdate = self.comp2timestr(startdate)
                    if not startdate in all_dates_DTGT:
                        raise _XmlAccessInputError("The start date %s is not\
                             in the timeAxis. Choose one date from here %s" %
                                         (startdate, str(all_dates_COMP)))
                    # retain start date as same as passed by user
                    startdate = date[0]
                elif self.ymdpattern.match(startdate):
                    # checking startdate and change date as component object
                    startdate = self.timestr2comp(startdate)
                    if not startdate in all_dates_COMP:
                        raise _XmlAccessInputError("The start date %s is not\
                            in the timeAxis. Choose one date from here %s" %
                                       (str(startdate), str(all_dates_DTGT)))
                else:
                    raise _XmlAccessInputError("startdate must be either \
                                                yyyymmdd or yyyymmddhh or \
                                 cdtime.comptime object/string formate only")
                # startdate checking ends
                # enddate checking begins
                if (str(type(enddate)) == "<type 'comptime'>"):
                    # component time object passed
                    pass
                elif self.comppattern.match(enddate):
                    # checking end date
                    enddate = self.comp2timestr(enddate)
                    if not enddate in all_dates_DTGT:
                        raise _XmlAccessInputError("The end date %s is not \
                            in the timeAxis. Choose one date from here %s" %
                                        (enddate, str(all_dates_COMP)))
                     # retain end date as same as passed by user
                    enddate = date[1]
                elif self.ymdpattern.match(enddate):
                    # checking enddate and change date as component object
                    enddate = self.timestr2comp(enddate)
                    if not enddate in all_dates_COMP:
                        raise _XmlAccessInputError("The end date %s is not\
                            in the timeAxis. Choose one date from here %s" %
                                         (str(enddate), str(all_dates_DTGT)))
                else:
                    raise _XmlAccessInputError("enddate must be either \
                                                yyyymmdd or yyyymmddhh or \
                                 cdtime.comptime object/string formate only")
                # enddate checking ends
                date = (startdate, enddate)

            elif isinstance(date, int):
                # interger type of date input must be either yyymmddhh or
                # yyyymmdd formate only
                date = str(date)
                if self.ymdpattern.match(date):
                    # checking date and change date as component object
                    date = self.timestr2comp(date)
                    if not date in all_dates_COMP:
                        raise _XmlAccessInputError("The passed date %s is not\
                            in the timeAxis. Choose one date from here %s" %
                                            (date, str(all_dates_COMP)))
                else:
                    raise _XmlAccessInputError("date must be eitehr yyyymmdd \
                               yyymmddhh or  or cdtime.comptime object/string\
                                                               formate only ")

            elif str(type(date)) == "<type 'comptime'>":
                # component time object passed
                if not date in all_dates_COMP:
                    raise _XmlAccessInputError("The passed date %s is not\
                            in the timeAxis. Choose one date from here %s" %
                                            (date, str(all_dates_COMP)))

            elif isinstance(date, slice):
                # slice args passed
                pass

            else:
                raise _XmlAccessTypeError("The date should be either string \
                  or tuple type only. But you passed %s type " % (type(date)))

            if lat and lon:
                # extract the partial data w.r.t passed lat & lon
                if lev:
                    # extract paticular level only
                    VAR = self.xmlobj(var, time = date, level = lev,
                                    longitude = lon, latitude = lat,
                                               squeeze = squeezeVal)
                else:
                    # extract all the levels
                    VAR = self.xmlobj(var, time = date, longitude = lon,
                                      latitude = lat, squeeze = squeezeVal)
            elif regionVar:
                # extract the partial data w.r.t passed region variable
                if lev:
                    VAR = self.xmlobj(var, regionVar, time = date,
                                 level = lev, squeeze = squeezeVal)
                else:
                    VAR = self.xmlobj(var, regionVar, time = date,
                                              squeeze = squeezeVal)
            else:
                # extract the whole (available lat,lon) variable
                if lev:
                    VAR = self.xmlobj(var, time = date,
                                 level = lev, squeeze = squeezeVal)
                else:
                    VAR = self.xmlobj(var, time = date,
                                              squeeze = squeezeVal)
        # end of if date == None:

        # Resetting the var id once we extracted by region or lat,lon data
        VAR.id = var
        return VAR
    # end of def getXmlData(...):
# end of class Xml_Access:

class _GribXmlAccessError(Exception):

    def __init__(self, *args):
        print "\nGribXmlAccessError Error : "
        for i in args:
            print i


class _GribInputStringError(_GribXmlAccessError):
    pass


class _GribInputError(_GribXmlAccessError):
    pass


class _GribAccessError(_GribXmlAccessError):
    pass


class _GribAccessTypeError(_GribXmlAccessError):
    pass


class _RainfallAccessError(_GribXmlAccessError):
    pass

class GribXmlAccess(XmlAccess, TimeUtility):
    ''' xml access methods '''

    def __init__(self, XmlDir):
        self._globalXml = {}
        if XmlDir:
            self._collectXmlPath(XmlDir)
        else:
            raise _GribXmlAccessError("You must pass the xml directory")
        self._forecastdays_ = {01: 0, 24: 1, 48: 2, 72: 3, 96: 4, 120: 5,
                               144: 6, 168: 7, 192:8, 216:9, 240:10}
        # initializing the anl and fcst xml objects
        self._anlxmlobj = None
        self._f01xmlobj = None
        self._f24xmlobj = None
        self._f48xmlobj = None
        self._f72xmlobj = None
        self._f96xmlobj = None
        self._f120xmlobj = None
        self._f144xmlobj = None
        self._f168xmlobj = None
        self._f192xmlobj = None
        self._f216xmlobj = None
        self._f240xmlobj = None
        # initializing the observation xml objects
        self._obsxmlobj = None
        # initializing the rainfall xml objects
        self.rainfallXmlPath = None
        self.rainfallXmlVar = None
        self.rainfallModel = None
        # we must call the inherited class's __init__ method.
        # then only we can access all its super class member variables
        # initializing the TimeUtility class __init__ attributes
        TimeUtility.__init__(self)
    # end of def __init__(self, XmlDir):

    def _collectXmlPath(self, xmldir):
        """
        Collecting xml file path from the passed directory into the dictionary
        by parsing regular expression  for future purpose through out the
        live session of this program
        """
        # setting pattern for the anl and fcst hours xml file
        anlpattern = r'all(.*)anl(.*)xml'
        f01pattern = r'all(.*)fcst(.*)01(.*)xml'
        f24pattern = r'all(.*)fcst(.*)24(.*)xml'
        f48pattern = r'all(.*)fcst(.*)48(.*)xml'
        f72pattern = r'all(.*)fcst(.*)72(.*)xml'
        f96pattern = r'all(.*)fcst(.*)96(.*)xml'
        f120pattern = r'all(.*)fcst(.*)120(.*)xml'
        f144pattern = r'all(.*)fcst(.*)144(.*)xml'
        f168pattern = r'all(.*)fcst(.*)168(.*)xml'
        f192pattern = r'all(.*)fcst(.*)192(.*)xml'
        f216pattern = r'all(.*)fcst(.*)216(.*)xml'
        f240pattern = r'all(.*)fcst(.*)240(.*)xml'
        obspattern = r'all(.*)obs(.*)xml'

        files = [fname for fname in os.listdir(xmldir) if fname.endswith('.xml')]
        print "Collecting xml files path\n"
        for xml in files:            
            xmlabspath = os.path.join(xmldir, xml)
            if re.search(anlpattern, xml, re.M|re.I):
                # get anl xml file path
                self._globalXml['anl'] = xmlabspath
            elif re.search(f01pattern, xml, re.M|re.I):
                # get fcst 01 hr xml file path
                self._globalXml['f01'] = xmlabspath
            elif re.search(f24pattern, xml, re.M|re.I):
                # get fcst 24 hr xml file path
                self._globalXml['f24'] = xmlabspath
            elif re.search(f48pattern, xml, re.M|re.I):
                # get fcst 48 hr xml file path
                self._globalXml['f48'] = xmlabspath
            elif re.search(f72pattern, xml, re.M|re.I):
                # get fcst 72 hr xml file path
                self._globalXml['f72'] = xmlabspath
            elif re.search(f96pattern, xml, re.M|re.I):
                # get fcst 96 hr xml file path
                self._globalXml['f96'] = xmlabspath
            elif re.search(f120pattern, xml, re.M|re.I):
                # get fcst 120 hr xml file path
                self._globalXml['f120'] = xmlabspath
            elif re.search(f144pattern, xml, re.M|re.I):
                # get fcst 144 hr xml file path
                self._globalXml['f144'] = xmlabspath
            elif re.search(f168pattern, xml, re.M|re.I):
                # get fcst 168 hr xml file path
                self._globalXml['f168'] = xmlabspath
            elif re.search(f192pattern, xml, re.M|re.I):
                # get observation xml file path
                self._globalXml['f192'] = xmlabspath
            elif re.search(f240pattern, xml, re.M|re.I):
                # get fcst 144 hr xml file path
                self._globalXml['f240'] = xmlabspath
            elif re.search(f216pattern, xml, re.M|re.I):
                # get fcst 168 hr xml file path
                self._globalXml['f216'] = xmlabspath
            elif re.search(obspattern, xml, re.M|re.I):
                # get observation xml file path
                self._globalXml['obs'] = xmlabspath
            else:
                print "unwanted xml are present in the directory"
            # end of if re.search(anlpattern, xml, re.M|re.I):
        # end of for xml in files:
    # end of def _collectXmlPath(self, xmldir):

    def _getXmlAccessObj(self, Type, hour=None):
        """
        _getXmlAccessObj : get the XmlAccess class object, to access the xml
        and getData.By passing the anl or obs and/or fcst and its hours, this should
        return its appropriate object.
        If the object is already exists in the memory means, it just retun
        that object as it is.
        If not exist means, if xml directory contains the needed file means
        it should genearate new object for that. (now it exists in memory)

        If xml directory doesnot contain needed file means, it should return
        None

        Written by : Arulalan.T

        Date : 10.07.2011

        """
        if Type in ['a', 'anl']:
            if not self._anlxmlobj:
                # anlxlmobj is None
                xmlPath = self._globalXml.get('anl')
                self._anlxmlobj = XmlAccess(xmlPath)
            return self._anlxmlobj

        elif Type in ['o', 'obs']:
            if not self._obsxmlobj:
                # anlxlmobj is None
                xmlPath = self._globalXml.get('obs')
                self._obsxmlobj = XmlAccess(xmlPath)
            return self._obsxmlobj

        elif Type in ['f', 'fcst', 'r', 'R']:
            if hour:
                if isinstance(hour, int):
                    hour = str(hour)
                if not hour.isdigit():
                    raise _GribInputError("hour must be digit")
                key = 'f' + hour
                xmlPath = self._globalXml.get(key)
                if not xmlPath:
                    return None
                if hour == '01':
                    if not self._f01xmlobj:
                        self._f01xmlobj = XmlAccess(xmlPath)
                    return self._f01xmlobj

                elif hour == '24':
                    if not self._f24xmlobj:
                        self._f24xmlobj = XmlAccess(xmlPath)
                    return self._f24xmlobj

                elif hour == '48':
                    if not self._f48xmlobj:
                        self._f48xmlobj = XmlAccess(xmlPath)
                    return self._f48xmlobj

                elif hour == '72':
                    if not self._f72xmlobj:
                        self._f72xmlobj = XmlAccess(xmlPath)
                    return self._f72xmlobj

                elif hour == '96':
                    if not self._f96xmlobj:
                        self._f96xmlobj = XmlAccess(xmlPath)
                    return self._f96xmlobj

                elif hour == '120':
                    if not self._f120xmlobj:
                        self._f120xmlobj = XmlAccess(xmlPath)
                    return self._f120xmlobj

                elif hour == '144':
                    if not self._f144xmlobj:
                        self._f144xmlobj = XmlAccess(xmlPath)
                    return self._f144xmlobj

                elif hour == '168':
                    if not self._f168xmlobj:
                        self._f168xmlobj = XmlAccess(xmlPath)
                    return self._f168xmlobj

                elif hour == '192':
                    if not self._f192xmlobj:
                        self._f192xmlobj = XmlAccess(xmlPath)
                    return self._f192xmlobj

                elif hour == '240':
                    if not self._f240xmlobj:
                        self._f240xmlobj = XmlAccess(xmlPath)
                    return self._f240xmlobj

                elif hour == '216':
                    if not self._f216xmlobj:
                        self._f216xmlobj = XmlAccess(xmlPath)
                    return self._f216xmlobj

                else:
                    raise _GribXmlAccessError("wrong hour %s passed,cant \
                                create xmlobj for that " % (hour))
               # end of if hour:

            else:
                raise _GribXmlAccessError("you must pass the hour to choose \
                                          fcst xml file ")
        else:
            raise _GribXmlAccessError("Type either 'a' or 'f' or 'o' ")
        # end of if Type in ['a', 'anl']:
    # end of  def _getXmlAccessObj(self, Type, hour=None):

    def closeXmlObjs(self):
        """
        :func:`closeXmlObjs`: close all the opened xml file objects by
        cdms2. If we called this method, it will check all the 8 xml objects
        are either opened or not. If that is opened by cdms2 means, it will
        close that file object properly. We must call this method for the
        safety purpose.

        ..note:: If we called this method, at the end of the program then
            it should be optimized one. If this method called at any inter
            mediate level means, then again it need to create the xml object.

        Written By: Arulalan.T

        Date : 10.09.2011

        """

        xmlobjs = [self._obsxmlobj, self._anlxmlobj, self._f01xmlobj,
                   self._f24xmlobj, self._f48xmlobj, self._f72xmlobj,
                   self._f96xmlobj, self._f120xmlobj, self._f144xmlobj,
                   self._f168xmlobj, self._f192xmlobj, self._f216xmlobj,
                                                       self._f240xmlobj]
        for xmlobj in xmlobjs:
            if xmlobj:
                try:
                    # close the file object which is opened by cdms2
                    xmlobj.close()
                except:
                    pass
    # end of def closeXmlObjs(self):

    def getXmlPath(self, Type, hour=None):
        """
        :func:`getXmlPath`: To get the xml's absolute path.

        Inputs : Type is either 'a' or 'o' or 'f' or 'r'
                 hour is mandatory when you pass 'f' or 'r'.
                 'a' - analysis, 'f' - forecast,
                 'o' - observation, 'r' - reference.
        Written by : Arulalan.T

        Date : 21.08.2011

        """
        if Type in ['a', 'anl']:
                return self._globalXml.get('anl')
        elif Type in ['o', 'obs']:
                return self._globalXml.get('obs')
        elif Type in ['f', 'fcst', 'r', 'R']:
            if hour:
                if isinstance(hour, int):
                    hour = str(hour)
                if not hour.isdigit():
                    raise _GribInputError("hour must be digit")
                key = 'f' + hour
                xmlPath = self._globalXml.get(key)
                if xmlPath:
                    return xmlPath
                else:
                    raise _GribXmlAccessError("wrong hour %s passed,cant \
                                find fcst xml path for that. Choose correct\
                                hour from this %s " % (hour,
                                                 self._forecastdays_.keys()))
            else:
                raise _GribXmlAccessError("you must pass the hour to choose \
                                          fcst xml file ")
        else:
            raise _GribXmlAccessError("Type either 'a' or 'f' ")
    # end of  def _getXmlAccessObj(self, Type, hour=None):

    def __getitem__(self, args):
        """
        Inputs : var, Type, hour

        Usage : var is a variable which should be in the xml file
                Choose need Type like 'a' or 'o' or 'f' or 'r'.
                hour is must when Type is 'f' or 'r'.
                'a' - analysis, 'f' - forecast, 'o' - observation
                'r' - reference.
                Get the variable as <class 'cdms2.variable.DatasetVariable'>
                by passing the Type and hour (if needed).

                This DatasetVariable is efficient one, to access its
                dimensions and its data whenever, whichever need.

        example :
            >>> obj = x.GribXmlAccess('/NCMRWF/all_xml')
            >>> obj['ugrdprs','a']
            >>> <Variable: ugrdprs, dataset: none, shape: (129, 26, 361, 720)>
             .. note:: Here we passed 'a' as Type.

            >>> obj['ugrdprs','f',48]
            >>> <Variable: ugrdprs, dataset: none, shape: (129, 26, 361, 720)>
             .. note:: Here we passed 'f' as Type and 48 as hour

        Written By : Arulalan.T

        Date : 19.08.2011

        """
        if isinstance(args, str):
            raise _GribInputError("You must pass var and Type")
        elif isinstance(args, tuple):
            var = args[0]
            Type = args[1]
            hour = None
            if Type in ['f', 'fcst', 'r', 'R']:
                if not len(args) == 3:
                    raise _GribInputError("You must pass hour as third arg to\
                                     choose fcst file")
                hour = args[2]
            xmlobj = self._getXmlAccessObj(Type, hour)
            return xmlobj[var]
        else:
            raise _GribInputError("argument must be either string or tupe")
    # end of def __getitem__(self, args):

    def listvariable(self, Type, hour=None):
        """
        :func:'listvariable': By passing Type and/or hour args to this method,
        it will return the listvariable method of the appropriate xml file.

        Returns the listvariable of cdms2 open object method result
        """
        xmlobj = self._getXmlAccessObj(Type, hour)
        return xmlobj.listvariable()
    # end of def listvariable(self, Type, hour=None):

    def findPartners(self, Type, date, hour=None, returnType='c'):
        """
        :func:`findPartners`: To find the partners of the any particular
        day anl or any particular day and hour of the fcst.
        Each fcst file(day) has its truth anl file(day).
        i.e. today 24 hour fcst file's partner is tomorrow's truth anl file.
        today 48 hour fcst file's partner is the day after tomorrow's
        truth anl file. Keep going on the fcst vc anl files.

        Same concept for anl files partner but in reverse concept.
        Today's truth anl file's partners are yesterdays' 24 hour fcst file,
        day before yesterday's 48 hour fcst file and keep going backward ...

        This what we are calling as the partners of anl and fcst files.
        For present fcst hours partner is future anl file and for present anl
        partners are the past fcst hours files.

        Condition :

                  if 'f' as passed then hour is mandatory one
                  else 'a' as passed then hour is optional one.
                  returnType either 'c' or 's'
        Inputs :

           Type = 'f' or 'a' or 'o' i.e fcst or anl or obs file
           date must be cdtime.comptime object or its string formate
           hour is like 24 multiples in case availability of the fcst files

        Outputs :

               If 'f' has passed this method returns a corresponding partner
               of the anlysis date in cdtime.comptime object
               If 'a' or 'o' has passed this method returns a dictionary.
               It contains the availability of the fcst hours as key and its
               corresponding fcst date in cdtime.comptime object as value of
               the dict.

               we can get the return date as yyyymmdd string formate by
               passing returnType = 's'

         Usage :

           example 1 :
              >>> findPartners('f','2010-5-25',24)
                  2010-5-26 0:0:0.0

               .. note:: The passed date in comptime in string type.

              >>> findPartners('f',cdtime.comptime(2010,5,25),24)
                  2010-5-26 0:0:0.0

               .. note:: The passed date in comptime object itself.

              >>> findPartners('a','2010-5-26')
                  {24: 2010-5-25 0:0:0.0}

               .. note:: Returns dictionary which contains key as hour and its
                        corresponding date

           example 2 :
              >>> findPartners('f','2010-5-25',72)
                  2010-5-28 0:0:0.0

              >>> findPartners('a','2010-6-1', returnType ='s')
                   {24: '20100531',
                    48: '20100530',
                    72: '20100529',
                    96: '20100528',
                   120: '20100527',
                   144: '20100526',
                   168: '20100525'}

              .. note:: Depends upon the availability of the fcst and anl
                        files, it should return partner date

           example 3 :
              >>> findPartners('a','20100601',144)
                  2010-5-26 0:0:0.0

              .. seealso:: If not available for the passed hour means
                          it should return None

        Written by : Arulalan.T

        Date : 03.04.2011

        """
        if str(type(date)) == "<type 'comptime'>":
            datecomp = date

        elif (str(date).find('-')) != -1:
            #convert cdtime string into comptime
            datecomp = cdtime.s2c(date)
        elif self.ymdpattern.match(date):
            # conver from yyymmddhh into comptime
            datecomp = self.timestr2comp(date)
        else:
            raise _GribInputStringError("The passed date should be the \
                            cdtime.comptime formate or its str formate ")
        # getting component time properties
        year = datecomp.year
        month = datecomp.month
        day = datecomp.day

        if isinstance(hour, str):
            hour = int(hour)

        if Type in ['f', 'F', 'fcst']:
            # fcst arg passed
            if hour == None:
                raise _GribInputError("you must pass hour to find out the \
                                    forecast partner date")

            if hour in self._forecastdays_:
                partner_day = self._forecastdays_.get(hour)
            else:
                raise _GribInputError("the passed %d hour not match with keys\
                                         of forecastdays dict " %(hour))

            # calling the TimeUtility's method moveTime to find out
            # the partner's day
            truth_anl_day = self.moveTime(year, month, day, partner_day,
                                           returnType = returnType)
            return truth_anl_day

        if Type in ['a', 'A', 'anl', 'analysis', 'r', 'R', 'reference',
                                                'o', 'obs', 'obeservation']:
            # anl arg passed or rainfall arg passed
            if hour:
                # hour is not None
                # finding the partner day by passing the arg as partner hour
                if hour in self._forecastdays_:
                    partner_day = self._forecastdays_.get(hour)
                else:
                    raise _GribInputError("the passed %d hour not match with\
                                        keys of forecastdays dict " %(hour))

                # to find the previous day, passing the -ve sign to the
                # TimeUtility's moveTime method
                previous_fcst_day = self.moveTime(year, month, day,
                                partner_day * -1, returnType = returnType)
                return previous_fcst_day

            else:
                # hour is none. i.e. need to extract all the fcst hours
                fcst_hours_vs_date = {}

                # loop throughing all the partner days and hours accordingly
                for partner_hour, partner_day in self._forecastdays_.items():
                    # To find the availability of the fcst hour xml file,
                    # we call _getXmlAccessObj. If passed hour is not
                    # available means it should return None                    
                    #if partner_hour and self._getXmlAccessObj('f', partner_hour):
                        # commented the above line to check the fcst hour file 
                        # is exist or not, for the generic functionality purpose.
                        # to find the previous day, passing the -ve sign to
                        # the TimeUtility's moveTime method
                        previous_fcst_day = self.moveTime(year, month, day,
                                    partner_day * -1, returnType =returnType)
                        # adding to the temporary dictionay
                        fcst_hours_vs_date[partner_hour] = previous_fcst_day
                # end of for ...:
                return fcst_hours_vs_date
        # end of if Type in ['a','A','r','R']:
    # end of def findPartners(...):

    def _getDataOfPartners(self, var, Type, date, hour=None, level='all', \
                                                             **latlonregion):
        """
        _getDataOfPartners : It can extract the data_of_partners.
        i.e it returns the partners data not along with its source Type data.
        It extracts the multiple data (depends upon the level,partners and
                                 dates) and returns in single MV2 variable.

        Condition :
          level is optional. level takes default 'all'. if level passed,
          it must be belongs to the data variable.
          hour is must when Type arg should be 'f' (fcst).
          Pass either (lat,lon) or region.

        Inputs:
           Type - either 'a' or 'f' or 'r' or 'o'
           var,level must be belongs to the data
           startdate and enddate must be in cdtime.comp string formate.
           skipdays must be an integer
           key word arg lat,lon or region should be passed

        Outputs:
              It should return the partners data as single MV2 variable in
              shape of (time,level,lat,lon). i.e with time axis,level axis,
              lat axis and lon axis.
              If level has squeezed while extract the data,
              then it should return only shape of (time,lat,lon).

        Usage:

           example 1:
             _getDataOfPartners(var = "Geopotential Height",Type = 'f',
               date = '2010-5-25', hour = 24,level = 'all' ,region = AIR )
               #lat=(-90,90),lon=(0,359.5)

        Refer :
            method findPartners(...) of class TimeUtility:

        Written by: Arulalan.T

        Date: 09.04.2011

        """

        # have to enable this...
        # self.checking_major_parameter_to_extract_data(Type,date,hour)
        datavariables = []

        partner_date = self.findPartners(Type, date, hour)
        if isinstance(partner_date, dict):
            # multiple dates
            partner_hours = partner_date.keys()
            partner_hours.sort()

            for hour in partner_hours:
                date = partner_date.get(hour)
                variable = self.getData(var, Type, date, hour,
                                        level, **latlonregion)
                variable.date = date
                # squeezing MV2 variable
                variable = variable(squeeze = 1)
                datavariables.append(variable)
        else:
            # single date
            variable = self.getData(var, Type, partner_date, hour,
                                             level, **latlonregion)
            # squeezing MV2 variable
            variable = variable(squeeze = 1)
            variable.date = partner_date
            datavariables.append(variable)

        # get the start date from the datavariables
        startdate = datavariables[0].date
        # create the time axis in -ve. i.e. Backward days
        timeAxis = self._generateTimeAxis(len(datavariables), startdate, -1)
        # get the level,lat,lon axis information
        levelAxis = datavariables[0].getLevel()
        latAxis = datavariables[0].getLatitude()
        lonAxis = datavariables[0].getLongitude()

        if levelAxis == None:
            # shape (time,lat,lon)
            VAR = cdms2.createVariable(data = datavariables,
                                       axes = [timeAxis, latAxis, lonAxis])
        else:
            # shape (time,level,lat,lon)
            VAR = cdms2.createVariable(data = datavariables,
                              axes = [timeAxis, levelAxis, latAxis, lonAxis])

        return VAR
    # end of def _getDataOfPartners(...):

    def getData(self, var, Type, date, hour=None, level='all', **latlonregion):
        """
        :func:`getData`: It can extract either the data of a single date or
             range of dates. It depends up on the input of the date argument.
             Finally it should return MV2 variable.

        Condition :
            date is either tuple or string.
            level is optional. level takes default 'all'.
            if level passed, it must be belongs to the data variable
            hour is must when Type arg should be 'f' (fcst) to choose
            xml object.
            Pass either (lat,lon) or region.

        Inputs :
          Type - either 'a'[analysis] or 'f'[forecast] or 'o'[observation]
          var,level must be belongs to the data file
          key word arg lat,lon or region should be passed
          date formate must one of the followings

          date formate 1:
              date = (startdate, enddate)
              here startdate and enddate must be like cdtime.comptime formate.

          date formate 2:
               date = (startdate)

          date formate 3:
               date = 'startdate' or date = 'date'

          eg for date input :
               date = ('2010-5-1','2010-6-30')
               date = ('2010-5-30')
               date = '2010-5-30'

         Outputs :

               If user passed single date in the date argument, then it should
               return the data of that particular date as single MV2 variable.

               If user passed start and enddate in the date argument,
               then it should return the data for the range of dates as
               single MV2 variable with time axis.

        Written by: Arulalan.T

        Date: 10.05.2011

        """

        xmlobj = self._getXmlAccessObj(Type, hour)
        data = xmlobj.getXmlData(var, date, level, **latlonregion)
        return data
    # end of def getData(...):

    def getDataPartners(self, var, Type, date, hour=None, level='all',
                        orginData=0, datePriority='o', **latlonregion):
        """
        :func:`getDataPartners`: It can extract either the orginDate with its
        partnersData or it can extract only the partnersData without its
        orginData for a single date or range of dates.

        It depends up on the input of the orginData, datePriority,date args.
        Finally it should return partnersData and/or orginData as MV2 variable

        Condition :

         date is either tuple or string.
         level is optional. level takes default 'all'.
         if level passed, it must be belongs to the data variable
         hour is must when Type arg should be 'f' (fcst) to select xml object.
         hour is must when range of date passed, even thogut Type arg should
         be 'a'(anl) or 'o'(obs),to choose one fcst xml object along with hour.
         Pass either (lat,lon) or regionself.

        Inputs:

           Type - either 'a'[analysis] or 'f'[forecast] or 'o'[observation]
           var,level must be belongs to the data file
           orginData - either 0 or 1. 0 means it shouldnot return the
                       orginData as single MV2 var.
                          1 means it should return both the orginData and its
                          partnersData as two seperate MV2 vars.
           datePriority - either 'o' or 'p'. 'o' means passed date is with
                          respect to orginData. According to this
                          orginData's date, it should return its partnersData.
                        'p' means passed date is with respect to partnersData.
                            According to this partnersData's date, it should
                            return its orginData.

           key word arg lat,lon or region should be passed

           date formate 1:
              date = (startdate,enddate)
              here startdate and enddate must be like cdtime.comptime formate.

           date formate 2:
               date = (startdate)

           date formate 3:
               date = 'startdate' or date = 'date'

           eg for date input :
                  date = ('2010-5-1','2010-6-30')
                   date = ('2010-5-30')
                   date = '2010-5-30'

        Outputs:

           If user passed single date in the date argument, then it should
           return the data of that particular date
           (both orginData & partnersData) as a single MV2 variable.

           If user passed start and enddate in the date argument, then it
           should return the data (both orginData & partnersData)
           for the range of dates as a single MV2 variable with time axis.


        Usage:

           .. note::  if 'a'(anl) file is orginData means 'f'(fcst) files are
                   its partnersData and vice versa.

           example1:
             >>> a,b = getDataPartners(var = 'U component of wind',Type = 'a',
                    date = '2010-6-5',hour = None,level = 'all',orginData = 1,
                    datePriority = 'o', lat=(-90,90),lon=(0,359.5))

             a is orginData. i.e. anl. its timeAxis date is '2010-6-5'.
             b is partnersData. i.e. fcst. its 24 hour fcst date w.r.t
             orginData is '2010-6-4'. 48 hour is '2010-6-3'.

             Depends upon the availability of date of fcst files,it should
             return the data.
             In NCMRWF2010 model, it should return maximum of 7 days fcst.

             If we will specify any hour in the same eg, that should return
             only that hour fcst file data instead of returning all the
             available fcst hours data.

           example2:
             >>> a,b = getDataPartners(var = 'U component of wind',Type = 'f',
                      date = '2010-6-5',hour = 24,level = 'all',orginData = 1,
                      datePriority = 'o', lat=(-90,90),lon=(0,359.5))

             a is orginData. i.e.fcst 24 hour.its timeAxis date is '2010-6-5'.
             b is partnersData. i.e. anl. its anl date w.r.t orginData is
             '2010-6-6'.

           example3:
             >>> b = getDataPartners(var = 'U component of wind',Type = 'f',
                     date = '2010-6-5',hour = 24,level = 'all', orginData = 0,
                     datePriority = 'o', lat=(-90,90),lon=(0,359.5))

             b is partnersData. i.e. anl. its anl date w.r.t orginData is
             '2010-6-6'. No orginData. Because we passed orginData as 0.

           example4:
             >>> a,b = getDataPartners(var = 'U component of wind',Type = 'f',
                      date = '2010-6-5',hour = 24,level = 'all',orginData = 1,
                      datePriority = 'p', lat=(-90,90),lon=(0,359.5))

             a is orginData. i.e. fcst 24 hour.its timeAxis date is '2010-6-6'.
             b is partnersData. i.e. anl. its anl date w.r.t orginData is
             '2010-6-5'.
             we can compare this eg4 with eg2. In this we passed datePriority
             as 'p'. So the passed date as set to the partnersData and
             orginData's date has shifted to the next day.

           example5:
             >>> a,b = getDataPartners(var = 'U component of wind',Type = 'a',
                      date = ('2010-6-5','2010-6-6'),hour = 24,level = 'all',
                 orginData = 1,datePriority = 'o', lat=(-90,90),lon=(0,359.5))

                 .. note:: Even though we passed 'a' Type, we must choose the
                           hour option to select the fcst file, since we are
                           passing the range of dates.

             a is orginData. i.e. anl. its timeAxis size is 2.
              date are '2010-6-5' and '2010-6-6'.

             b is partnersData. i.e. fcst 24 hour data.
             its timeAxis size is 2. date w.r.t orginData are '2010-6-4' and
             '2010-6-5'.

             a's '2010-6-5' has partner is b's '2010-6-4'.i.e.orginData(anl)
             partners is partnersData's (fcst).

             same concept for the remains day.
             a's '2010-6-6' has partner is b's '2010-6-5'.

           example6:
             >>> a,b = getDataPartners(var = 'U component of wind',Type = 'a',
                       date = ('2010-6-5','2010-6-6'),hour = 24,level = 'all',
                 orginData = 1,datePriority = 'p', lat=(-90,90),lon=(0,359.5))

                 .. note:: Even though we passed 'a' Type, we must choose the
                           hour option to select the fcst file, since we are
                           passing the range of dates.

             a is orginData. i.e. anl. its timeAxis size is 2.
             date are '2010-6-6' and '2010-6-7'.

             b is partnersData. i.e. fcst 24 hour data.
             its timeAxis size is 2. date w.r.t orginData are '2010-6-5' and
             '2010-6-6'.

             a's '2010-6-6' has partner is b's '2010-6-5'.i.e.orginData(anl)
             partners is partnersData's (fcst).

             same concept for the remains day.
             a's '2010-6-7' has partner is b's '2010-6-6'.
             we can compare this eg6 with eg5.In this we passed datePriority
             as 'p'. So the passed date as set to the partnersData and
             orginData's date has shifted towards the next days.

        Written by: Arulalan.T

        Date: 27.05.2011

        """
        orgin_enddate = None

        if isinstance(date, tuple):
            orgin_startdate = date[0] # assign startdate
            if len(date) >= 2:
                orgin_enddate = date[1] # assign enddate
            # end of if len(date) >= 2:

        elif isinstance(date, str) or str(type(date)) == "<type 'comptime'>":
            orgin_startdate = date # assign date

        else:
            raise _GribAccessTypeError('date either must be tuple or string\
                                           or cdtime.component time object')

        if isinstance(hour, str):
            hour = int(hour)

        xdrange = False
        if orgin_enddate:
            xdrange = True
            # enddate has passed. so we need hour to get the partners data
            if not hour:
                raise _GribAccessError('You must pass the hour to return the \
                                        partners data,since you passed the \
                                        enddate. i.e range of date.')

        # end of if endCompTime:

        if not orginData in [0, 1]:
            raise _GribAccessTypeError('orginData either 0 or 1.  \
                        0 means without orginData. i.e. only partners data. \
                          1 means with orginData. i.e. both orginData \
                          and partnersData. Default it takes 0.')
        if datePriority not in ['o', 'p']:
            raise _GribAccessTypeError("datePriority either 'o' or 'p'. \
                             'o' means passed date set to the orginData. \
                             'p' means passed date set to the partnersData.")

        # find out the partners startdate
        partner_startdate = self.findPartners(Type = Type,
                                    date = orgin_startdate, hour = hour)

        if xdrange:
            # enddate passed
            # find out the partners enddate
            partner_enddate = self.findPartners(Type = Type,
                                    date = orgin_enddate, hour = hour)

            if datePriority == 'p' and orginData:
                # swaping the orgin date and partners date
                orgin_startdate, partner_startdate = partner_startdate, orgin_startdate
                orgin_enddate, partner_enddate = partner_enddate, orgin_enddate

                # orginData is 1
                # make date into comptime object
                partner_startdate = self.timestr2comp(partner_startdate)
                partner_enddate = self.timestr2comp(partner_enddate)

                if hour in self._forecastdays_:
                    movedays = self._forecastdays_.get(hour)
                else:
                    raise _GribAccessError("wrong %d hour has passed as \
                        arg, its not belongs to fcst grib file hours\n \
                                        Choose correct hour\n" % (hour))

                # find out the orgin startdate and enddate
                orgin_startdate = self.moveTime(partner_startdate.year,
                                                partner_startdate.month,
                                        partner_startdate.day, movedays)
                orgin_enddate = self.moveTime(partner_enddate.year,
                                                partner_enddate.month,
                                        partner_enddate.day, movedays)

            elif datePriority == 'o':
                # default behaviour. so no need to do any actions
                pass


            if orginData:
                # orginData is 1
                # get the orgin data with respect to orgin_startdate
                # and orgin_enddate
                orgin_time = (orgin_startdate, orgin_enddate)
                orgin_data = self.getData(var, Type, orgin_time, hour,
                                                level, **latlonregion)
            # end of if orginData:

            # get the orgin's parnter data with respect to partner_startdate
            # and partner_enddate
            partner_time = (partner_startdate, partner_enddate)
            partner_data = self.getData(var, Type, partner_time, hour,
                                                level, **latlonregion)

        else:
            # end date doesnt passed
            # actions for single date

            if datePriority == 'o':
                # default behaviour. so no need to do any actions
                # calling single date method to extract the data
                if orginData:
                    # orginData is 1
                    # get the orgin data with respect to orgin_startdate
                    orgin_data = self.getData(var, Type, orgin_startdate,
                                              hour, level, **latlonregion)
                # end of if orginData:

                # get the partner data with respect to orgin_startdate.
                # _getDataOfPartners will find its partner_date
                partner_data = self._getDataOfPartners(var, Type,
                             orgin_startdate, hour, level, **latlonregion)

            elif datePriority == 'p':

                if hour:
                    # hour is not None
                    # swaping the orgin date and partners date
                    orgin_startdate, partner_startdate = partner_startdate, orgin_startdate

                    if orginData:
                        # orginData is 1
                        # make date into comptime object
                        partner_startdate = self.timestr2comp(partner_startdate)

                        if hour in self._forecastdays_:
                            movedays = self._forecastdays_.get(hour)
                        else:
                            raise _GribAccessError("wrong %d hour has passed\
                             as arg, its not belongs to fcst grib file hours\
                                        Choose correct hour\n" % (hour))

                        # find out the orgin startdate
                        orgin_startdate = self.moveTime(partner_startdate.year,
                                                    partner_startdate.month,
                                            partner_startdate.day, movedays)

                        # get the orgin data with respect to orgin_startdate
                        orgin_data = self.getData(var, Type, orgin_startdate,
                                                hour, level, **latlonregion)
                    # end of if orginData:

                    # get the orgin's partner data with respect to
                    # partner_startdate
                    partner_data = self.getData(var, Type, partner_startdate,
                                                hour, level, **latlonregion)

                else:
                    # hour is None
                    raise _GribAccessError("you must pass the hour to choose \
                    the partners, since you have set datePriority as 'p' ")

            # end of if datePriority == 'o':
        # end of if xdrange:
        # Resetting the var id
        partner_data.id = var
        if orginData:
            # orginData is 1
            return orgin_data, partner_data
        else:
            # orginData is 0
            return partner_data
    # end of def getDataPartners(...)

    def getRainfallData(self, date=None, level='all', **latlonregion):
        """
        :func:`getRainfallData`: Extract the rainfall data from the xml file
                                 which has created by the cdscan command.

        Inputs : var takes from the instance member of GribAccess class
                if we passed date,level then it should return data accordingly
                 By default level takes 'all' levels.
                 Pass either (lat,lon) or region keyword arg

        Condition : we must set the member variable called rainfallXmlPath
                    and (rainfallXmlVar or rainfallModel), then only we can
                    access this method. rainfallXmlVar is the obeservation
                    rainfall variable name to access the data. OR
                    rainfallModel is the model name, which has set in the
                    global variable names settings. By Using it, this method
                    should get the observation rainfall variable name.

        Written by : Arulalan.T

        Date : 29.05.2011

        """
        if not self.rainfallXmlPath:
            raise _RainfallAccessError("You must set the rainfallXmlPath \
                                      member of this GribAccess instance")
        if not (self.rainfallXmlVar and self.rainfallModel):
            raise _RainfallAccessError("You must set the rainfallXmlVar \
                     or rainfallModel member of this GribAccess instance")
        # create normal XmlAccess object
        rainXmlObj = XmlAccess(self.rainfallXmlPath)
        if self.rainfallXmlVar:
            rainvar = self.rainfallXmlVar
        elif self.rainfallModel:
            # get the observation rainvar name from the global vars settings
            rainvar = variables.get(self.rainfallModel).get('rain').obs_var

        # get the data accessing above object
        rainfall_data = rainXmlObj.getXmlData(rainvar, date, level,
                                                    **latlonregion)
        return rainfall_data
    # end of def getRainfallData(...):

    def getRainfallDataPartners(self, date, hour=None, level='all',
                            orginData=1, datePriority='o', **latlonregion):
        """
        :func:`getRainfallDataPartners`: It returns the rainfall data & its
                     partners data(fcst is the partner of the observation.
                     i.e. rainfall) as MV2 vars

        Condition:
                  startdate is must. enddata is optional one.
                  If both startdate and enddate has passed means, it should
                  return the rainfall data and partnersData within that range.

        Inputs:

           orginData - either 0 or 1. 0 means it shouldnot return the
                       orginData as single MV2 var.
                          1 means it should return both the orginData and its
                          partnersData as two seperate MV2 vars.

           datePriority - either 'o' or 'p'. 'o' means passed date is with
                        respect to orginData. According to this orginData's
                        date, it should return its partnersData.
                        'p' means passed date is with respect to partnersData.
                         According to this partnersData's date, it should
                         return its orginData.

           key word arg lat,lon or region should be passed
           By default hour is None and level is 'all'.

           self.rainfallXmlPath is mandatory one when you choosed orginData
           is 1. you must set the rainfall xml path to the rainfallXmlPath.

           self.rainfallModel is the model name, which has set in the global
           variables settings, to get the model fcst and its obeservation
           variable name to access the data. It is mandatory one.

           date formate 1:
             date = (startdate,enddate)
             here startdate and enddate must be like cdtime.comptime formate.

           date formate 2:
               date = (startdate)

           date formate 3:
               date = 'startdate' or date = 'date'

           eg for date input :
               date = ('2010-5-1','2010-6-30')
               date = ('2010-5-30')
               date = '2010-5-30'

            By default skipdays as 1 takes place. User cant override till now.

        Outputs :

           If user passed single date in the date argument, then it should
           return the data of that particular date
           (both orginData & partnersData) as MV2 variable.

           If user passed start and enddate in the date argument, then it
           should return the data (both orginData & partnersData) for the
           range of dates as MV2 variable with time axis.

        Usage :

             .. note::  if 'r'(observation) file is orginData means 'f'(fcst)
                       files are its partnersData.

           example1:
             >>> a,b = getRainfallDataPartners(date = '2010-6-5',hour = None,
                              level = 'all',orginData = 1,datePriority = 'o',
                                                  lat=(-90,90),lon=(0,359.5))

             a is orginData. i.e. rainfall observation.
             its timeAxis date is '2010-6-5'.

             b is partnersData. i.e. fcst. its 24 hour fcst date w.r.t
             orginData is '2010-6-4'. 48 hour is '2010-6-3'.

             Depends upon the availability of date of fcst files,it should
             return the data.
             In NCMRWF2010 model, it should return maximum of 7 days fcst.

             If we will specify any hour in the same eg, that should return
             only that hour fcst file data instead of returning all the
             available fcst hours data.

           example2:
             >>> a,b = getRainfallDataPartners(date = '2010-6-5',hour = 24,
                              level = 'all',orginData = 1,datePriority = 'o',
                                                  lat=(-90,90),lon=(0,359.5))

             a is orginData. i.e. rainfall observation.
             its timeAxis date is '2010-6-5'.
             b is partnersData. i.e. fcst 24 hour. its fcst date w.r.t
             orginData is '2010-6-6'.

           example3:
             >>> b = getRainfallDataPartners(date = '2010-6-5',hour = 24,
                              level = 'all',orginData = 0,datePriority = 'o',
                                                  lat=(-90,90),lon=(0,359.5))

             b is partnersData. i.e. fcst. its fcst date w.r.t orginData
             is '2010-6-6'.  No orginData. Because we passed orginData as 0.

           example4:
             >>> a,b = getRainfallDataPartnerss(date = '2010-6-5',hour = 24,
                              level = 'all',orginData = 1,datePriority = 'p',
                                                  lat=(-90,90),lon=(0,359.5))

             a is orginData. i.e. rainfall observation.
             its timeAxis date is '2010-6-6'.

             b is partnersData. i.e. fcst 24 hour. its fcst date w.r.t
             orginData is '2010-6-5'.  we can compare this eg4 with eg2.

             In this we passed datePriority as 'p'. So the passed date as
             set to the partnersData and orginData's date has shifted to
             the next day.

           example5:
             >>> a,b = getRainfallDataPartners(date = ('2010-6-5','2010-6-6'),
                                       hour = 24,level = 'all',orginData = 1,
                              datePriority = 'o', lat=(-90,90),lon=(0,359.5))

                  .. note:: We must choose the hour option to select the fcst
                           file, since we are passing the range of dates.

             a is orginData.i.e.rainfall observation.its timeAxis size is 2.
             date are '2010-6-5' and '2010-6-6'.

             b is partnersData.i.e.fcst 24 hour data.its timeAxis size is 2.
             date w.r.t orginData are '2010-6-4' and '2010-6-5'.

             a's '2010-6-5' has partner is b's '2010-6-4'. i.e.
             orginData(rainfall observation) partners is partnersData(fcst)

             same concept for the remains day.
             a's '2010-6-6' has partner is b's '2010-6-5'.

           example6:
             >>> a,b = getRainfallDataPartners(date = ('2010-6-5','2010-6-6'),
                                      hour = 24,level = 'all',orginData = 1,
                              datePriority = 'p', lat=(-90,90),lon=(0,359.5))

                  .. note : We must choose the hour option to select the fcst
                            file, since we are passing the range of dates.

             a is orginData. i.e. rainfall observation.
             its timeAxis size is 2. date are '2010-6-6' and '2010-6-7'.

             b is partnersData. i.e. fcst 24 hour data.
             its timeAxis size is 2. date w.r.t orginData are '2010-6-5'
             and '2010-6-6'.

             a's '2010-6-6' has partner is b's '2010-6-5'. i.e.
             orginData(rainfall observation) partners is partnersData(fcst)

             same concept for the remains day.
             a's '2010-6-7' has partner is b's '2010-6-6'. we can compare
             this eg6 with eg5. In this we passed datePriority as 'p'.
             So the passed date as set to the partnersData and orginData's
             date has shifted towards the next days.

        Written by: Arulalan.T

        Date: 29.05.2011

        """

        orgin_enddate = None

        if isinstance(date, tuple):
            orgin_startdate = date[0] # assign startdate
            if len(date) >= 2:
                orgin_enddate = date[1] # assign enddate
            # end of if len(date) >= 2:

        elif isinstance(date, str) or str(type(date)) == "<type 'comptime'>":
            orgin_startdate = date # assign date

        else:
            raise _GribAccessTypeError('date either must be tuple or string \
                                           or cdtime.component time object')
        # end of if isinstance(date,tuple):

        if orgin_enddate:
            # enddate has passed. so we need hour to get the partners data
            if not hour:
                raise _GribAccessError('You must pass the hour to return the\
             partners data,since you passed the enddate. i.e range of date.')
        # end of if orgin_enddate:

        if not orginData in [0, 1]:
            raise _GribAccessTypeError('orginData either 0 or 1.\
              0 means without orginData. i.e. only partners data. \
              1 means with orginData. i.e. both orginData and partnersData. \
              Default it takes 0.')
        # end of if not orginData in [0, 1]:

        if orginData:
            # orginData is 1
            if datePriority == 'p':

                if hour in self._forecastdays_:
                    movedays = self._forecastdays_.get(hour)
                else:
                    raise _GribAccessError("wrong %d hour has passed as arg\
                                  its not belongs to fcst grib file hours. \
                                  Choose correct hour\n" % (hour))

                #
                # Finding the Orgin's Shift startdate and enddate
                #

                # find out the partners startdate
                partner_startdate = self.findPartners(Type = 'r',
                                        date = orgin_startdate, hour = hour)
                # swaping the orgin date and partners date
                orgin_startdate, partner_startdate = partner_startdate, orgin_startdate

                # find out the orgin startdate
                orgin_startdate = self.moveTime(partner_startdate.year,
                                        partner_startdate.month,
                                        partner_startdate.day, movedays)
                # setting time to extract orginData with start date only
                orgin_time = orgin_startdate

                if orgin_enddate:
                    # find out the partners enddate for rainfall type
                    partner_enddate = self.findPartners(Type = 'r',
                                            date = orgin_enddate, hour = hour)
                    # swaping the orgin date and partners date
                    orgin_enddate, partner_enddate = partner_enddate, orgin_enddate
                    # find out the orgin enddate
                    orgin_enddate = self.moveTime(partner_enddate.year,
                                                partner_enddate.month,
                                                partner_enddate.day, movedays)
                    # setting time to extract orginData with startdate and
                    # enddate
                    orgin_time = (orgin_startdate, orgin_enddate)
                # end of if orgin_enddate:

            elif datePriority == 'o':
                # default behaviour.
                if not orgin_enddate:
                    # setting time to extract orginData with start date only
                    orgin_time = orgin_startdate
                else:
                    # setting time to extract orginData with startdate and
                    # enddate
                    orgin_time = (orgin_startdate, orgin_enddate)
                # end of if not orgin_enddate:

            else:
                raise _GribAccessTypeError("datePriority either 'o' or 'p'. \
                                'o' means passed date set to the orginData.\
                              'p' means passed date set to the partnersData")

            # get the data accessing above object
            rainfall_data = self.getRainfallData(date = orgin_time,
                                                level = level, **latlonregion)
        # end of if orginData:
        # get the model fcst rainvar name from the global vars settings
        fcstrainvar = variables.get(self.rainfallModel).get('rain').model_var
        #
        # Find and get the rainfall partners data
        #
        rainfall_partners_fcst_data = self.getDataPartners(fcstrainvar,
                          Type = 'r', date = date, hour = hour, level = level,
                          orginData = 0, datePriority = datePriority,
                          **latlonregion)
        # apcpsfc is a fcst var for total precipitation.i.e. rain in NCMR grib
        # files
        if orginData:
            # orginData is 1
            return rainfall_data, rainfall_partners_fcst_data
        else:
            # orginData is 0
            return rainfall_partners_fcst_data
    # end of def getRainfallDataPartners(...):

    def getMonthAvgData(self, var, Type, level, month, year,
                        calendarName=None, hour=None, **latlonregion):
        """
        :func:`getMonthAvgData`: It returns the average of the given month
                data (all days in the month) for the passed variable options

        Condition :
         calendarName,level are optional.
         level takes default 'all' if not pass arg for it.
         hour is must when Type arg should be 'f' (fcst) to select xml object.
         Pass either (lat,lon) or region.

        Inputs :
           Type - either 'a' or 'f' or 'o'
           var,level must be belongs to the data file
           month may be even in 3 char like 'apr' or 'April' or 'aPRiL' or
           like any month
           year must be passed as integer
           calendarName default None, it takes cdtime.DefaultCalendar
           key word arg lat,lon or region should be passed

        Outputs :
           It should return the average of the whole month data for the given
           vars as MV2 variable

        Usage :

           example :
             >>> getMonthAvgData(var = "Geopotential Height",Type = 'f',
                         level = 'all', month = 'july',year=2010 , hour = 24,
                          region = AIR ) #lat=(-90,90),lon=(0,359.5)

             returns dataAvg of one month data as single MV2 variable

        Written by: Arulalan.T

        Date: 29.04.2011

        """
        # calling TimeUtility's method monthFirstLast to get the First Last
        # dates of the passed month
        monthFLDate = self.monthFirstLast(month, year, calendarName)
        data = self.getData(var = var, Type = Type, date = monthFLDate,
                            hour = hour, level = level, **latlonregion)
        #
        # Taking average the data over the time axis.
        # The averager will sum all the day data and divide by the no of days
        # in the time axis. finally it should return the AVG data.
        #
        dataAvg = cdutil.averager(data, axis = 't', weights = 'equal')
        return dataAvg
    # end of def getMonthAvgData(...):

