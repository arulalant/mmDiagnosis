"""
.. module:: timeutils
   :synopsis: A useful module for cdtime.comptime conversion to timestr,
              moveTime, tRange, xtRange, cdtime.timeAxis and more ...
.. moduleauthor:: Arulalan.T <arulalant@gmail.com>

"""
import re
import cdms2
import cdutil
import cdtime
import numpy


class _TimeUtilityError(Exception):

    def __init__(self, *args):
        print "\nDaysError Error : "
        for i in args:
            print i


class _TimeUtilityStringError(_TimeUtilityError):
    pass


class _TimeUtilityIntegerError(_TimeUtilityError):
    pass


class _TimeUtilityTypeError(_TimeUtilityError):
    pass


class _TimeUtilityInputError(_TimeUtilityError):
    pass


class TimeUtility():

    def __init__(self):

        self.timeAxis = None
        # set cdtime.comptime pattern regular expression object
        self.comppattern = re.compile(r"""
                                ([0-9]{1,4})          # YYYY formate (1 to 4
                                                      # digits of year accept)
                                -                     # ifen - seperator
                                ([01]?[0-9])          # MM formate
                                -                     # ifen - seperator
                                ([0123]?[0-9])        # DD formate
                                (\s{1}                # space seperator
                                ([012]?[0-9])         # hh formate
                                :?                    # colon : seperator
                                ([012345]?[0-9])?     # mm formate
                                :?                    # colon : seperator
                                ([012345]?[0-9])?     # ss formate (Sec)
                                .?                    # dot seperator
                                ([0-9]))?             # ss formate (millisec)
                                $                     # End of input
                                # hh:mm:ss.ss all are optional one by suffix ?
                                """, re.VERBOSE)

        # set yyyymmddhh pattern regular expression object
        self.ymdpattern = re.compile(r"""
                               (\d{4})                 # YYYY formate
                               ([01][1-9])             # MM formate
                               ([0123][0-9])           # DD formate
                               ([01][0-9]|[2][0-3])?   # HH formate (optional)
                               $                       # End of input
                               """, re.VERBOSE)
    # end of def __init__(self):

    def __add__(self, otherTimeAxis):
        """
        We can add two cdtime.timeAxis using the '+' operator.

        The resultant timeaxis should be w.r.t first timeAxis's units.

        To use this, user must set the first time axis by instance of this
        class variable called 'timeAxis'.

        Usage:
            example 0:
                >>> timobj = TimeUtility()
                >>> timobj.timeAxis = fistTimeAxis
                >>> newTimeAxis = timobj + secondTimeAxis

                 ..note:: Assign the first time axis to the TimeUtility object
                          Then using '+' operator add the second axis. It
                          should return the third axis (first + second).
                          The second time axis units should be w.r.t first
                          time axis's units.

            example 1:
                >>> timobj = TimeUtility()
                >>> timobj.timeAxis = fistTimeAxis
                >>> print fistTimeAxis
                >>> id: time
                   Designated a time axis.
                   units:  days since 2011-5-8 12:0
                   Length: 238
                   First:  0.0
                   Last:   237.0
                   Other axis attributes:
                      calendar: gregorian
                      axis: T
                   Python id:  0x252c550
                >>>
                 ..note:: Assign the first time axis to the TimeUtility object
                          fistTimeAxis units is 'days since 2011-5-8 12:0'.
                          Its total days from '2011-5-8 12:0' to
                          '2011-12-31 12:0'.

                >>> print secondTimeAxis
                >>>id: time
                   Designated a time axis.
                   units:  days since 2011-5-8 12:0
                   Length: 128
                   First:  238.0
                   Last:   365.0
                   Other axis attributes:
                      calendar: gregorian
                      axis: T
                   Python id:  0x252c790
                >>>
                 ..note:: secondTimeAxis units is 'days since 2011-5-8 12:0'.
                          Its total days from '2012-1-1 12:0' to
                          '2012-5-7 12:0'.

                >>> newTimeAxis = timobj + secondTimeAxis
                >>> print newTimeAxis
                   id: time
                   Designated a time axis.
                   units:  days since 2011-5-8 12:0
                   Length: 366
                   First:  0.0
                   Last:   365.0
                   Other axis attributes:
                      calendar: gregorian
                      axis: T
                   Python id:  0x251ca90
                >>>
                 ..note:: add the first time axis obj + secondTimeAxis. The
                          result  thirdTimeAxis units is same as first time
                          axis units 'days since 2011-5-8 12:0'.
                          Its total days from '2011-5-8 12:0' to
                          '2012-5-7 12:0'.

            example 2:
                >>> t1 = timobj._generateTimeAxis(365, '2011-1-1')
                >>> t1
                   id: time
                   Designated a time axis.
                   units:  days since 2011-1-1
                   Length: 365
                   First:  0
                   Last:   364
                   Other axis attributes:
                      calendar: gregorian
                      axis: T
                   Python id:  0x7fc2279aab50
                >>>
                 ..note:: generate the time axis of 2011 year. Its unit is
                          'days since 2011-1-1'. It contains 365 days.
                                                    '
                >>> t2 = timobj._generateTimeAxis(365, '2012-1-1')
                >>> t2
                   id: time
                   Designated a time axis.
                   units:  days since 2012-1-1
                   Length: 365
                   First:  0
                   Last:   364
                   Other axis attributes:
                      calendar: gregorian
                      axis: T
                   Python id:  0x251cd50
                >>>
                 ..note:: generate the time axis of 2012 year. Its unit is
                          'days since 2012-1-1'. It contains 366 days.

                >>> timobj.timeAxis = t1
                >>> t3 = timobj + t2
                >>> t3
                   id: time
                   Designated a time axis.
                   units:  days since 2011-1-1
                   Length: 730
                   First:  0
                   Last:   729
                   Other axis attributes:
                      calendar: gregorian
                      axis: T
                   Python id:  0x251c890
                >>>
                 ..note:: assing timobj.timeAxis as t1, then t3 = timobj + t2.
                          The resultant t3 time axis units is
                          'days since 2011-1-1'. And its contains both 2011
                          and 2012 year days. Its total length is 729.

        Written By : Arulalan.T

        Date : 12.06.2012

        """
        if self.timeAxis  is None:
            raise ValueError("Please set the '%s' Cls instance 'timeAxis' \
                              variable, to add with another timeAxis." % self.__class__)

        if not (isinstance(self.timeAxis, cdms2.axis.TransientAxis) or
                isinstance(self.timeAxis, cdms2.axis.FileAxis) or
                isinstance(self.timeAxis, cdms2.axis.Axis)):
            print "'%s' Cls instance 'timeAxis' " % self.__class__, self.timeAxis
            raise _TimeUtilityTypeError("first timeAxis is not the type of \
                                cdms2.axis.Axis or cdms2.axis.TransientAxis")

        if not (isinstance(otherTimeAxis, cdms2.axis.TransientAxis) or
                isinstance(otherTimeAxis, cdms2.axis.FileAxis) or
                isinstance(otherTimeAxis, cdms2.axis.Axis)):
            print "Second operand timeAxis of add method ", otherTimeAxis
            raise _TimeUtilityTypeError("second timeAxis is not the type of \
                                cdms2.axis.Axis or cdms2.axis.TransientAxis")

        # convert the first and second time axis as list
        firstTimeAxisValues = list(self.timeAxis[:])
        secondTimeAxisValues = list(otherTimeAxis[:])

        if self.timeAxis.units != otherTimeAxis.units:
            # two time axis units are different. So we need to adjust the
            # second time axis time values w.r.t to first time axis units.

            # get the last day count val of the fist time axis and add 1.
            # i.e. counter is 366 or 367. so the second time axis, first day
            # should be 366 or 377 w.r.t first time axis units.
            counter = firstTimeAxisValues[-1] + 1
            # keep add the counter to the whole second axis values
            secondTimeAxisValues = [counter + val for val in secondTimeAxisValues]
        # add the first and second time axis values
        newTimeAxisValues = firstTimeAxisValues + secondTimeAxisValues
        # get the first time axis units
        timeUnits = self.timeAxis.units.split('since ')
        # unit values i.e. days or months
        unitvalue = timeUnits[0].strip()
        # unit days/months since date
        sincedate = timeUnits[1]
        # generate the combined (first time axis + second time axis) new time
        # axis units w.r.t first time axis and return it.
        return self._generateTimeAxis(newTimeAxisValues, sincedate, units = unitvalue)
    # end of def __add__(self, otherTimeAxis):

    def timestr2comp(self, date):
        """
        :func:`timestr2comp`: To convert date from yyyymmdd[hh] formate into
                          cdtime.comptime formate
        Condition :
                passing date must be yyyymmdd formate in either int or str
        Inputs:
                date in yyyymmdd formate or yyyymmddhh formate.
                i.e. hour(hh) is optional.
        Outputs:
                It should return the date in cdtime.comptime object type
        Usage:
            example1:
                >>> timestr2comp(20110423)
                2011-4-23 0:0:0.0
                  .. note:: It should return as cdtime.comptype. Here we didnt
                            pass the hour. i.e only yyyymmdd formate
            example2:
                >>> timestr2comp(2011082010)
                2011-8-20 10:0:0.0
                  ..note:: Here it should return cdtime with hours also.
                           We passed yyyymmddhh formate. i.e include hh
            example3:
                >>> timestr2comp(2011082023)
                2011-8-20 23:0:0.0
                  ..note:: we cannot pass 24 as hour here. Max 23 hours only.

        Written by: Arulalan.T

        Date: 23.04.2011
        Updated : 21.08.2011

        """
        if str(type(date)) == "<type 'comptime'>":
            # passed date itself comptime object only
            return date
        if isinstance(date, int):
            date = str(date)
        # re match
        if self.comppattern.match(date):
            # i.e. date is comptime in string formate
            # so make it as comptime object
            return cdtime.s2c(date)

        if self.ymdpattern.match(date):
            # i.e date is yyyymmdd string formate
            year = int(date[0:4])
            month = int(date[4:6])
            day = int(date[6:8])
            if len(date) == 10:
                hour = int(date[-2:])
                return cdtime.comptime(year, month, day, hour)
            else:
                return cdtime.comptime(year, month, day)
        else:
            raise _TimeUtilityStringError('The given date either comptime \
                         object or comptime string or yyyymmdd formate only')
    # end of def timestr2comp(self, date):

    def comp2timestr(self, comptime, returnHour='y'):
        """
        :func:`comp2timestr`: To convert date from cdtime.comptime into
                                'yyyymmdd' formate or 'yyyymmddhh' formate
                                as string

        Condition :   passing date must be comptime formate

        Inputs :    date in comptime.
                    returnHour takes 'y' or 'yes' or 'n' or 'no'.
                    Default it takes 'y'.

        Outputs : It should return the date in 'yyyymmddhh' string formate, if
                  returnHour passed 'y' or 'yes'.
                  It should return the date in 'yyyymmdd' string formate, if
                  returnHour passed 'n' or 'no'.

        Usage :
          example1 :
             >>> compobj = cdtime.comptime(2010,4,29) -> 2010-4-29 0:0:0.0
             >>> comp2timestr(compobj)
             >>> '2010042900'
           .. note:: It should return in yyyymmddhh string formate by default.
                     Hour is 00.

          example2 :
             >>> compobj = cdtime.comptime(2010,4,29,10) -> 2010-4-29 10:0:0.0
             >>> comp2timestr(compobj)
             >>> '2010042910'
           .. note:: It should return in yyyymmddhh string formate by default.
                     Hour is 10.

          example2 :
             >>> compobj = cdtime.comptime(2010,4,29,10) -> 2010-4-29 10:0:0.0
             >>> comp2timestr(compobj, returnHour = 'n')
             >>> '20100429'
           .. note:: It should return in yyyymmdd string formate only even
                     though hour passed in the component object. Because we
                     passed returnHour as 'n'.

        Written by : Arulalan.T

        Date : 29.04.2011
        Updated : 21.08.2011

        """

        if str(type(comptime)) == "<type 'comptime'>":
            # convert comptime into yyyymmdd
            yyyymmdd = str(int(comptime.absvalue))
        if isinstance(comptime, str):
            # if comptime is string
            if self.comppattern.match(comptime):
                comptime = cdtime.s2c(comptime)
                yyyymmdd = str(int(comptime.absvalue))
            else:
                raise _TimeUtilityTypeError("passed date is not \
                              cdtime.comptime object or its string formate")
        if returnHour in ['y', 'yes']:
            hh = str(comptime.hour)
            if len(hh) == 1:
                # make h as hh formate
                hh = '0' + hh
            return yyyymmdd + hh
        elif returnHour in ['n', 'no']:
            return yyyymmdd
        else:
            raise _TimeUtilityTypeError("returnHour takes either 'y/yes' \
                                                    or 'n/no' option only")
        # end of def comp2timestr(self, comptime):

    def monthFirstLast(self, month, year, calendarName=None, returnType='c',
                                                             returnHour='n'):
        """
        :func:`monthFirstLast`: To find and return the first date and
        last date of the given month of the year, with cdtime.calendar option.

        Condition :
           passing month should be either integer of month or name of
           the month in string.
           year should be an integer or string
           calendar is optional. It takes default calendar

        Inputs :
           month may be even in 3 char like 'apr' or 'April' or 'aPRiL' or
           like any month
           year must be passed as integer.
           returnType is either 'c' or 's'. If 'c' means it should return
           as cdtime.comptime object and if 's' means it should return date as
           yyymmddhh or yyyymmdd string formate.
           returnHour is either 'y' or 'n'. If yes means, and returnType is
           's' means, it should return hour also.(i.e yyymmddhh), otherwise
           yyyymmdd only (by default).

        Outputs :
           It should return the first date and last date of the given month
           & year in yyyymmdd string formate inside tuple

        Usage :
           example1 :
             >>> monthFirstLast(4,2010)
             >>> (2010-4-1 0:0:0.0, 2010-4-30 0:0:0.0)
            .. note::  It should return as cdtime.comptime object

           example2 :
             >>> monthFirstLast('feb','2010',returnType = 's')
             >>> ('20100228', '20100228')
            .. note::  It should return in yyyymmdd string formate

        Written by : Arulalan.T

        Date : 29.04.2011

        """
        if isinstance(month, int):
            if not 1 <= month <= 12:
                raise _TimeUtilityIntegerError('not valid month passed. \
                                month must be in between 1 to 12')

        elif isinstance(month, str):
            # use cdutil method to get the month index
            month = cdutil.getMonthIndex(month)
            if month == []:
                raise _TimeUtilityError('wrong month arg passed')
            else:
                month = month[0]
        else:
            raise _TimeUtilityTypeError("month either string or interger\
                                 of the month in between 1 to 12")

        if not isinstance(year, int):
            year = int(year)

        if calendarName == None:
            calendar = cdtime.DefaultCalendar
        else:
            if not isinstance(calendarName, int):
                raise _TimeUtilityError(' The passed calendarName is not an \
                                instance of cdtime.calendar ')
            calendar = calendarName

        if not returnType in ['c', 's']:
            raise _TimeUtilityTypeError("returnType is either 'c' or 's'")
        if not returnHour in ['y', 'yes', 'n', 'no']:
            raise _TimeUtilityTypeError("returnHour is either 'y/yes' or \
                                                             'n/no' only")
        firstday = cdtime.comptime(year, month, 1)
        nextmonth = firstday.add(1, cdtime.Month, calendar)
        lastday = nextmonth.sub(1, cdtime.Day, calendar)

        if returnType == 's':
            firstday = self.comp2timestr(firstday, returnHour)
            lastday = self.comp2timestr(lastday, returnHour)

        return (firstday, lastday)
    # end of def monthFirstLast(...):

    def _getYearFirstLast(self, year):
        """
        Date : 29.07.2013
        """
        if isinstance(year, int):
            sdate = str(year) + '-1-1 0:0:0.0'
            edate = str(year) + '-12-31 23:59:0.0'
        elif isinstance(year, tuple):
            sdate = str(year[0]) + '-1-1 0:0:0.0'
            edate = str(year[1]) + '-12-31 23:59:0.0'
        else:
            raise ValueError("pass year as either int or tuple of numbers")
        return (sdate, edate)
    # end of def _getYearFirstLast(year):

    def moveTime(self, year, month, day, moveday=0, movehour=0,
                                 calendarName=None, returnType='c'):
        """
        :func:`moveTime`: To move the day or/and hour in both direction and
                           get the moved date yyyymmdd/yyyymmddhh format

        Condition : passing year,month,day,moveday,movehour should be integer
                    type.

        Inputs : moveday is an integer to move the date. If it is negative,
                 then we should get the previous date with interval of the
                 no of days [i.e. moveday]

                 movehour is an integer to move the hours. If it is negative,
                 then we should get the previous day hours with interval of
                 the hours [i.e. movehour]

                 returnType is either 'c' or 's'.
                 'c' means cdtime.comptime object
                 's' means yyyymmdd string formate if movehour is 0 and
                    yyyymmddhh if movehour has passed some hour.

        Outputs : It should return the comptime date object by default.
                  using returnType = 's', we can get yyyymmdd or yyymmddhh
                  string formate.

        Usage :
           example1 :
                >>> moveTime(2011, 04, 03, moveday=200)
                2011-10-20 0:0:0.0
                    ..note:: 200 days moved
                >>> moveTime(2011, 04, 03, moveday = -200, returnType='s')
                '2010-9-15'
                    ..note:: 200 days moved in backward and return as string
                             in yyyymmdd formate
           example2 :
                >>> moveTime(2011, 4, 3, moveday = 0, movehour = 10)
                2011-4-3 10:0:0.0
                    ..note:: 0 days moved.But 10 hours moved.

                >>> moveTime(2011,4,3, moveday = 2, movehour = 10)
                2011-4-5 10:0:0.0
                    ..note:: Both days and hours are moved.
                             2 days, 10 hours moved.

           example3 :
                >>> moveTime(2011,4,3,moveday=2,movehour=10,returnType='s')
                '2011040510'
                    ..note:: Here passed returnType as 's'. Also passed hour
                             as 10. So it should return as yyyymmddhh fromate

                >>> moveTime(2011,4,3,moveday = 2,returnType='s')
                '20110405'
                    ..note:: Here we didnt pass hour. So it should return
                             yyyymmdd formate only.

           example4 :
                >>> moveTime(2011,4,3,returnType='s')
                '20110403'
                    ..note:: Here we didnt pass any moveday and any movehour.
                             So it should return only what we passed the date,
                             without any movements in days/hours.

           example4 :
                >>> moveTime(2011,2,28,366)
                2012-2-29 0:0:0.0
                    ..note:: 2012 is a leap year. By default it take
                             cdtime.DefaultCalendar.

                >>> moveTime(2011,2,28,366,calendarName=cdtime.NoLeapCalendar)
                2012-3-1 0:0:0.0
                    ..note:: Eventhough 2012 is a leap year, it doesnt give
                             date like previous example, because we have
                             passed cdtime.cdtime.NoLeapCalendar.

        Written by : Arulalan.T

        Date : 06.04.2011
        Updated : 21.08.2011

        """

        # already imported cdtime module from cdat path
        if not (isinstance(year, int) and isinstance(month, int) and
                isinstance(day, int) and isinstance(moveday, int) and
                isinstance(movehour, int)):
            raise _TimeUtilityIntegerError('year, month, day, moveday, \
                                            movehour should be interger type')

        if calendarName == None:
            calendar = cdtime.DefaultCalendar
        else:
            if not isinstance(calendarName, int):
                raise _TimeUtilityError('The passed calendarName is not an \
                                insstnce of cdtime.calendar ')
            calendar = calendarName
         # end of if

        if not returnType in ['c', 's']:
            raise _TimeUtilityTypeError("returnType either should 's' or 'c'.\
                    if 's' means the return date should be in string type. \
                  if 'c' means the return date should be cdtime type itself")

        comptime = cdtime.comptime(year, month, day)
        daychanges = comptime.add(moveday, cdtime.Days, calendar)
        hourchanges = daychanges.add(movehour, cdtime.Hours, calendar)
        if returnType == 'c':
            return hourchanges
        if returnType == 's':
            if movehour:
                return self.comp2timestr(hourchanges, returnHour = 'y')
            else:
                return self.comp2timestr(hourchanges, returnHour = 'n')
    # end of def moveTime(...):

    def xtRange(self, startdate, enddate, stepday=0, stephour=0,
                        calendarName=None, returnType='c', returnHour='y'):
        """
        :func:`xtRange`: generate the dates in yyyymmdd formate or yyymmddhh
                  formate or cdtime.comptime object from startdate to enddate
                  with stepday or stephour.
                  we can set the cdtime.calendarName to generate the date(s)
                  in between the given range.

                  xtRange means xtimeRange

        Condition :
                 The startdate and enddate must be either yyyymmdd or
                 yyyymmddhh or cdtime.comptime object or cdtime.comptime
                 string formate.
                 We can use either stepday or stephour at a time. Can not use
                 both(stepday and stephour) at the same time.
                 if enddate is higher than the startdate, then stepday/
                 stephour must be +ve.
                 if enddate is lower than the startdate, then stepday/stephour
                 must be -ve.
                 By default stepday is 0 day and stephour is 0 hour.

        Inputs :
                 startdate, enddate
                 stepday to skip the days.
                 stephour to skip the hours.
                 calendarName is one of the cdtime calendar type
                 returnType is either 's' or 'c'. if 's' means the return date
                 should be in string type. if 'c' means the return date should
                 be cdtime type itself.
                 Default returnType takes 'c' as arg.
                 returnHour is either 'y' or 'yes' or 'n' or 'no'. If 'y/yes'
                 means it should return the hour (yyymmddhh), if returnType
                 is 's'. If 'n/no' means it shouldnt return hour (yyyymmdd),
                 if returnType is 's'.
                 Default returnHour takes 'y' as arg.

        Outputs :
                 It should return a generator not as list.
                 Using this generator we can produce the date(s) in between
                 the startdate and enddate including both the startdate and
                 enddate.

        Usage :
           example1 :
               >>> gen = xtRange(20110407, 20110410, stepday = 1,
               ...                                         returnType = 's')
               >>> for i in gen:
               ...     print i
               ...
               2011040700
               2011040800
               2011040900
               2011041000
             ..note::  Here returnType is 's' and returnHour is 'yes' by
                           default. So it should return with hour (yyymmddhh).

               >>> gen = xtRange(20110407, 20110410, stepday = 1,
               ...                       returnType = 's', returnHour = 'no')
               >>> for i in gen:
               ...     print i
               ...
               20110407
               20110408
               20110409
               20110410
             ..note:: Here we passed returnHour is 'no'. So it should not
                          return hour. (only yyyymmdd)

           example2 :
              >>> gen = xtRange(20120227, 20120301 , stepday = 1,
              ...                  calendarName = cdtime.NoLeapCalendar,
              ...                   returnType = 's', returnHour = 'no')
              >>> for i in gen:
              ...     print i
              ...
              20120227
              20120228
              20120301

            .. note:: In the example 2, 2012 is leap year, since we passed
              cdtime.NoLeapCalendar it generated without 29th day in feb 2012.
              we can use stepday as any +ve integer number.
              The generator returns both startdate and enddate also.

           example3 :
              >>> gen = xtRange(startdate = 20110407, enddate = 20110410)
              >>> for i in gen:
              ...     print i
              ...
              >>>
            .. note:: In this example it should not generate any dates in
                      between the startdate and enddate, since we didnt pass
                      either stepday or stephour.

           example4 :
              >>> gen = xtRange(startdate = cdtime.comptime(2011,04,07),
              ...          enddate = cdtime.comptime(2011,04,10), stepday = 1,
              ...                                            returnType = 'c')
              >>> for i in gen:
              ...     print i
              ...
              2011-4-7 0:0:0.0
              2011-4-8 0:0:0.0
              2011-4-9 0:0:0.0
              2011-4-10 0:0:0.0

            .. note:: Here the input dates are cdtime.comptime object itself.

           example5 :
              >>> gen = xtRange(startdate = cdtime.comptime(2011,04,11),
              ...          enddate = cdtime.comptime(2011,04,7), stepday = -1,
              ...          returnType = 'c')
              >>> for i in gen:
              ...     print i
              ...
              2011-4-10 0:0:0.0
              2011-4-9 0:0:0.0
              2011-4-8 0:0:0.0
              2011-4-7 0:0:0.0

            .. note:: In this example we have passed startdate is higher than
              then enddate, So we must have to pass the stepdays in -ve sign.

           example 6:
              >>> gen = xtRange('2011-4-7', '2011-4-10', stepday = 1)
              >>> for i in gen:
              ...     print i
              ...
              2011-4-7 0:0:0.0
              2011-4-8 0:0:0.0
              2011-4-9 0:0:0.0
              2011-4-10 0:0:0.0

             ..note:: Here it genearates the cdtime.comptime object by default
                      We passed the inputs are cdtime.comptime date string
                      formate (yyyymmdd)only.

              >>> gen = xtRange('2011-4-7 12:0:0.0', '2011-4-10 0:0:0.0',
                                                                stephour = 12)
              >>> for i in gen:
              ...     print i
              ...
              2011-4-7 12:0:0.0
              2011-4-8 0:0:0.0
              2011-4-8 12:0:0.0
              2011-4-9 0:0:0.0
              2011-4-9 12:0:0.0
              2011-4-10 0:0:0.0

             ..note:: Here we passed 12:0:0.0 hours in startdate, 0:0:0.0
                      hours in enddate, and stephour as 12. Note here the
                      input dates are not cdtime.comptime object. But those
                      are cdtime.comptime string formate (yyymmddhh).
           example 7:
              >>> gen = xtRange('2011040712', '2011-4-10 10:0:0.0',
              ...                                             stephour = 12)
              >>> for i in gen:
              ...     print i
              ...
              2011-4-7 12:0:0.0
              2011-4-8 0:0:0.0
              2011-4-8 12:0:0.0
              2011-4-9 0:0:0.0
              2011-4-9 12:0:0.0
              2011-4-10 0:0:0.0

            ..note:: Here startdate as in 'yyymmddhh' string formate and
                     enddate as in cdtime.comptime string formate. you can
                     play with combination of differnt inputs.

        Written by : Arulalan.T

        Date : 07.04.2011

        Updated : 23.08.2011

        """
        if stepday and stephour:
            raise _TimeUtilityInputError("You cannot pass both stepday and \
                                                                    stephour")

        if not returnHour in ['y', 'yes', 'n', 'no']:
            raise _TimeUtilityInputError("returnHour must be 'y/n' only")

        if not isinstance(stepday, int):
                raise _TimeUtilityIntegerError('stepday must be an integer')

        if not isinstance(stephour, int):
                raise _TimeUtilityIntegerError('stephour must be an integer')

        if calendarName == None:
            calendar = cdtime.DefaultCalendar
        else:
            if not isinstance(calendarName, int):
                raise _TimeUtilityError('The passed calendarName is not an \
                                         instance of cdtime.calendar')
            calendar = calendarName
        # end of if calendarName == None:

        if not returnType in ['c', 's']:
            raise _TimeUtilityTypeError("returnType either should 's' or 'c'.\
                if 's' means the return date should be in string type. \
               if 'c' means the return date should be cdtime type itself")
        # end of if not returnType in [0,1]:
        # finding the passed dates are cdtime.comptime type.
        # We cant find this using 'isinstance' method.
        # so we are using str comparision
        if (str(type(startdate)) == "<type 'comptime'>" and
                    str(type(enddate)) == "<type 'comptime'>"):
            startcomp = startdate
            endcomp = enddate
        else:
            if not isinstance(startdate, str):
                startdate = str(startdate)
            if not isinstance(enddate, str):
                enddate = str(enddate)

            if not (self.comppattern.match(startdate) or
                    self.ymdpattern.match(startdate)):
                raise _TimeUtilityStringError('The startdate either comptime \
                object or comptime string or yyyymmdd/yyymmddhh formate only')
            if not (self.comppattern.match(enddate) or
                    self.ymdpattern.match(enddate)):
                raise _TimeUtilityStringError('The enddate either comptime \
                object or comptime string or yyyymmdd/yyymmddhh formate only')

            if self.ymdpattern.match(startdate):
                # genearate start comptime object from yyyymmdd formate
                startyear = int(startdate[0:4])
                startmonth = int(startdate[4:6])
                startday = int(startdate[6:8])
                if len(startdate) == 10:
                    starthour = int(startdate[-2:])
                    startcomp = cdtime.comptime(startyear, startmonth,
                                                    startday, starthour)
                else:
                    startcomp = cdtime.comptime(startyear, startmonth,
                                                                  startday)
                # end of if len(startdate) == 10:
            else:
                # It must be string type and comppattern only
                # genearate start comptime object from its str type formate
                startcomp = cdtime.s2c(startdate)

            if self.ymdpattern.match(enddate):
                # genearate end comptime object from yyyymmdd formate
                endyear = int(enddate[0:4])
                endmonth = int(enddate[4:6])
                endday = int(enddate[-2:])
                if len(enddate) == 10:
                    endhour = int(enddate[-2:])
                    endcomp = cdtime.comptime(endyear, endmonth, endday,
                                                                     endhour)
                else:
                    endcomp = cdtime.comptime(endyear, endmonth, endday)
                # end of if len(enddate) == 10:
            else:
                 # It must be string type and comppattern only
                # genearate end comptime object from its str type formate
                endcomp = cdtime.s2c(enddate)
        # end of if str(type(startdate)) == "<type 'comptime'>" ...:

        # comparing startcompdate and endcompdate
        compare = startcomp.cmp(endcomp)

        if compare == 1:
            # The end date is lower than the start date
            if stepday:
                if cmp(stepday, 0) != -1:
                    raise _TimeUtilityError("The stepdays must be negative \
                           since the startdate is 'higher' than the enddate")
                else:
                    stepday = stepday * -1
                    sign = -1
                # end of if cmp(stepday,0) != -1:
            # end of stepday
            if stephour:
                if cmp(stephour, 0) != -1:
                    raise _TimeUtilityError("The stephour must be negative \
                           since the startdate is 'higher' than the enddate")
                else:
                    stephour = stephour * -1
                    sign = -1
                # end of if cmp(stephour,0) != -1:
            # end of stephour
        elif compare == 0:
            raise _TimeUtilityError("both are same date ")
        else:
            sign = 1
            if cmp(stepday, 0) == -1:
                raise _TimeUtilityError("The stepdays must be positive since \
                            the startdate is 'lower' than the enddate")
            # end of if cmp(stepdays,0) == -1:
            if cmp(stephour, 0) == -1:
                raise _TimeUtilityError("The stephour must be positive since \
                            the startdate is 'lower' than the enddate")
            # end of if cmp(stepdays,0) == -1:
        # end of if compare == 1:

        # making hourstring from startcomp to find out the no of days in b/w
        # startdate and enddate
        hourstring = 'hours since %s' % (startcomp)
        # genearating the relative cdtime of startdate
        startdaysrel = startcomp.torel(hourstring, calendar)
        starthours = startdaysrel.value

        # genearating the relative cdtime of enddate
        enddaysrel = endcomp.torel(hourstring, calendar)
        endhours = enddaysrel.value
        # finding the difference hours in between starthours and endhours
        # multiplying the sign value to make it as +ve, if difference is -ve
        diffhours = (endhours - starthours) * sign

        diffdays = int(diffhours / 24.0)
        if stepday:
            for movedays in xrange(0, diffdays + 1, stepday):
                # Here we are multiplying the movedays with sign.
                # If that is -ve means, days goes backward
                returndate = startcomp.add(movedays * sign, cdtime.Days,
                                                                 calendar)
                if returnType == 'c':
                    # returning the comptime type date
                    yield returndate
                else:
                    # returning the string type (yyyymmdd) date
                    returndate = self.comp2timestr(returndate, returnHour)
                    yield returndate
            # end of for movedays in xrange(0,diffdays+1,stepdays):
        # end of if stepday:
        if stephour:
            diffhours = int(diffhours)
            for movehours in xrange(0, diffhours + 1, stephour):
                # Here we are multiplying the movehours with sign.
                # If that is -ve means, hours goes backward
                returndate = startcomp.add(movehours * sign, cdtime.Hours,
                                                                  calendar)
                if returnType == 'c':
                    # returning the comptime type date
                    yield returndate
                else:
                    # returning the string type (yyyymmddhh) date
                    returndate = self.comp2timestr(returndate, returnHour)
                    yield returndate
            # end of for movehours in xrange(0, diffhours + 1, stephour):
        # end of if stephour:

    # end of def xtRange(...):

    def tRange(self, startdate, enddate, stepday=0, stephour=0,
                         calendarName=None, returnType='c', returnHour='y'):
        """
        :func:`tRange`: generate the dates in yyyymmdd formate or yyymmddhh
                  formate or cdtime.comptime object from startdate to enddate
                  with stepday or stephour.
                  we can set the cdtime.calendarName to generate the date(s)
                  in between the given range.

                  tRange means timeRange

        Condition :
                 The startdate and enddate must be either yyyymmdd or
                 yyyymmddhh or cdtime.comptime object or cdtime.comptime
                 string formate.
                 We can use either stepday or stephour at a time. Can not use
                 both(stepday and stephour) at the same time.
                 if enddate is higher than the startdate, then stepday/
                 stephour must be +ve.
                 if enddate is lower than the startdate, then stepday/stephour
                 must be -ve.
                 By default stepday is 0 day and stephour is 0 hour.

        Inputs :
                 startdate, enddate
                 stepday to skip the days.
                 stephour to skip the hours.
                 calendarName is one of the cdtime calendar type
                 returnType is either 's' or 'c'. if 's' means the return date
                 should be in string type. if 'c' means the return date should
                 be cdtime type itself.
                 Default returnType takes 'c' as arg.
                 returnHour is either 'y' or 'yes' or 'n' or 'no'. If 'y/yes'
                 means it should return the hour (yyymmddhh), if returnType
                 is 's'. If 'n/no' means it shouldnt return hour (yyyymmdd),
                 if returnType is 's'.
                 Default returnHour takes 'y' as arg.

        Outputs :
                 It should return a list which contains the date(s) in between
                 the startdate and enddate including both the startdate and
                 enddate.

        Usage :
           example1 :
               >>> tRange(20110407, 20110410, stepday = 1, returnType = 's')
               ['2011040700', '2011040800', '2011040900', '2011041000']

             ..note::  Here returnType is 's' and returnHour is 'yes' by
                           default. So it should return with hour (yyymmddhh).

               >>> tRange(20110407, 20110410, stepday = 1, returnType = 's',
                                                        returnHour = 'no')
               ['20110407', '20110408', '20110409', '20110410']

             ..note:: Here we passed returnHour is 'no'. So it should not
                          return hour. (only yyyymmdd)

           example2 :
              >>> tRange(20120227, 20120301 , stepday = 1,
                                calendarName = cdtime.NoLeapCalendar,
                                returnType = 's', returnHour = 'no')
              ['20120227', '20120228', '20120301']

            .. note:: In the example 2, 2012 is leap year, since we passed
              cdtime.NoLeapCalendar it generated without 29th day in feb 2012.
              we can use stepday as any +ve integer number.
              The generator returns both startdate and enddate also.

           example3 :
              >>> tRange(startdate = 20110407, enddate = 20110410)
              []
            .. note:: In this example it should not generate any dates in
                      between the startdate and enddate, since we didnt pass
                      either stepday or stephour.

           example4 :
              >>> tRange(startdate = cdtime.comptime(2011,04,07),
              ...          enddate = cdtime.comptime(2011,04,10), stepday = 1,
              ...                                            returnType = 'c')
              [2011-4-7 0:0:0.0, 2011-4-8 0:0:0.0, 2011-4-9 0:0:0.0,
                                                  2011-4-10 0:0:0.0]

            .. note:: Here the input dates are cdtime.comptime object itself.

           example5 :
              >>> tRange(startdate = cdtime.comptime(2011,04,11),
              ...          enddate = cdtime.comptime(2011,04,7), stepday = -1,
              ...          returnType = 'c')
              [2011-4-11 0:0:0.0, 2011-4-10 0:0:0.0, 2011-4-9 0:0:0.0,
                                    2011-4-8 0:0:0.0, 2011-4-7 0:0:0.0]

            .. note:: In this example we have passed startdate is higher than
              then enddate, So we must have to pass the stepdays in -ve sign.

           example 6:
              >>> tRange('2011-4-7', '2011-4-10', stepday = 1)
              [2011-4-7 0:0:0.0, 2011-4-8 0:0:0.0, 2011-4-9 0:0:0.0,
                                                   2011-4-10 0:0:0.0]

             ..note:: Here it genearates the cdtime.comptime object by default
                      We passed the inputs are cdtime.comptime date string
                      formate (yyyymmdd)only.

              >>> tRange('2011-4-7 12:0:0.0', '2011-4-10 0:0:0.0',
              ...                                            stephour = 12)
              [2011-4-7 12:0:0.0, 2011-4-8 0:0:0.0, 2011-4-8 12:0:0.0,
               2011-4-9 0:0:0.0, 2011-4-9 12:0:0.0, 2011-4-10 0:0:0.0]

             ..note:: Here we passed 12:0:0.0 hours in startdate, 0:0:0.0
                      hours in enddate, and stephour as 12. Note here the
                      input dates are not cdtime.comptime object. But those
                      are cdtime.comptime string formate (yyymmddhh).

            example 7:
              >>> tRange('2011040712', '2011-4-10 10:0:0.0', stephour = 12)
              [2011-4-7 12:0:0.0, 2011-4-8 0:0:0.0, 2011-4-8 12:0:0.0,
               2011-4-9 0:0:0.0, 2011-4-9 12:0:0.0, 2011-4-10 0:0:0.0]

            ..note:: Here startdate as in 'yyymmddhh' string formate and
                     enddate as in cdtime.comptime string formate. you can
                     play with combination of differnt inputs.

        Written by : Arulalan.T

        Date : 23.08.2011

        """
        xtrangegenerator = self.xtRange(startdate, enddate, stepday, stephour,
                                        calendarName, returnType, returnHour)
        rangedates = []
        for date in xtrangegenerator:
            rangedates.append(date)
        # end of for date in xtrangegenerator:
        return rangedates
    # end of def tRange(...):

    def _generateTimeAxis(self, days, startdate, skipdays=1, bounds='daily',
                                           units='days', calendarName=None):
        """
        :func:`_generateTimeAxis`: It should generate the time axis
                                    with its bounds

        Condition :
              We must pass days as integer or list contains the days counter
              to generate the timeAxis.
              startdate as cdtime.comp formate or its str formate.
              since must be any one of the default string to represent the
              cdtime units.

        Inputs:
           days is either integer (no of days) or if it is list means, it can
           be set to create timeAxis.

           startdate which date should set in the time axis units.

           Skipdays passed then it should genearate the days with
           that skipdays (if skipdays is +ve means timeAxis should be forward,
           if it is -ve means timeAxis should be backward).Default it takes 1.

           bounds is either 'daily' or 'monthly' or 'yearly' or user defined
           bounds. By default it takes 'daily'. user defined bounds means,
           user need to pass their own bounds as numpy array with proper
           shape.

           units is any one of the predefined units such as 'day', 'hour',
           'month', 'year'. By default it takes as 'days'.

        Outputs:
           It should return time axis with its bounds.
           its units as 'units since startdate'

        Usage:

           example 1:
               >>> t = _generateTimeAxis(10,'2010-5-25')
               >>> t
                   id: axis_1
                   Designated a time axis.
                   units:  days since 2010-5-25 0:0:0.0
                   Length: 10
                   First:  0
                   Last:   9
                   Other axis attributes:
                      calendar: gregorian
                      axis: T
                   Python id:  0xa56a22c
               >>>
               >>> t.getBounds()
               array([[ 0.,  1.],
                   [ 1.,  2.],
                   [ 2.,  3.],
                   [ 3.,  4.],
                   [ 4.,  5.],
                   [ 5.,  6.],
                   [ 6.,  7.],
                   [ 7.,  8.],
                   [ 8.,  9.],
                   [ 9.,  9.]])

           example2:
               >>> t = _generateTimeAxis(10,'2010-5-25',2)
               >>> t
                   id: time
                   Designated a time axis.
                   units:  days since 2010-5-25 0:0:0.0
                   Length: 10
                   First:  0
                   Last:   18
                   Other axis attributes:
                      calendar: gregorian
                      axis: T
                   Python id:  0x9d06eec
               >>>
               >>> t.getBounds()
                array([[  0.,   1.],
                       [  2.,   3.],
                       [  4.,   5.],
                       [  6.,   7.],
                       [  8.,   9.],
                       [ 10.,  11.],
                       [ 12.,  13.],
                       [ 14.,  15.],
                       [ 16.,  17.],
                       [ 18.,  19.]])

           example3:
               >>> t = _generateTimeAxis(3,'2010-6-30',-1)
               >>> t
                   id: time
                   Designated a time axis.
                   units:  days since 2010-6-30
                   Length: 3
                   First:  0
                   Last:   -2
                   Other axis attributes:
                      calendar: gregorian
                      axis: T
                   Python id:  0x85045cc
               >>>
               >>> t.getBounds()
                array([[ 0.,  1.],
                       [-1.,  0.],
                       [-2., -1.]])
            example4:
                >>> t = _generateTimeAxis(1,'2010-7-1',bounds='monthly')
                >>> t
                   id: time
                   Designated a time axis.
                   units:  days since 2010-7-1
                   Length: 1
                   First:  0
                   Last:   0
                   Other axis attributes:
                      calendar: gregorian
                      axis: T
                   Python id:  0x97c272c
                >>>
                >>> t.getBounds()
                array([[  0.,  31.]])

              ..note:: Here we passed bounds is 'monthly'. So the bounds are
                the start and ends of the days of the passed month & year.

                >>> _generateTimeAxis(1,'2010-9-1',bounds='monthly').getBounds()
                array([[  0.,  30.]])

                >>> _generateTimeAxis(1,'2012-2-1',bounds='monthly').getBounds()
                array([[  0.,  29.]])

              ..note:: Depends upon the months, it should return the bounds
                start and end regions. Same way for 'yearly' bounds settings.

            example5:
                >>> daylist = [0, 31, 59]
                >>> boundlist = [0, 31, 59, 90]
                >>> mybound = _generateBounds(boundlist)
                >>> mybound
                array([[  0.,  31.],
                       [ 31.,  59.],
                       [ 59.,  90.]])
                >>>
                >>> t = _generateTimeAxis(daylist, '2010-1-1', bounds = mybound)
                >>> t
                   id: time
                   Designated a time axis.
                   units:  days since 2010-1-1
                   Length: 3
                   First:  0
                   Last:   59
                   Other axis attributes:
                      calendar: gregorian
                      axis: T
                   Python id:  0xa56010c
                >>>
                >>> t.asComponentTime()
                    [2010-1-1 0:0:0.0, 2010-2-1 0:0:0.0, 2010-3-1 0:0:0.0]
                >>>
                >>> t.getBounds()
                array([[  0.,  31.],
                       [ 31.,  59.],
                       [ 59.,  90.]])

              ..note:: In this example, both daylist and bounds are user
               defined.

        ToDo : Have to update skiphours in this method ...

        Written by : Arulalan.T

        Date : 09.04.2011
        Updated : 02.12.2011

        """
        # checking arguments
        if isinstance(startdate, int):
            startdate = str(startdate)
        if not (self.comppattern.match(str(startdate)) or
                                str(type(startdate)) == "<type 'comptime'>"):
            # i.e. date is comptime in string or comptime object formate
            raise _TimeUtilityTypeError('the startdate should be cdtime.comp\
                                         string formate or its comp object ')
        if isinstance(skipdays, float):
            raise _TimeUtilityTypeError('The passed skipdays should not be \
                                        float value. It must be an integer')
        ulist = ['hour', 'hours', 'day', 'days', 'month', 'months', 'year', 'years']
        if not units in ulist:
            raise _TimeUtilityTypeError("arg 'since' must be any one in the \
            list ", str(ulist))
        #
        # Creating Time Axis for these range of dates
        #
        if isinstance(days, int):
            if skipdays == 1:
                # default action
                lendate = range(0, days)
            # end of if skipdays == 1:
            if skipdays <> 1:
                # if skipdays has passed, then timeAxis should set with proper
                # days from the startdate. So we should generate the correct
                # timeAxis with that skipdays.
                if skipdays:
                    lendate = range(0, days * skipdays, skipdays)
                else:
                    raise _TimeUtilityError('skipdays should not be 0')
            # end of if skipdays > 1:
        elif isinstance(days, (list, tuple)):
            lendate = days
        else:
            raise _TimeUtilityIntegerError('no of days sould be integer or \
                          list/tuple which contains the day counts properly')

        if calendarName is None:
            calendarName = cdtime.DefaultCalendar

        # setting time axis properties begins
        time = cdms2.createAxis(lendate)
        time.designateTime(persistent = 0, calendar = calendarName)
        time.id = 'time'
        time.units = '%s since %s' %(units, startdate)
        if bounds in ['daily', 'day']:
            # setting time axis units and bounds as daily
            cdutil.setTimeBoundsDaily(time)
        elif bounds in ['monthly', 'month']:
            # setting time axis units and bounds as monthly
            cdutil.setTimeBoundsMonthly(time)
        elif bounds in ['yearly', 'year']:
            # setting time axis units and bounds as yearly
            cdutil.setTimeBoundsYearly(time)
        elif isinstance(bounds, numpy.ndarray):
            # Setting user defined bounds
            if bounds.shape[0] == len(days):
                time.setBounds(bounds)
            else:
                raise _TimeUtilityInputError('bounds length should be equlal \
                                                to passed days')
        # setting time axis properties ends
        return time
    # end of def _generateTimeAxis(self,days,startdate):

    def _correctTimeAxis(self, timeAxis):
        """
        :func:`_correctTimeAxis`: some of time axis may not have its bounds.
                       This function return that time axis with its bounds.

        ToDo : This is works only for continous days.
            In future it should works for even hours and find out skipdays
            from the passed timeAxis.

        Written By : Arulalan.T

        Date : 20.07.2011
        """
        if not (isinstance(timeAxis, cdms2.axis.TransientAxis) or
                isinstance(timeAxis, cdms2.axis.FileAxis) or
                isinstance(timeAxis, cdms2.axis.Axis)):
            raise _TimeUtilityTypeError("Passed timeAxis is not the type of \
                                cdms2.axis.Axis or cdms2.axis.TransientAxis")

        timeAxisWithBounds = timeAxis.asDTGTime()
        days = len(timeAxisWithBounds)
        startdate = self.timestr2comp(timeAxisWithBounds[0])
        timeAxisWithBounds = self._generateTimeAxis(days, startdate)
        return timeAxisWithBounds
    # end of def correctTimeAxis(self, timeAxis):

    def _generateBounds(self, data):
        """ creating bounds array and return it
        We need to pass the data as list which consists of the bound's weights
        values. Then it should create return bounds as numpy array with
        proper shape.

        example 1:
            >>> boundlist = [0, 1, 2, 3, 4]
            >>> bounds = _generateBounds(boundlist)
            >>> bounds
            array([[ 0.,  1.],
                   [ 1.,  2.],
                   [ 2.,  3.],
                   [ 3.,  4.]])

        example 2:
            >>> boundlist = [0, 30, 58, 89, 119]
            >>> bounds = t._generateBounds(boundlist)
            >>> bounds
            array([[   0.,   30.],
                   [  30.,   58.],
                   [  58.,   89.],
                   [  89.,  119.]])

        """
        data_length = len(data) - 1
        bounds = numpy.zeros((data_length, 2))
        for i in range(data_length):
            bounds[i][0] = data[i]
            bounds[i][1] = data[i+ 1]
        # end of for i in range(data_length):
        return bounds
    # end of def bounds_generation(self,data):

    def getTimeAxisMonths(self, timeAxis, returnType='c', returnHour='y'):
        """
        :func:`getTimeAxisMonths`: Get the available months name and its
                             firstday & lastday from the passed timeAxis.

        Condition : timeAxis must be an instance of cdms2.axis.TransientAxis

        Inputs : Pass the any range of timeAxis object.
                 returnType is either 'c' or 's'. If 'c' means the dates are
                 cdtime.comptime object itself. if 's' means the dates are
                 yyyymmddhh string (by default) or yyyymmdd w.r.t returnHour.
                 returnHour takes either 'y/yes' or 'n/no'.

        Outputs : It should return a dictionary which has key as the year.
                  This year key has the value as dictionary type itself.
                  The nested dictionary has month as key and
                  value as tuple, which contains the stardate and enddate of
                  that month.
                  It should return month only for the available months in the
                  passed timeAxis.

        Usage :
            ..seealso:: we can pass any range of timeAxis. Even its hourly
                        series, it should works.
        ..seealso:: getTimeAxisFullMonths(), getTimeAxisPartialMonths()

            example 1:
                >>> tim = _generateTimeAxis(70, '2011-5-25')
                >>> tim
                   id: time
                   Designated a time axis.
                   units:  days since 2011-5-25
                   Length: 70
                   First:  0
                   Last:   69
                   Other axis attributes:
                      calendar: gregorian
                      axis: T
                   Python id:  0x8aea74c

                >>> getTimeAxisMonths(tim)
                {2011: {
                'MAY': (2011-5-25 0:0:0.0, 2011-5-31 0:0:0.0),
                'JUNE': (2011-6-1 0:0:0.0, 2011-6-30 0:0:0.0),
                'JULY': (2011-7-1 0:0:0.0, 2011-7-31 0:0:0.0),
                'AUGUST': (2011-8-1 :0:0.0, 2011-8-2 0:0:0.0)}
                }

             ..note::  Here 2011 as the key for the primary dictionary.
                       And MAY, JUNE, JULY and AUGUST are the keys for the
                       secondary(inner) dictionary, which contains the
                       stardate and enddate of that month and year.

                >>> tim.asComponentTime()[0]
                2011-5-25 0:0:0.0
             ..note:: The actual firstdate of the timeAxis is 25th may 2011.
                      But its not complete month. Even though it is returning
                      that available may month startdate and its enddate.

                >>> tim.asComponentTime()[-1]
                2011-8-2 0:0:0.0
             ..note:: The actual lastdate of the timeAxis is 2nd aug 2011.
                      But its not complete month. Even though it is returning
                      that available may month startdate and its enddate.

             ..note:: It also returnning the fully available months, in this
                      example June & July.

            example 2:
                >>> tim1 = _generateTimeAxis(70, '2011-12-1')
                >>> tim1
                   id: time
                   Designated a time axis.
                   units:  days since 2011-12-1
                   Length: 70
                   First:  0
                   Last:   69
                   Other axis attributes:
                      calendar: gregorian
                      axis: T
                   Python id:  0xa2c10ac

                >>> getTimeAxisMonths(tim1, returnType = 's',
                                             returnHour = 'n')
                {2011: {'DECEMBER': ('20111201', '20111231')},
                 2012: {'JANUARY': ('20120101', '20120131')}}

              ..note:: In this example, we will get 2011 and 2012 are the
                       keys of the primary dictionary. And 2011 has 'DECEMBER'
                       month and its startdate & enddate as key and value.
                       Same as for 2012 has 'JANUARY' month and its startdate
                       & enddate as key and value. Here dates are in yyyymmdd
                       string formate. Here we passed returnHour as 'n'.

        Written By : Arulalan.T

        Date : 06.03.2013

        """
        if not (isinstance(timeAxis, cdms2.axis.TransientAxis) or
                isinstance(timeAxis, cdms2.axis.FileAxis) or
                isinstance(timeAxis, cdms2.axis.Axis)):
            raise _TimeUtilityTypeError("Passed timeAxis is not the type of \
                                cdms2.axis.Axis or cdms2.axis.TransientAxis")
        if not returnType in ['c', 's']:
            raise _TimeUtilityTypeError("returnType either should 's' or 'c'.\
                if 's' means the return date should be in string type. \
               if 'c' means the return date should be cdtime type itself")
        if not returnHour in ['y', 'yes', 'n', 'no']:
            raise _TimeUtilityInputError("returnHour must be 'y/n' only")
        availableMonths = {}
        # store the timeAxis as component time objects in list
        timeAxisCompTime = timeAxis.asComponentTime()
        for month in range(1, 13):
            # Doing the find process for all the 12 months
            # getting the month string
            month = cdutil.getMonthString(month)
            # slice the timeaxis based on month
            monthlist = cdutil.monthBasedSlicer(timeAxis, month)
            if monthlist[0]:
                # day are available in this month. i.e. not empty month
                # get the first and last index of the month in timeAxis
                for n in range(0, len(monthlist[0])):
                    # this loop is for big scale timeAxis
                    monthFirstIndex = monthlist[0][n][0]
                    monthLastIndex = monthlist[0][n][-1]
                   # get the first and last date of month from the timeAxis
                    # as component time object.
                    monthFirstTime = timeAxisCompTime[monthFirstIndex]
                    monthLastTime = timeAxisCompTime[monthLastIndex]
                    # get the year
                    year = monthFirstTime.year

                    if returnType == 's':
                        # get the stardate & enddate as string
                        monthFirstTime = self.comp2timestr(monthFirstTime,
                                                          returnHour)
                        monthLastTime = self.comp2timestr(monthLastTime,
                                                          returnHour)
                    # end of if returnType == 's':
                    monthTimeRange = (monthFirstTime, monthLastTime)

                    if year in availableMonths:
                        availableMonths[year][month] = monthTimeRange
                    else:
                        availableMonths[year] = {month: monthTimeRange}
                    # end of if year in availableMonths:
                # end of for n in range(0, len(monthlist[0])):
            else:
                # days are not available in this month, in the passed timeAxis
                continue
            # end of if monthlist[0]:
        # end of for month in range(1, 13):
        # make memory free
        del timeAxisCompTime
        # return the fully available months of the timeAxis
        return availableMonths
    # end of def getTimeAxisMonths(self, timeAxis, ...):

    def getTimeAxisFullMonths(self, timeAxis, returnType='c', returnHour='y'):
        """
        :func:`getTimeAxisFullMonths`: Get the fully available months name and
                           its firstday & lastday from the passed timeAxis.

        Condition : timeAxis must be an instance of cdms2.axis.TransientAxis

        Inputs : Pass the any range of timeAxis object.
                 returnType is either 'c' or 's'. If 'c' means the dates are
                 cdtime.comptime object itself. if 's' means the dates are
                 yyyymmddhh string (by default) or yyyymmdd w.r.t returnHour.
                 returnHour takes either 'y/yes' or 'n/no'.

        Outputs : It should return a dictionary which has key as the year.
                  This year key has the value as dictionary type itself.
                  The nested dictionary has month as key and
                  value as tuple, which contains the stardate and enddate of
                  that month.
                  It should return month only for fully available month in the
                  passed timeAxis.
                  i.e. If timeAxis has some incomplete months of particular
                  year means, it should not return that month and its dates.

        Usage :
            ..seealso:: we can pass any range of timeAxis. Even its hourly
                        series, it should works. But it should return month &
                        dates for fully available dates of months in timeAxis.

            example 1:
                >>> tim = _generateTimeAxis(70, '2011-5-25')
                >>> tim
                   id: time
                   Designated a time axis.
                   units:  days since 2011-5-25
                   Length: 70
                   First:  0
                   Last:   69
                   Other axis attributes:
                      calendar: gregorian
                      axis: T
                   Python id:  0x8aea74c

                >>> getTimeAxisFullMonths(tim)
                {2011: {
                'JULY': (2011-7-1 0:0:0.0, 2011-7-31 0:0:0.0),
                'JUNE': (2011-6-1 0:0:0.0, 2011-6-30 0:0:0.0)}
                }

             ..note::  Here 2011 as the key for the primary dictionary.
                       And JUNE, JULY are the keys for the secondary(inner)
                       dictionary, which contains the stardate and enddate
                       of that month and year.

                >>> tim.asComponentTime()[0]
                2011-5-25 0:0:0.0
             ..note:: The actual firstdate of the timeAxis is 25th may 2011.
                      But its not complete month. So this may month is not
                      returned in the above.

                >>> tim.asComponentTime()[-1]
                2011-8-2 0:0:0.0
             ..note:: The actual lastdate of the timeAxis is 2nd aug 2011.
                      But its not complete month. So this aug month is not
                      returned in the above.

            example 2:
                >>> tim1 = _generateTimeAxis(70, '2011-12-1')
                >>> tim1
                   id: time
                   Designated a time axis.
                   units:  days since 2011-12-1
                   Length: 70
                   First:  0
                   Last:   69
                   Other axis attributes:
                      calendar: gregorian
                      axis: T
                   Python id:  0xa2c10ac

                >>> getTimeAxisFullMonths(tim1, returnType = 's',
                                                            returnHour = 'n')
                {2011: {'DECEMBER': ('20111201', '20111231')},
                 2012: {'JANUARY': ('20120101', '20120131')}}

              ..note:: In this example, we will get 2011 and 2012 are the
                       keys of the primary dictionary. And 2011 has 'DECEMBER'
                       month and its startdate & enddate as key and value.
                       Same as for 2012 has 'JANUARY' month and its startdate
                       & enddate as key and value. Here dates are in yyyymmdd
                       string formate. Here we passed returnHour as 'n'.

        Written By : Arulalan.T

        Date : 24.08.2011

        """
        if not (isinstance(timeAxis, cdms2.axis.TransientAxis) or
                isinstance(timeAxis, cdms2.axis.FileAxis) or
                isinstance(timeAxis, cdms2.axis.Axis)):
            raise _TimeUtilityTypeError("Passed timeAxis is not the type of \
                                cdms2.axis.Axis or cdms2.axis.TransientAxis")
        if not returnType in ['c', 's']:
            raise _TimeUtilityTypeError("returnType either should 's' or 'c'.\
                if 's' means the return date should be in string type. \
               if 'c' means the return date should be cdtime type itself")
        if not returnHour in ['y', 'yes', 'n', 'no']:
            raise _TimeUtilityInputError("returnHour must be 'y/n' only")
        availableMonths = {}
        # store the timeAxis as component time objects in list
        timeAxisCompTime = timeAxis.asComponentTime()
        for month in range(1, 13):
            # Doing the find process for all the 12 months
            # getting the month string
            month = cdutil.getMonthString(month)
            # slice the timeaxis based on month
            monthlist = cdutil.monthBasedSlicer(timeAxis, month)
            if monthlist[0]:
                # day are available in this month. i.e. not empty month
                # get the first and last index of the month in timeAxis
                for n in range(0, len(monthlist[0])):
                    # this loop is for big scale timeAxis
                    monthFirstIndex = monthlist[0][n][0]
                    monthLastIndex = monthlist[0][n][-1]
                    monthLength = len(monthlist[0][n])
                    # get the total days of this month from the timeAxis
                    lastDayOfMonth = int(monthlist[-1][n][0])
                    # get the first and last date of month from the timeAxis
                    # as component time object.
                    monthFirstTime = timeAxisCompTime[monthFirstIndex]
                    monthLastTime = timeAxisCompTime[monthLastIndex]
                    # get the year
                    year = monthFirstTime.year
                    # get the first and last date of the month (not from the
                    # timeAxis). Calling the method of this class
                    monthrange = self.monthFirstLast(month, year, returnType = 'c')
                    # comparing first and last date of month from the timeAxis
                    #with correct inbuilt method(not from the passed timeAxis)
                    if (monthFirstTime == monthrange[0] and
                                            monthLastTime == monthrange[1]):
                        # both the first and last date of month in the
                        # timeAxis are same.
                        if returnType == 's':
                            # get the stardate & enddate as string
                            monthFirstTime = self.comp2timestr(monthFirstTime,
                                                              returnHour)
                            monthLastTime = self.comp2timestr(monthLastTime,
                                                              returnHour)
                        # end of if returnType == 's':
                        monthTimeRange = (monthFirstTime, monthLastTime)

                        if monthLength == lastDayOfMonth:
                            # this month has all the dates.
                            # So this is a complete month.
                            # timeAxis contains day wise time series
                            if year in availableMonths:
                                availableMonths[year][month] = monthTimeRange
                            else:
                                availableMonths[year] = {month: monthTimeRange}

                        elif monthLength > lastDayOfMonth:
                            # time axis doesnt contains daywise time series.
                            # It may be hour wise time axis.
                            slicer = slice(monthFirstIndex, monthLastIndex +1)
                            availableMonthCompTime = timeAxisCompTime[slicer]
                            # date starts from 1.
                            totaldays = range(1, lastDayOfMonth + 1)
                            templist = []
                            for comp in availableMonthCompTime:
                                # get day from the comptime object of timeAxis
                                day = comp.day
                                if day in totaldays:
                                    templist.append(day)
                            if totaldays.sort() == list(set(templist)).sort():
                                # finally we came to know, this month timeAxis
                                # series has all the dates.
                                if year in availableMonths:
                                    availableMonths[year][month] = monthTimeRange
                                else:
                                    availableMonths[year] = {month: monthTimeRange}

                        else:
                            pass
                        # end of if len(monthlist[0][0]) == totaldays:
                    elif (monthLength == 1 and monthFirstTime == monthrange[0]):
                        # Got the timeAxis length is 1. so we need to check
                        # it by its bounds and lastDayOfMonth are equal or not
                        pass
                    # end of if (monthFirstTime ... and ...):
                # end of for n in range(0, len(monthlist[0])):
            else:
                # days are not available in this month, in the passed timeAxis
                continue
            # end of if monthlist[0]:
        # end of for month in range(1, 13):
        # make memory free
        del timeAxisCompTime
        # return the fully available months of the timeAxis
        return availableMonths
    # end of def getTimeAxisFullMonths(self, timeAxis):

    def getTimeAxisPartialMonths(self, timeAxis, fullMonths='auto',
                                              returnType='c', returnHour='y'):
        """
        :func:`getTimeAxisPartialMonths`: Get the partially available months
                    name and  its firstday & lastday from the passed timeAxis.
                    Its not fully available months.

        Condition : timeAxis must be an instance of cdms2.axis.TransientAxis

        Inputs : Pass the any range of timeAxis object.

                 fullMonths is which contains the year and its full months
                 name in dictionary. i.e. fullMonths is the output of the
                 `getTimeAxisFullMonths`(...) method for the same timeAxis.
                 By default it takes 'auto' string. It means, it should call
                 the `getTimeAxisFullMonths` method. Otherwise user can pass
                 the same kind of input.

                 returnType is either 'c' or 's'. If 'c' means the dates are
                 cdtime.comptime object itself. if 's' means the dates are
                 yyyymmddhh string (by default) or yyyymmdd w.r.t returnHour.

                 returnHour takes either 'y/yes' or 'n/no'.

        Outputs : It should return a dictionary which has key as the year.
                  This year key has the value as dictionary type itself.
                  The nested dictionary has month as key and
                  value as tuple, which contains the stardate, enddate and
                  no of days of that partial month.
                  It should return month only for partially available month
                  in the passed timeAxis.
                  i.e. If timeAxis has some incomplete months of particular
                  year means, those months start,enddate and its no of days
                  should be retuned.

        Usage :
            ..seealso:: we can pass any range of timeAxis. Even its hourly
                        series, it should works. But it should return month,
                        dates, total days for partially available dates of
                        months in timeAxis.

            example 1:
                >>> tim = _generateTimeAxis(37, '2011-5-25')
                # here we genearate the time axis with partial May month and
                # complete June month.
                >>>
                >>> tim
                   id: time
                   Designated a time axis.
                   units:  days since 2011-5-25
                   Length: 37
                   First:  0
                   Last:   36
                   Other axis attributes:
                      calendar: gregorian
                      axis: T
                   Python id:  0xa5604ec
                >>>
                >>> getTimeAxisPartialMonths(tim)
                {2011: {'MAY': (2011-5-25 0:0:0.0, 2011-5-31 0:0:0.0, 7)}}

             ..note::  Here 2011 as the key for the primary dictionary.
                       And May is the key for the secondary(inner)
                       dictionary, which contains the stardate, enddate and
                       total days of the May month.
                       of that month and year.

                >>> getTimeAxisFullMonths(tim)
                {2011: {'JUNE': (2011-6-1 0:0:0.0, 2011-6-30 0:0:0.0)}}

              ..note:: Here we called the fullMonths. So the June month has
                       returned with its stardate and enddate.

                >>> tim.asComponentTime()[0]
                2011-5-25 0:0:0.0
             ..note:: The actual firstdate of the timeAxis is 25th may 2011.
                      But its not complete month. So this may month is
                      returned in the above getTimeAxisPartialMonths() method
                      example.

                >>> tim.asComponentTime()[-1]
                2011-6-30 0:0:0.0

             ..note:: The June month is complete month. So it should return
                      only when we call the getTimeAxisFullMonths() method,
                      not in getTimeAxisPartialMonths() method.

        Written By : Arulalan.T

        Date : 28.11.2011

        """

        if not (isinstance(timeAxis, cdms2.axis.TransientAxis) or
                isinstance(timeAxis, cdms2.axis.FileAxis) or
                isinstance(timeAxis, cdms2.axis.Axis)):
            raise _TimeUtilityTypeError("Passed timeAxis is not the type of \
                                cdms2.axis.Axis or cdms2.axis.TransientAxis")
        if not returnType in ['c', 's']:
            raise _TimeUtilityTypeError("returnType either should 's' or 'c'.\
                if 's' means the return date should be in string type. \
               if 'c' means the return date should be cdtime type itself")
        if not returnHour in ['y', 'yes', 'n', 'no']:
            raise _TimeUtilityInputError("returnHour must be 'y/n' only")

        if fullMonths == 'auto':
            fullMonths = self.getTimeAxisFullMonths(timeAxis)
        elif isinstance(fullMonths, dict):
            print "Passed 'fullMonths' arg ", fullMonths
            print "except these full months, the partial months will be \
                    returned from the timeAxis"
        else:
            print "Passed 'fullMonths' arg ", fullMonths
            print "Expecting fullMonths as getTimeAxisFullMonths() return type"
            print "So we cannot take action w.r.t passed fullMonths. \
                   Use 'auto' option for fullMonths arg of this method."
            return None

        availablePMonths = {}
        # store the timeAxis as component time objects in list
        timeAxisCompTime = timeAxis.asComponentTime()

        for month in range(1, 13):
            # Doing the find process for all the 12 months
            # getting the month string
            month = cdutil.getMonthString(month)
            # slice the timeaxis based on month
            monthlist = cdutil.monthBasedSlicer(timeAxis, month)
            if monthlist[0]:
                # day are available in this month. i.e. not empty month
                # get the first and last index of the month in timeAxis
                for n in range(0, len(monthlist[0])):
                    # this loop is for big scale timeAxis
                    monthFirstIndex = monthlist[0][n][0]
                    monthLastIndex = monthlist[0][n][-1]
                    monthLength = len(monthlist[0][n])
                    # get the first and last date of month from the timeAxis
                    # as component time object.
                    monthFirstTime = timeAxisCompTime[monthFirstIndex]
                    monthLastTime = timeAxisCompTime[monthLastIndex]
                    # get the year
                    year = monthFirstTime.year
                    if returnType == 's':
                        # get the stardate & enddate as string
                        monthFirstTime = self.comp2timestr(monthFirstTime,
                                                          returnHour)
                        monthLastTime = self.comp2timestr(monthLastTime,
                                                          returnHour)
                    # end of if returnType == 's':
                    monthTimeRange = (monthFirstTime, monthLastTime,
                                                          monthLength)

                    if not year in fullMonths:
                        # year is not available in fullMonths. so we can add
                        # this month into partially available months dict.
                        if year in availablePMonths:
                            availablePMonths[year][month] = monthTimeRange
                        else:
                            availablePMonths[year] = {month: monthTimeRange}

                    else:
                        # this year is available in fullMonths. so we need to
                        # check the month is either available in the fullMonths
                        # dictionary or not.
                        if not month in fullMonths.get(year):
                            # this month is not available in the fullMonths.
                            # so we can add this month into partially
                            # available months dict.
                            availablePMonths[year] = {month: monthTimeRange}
                        # end of if not month in fullMonths.get(year):
                    # end of if not year in fullMonths:
                # end of for n in range(0, len(monthlist[0])):
            else:
                # days are not available in this month, in the passed timeAxis
                continue
            # end of if monthlist[0]:
        # end of for month in range(1, 13):
        # make memory free
        del timeAxisCompTime
        # return the partially available months of the timeAxis
        return availablePMonths
    # end of def getTimeAxisPartialMonths(...):

    def _getDayCountOfYear(self, date, year=None, calendarName=None):
        """
        :func:`_getDayCountOfYear`: Get the day count of the year for the
                passed date. Its a Julien day. We can rename this function
                as getJulienDay.

        Inputs : date must be either component time object or its string
                 formate, or yyyymmddhh or yyyymmdd string formate.

        Outputs : It should return the day count of the passed date.
                  January 1st represents as 0 and January 2nd represent as 1,
                  and so on...
        Usage :

            example 1:
                >>> _getDayCountOfYear('2011-1-1')
                    0
                >>> _getDayCountOfYear(cdtime.comptime(2011, 1, 31))
                    30
                >>> _getDayCountOfYear(20110201)
                    31
                >>> _getDayCountOfYear('2011-12-31')
                    364
                >>> _getDayCountOfYear('2012-12-31')
                    365

             ..note::  Here we passed various type of date input. 1st January
                       starts from '0'. And 31st December takes 364 in
                       No Leap Year. If Leap Year means, 31st December takes
                       365, because 29th day as introduced in Feburary month.

        Written By : Arulalan.T

        Date : 02.12.2011

        """

        enddaycomp = self.timestr2comp(str(date))
        if year:
            year = str(year)
        else:
            year = str(enddaycomp.year)

        if calendarName is None:
            calendar = cdtime.DefaultCalendar

        # making hourstring from startcomp to find out the no of days in b/w
        daystring = 'days since %s-1-1' % (year)
        # genearating the relative cdtime of enddate & get its day count
        daycount = enddaycomp.torel(daystring, calendar).value
        # return the day count of the year w.r.t passed date
        return int(daycount)
    # end of def _getDayCountOfYear(self, date, calendarName=None):

    def _dayCount2Comp(self, day, year=1):
        """
        It just does the reverse job of the _getDayCountOfYear

        eg1:
            >>> _dayCount2Comp(59)
                1-3-1 0:0:0.0
                # it returns march 1st of year 1 as comptime.
        eg2:
             >>> _dayCount2Comp(59, year=4)
                4-2-29 0:0:0.0
                # it returns feb 29th of year 4 as comptime.

        Written By : Arulalan.T

        Date : 13.08.2013
        """

        units = 'days since %d-1-1' % (year)
        return cdtime.reltime(day, units).tocomp()
    # end of def _dayCount2Comp(day, year=1):

    def _sortMonths(self, months):
        """
        :func:`_sortMonths`: Sorting the months and seasons with respect to
                             the calendar.

        Inputs : months is list which contains the combinations of months name
                 and seasons name.

        Outputs : It should return the list which contains the sorted months
                  first and then followed by seasons.

        Usage :

            example 1:
                >>> x = ['JANUARY', 'august', 'November', 'mar']
                >>> _sortMonths(x)
                ['JANUARY', 'mar', 'august', 'November']

            example 2:
                >>> x = ['DJF', 'JJAS']
                >>> t._sortMonths(x)
                ['JJAS', 'DJF']

            example 3:
                >>> x = ['DJF', 'december', 'March', 'JJAS', 'Nov']
                >>> _sortMonths(x)
                ['March', 'Nov', 'december', 'JJAS', 'DJF']

             ..note::  Here we passed various type of month string types.
                       i.e. Here case is in-senstive. Even we mixed the months
                       and seasons, it should be arranged the sorted months
                       and then sorted seasons.

        Written By : Arulalan.T

        Date : 03.12.2011

        """
        Months = {}
        Seasons = {}
        sortedMonths = []

        for mon in months:
            index = cdutil.getMonthIndex(mon)
            if len(index) > 1:
                # Got Season
                Seasons[index[0]] = mon
            else:
                # Got Month
                Months[index[0]] = mon
        # Sort the month and append to the list
        mkeys = Months.keys()
        mkeys.sort()
        for monidx in mkeys:
            sortedMonths.append(Months.get(monidx))
        # Sort the season and append to the list
        skeys = Seasons.keys()
        skeys.sort()
        for seaidx in skeys:
            sortedMonths.append(Seasons.get(seaidx))
        return sortedMonths
    # end of def sortMonths(self, months):

    def _generateMonthlyMeanTimeAxis(self, firstOfMonth, lastOfMonth=None,
                                                                  days=None):
        """
        :func:`_generateMonthlyMeanTimeAxis`: Generate the monthly mean time
                axis. And its bounds are calculated w.r.t timeAxis last month
                weights and current month days count, if timeAxis has passed.
                Otherwise bounds should be calculated w.r.t position of the
                startdate and current month days count.

        Inputs : firstOfMonth is the stardate of the month and lastOfMonth is
                 the enddate of the month. Both must be in cdtime.comptime
                 object type itself. lastOfMonth is an optional one.
                 days is the integer count. i.e total no of days in that month.
                 It should become the part of the bounds. Its optional one.
                 By default it bound's weight will be set w.r.t total no of
                 days of the month (calculated w.r.t firstOfMonth).

        Outputs : This method aims is to genearate the timeaxis with proper
                  bounds value for monthly mean time axis. i.e. To create or
                  append the timeAxis for the monthly mean. Here 'mean' is
                  also called as 'average'. So the monthly average data
                  should consists the timeAxis length is 1, bound's weight is
                  total no of days in that month.

        Note : The genearated time axis units is 'days since year-1-1',
                  the year takes from the passed dates.

        Usage :

            example 1:
                >>> first = cdtime.comptime(2011, 5, 1)
                >>> first
                    2011-5-1 0:0:0.0
                >>> last = cdtime.comptime(2011, 5, 31)
                >>> last
                    2011-5-31 0:0:0.0

             ..note:: Here first and last are the comptime of 5th month

                >>> T = _generateMonthlyMeanTimeAxis(first, last)
                >>> T
                   id: time
                   Designated a time axis.
                   units:  days since 2011-1-1
                   Length: 1
                   First:  120
                   Last:   120
                   Other axis attributes:
                      calendar: gregorian
                      axis: T
                   Python id:  0xb75a542cL
                >>>
                >>> T.asComponentTime()
                [2011-5-1 0:0:0.0]
                >>> T.shape
                (1,)
                >>> T.getBounds()
                array([[ 120.,  151.]])

             ..note:: In the above steps, we have passed the first & last to
                      the `_generateMonthlyMeanTimeAxis` which returns to T.
                      T length is 1. Its position is 120 (i.e. day counter
                      of the year). Its bounds from 120 to 151. (i.e for the
                      May month bound, 31 days)

                >>> nfirst = cdtime.comptime(2011, 8, 1)
                >>> nfirst
                    2011-8-1 0:0:0.0
                >>> nlast = cdtime.comptime(2011, 8, 31)
                >>> nlast
                    2011-8-31 0:0:0.0

             ..note:: In the same session, nfirst and nlast are the comptime
                      of 8th month

                >>> T1 = _generateMonthlyMeanTimeAxis(nfirst, nlast, days=25)
                >>> T1
                   id: time
                   Designated a time axis.
                   units:  days since 2011-1-1
                   Length: 1
                   First:  212
                   Last:   212
                   Other axis attributes:
                      calendar: gregorian
                      axis: T
                   Python id:  0x994fe2c
                >>>
                >>> T1.asComponentTime()
                [2011-8-1 0:0:0.0]

                >>> T1.getBounds()
                array([[ 212.,  237.]])

             ..note:: In the above steps, we have passed the nfirst, nlast &
                      days(25) to the method `_generateMonthlyMeanTimeAxis`
                      which returns to T1. T1 length is 1.Its position is 212.
                      Its bound's weight is from 212 to 237. i.e. only for 25
                      days, it should set the bounds, since we passed days as
                      25. (If it is full months means its bounds would be
                      from 212 to 243. i.e for 31 days)

        Written By : Arulalan.T

        Date : 06.12.2011

        """
        if days:
            # total no of days in the month
            totalDaysOfMonth = days
        else:
            if not lastOfMonth:
                # find out the last date of this month
                nextMonth = firstOfMonth.add(1, cdtime.Months)
                lastOfMonth = nextMonth.sub(1, cdtime.Days)
            # end of if not lastOfMonth:
            # totoal no of days in the current month w.r.t fully available
            # month data.
            totalDaysOfMonth = lastOfMonth.day
        # end of if days:
        # get the start day count of the month startdate of this year
        firstDayCount = self._getDayCountOfYear(firstOfMonth)
        # get the current year,January,day 1st
        YearFirstDate = str(firstOfMonth.year) + '-1-1'
        # total no of days of the current month in case of fully
        # available w.r.t startDayCount
        newWeight = firstDayCount + totalDaysOfMonth
        # current month bound
        boundlist = [firstDayCount, newWeight]
        # end of if timeAxis:
        # generate the bounds as numpy array with n X 2 shape
        monthBound = self._generateBounds(boundlist)
        # generate the new time axis for the current 'mean month'
        meanTimeAxis = self._generateTimeAxis([firstDayCount],
                                    YearFirstDate, bounds = monthBound)
        return meanTimeAxis
    # end of def _generateMonthlyMeanTimeAxis(...):

    def getSeasonName(self, startBound, endBound, year='1', units='days'):
        """
        Inputs : start bound and end bound of the season.
        Returns : Season name
        Date : 03.06.2012
        """
        cntlstr = units + ' since ' + str(year) + '-1-1'
        startdate = cdtime.reltime(startBound, cntlstr).tocomp()
        enddate = cdtime.reltime(endBound, cntlstr).tocomp()
        season = ''
        for mon in range(startdate.month, enddate.month+1):
            season += cdutil.getMonthString(mon)[0]
        return season
    # end of def getSeasonName(startBound, endBound, year='1', units='days'):

    def _genTimeAxis(self, startdate, enddate, calendarName=None):
        """

        Date : 11.06.2012
        """
        if not (self.comppattern.match(str(startdate)) or
                                str(type(startdate)) == "<type 'comptime'>"):
            # i.e. date is comptime in string or comptime object formate
            raise _TimeUtilityTypeError('the startdate should be cdtime.comp\
                                         string formate or its comp object ')

        if not (self.comppattern.match(str(enddate)) or
                                str(type(enddate)) == "<type 'comptime'>"):
            # i.e. date is comptime in string or comptime object formate
            raise _TimeUtilityTypeError('the enddate should be cdtime.comp\
                                         string formate or its comp object ')

        startdate = self.timestr2comp(str(startdate))
        enddate = self.timestr2comp(str(enddate))

        # get the starting day count w.r.t startdate year
        sday = self._getDayCountOfYear(startdate, startdate.year, calendarName)
        # get the ending day count w.r.t startdate year
        eday = self._getDayCountOfYear(enddate, startdate.year, calendarName)

        days = range(sday, eday+1)
        return self._generateTimeAxis(days, startdate)
    # end of def _genTimeAxis(startdate, enddate, calendarName=None):

    def _getYears(self, timeAxis, skip=1, deepsearch=False):

        """
        return the available years as list from the passed timeAxis object.

        If deepsearch arg set as True, then it should loop through all the
        available component time. For this option user no need to pass
        args skip and tlen.

        If deepsearch arg set as False, then it should loop through by some
        intelligent way, to minimize the computational time period. It will
        works correctly for continous time series axis object only.

        Date : 11.06.2012
        """

        if not (isinstance(timeAxis, cdms2.axis.TransientAxis) or
                isinstance(timeAxis, cdms2.axis.FileAxis) or
                isinstance(timeAxis, cdms2.axis.Axis)):
            raise _TimeUtilityTypeError("Passed timeAxis is not the type of \
                                cdms2.axis.Axis or cdms2.axis.TransientAxis")

        years = set()
        avldates = timeAxis.asComponentTime()

        if deepsearch:
            for date in avldates:
                year = date.year
                if not year in years:
                    years.add(year)
            # end of for date in avldates:
        else:
            looplen = len(avldates)
            index = 0
            while index < looplen:
                date = avldates[index]
                years.add(date.year)
                # increase the index by 365 days/12 months and decrease by
                # date count of the year
                index += 365 - (self._getDayCountOfYear(date)*skip)
                # generate the leap day to check the leap year status
                leapday = cdtime.comptime(date.year, 2, 29, date.hour)
                if leapday in avldates:
                    # leap date is present in the available time axis. So
                    # increase index by 1.
                    index += 1
            # end of while index < looplen:
        # end of if deepsearch:

        # make free memory
        del avldates

        # make it as list and sort it.
        years = list(years)
        years.sort()

        return years
    # end of def _getYears(self, timeAxis, skip=1)

    def _getTimeAxisIndex(self, timeAxis, days, months, hours=[0], deepsearch=True):
        """
        This will return a tuple contains the list of timeaxis index of the
        corresponding component time of passed days & months for the available
        years in the passed timeAxis object.

        days - it must be a list of days
        month - it must be a list of months
        hours - it must be a list of hours. By default it takes as [0].
        deepsearch - arg for _getYears() function. By default it takes True.

        Date : 08.03.2013
        """
        avlYears = self._getYears(timeAxis, skip=1, deepsearch=deepsearch)
        avldates = timeAxis.asComponentTime()
        neededIdx = []
        neededDays = []
        for year in avlYears:
            for mon in months:
                for day in days:
                    for hr in hours:
                        neededDayComp = cdtime.comptime(year, mon, day, hr)
                        if neededDayComp in avldates:
                            cIdx = avldates.index(neededDayComp)
                            neededIdx.append(timeAxis[cIdx])
                            neededDays.append(neededDayComp)
                        # end of if neededDayComp in avldates:
                    # end of for hr in hours:
                # end of for day in days:
            # end of for mon in months:
        # end of for year in avlYears:
        return (neededIdx, neededDays)
    # end of def _getTimeAxisIndex(self, timeAxis, days, months):

    def has_all(self, timeAxis, deepsearch=False, missingYears=0,
                                 missingMonths=0, missingHours=0):
        """
        has_all : either the passed time axis has all the time series or not !

        Returns : True it timeAxis has no missing value and no duplicates.
                  Otherwise returns False.

        deepsearch - 1 | 0.
                  If deepsearch enabled return if it has missing time series
                  in between, then it should return those missing time series
                  as component time string in list along with False.

                  deepsearch 0 will return the boolean value in rapid speed.

        missingYears - 1 | 0.
                 If deepsearch is 1 and missingYears is 1, then it should find
                 only the missing years from the passed timeAxis. It will not
                 worry about the months & hours until missingMonths &
                 missingHours are enabled.

        missingMonths - 1 | 0.
                 If deepsearch is 1, missingYears is 1 and missingHours is 1,
                 then it will find the missing months also in the timeAxis.
                 It will not worry about the missing hours.

        missingHours - 1 | 0.
                 If deepsearch is 1, missingYears is 1, missingMonths is 1
                 and missingHours is 1, it will do just find all missing
                 sequance time slice from the timeAxis.

                 User can enable deepsearch alone instead of enabling all the
                 missingYears, missingMonths and missingHours.

        ..note:: By default deepsearch flag, will try to find out the missing
                 time sequance from the user passed timeAxis itself.
                 This function should works correctly for the timeAxis which
                 contains same delta(diff b/w first and second timeAxisIndex)
                 through out the timeAxis. Otherwise user can use missingYears
                 and/or missingMonths for complex timeAxis.

        ..note:: return true if user passed length of 1 timeAxis or if user
                 enabled missingYears, then if that retunes only one year,
                 then we can just return True ! (In that case it could be
                 daily or monthly or hourly) it may be have missing time
                 slice also, if user passed missingYears. so user has take
                 care of this !

        Refer : _getYears()

        Written By : Arulalan.T

        Date : 09.10.2012

        """

        if not (isinstance(timeAxis, cdms2.axis.TransientAxis) or
                isinstance(timeAxis, cdms2.axis.FileAxis) or
                isinstance(timeAxis, cdms2.axis.Axis)):
            raise _TimeUtilityTypeError("Passed timeAxis is not the type of \
                                cdms2.axis.Axis or cdms2.axis.TransientAxis")


        if missingYears and not (missingMonths and missingHours):
            # get the years alone as list from the user passed timeAxis
            tyears = self._getYears(timeAxis, deepsearch=True)
            # create our own yealy timeAxis and overwrite the used passed
            # timeAxis within this fuction alone.
            sinceyear = tyears[0]
            tyears = numpy.array(tyears) - sinceyear
            timeAxis = cdms2.createAxis(tyears, id='time')
            timeAxis.designateTime()
            timeAxis.units = 'years since %s-1-1' % str(sinceyear)
            # get the yearly timeAxis index as list
            tindex = tyears.tolist()
        elif missingYears and missingMonths and not missingHours:
            # Need to find the missing months alone. Not hours.
            pass
            raise ValueError("Method Not Yet Implemented !")
        else:
            # Need to find the missing years, months and hours also.
            # so just use the timeAxis as it is which is passed by the user.
            # get the timeAxis index as list
            tindex = timeAxis[:].tolist()
        # end of if missingYears and (not missingMonths and not missingHours):

        # get the original timeAxis length
        tlen = len(tindex)
        # return true if user passed length of 1 timeAxis or if user enabled
        # missingYears, then if that retunes only one year, then we can just
        # return True ! (in that case it could be daily or monthly or hourly)
        # it may be have missing time slice also, if user passed missingYears.
        # so user take care of this !
        if tlen == 1: return True
        # get the unique timeAxis length
        tulen = len(set(tindex))
        if tlen != tulen:
            # time axis length not match with its unique length.
            # i.e. it has duplicates !
            return False
        # end of if tlen != tulen

        # get the first, second, last nos from the tindex list without sort
        tlast = max(tindex)
        tfirst = min(tindex)
        tfidx = tindex.index(tfirst)
        tindex.remove(tfirst)
        tsecond = min(tindex)
        tindex.insert(tfidx, tfirst)

        # find the delta from the first & second nos
        delta = tsecond - tfirst
        # get the total nos should be in the timeAxis list
        total = tlast - tfirst
        # take 0 into the account
        if tfirst <= 0 <= tlast:
            total += 1
        # end of if tfist < 0 <= tlast:
        # correct length. i.e. the passed timeAxis length should be as below
        clen = total / delta

        if tlen == clen:
            # both passed timeAxis length and its correct length is same.
            # so it is continous, but the nos may not be in order or even
            # arranged by random order also.
            # simply we can say there is no missing index nos in the passed
            # timeAxis list.
            return True
        else:
            if not deepsearch:
                # it has missing time series
                return False
            else:
                # get the difference of two lengths. So that many time slice
                # are missing. isnt it ?!
                dlen = abs(tlen-clen)
                # sort the time index. why?. time axis may not be in acending
                # or decending order. Even it may be random order though !
                tindex.sort()
                x1 = tfirst
                missing_tindex = []
                missing_tvalue = []

                # loop through all the time series. OMG !
                # dont worry ! we get rid of this loop once we found the
                # missing time series count as equal to the dlen.
                for x2 in tindex[1:]:
                    # get the difference b/w two consecutive nos and compare
                    # with delta. if not match, then there are missing time
                    # slice
                    if delta != x2 - x1:
                        # reduce the dlen according to missing slice length!
                        dlen -= x2 - x1
                        # store those missing time slice into the list
                        missing_tindex.append((x1, x2))
                    # end of if delta != (x2 - x1):
                    # if all missing found then break the loop.
                    if dlen<= 0: break
                    # reassign the x1 in loop
                    x1 = x2
                # end of for x2 in tindex[1:]:

                tunits = timeAxis.units
                # convert the missing time index as time string
                for x1, x2 in missing_tindex:
                    xdiff = x2 - x1
                    missing = []
                    # make adjust as -ve 1 to reduce the timeslcie by 1.
                    adj = 1
                    for x in [x1, x2]:
                        # get the index. Its not necessary timeAxis should
                        # start from 0 index. It may be even float.
                        xidx = tindex.index(x)
                        # get the relative time object
                        rt = cdtime.reltime(timeAxis[xidx], tunits)
                        if not tunits.startswith('second'):
                            # Just adjust the time value exactly from which
                            # time slice to which slice of timeAxis is missing
                            rt = cdtime.reltime(rt.value + adj,  tunits)
                        # end of if not tunits.startswith('second'):

                        # convert rt into component time object
                        ct = cdtime.r2c(rt)
                        if missingYears and not (missingMonths and missingHours):
                            # adding only missing year
                            missing.append(ct.year)
                        else:
                            hr = ct.hour
                            st = str(ct)
                            if not hr: st = st.split(' ')[0]
                            # adding the t as component time as string itself.
                            missing.append(st)
                        # end of if missingYears and not (missingMonths...):
                        if xdiff == 1: break
                        # make adjust as -ve 1 to reduce the timeslcie by 1.
                        adj = -1
                    # end of for x in [x1, x2]:
                    missing_tvalue.append(tuple(missing))
                # end of for x1, x2 in missing_tindex:

                # make memory free
                del tindex

                return False, missing_tvalue
            # end of if not deepsearch:
        # end of if tlen == clen:
    # end of def has_all(self, timeAxis, deepsearch=False):

    def has_missing(self, timeAxis, deepsearch=False, missingYears=0,
                                     missingMonths=0, missingHours=0):

        """

        has_missing : either the passed time axis has missing time series
                      or not !

        It just return the opposite boolean flag of the function
        self.has_all(timeAxis, ...)

        For more doc, see the has_all.__doc__

        Refer : has_all(), _getYears()

        Date : 11.10.2012
        """

        has_all = self.has_all(timeAxis, deepsearch, missingYears,
                                       missingMonths, missingHours)
        missing_value = None

        if isinstance(has_all, tuple):
            all_flag, missing_value = has_all
        else:
            all_flag = has_all
        # end of if isinstance(has_all, tuple):

        # make the opposite boolean to missing_flag w.r.t all_flag
        if all_flag:
            missing_flag = False
        else:
            missing_flag = True
        # end of if all_flag:

        if deepsearch and missing_value:
            return missing_flag, missing_value
        else:
            return missing_flag
        # end of if deepsearch and missing_value:
    # end of def has_missing(timeAxis, deepsearch=False):


    def getSeasonalData(self, varName, fpath, sday, smon, eday, emon, hr=0, **kwarg):

        """
        getSeasonalData : user defined season data extraction from the filepath.
                          It will extract the specified season (passed in the args)
                          from all the available years or user can pass the needed
                          year/s.
                          User can extract same day for all the available years/
                          needed year/s. For eg : One can get all the leapday data
                          alone from all the years.

        Inputs:
            varName : variable name
            fpath : data (nc/ctl/grib/xml/cdml) file path
            sday : starting day of the season [of all the years of the data]
            smon : starting month of the season [of all the years of the data]
            eday : ending day of the season [of all the years of the data]
            emon : ending month of the season [of all the years of the data]
            hr : hour for both start and end date
            KWargs : (latitude and/or longitude) or (region) and/or level
                     and/or cyclic.
             cyclic : If cyclic is true, it extract the cyclic year data also.
                 i.e. In winter season (Nov to Apr), then it will extract the
                 first year (Jan to Apr) and last year (Nov to Dec) also.
                 So it will be look like cyclic year of seasonData.
                      If cyclic is false means, it will not extract the last
                 year partial months data. i.e. it will not extract last year
                 (Nov to Dec) for winter season.
              year : Its optional only. By default it is None. i.e. It will
                     extract all the available years seasonalData.
                     If one interger year has passed means, then it will do
                     extract of that particular year seasonData alone.
                     If two years has passed in tuple, then it will extract
                     the range of years seasonData from year[0] to year[1].
                     eg1 : year=2005 it will extract seasonData of 2005 alone.
                     eg2 : year=(1971, 2013) it will extract seasonData from
                           1971 to 2013 years.

        ..note:: If end day and end month is lower than the start day & start
             month, then we need to extract the both current and next year
             data. For eg : Winter Season (November to April).
             It can not be reversed for this winter season. We need to
             extract data from current year november month upto next year
             march month.
                If you pass one year data and passed the above
             winter season, then it will be extracted november and december
             months data and will be calculated variance for that alone.
                If you will pass two year data then it will extract the data
             from november & december of first year and january, feburary &
             march of next year will be extracted and calculated variance
             for that.

         ..note:: If both sday == eday and smon == emon then it will extract
              the this particular day from all the available years.
              Ofcourse you can control the needed year/s also.
              Eg1: To get leap day data from all the available years,
                getSeasonalData(varName, path, sday=29, smon=2, emon=29, emon=2)
                It will return all years the leapday data (Feb 29) along with
                its timeAxis and missing values.

        Written By : Arulalan.T

        Date : 26.07.2012
        Updated : 13.08.2013

        """

        lat = kwarg.get('latitude', None)
        lon = kwarg.get('longitude', None)
        region = kwarg.get('region', None)
        lev = kwarg.get('level', None)
        year = kwarg.get('year', None)
        cyclic = kwarg.get('cyclic', False)
        _cyclic = cyclic
        f = cdms2.open(fpath, 'r')
        timeAxis = f[varName].getTime()
        # Todo:
        # need to optimize this component time to avoid extract everytime
        # when the same method will be called for the same varName and
        # same file input. Store it as self object in dic with varName
        # and filename. Or store by timeAxis python object id.
        # Then we can save so many place to avoid repeated statement
        # asComponentTime()...
        timeAxisCompTime = timeAxis.asComponentTime()
        # get the available years of the time axis
        avlyears = self._getYears(timeAxis)
        if (sday == eday and smon == emon):
            sameDay = True
        else:
            sameDay = False
        # end of if (sday == eday and smon == emon):
        if year:
            if isinstance(year, int):
                if (smon > emon or (smon == emon and sday >= eday)) and not _cyclic:
                    # Winter Season and cyclic is False.
                    # So we need two consecutive years to extract the winter season
                    if year and year+1 in avlyears:
                        avlyears = [year, year+1]
                    else:
                        raise ValueError("Passed year %d & its next year %d \
                         (since cyclic has not enabled)  is not available" % (year, year+1))
                    # end of if year and year+1 in avlyears:
                else:
                    # cyclic is True. So we can extract winter season with in same year
                    if year in avlyears:
                        avlyears = [year]
                    else:
                        raise ValueError("Passed year %d is not available" % year)
                    # end of if year in avlyears:
                # end of if (smon > emon or (smon == emon and sday >= eday)) and not _cyclic:
            elif isinstance(year, (tuple, list)):
                if len(year) == 2:
                    syearIdx = avlyears.index(year[0])
                    eyearIdx = avlyears.index(year[1])
                    avlyears = avlyears[syearIdx: eyearIdx + 1]
        # end of if year:

        if cyclic:
            # this will add the first year one more time
            # to make it as cyclic year/s
            avlyears.insert(0, avlyears[0])
        # end of if cyclic:
        # season data for all the years of the data
        allYearSeasonalData = numpy.array([])
        allYearSeasonalTimeIdx = None

        latAxis = None
        lonAxis = None
        levAxis = None

        for year in avlyears:
            # loop through available years of the data
            if _cyclic:
                # genearate the start of the current year with Jan 1.
                # To extract the partial winter season at the fist year from
                # (year,1,1) to (year, emon, eday). This will be used only
                # for winter season to extract the first year JFMA months also
                #
                sdate = cdtime.comptime(year, 1, 1, hr)
            else:
                # genearate the start of the current year (season)
                sdate = cdtime.comptime(year, smon, sday, hr)
            # end of if _cyclic:
            if sameDay:
                if sdate not in timeAxisCompTime:
                    continue
                # end of if sdate not in timeAxisCompTime:
            # end of if sameDay:
            if (smon > emon or (smon == emon and sday >= eday)) and not _cyclic \
                and not sameDay:
                # if end day and end month is lower than the start day and start
                # month, then we need to extract the both current and next year
                # data. For eg : Winter Season (November to April).
                # It can not be reversed for this winter season. We need to
                # extract data from current year november month upto next year
                # march month.
                #
                # increase one year to the enddate to extract the next year data.
                year += 1
            # end of (if smon > emon or (smon == emon and sday >= eday)) ...:

            # generate the end date either for current year or next year.
            edate = cdtime.comptime(year, emon, eday, hr)
            if not cyclic and year not in avlyears:
                # cyclic is false. So no need to extract the last year partial
                # data. eg. No need to extract the winter season (Nov to Dec)
                # of the last year.
                break
            # end of if not cyclic and year not in avlYears:

            # make false the cyclic flag. We set the partial first year
            # end date. So in the next loop, it will be as per full seasonal
            # end date.
            if cyclic: _cyclic = False

            # extract the season data from file object and append to
            # the numpy array (allYearSeasonalData).
            if allYearSeasonalData.shape == (0,):
                # first year season extract it
                try:
                    if region:
                        allYearSeasonalData = f(varName, time=(sdate, edate))
                        allYearSeasonalData = allYearSeasonalData(region)
                    elif lat and lon:
                        allYearSeasonalData = f(varName, time=(sdate, edate),
                                                  latitude=lat, longitude=lon)
                    elif lat:
                        allYearSeasonalData = f(varName, time=(sdate, edate),
                                                                 latitude=lat)
                    elif lon:
                        allYearSeasonalData = f(varName, time=(sdate, edate),
                                                                longitude=lon)
                    else:
                        allYearSeasonalData = f(varName, time=(sdate, edate))
                    # end of if region:

                    if lev:
                        allYearSeasonalData = allYearSeasonalData(level=lev)
                    # end of if lev:
                except Exception, e:
                    print e
                    continue
                # end of try:

                # get the time axis index of this first seasonal data
                allYearSeasonalTimeIdx = allYearSeasonalData.getTime()[:]
                latAxis = allYearSeasonalData.getLatitude()
                lonAxis = allYearSeasonalData.getLongitude()
                levAxis = allYearSeasonalData.getLevel()
                fillvalue = allYearSeasonalData.fill_value
                allYearSeasonalData = allYearSeasonalData.filled()
            else:
                # extract the seasonData from second year onwards in loop
                try:
                    if region:
                        seasonData = f(varName, time=(sdate, edate))
                        seasonData = seasonData(region)
                    elif lat and lon:
                        seasonData = f(varName, time=(sdate, edate),
                                         latitude=lat, longitude=lon)
                    elif lat:
                        seasonData = f(varName, time=(sdate, edate),
                                                        latitude=lat)
                    elif lon:
                        seasonData = f(varName, time=(sdate, edate),
                                                       longitude=lon)
                    else:
                        seasonData = f(varName, time=(sdate, edate))
                    # end of if region:

                    if lev:
                        seasonData = seasonData(level=lev)
                    # end of if lev:
                except Exception, e:
                    print e
                    continue
                # end of try:

                # get the time axis index of this current year seasonal data
                seasonalTimeIdx = seasonData.getTime()[:]
                # append to the allYearSeasonalTimeIdx array
                allYearSeasonalTimeIdx = numpy.append(allYearSeasonalTimeIdx,
                                                             seasonalTimeIdx)
                seasonData = seasonData.filled()
                # from next year onwards just concatenate the extracted season
                # data to the first year season data.
                allYearSeasonalData = numpy.concatenate((allYearSeasonalData,
                                                                 seasonData))
                # make memory free
                del seasonData
            # end of if allYearSeasonalData.shape == (0,):
        # end of for year in avlyears:
        f.close()

        if not isinstance(allYearSeasonalTimeIdx, (list, tuple, numpy.ndarray)):
            raise ValueError("full season data may not be available. \
                                        Try to enable kwarg cyclic ")
        # end of if notisinstance(allYearSeasonalTimeIdx, ...):

        # create the new timeAxis for the all years seasonal data
        newTAxis = cdms2.createAxis(allYearSeasonalTimeIdx)
        newTAxis.id = 'time'
        newTAxis.units = timeAxis.units
        newTAxis.designateTime()

        # get the needed axis list
        axislist = [axis for axis in (newTAxis, levAxis, latAxis, lonAxis) if axis]
        # set all its dimensions to the var

        allYearSeasonalData = cdms2.createVariable(allYearSeasonalData)
        # get the mask which is equivalent to the fill_value
        allYearSeasonalMask = (allYearSeasonalData == fillvalue)
        if allYearSeasonalMask.any():
            # reset the full mask
            allYearSeasonalData.mask = allYearSeasonalMask
        # end of if allYearSeasonalMask.any():
        allYearSeasonalData.setAxisList(axislist)
        allYearSeasonalData.id = varName

        return allYearSeasonalData
    # end of def getSeasonData(self, varName, fpath, sday, smon, eday, emon, hr=0):

    def getSummerData(self, varName, fpath, sday=1, smon=5, eday=31, emon=10, hr=0, **kwarg):
        """
        getSummerData : summer season (May to October) data

        Inputs :
          varName - variable name
          fpath - file path
          sday : starting day of the summer season [of all the years of the data].
          smon : starting month of the summer season [of all the years of the data].
          eday : ending day of the summer season [of all the years of the data].
          emon : ending month of the summer season [of all the years of the data].
          hr : hour for both start and end date
          KWargs : (latitude and/or longitude) or (region) and/or level

        Refer: getSeasonData

        Written By : Arulalan.T

        Date : 26.07.2012

        """

        return self.getSeasonalData(varName, fpath, sday, smon, eday, emon, hr, **kwarg)
    # end of def summerVariance(...):


    def getWinterData(self, varName, fpath, sday=1, smon=11, eday=30, emon=4, hr=0, **kwarg):
        """
        getWinterData : winter season (November to April) data

        Inputs :
          varName - variable name
          fpath - file path
          sday : starting day of the winter season [of all the years of the data].
          smon : starting month of the winter season [of all the years of the data].
          eday : ending day of the winter season [of all the years of the data].
          emon : ending month of the winter season [of all the years of the data].
          hr : hour for both start and end date
          KWargs : (latitude and/or longitude) or (region) and/or level

        Refer: getSeasonData

        Written By : Arulalan.T

        Date : 26.07.2012

        """

        return self.getSeasonalData(varName, fpath, sday, smon, eday, emon, hr, **kwarg)
    # end of def winterVariance(...):

    def getSameDayData(self, varName, fpath, day, mon, hr=0, **kwarg):
        """
        getSameDayData : get same day data from all the available years or
                         needed year/s.

        Inputs :
          varName - variable name
          fpath - file path
          day : day of the needed  [of all the years of the data].
          mon : month of the needed [of all the years of the data].
          hr : hour of the needed
          KWargs : (latitude and/or longitude) or (region) and/or level
                   and/or year

        ..note:: It will extract the particular day from all the available years.
           Ofcourse you can control the needed year/s also by using year kwarg.
           Eg1: To get leap day data from all the available years,
                getSameDayData(varName, path, day=29, mon=2)
                It will return all years the leapday data (Feb 29) along with
                its timeAxis and missing values.

        Refer: getSeasonData

        Written By : Arulalan.T

        Date : 13.08.2013

        """

        return self.getSeasonalData(varName, fpath, sday=day, smon=mon,
                                     eday=day, emon=mon, hr=hr, **kwarg)
    # end of def winterVariance(...):

    def _sortFcstHours(self, namelist, endswith=' ', hours=None):
        """
        Inputs:
            namelist : List contains the forecast hours as string type.
            endswith : If hour string is endswith 'hr' or 'hour' that
                       user can pass it.
            hours : By default it takes None.
                    User can pass their own sorted hours list.
                    With respect to this hours arg list only, the namelist
                    string hours will be sorted out if user passed their
                    own list to this hours argument.
                    eg : hours = range(24, 264, 24) or
                    hours = range(264, 12, -24)

        Returns : It will return the sorted forecast hours list of str
                  fcst hours.

        Eg1:
            >>> hourlist = ['120', '24', '72', '48']
            >>> sortedHourList = _sortFcstHours(hourlist)
            >>> print sortedHourList
            >>> ['24', '48', '72', '120']

        Eg2:
            >>> hourlist = ['120hr', '24hr', '72hr', '48hr']
            >>> sortedHourList = _sortFcstHours(hourlist, endswith='hr')
            >>> print sortedHourList
            >>> ['24hr', '48hr', '72hr', '120hr']

        Eg3:
            >>> hourlist = ['60 hour', '36 hour', '12 hour', '48 hour', '24 hour']
            >>> sortedHourList = _sortFcstHours(hourlist,
                                        endswith=' hour', hours=range(12, 72, 12))
            >>> print sortedHourList
            >>> ['12 hour', '24 hour', '36 hour', '48 hour',  '60 hour']

        Eg 4: Decending order by passing own hours list.
            >>> hourlist = ['24', '48', '72', '120']
            >>> sortedHourList = _sortFcstHours(hourlist, hours=range(120, 12, -12))
            >>> print sortedHourList
            >>> ['120', '72', '48', '24']


          ..note :: Eg1 to Eg3 shows the acending order sort. But Eg4 shows in
                    decending order sort by user defined hours list.

        Written By : Arulalan.T
        Date : 11.08.2013
        """

        originalList = [name.split(endswith)[0] for name in namelist]
        if hours is None:
            hours = []
            names = []
            endflag = False
            for name in originalList:
                if name.endswith(endswith):
                    endflag = True
                    name = name.split(endswith)[0]
                if name.isdigit():
                    # number
                    hours.append(int(name))               
                elif name.isalpha():
                    # string
                    names.append(name)
                # end of if name.isdigit():
            # end of for name in originalList:
            hours.sort()
            names.sort()
            if endflag:
                hours = [str(hr) + endswith for hr in hours]
            else:
                hours = [str(hr) for hr in hours]
            # end of if endflag:
            return names + hours
        else:
            _truth_ = ['Merged', 'Obs', 'Observation', 'Anl', 'Analysis']
            _forecasthours_ = _truth_ + [str(hr) for hr in hours]
            sortedFcstList = []
            for hr in _forecasthours_:
                if hr in originalList:
                    sortedFcstList.append(namelist[originalList.index(hr)])
            # end of for hr in _forecasthours_:
            if not sortedFcstList:
                raise ValueError("Couldnt sort forecast hours. \
                        You can control the input args to get sorted it")
            # end of if not sortedFcstList:
            return sortedFcstList
     # end of def _sortFcstHours(self, namelist, endswith=' '):
# end of class TimeUtility():






