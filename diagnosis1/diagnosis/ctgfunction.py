#####********************************************************########
#This program is for finding 2x2 condigency table weather prediction#
# From 2x2 condigency table we can find thse statistical scores     #
#Hit Rate(HR), Bias(BS), Threat Score(TS), Odd Rate(ODR)...etc      #
####************************************************************#####
"""
.. module::ctgfunction
    :synopsis:A useful module for calculating statistical score, from 2x2
             contigency table.

.. moduleauthor:: Dileepkumar R <dileepkunjaai@gmail.com>
    updated by : Arulalan.T <arulalant@gmail.com>

"""


def contingency_table_2x2(obs, fcst, th):
    """
    :func:`contingency_table_2x2`:Creates the 2x2 contigency table useful for
            forecast verification. From 2x2 condigency table we can find thse
            statistical scores such as Hit Rate(HR), Bias(BS),
            Threat Score(TS), Odds Ratio(ODR)...etc

    Inputs: obs- the observed values has to be a numpy array(or whatever
                                                                you decide)
            fcst - the forecast values
            th  - the threshold value for which the contingency table needs
                                to be created (floating point value please!!)
    Outputs: A list of values [a, b, c, d]
             where a = No of values such that both observed and
                                                predicted > threshold
             b = No of values such that observed is < threshold and
                                                predicted > threshold
             c = No of values such that observed is > threshold and
                                                predicted < threshold
             d = No of values such that both observed and
                                                predicted < threshold
    Usage:

    example:
            From the contingency table the following statistics can be
            calculated.
            >>> HR = (a+d)/(a+b+c+d)
            >>> ETS = a/(a+b+c)
            >>> BS = (a+b)/(a+c)
            >>> ODR = (a*d)/(b*c)

    Reference: "Statistical Methods in the Atmospheric Sciences",
                                            Daniel S Wilks, ACADEMIC PRESS

    Links: http://www.cawcr.gov.au/projects/verification/#Atger_2001

    Written by: Dileepkumar R,
                JRF, IIT Delhi

    Date: 24/02/2011

    """

    import numpy.ma
    import numpy

    obs=numpy.ma.array(obs)
    fcst= numpy.ma.array(fcst)

    # We are masking observed values if it is greater than threshold value
    obs_t = numpy.ma.masked_where(obs>=th, obs)
    obs_t_mask = numpy.ma.getmask(obs_t)
    # We are masking forcast values if it is greater than threshold value
    fcst_t = numpy.ma.masked_where(fcst>=th, fcst)
    fcst_t_mask = numpy.ma.getmask(fcst_t)
    # Masking if both observed and predicted greater than threshold
    # i.e it goes to "a"

    both_agree_yes = numpy.ma.logical_and(obs_t_mask, fcst_t_mask)
    # Masking if both observed and predicted less than threshold
    #  ie it goes to "d"
    both_agree_no = numpy.ma.logical_and(numpy.ma.logical_not(obs_t_mask),
                                         numpy.ma.logical_not(fcst_t_mask))
    # Masking if  observed < threshold and predicted > threshold
    # .i.e it goes to "b    "
    obs_no_fcst_yes = numpy.ma.logical_and(numpy.ma.logical_not(obs_t_mask),
                                                                fcst_t_mask)
    # Masking if  observed > threshold and predicted < threshold
    # i.e it goes to "c    "
    obs_yes_fcst_no = numpy.ma.logical_and(obs_t_mask,
                                        numpy.ma.logical_not(fcst_t_mask))
    # Making an array of "1"s of order same as observed or predicted
    dummy = numpy.ones(obs.shape, numpy.int)

    total = float(numpy.sum(dummy.copy()))
    #Calculating the total no. of entries

    a_mat = numpy.ma.array(dummy.copy(), mask=both_agree_yes)
    d_mat = numpy.ma.array(dummy.copy(), mask=both_agree_no)
    c_mat = numpy.ma.array(dummy.copy(), mask=obs_yes_fcst_no)
    b_mat = numpy.ma.array(dummy.copy(), mask=obs_no_fcst_yes)
    #Masking the entries of dummy array with respect to the above conditions

    # Subtact this from total (WHY???)
    #Actually we are masking the needed values

    a = total - a_mat.count()
    b = total - b_mat.count()
    c = total - c_mat.count()
    d = total - d_mat.count()

    if (a == b == c ==d == 0):
        return 'Error, your data is not correct'
    else:
        # return the values are in 2x2 matrix table formate
        return [[a, b], [c, d]]
# end of def contingency_table_2x2(obs, fcst, th):

def accuracy(obs=None, fcst=None, th=None, **ctg):
    """
   :func:`accuracy`:Hit Rate ,the most direct and intuitive measure of the
        accuracy of categorical forecasts is hit rate. The average correspond-
        ence between individual nforecasts and the events they predict. Scalar
        measures  of accuracy are meant to summarize,in a single number, the
        overall quality of a set of forecasts. Can be mislead, since it is
        heavily influenced by the most common category, usually "no event"
        in the case of rare weather.

            Accuracy= (a+d)/(a+b+c+d); 'a' -hits, 'b'-false alarm,
                    'c'-misses, & 'd'- correct negatives


    Inputs: obs- the observed values has to be a numpy array(or whatever
                                                                you decide)
            fcst - the forecast values
            th  - the threshold value for which the contingency table needs
                                to be created (floating point value please!!)
            By default obs, fcst, th are None. Instead of passing obs, fcst,
            and th values, you can pass 'ctg_table' kwarg as 2x2 matrix value.

    Outputs:
        Range: 0 to 1

        Perfect Score: 1

    Reference: "Statistical Methods in the Atmospheric Sciences",
                Daniel S Wilks, ACADEMIC PRESS(Page No:236-240)

    Links : http://www.cawcr.gov.au/projects/verification/

    Written by: Dileepkumar R,
                    JRF, IIT Delhi

    Date: 24/02/2011

    """

    if 'ctg_table' in ctg:
        # user passed contigency table
        [[a, b], [c, d]] = ctg.get('ctg_table')
    else:
        if not obs:
            raise ValueError('You must pass obs value')
        if not fcst:
            raise ValueError('You must pass fcst value')
        if not th:
            raise ValueError('You must pass threshold value')
        # user passed obs, fcst, th values
        [[a, b], [c, d]] = contingency_table_2x2(obs, fcst, th)
    # end of if 'ctg_table' in ctg:
    denom = (a + b + c + d)
    if (denom == 0):
        return 1e+20
    else:
        return round((a+d)/(a+b+c+d), 4)
# end of def accuracy(obs=None, fcst=None, th=None, **ctg):

def bias_score(obs=None, fcst=None, th=None, **ctg):
    """
    :func:`bias_score`: Bias score(frequency bias)-Measures the correspondence
            between the average forecast and the average observed value of the
            predictand. This is different from accuracy, which measures the
            average correspondence between individual pairs of forecasts and
            observations.

                Bias= (a+b)/(a+c); 'a' -hits, 'b'-false alarm, & 'c'-misses

    Inputs: obs- the observed values has to be a numpy array(or whatever
                                                                you decide)
            fcst - the forecast values
            th  - the threshold value for which the contingency table needs
                                to be created (floating point value please!!)
            By default obs, fcst, th are None. Instead of passing obs, fcst,
            and th values, you can pass 'ctg_table' kwarg as 2x2 matrix value.

    Outputs:
        Range: 0 to infinity

        Perfect score: 1

    Reference: "Statistical Methods in the Atmospheric Sciences",
                Daniel S Wilks, ACADEMIC PRESS(Page No: 241)

    Links : http://www.cawcr.gov.au/projects/verification/

    Written by: Dileepkumar R,
                JRF, IIT Delhi

    Date: 24/02/2011

    """

    if 'ctg_table' in ctg:
        # user passed contigency table
        [[a, b], [c, d]] = ctg.get('ctg_table')
    else:
        if not obs:
            raise ValueError('You must pass obs value')
        if not fcst:
            raise ValueError('You must pass fcst value')
        if not th:
            raise ValueError('You must pass threshold value')
        # user passed obs, fcst, th values
        [[a, b], [c, d]] = contingency_table_2x2(obs, fcst, th)
    # end of if 'ctg_table' in ctg:
    denom = (a + c)
    if (denom == 0):
        return 1e+20
    else:
        return round((a+b)/(a+c), 4)
# end of def bias_score(obs=None, fcst=None, th=None, **ctg):

def pod(obs=None, fcst=None, th=None, **ctg):
    """
    :func:`pod`:Probability of detection(POD), simply the fraction of those
            occasions when the forecast event occurred on which it was also
            forecast.

              POD= a/(a+c); 'a' -hits, & 'c'-misses


    Inputs: obs- the observed values has to be a numpy array(or whatever
                                                                you decide)
            fcst - the forecast values
            th  - the threshold value for which the contingency table needs
                                to be created (floating point value please!!)
            By default obs, fcst, th are None. Instead of passing obs, fcst,
            and th values, you can pass 'ctg_table' kwarg as 2x2 matrix value.

    Outputs:
        Range: 0 to 1

        Perfect Score: 1

    Reference: "Statistical Methods in the Atmospheric Sciences",
                Daniel S Wilks, ACADEMIC PRESS(Page No: 240)

    Links: http://www.cawcr.gov.au/projects/verification/

    Written by: Dileepkumar R,
                JRF, IIT Delhi

    Date: 24/02/2011

    """

    if 'ctg_table' in ctg:
        # user passed contigency table
        [[a, b], [c, d]] = ctg.get('ctg_table')
    else:
        if not obs:
            raise ValueError('You must pass obs value')
        if not fcst:
            raise ValueError('You must pass fcst value')
        if not th:
            raise ValueError('You must pass threshold value')
        # user passed obs, fcst, th values
        [[a, b], [c, d]] = contingency_table_2x2(obs, fcst, th)
    # end of if 'ctg_table' in ctg:
    denom = (a+c)
    if (denom == 0):
        return 1e+20
    else:
        return round(a/(a+c), 4)
# end of def pod(obs=None, fcst=None, th=None, **ctg):

def far(obs=None, fcst=None, th=None, **ctg):
    """
    :func:`far`:False alarm ratio(FAR)-Proportion of forecast events that fail
            to materialize.

                FAR= b/(a+b); 'a' -hits, & 'b'-false alarm

    Inputs: obs- the observed values has to be a numpy array(or whatever
                                                                you decide)
            fcst - the forecast values
            th  - the threshold value for which the contingency table needs
                                to be created (floating point value please!!)
            By default obs, fcst, th are None. Instead of passing obs, fcst,
            and th values, you can pass 'ctg_table' kwarg as 2x2 matrix value.

    Outputs:

        Range: 0 to 1

        Perfect Score: 0

    Reference: "Statistical Methods in the Atmospheric Sciences",
                Daniel S Wilks, ACADEMIC PRESS(Page No: 240-241)

    Links: http://www.cawcr.gov.au/projects/verification/

    Written by: Dileepkumar R,
                JRF, IIT Delhi

    Date: 24/02/2011

    """

    if 'ctg_table' in ctg:
        # user passed contigency table
        [[a, b], [c, d]] = ctg.get('ctg_table')
    else:
        if not obs:
            raise ValueError('You must pass obs value')
        if not fcst:
            raise ValueError('You must pass fcst value')
        if not th:
            raise ValueError('You must pass threshold value')
        # user passed obs, fcst, th values
        [[a, b], [c, d]] = contingency_table_2x2(obs, fcst, th)
    # end of if 'ctg_table' in ctg:
    denom = (a + b)
    if (denom == 0):
        return 1e+20
    else:
        return round(b/(a+b), 4)
# end of def far(obs=None, fcst=None, th=None, **ctg):

def pofd(obs=None, fcst=None, th=None, **ctg):
    """
    :func:`podf`:Probability of false detection (false alarm rate), measures
            the fraction of false alarms given the event did not occur.

                POFD=b/(d+b); 'b'-false alarm & 'd'- correct negatives

    Inputs: obs - the observed values has to be a numpy array(or whatever
                                                                you decide)
            fcst - the forecast values
            th  - the threshold value for which the contingency table needs
                                to be created (floating point value please!!)
            By default obs, fcst, th are None. Instead of passing obs, fcst,
            and th values, you can pass 'ctg_table' kwarg as 2x2 matrix value.

    Outputs:

        Range: 0 to 1

        Perfect Score: 0

    Links: http://www.cawcr.gov.au/projects/verification/

    """

    if 'ctg_table' in ctg:
        # user passed contigency table
        [[a, b], [c, d]] = ctg.get('ctg_table')
    else:
        if not obs:
            raise ValueError('You must pass obs value')
        if not fcst:
            raise ValueError('You must pass fcst value')
        if not th:
            raise ValueError('You must pass threshold value')
        # user passed obs, fcst, th values
        [[a, b], [c, d]] = contingency_table_2x2(obs, fcst, th)
    # end of if 'ctg_table' in ctg:
    denom = d + b
    if(denom == 0):
        return 0
    else:
        return round(b/(d+b), 4)
# end of def pofd(obs=None, fcst=None, th=None, **ctg):

def ts(obs=None, fcst=None, th=None, **ctg):
    """
    :func:'ts':    Threat Score (Critical Success Index), a frequently used
            alternative to the hit rate, particularly when the event to be
            forecast (as the "yes" event) occurs substantially less frequently
            than the non-occurrence ("no").

                TS=a/(a+b+c); 'a' -hits, 'b'-false alarm, &'c'-misses

    Inputs: obs- the observed values has to be a numpy array(or whatever
                                                                you decide)
            fcst - the forecast values
            th  - the threshold value for which the contingency table needs
                                to be created (floating point value please!!)
            By default obs, fcst, th are None. Instead of passing obs, fcst,
            and th values, you can pass 'ctg_table' kwarg as 2x2 matrix value.

    Outputs:
        Range: 0 to 1

        Perfect Score: 1

    Reference: "Statistical Methods in the Atmospheric Sciences",
                Daniel S Wilks, ACADEMIC PRESS(Page No: 240)

    Links: http://www.cawcr.gov.au/projects/verification/

    Written by: Dileepkumar R,
                JRF, IIT Delhi

    Date: 24/02/2011

    """

    if 'ctg_table' in ctg:
        # user passed contigency table
        [[a, b], [c, d]] = ctg.get('ctg_table')
    else:
        if not obs:
            raise ValueError('You must pass obs value')
        if not fcst:
            raise ValueError('You must pass fcst value')
        if not th:
            raise ValueError('You must pass threshold value')
        # user passed obs, fcst, th values
        [[a, b], [c, d]] = contingency_table_2x2(obs, fcst, th)
    # end of if 'ctg_table' in ctg:
    denom = (a + b + c)
    if (denom == 0):
        return 0
    else:
        return round(a/(a+b+c), 4)
# end of def ts(obs=None, fcst=None, th=None, **ctg):

def ets(obs=None, fcst=None, th=None, **ctg):
    """
    :func:`ets`:Equitable threat score (Gilbert skill score), the number of
            forecasts of the event correct by chance, 'a_random',is determined
            by assuming that the forecasts are totally independent of the obs-
            ervations, and forecast will match the observation only by chance.
            This is one form of an unskilled forecast, which can be generated
            by just guessing what will happen.

                ETS=(a-a_random)/(a+c+b-a_random)
                a_random=[(a+c)(a+b)]/(a+b+c+d); 'a' -hits, 'b'-false alarm,
                                        'c'-misses, & 'd'- correct negatives

    Inputs: obs- the observed values has to be a numpy array(or whatever
                                                                you decide)
            fcst - the forecast values
            th  - the threshold value for which the contingency table needs
                                to be created (floating point value please!!)

            By default obs, fcst, th are None. Instead of passing obs, fcst,
            and th values, you can pass 'ctg_table' kwarg as 2x2 matrix value.

    Outputs:

        Range: -1/3 to 1, 0 indicate no skill.

        Perfect Score: 1

    Links: http://www.cawcr.gov.au/projects/verification/

    Written by: Dileepkumar R,
                JRF, IIT Delhi

    Date: 24/02/2011

    """

    if 'ctg_table' in ctg:
        # user passed contigency table
        [[a, b], [c, d]] = ctg.get('ctg_table')
    else:
        if not obs:
            raise ValueError('You must pass obs value')
        if not fcst:
            raise ValueError('You must pass fcst value')
        if not th:
            raise ValueError('You must pass threshold value')
        # user passed obs, fcst, th values
        [[a, b], [c, d]] = contingency_table_2x2(obs, fcst, th)
    # end of if 'ctg_table' in ctg:
    a_random = ((a+c)*(a+b))/(a+b+c+d)
    denom = (a + c + b -a_random)
    if (denom == 0):
        if (a == a+b+c+d):
            return 1
        elif (d == a+b+c+d):
            return 1
    else:
        return round((a-a_random)/(a+c+b-a_random), 4)
# end of def ets(obs=None, fcst=None, th=None, **ctg):

def kss(obs=None, fcst=None, th=None, **ctg):
    """
    :func:`kss`:Hanssen and Kuipers discriminant(Kuipers Skill Score), the
            contribution made to the Kuipers score by a correct "no" or
            "yes" forecast increases as the event is more or less likely,
            respectively.A drawback of this score is that it tends to converge
            to the POD for rare events, because the value of "d" becomes very
            large.

                HK= (ad-bc)/[(a + c)(b + d)]; 'a' -hits, 'b'-false alarm,
                'c'-misses, & 'd'- correct negatives

    Inputs: obs- the observed values has to be a numpy array(or whatever
                                                                you decide)
            fcst - the forecast values
            th  - the threshold value for which the contingency table needs
                                to be created (floating point value please!!)

            By default obs, fcst, th are None. Instead of passing obs, fcst,
            and th values, you can pass 'ctg_table' kwarg as 2x2 matrix value.

    Outputs:

        Range:-1 to 1
        Perfect Score: 1
    Reference: "Statistical Methods in the Atmospheric Sciences",
                    Daniel S Wilks, ACADEMIC PRESS(Page No: 249-250)

    Links: http://www.cawcr.gov.au/projects/verification/

    Written by: Dileepkumar R,
                JRF, IIT Delhi

    Date: 24/02/2011

    """

    if 'ctg_table' in ctg:
        # user passed contigency table
        [[a, b], [c, d]] = ctg.get('ctg_table')
    else:
        if not obs:
            raise ValueError('You must pass obs value')
        if not fcst:
            raise ValueError('You must pass fcst value')
        if not th:
            raise ValueError('You must pass threshold value')
        # user passed obs, fcst, th values
        [[a, b], [c, d]] = contingency_table_2x2(obs, fcst, th)
    # end of if 'ctg_table' in ctg:
    denom = (a + c)*(b + d)
    if (denom == 0):
        if (a==a+b+c+d):
            return 1
        elif (d==a+b+c+d):
            return 1
        return 0
    else:
        return round((a*d-b*c)/((a + c)*(b + d)), 4)
# end of def kss(obs=None, fcst=None, th=None, **ctg):

def hss(obs=None, fcst=None, th=None, **ctg):
    """
    :func:`hss`:Heidke skill score (Cohen's k), the reference accuracy
            measure in the Heidke score is the hit rate that would be
            achieved by random forecasts, subject to the constraint that
            the marginal distributions of forecasts and observations
            characterizing the contingency table for the random forecasts,
            P(Yi) and p(oj), are the same as the marginal distributions in
            the actual verification data set.

                HSS= 2.( a d - bc)/[(a + c)(c + d) + (a + b)(b + d)];
            'a' -hits, 'b'-false alarm, 'c'-misses, & 'd'- correct  negatives

    Inputs: obs- the observed values has to be a numpy array(or whatever
                                                                you decide)
            fcst - the forecast values
            th  - the threshold value for which the contingency table needs
                                to be created (floating point value please!!)
            By default obs, fcst, th are None. Instead of passing obs, fcst,
            and th values, you can pass 'ctg_table' kwarg as 2x2 matrix value.

    Outputs:

        Range: -infinity to 1, 0 indicate no skill.

        Perfect Score: 1

    Reference: "Statistical Methods in the Atmospheric Sciences",
                Daniel S Wilks, ACADEMIC PRESS(Page No: 248-249)

    Links: http://www.cawcr.gov.au/projects/verification/

    Written by: Dileepkumar R,
                JRF, IIT Delhi

    Date: 24/02/2011

    """

    if 'ctg_table' in ctg:
        # user passed contigency table
        [[a, b], [c, d]] = ctg.get('ctg_table')
    else:
        if not obs:
            raise ValueError('You must pass obs value')
        if not fcst:
            raise ValueError('You must pass fcst value')
        if not th:
            raise ValueError('You must pass threshold value')
        # user passed obs, fcst, th values
        [[a, b], [c, d]] = contingency_table_2x2(obs, fcst, th)
    # end of if 'ctg_table' in ctg:
    denom = ((a + c)*(c + d)) + ((a + b)*(b + d))
    if (denom == 0):
        if(a==a+b+c+d):
            return 1
        elif (d==a+b+c+d):
            return 1
        return "Data has some problem"
    else:
        return round(2*(a*d - b*c)/((a + c)*(c + d) + (a + b)*(b + d)), 4)
# end of def hss(obs=None, fcst=None, th=None, **ctg):

def odr(obs=None, fcst=None, th=None, **ctg):
    """
    :func:`odr`:Odds ratio, the odds ratio is the ratio of the odds of an
            event occurring in one group to the odds of it occurring in
            another group.cThe term is also used to refer to sample-based
            estimates of this ratio.Do not use if any of the cells in the
            contingency table are equal to 0. The logarithm of the odds
            ratio is often used instead of the original value.Used widely
            in medicine but not yet in meteorology.

                OD= ad/bc; 'a' -hits, 'b'-false alarm, 'c'-misses, &
                            'd'- correct negatives

    Inputs: obs- the observed values has to be a numpy array(or whatever
                                                                you decide)
            fcst - the forecast values
            th  - the threshold value for which the contingency table needs
                                to be created (floating point value please!!)
            By default obs, fcst, th are None. Instead of passing obs, fcst,
            and th values, you can pass 'ctg_table' kwarg as 2x2 matrix value.

    Outputs:

        Range: 0 to infinity, 1 indicate no skill

        Perfect Score: infinity

    Links: http://www.cawcr.gov.au/projects/verification/

    Written by: Dileepkumar R,
                JRF, IIT Delhi

    Date: 24/02/2011

    """

    if 'ctg_table' in ctg:
        # user passed contigency table
        [[a, b], [c, d]] = ctg.get('ctg_table')
    else:
        if not obs:
            raise ValueError('You must pass obs value')
        if not fcst:
            raise ValueError('You must pass fcst value')
        if not th:
            raise ValueError('You must pass threshold value')
        # user passed obs, fcst, th values
        [[a, b], [c, d]] = contingency_table_2x2(obs, fcst, th)
    # end of if 'ctg_table' in ctg:
    denom = b*c
    if(denom == 0):
        return 1e+20
    else:
        return round((a*d)/(b*c), 4)
# end of def odr(obs=None, fcst=None, th=None, **ctg):

def logodr(obs=None, fcst=None, th=None, **ctg):
    """
    :func:`logodr`: Log Odds ratio, LOR is the logaritham of odds ratio.
                When the sample is small/moderate it is better to use Log
                Odds Ratio. It is a good tool for finding associations
                between variables.

                    LOR=Log(Odds Ratio); Odds Ratio=ad/bc; 'a' -hits,
                        'b'-false alarm, 'c'-misses, & 'd'- correct negatives

    Inputs: obs- the observed values has to be a numpy array(or whatever
                                                                you decide)
            fcst - the forecast values
            th  - the threshold value for which the contingency table needs
                                to be created (floating point value please!!)
            By default obs, fcst, th are None. Instead of passing obs, fcst,
            and th values, you can pass 'ctg_table' kwarg as 2x2 matrix value.

    Outputs:

        Range: -infinity to infinity, 0 indicate no skill.

        Perfect Score: infinity

    Written by: Dileepkumar R,
                JRF, IIT Delhi

    Date: 24/02/2011

    """

    import math
    if 'ctg_table' in ctg:
        # user passed contigency table
        [[a, b], [c, d]] = ctg.get('ctg_table')
    else:
        if not obs:
            raise ValueError('You must pass obs value')
        if not fcst:
            raise ValueError('You must pass fcst value')
        if not th:
            raise ValueError('You must pass threshold value')
        # user passed obs, fcst, th values
        [[a, b], [c, d]] = contingency_table_2x2(obs, fcst, th)
    # end of if 'ctg_table' in ctg:
    denom = b*c
    nume = a*d
    if (denom == 0):
        return 1e+20
    else:
        if (nume == 0):
            return -1e+20
        else:
            return math.log(odr(ctg_table = [[a, b], [c, d]]))
# end of def logodr(obs=None, fcst=None, th=None, **ctg):

def orss(obs=None, fcst=None, th=None, **ctg):
    """
    :func:`orss`: Odds ratio skill score (Yule's Q), this score was proposed
            long ago as a 'measure of association' by the statistician
            G. U. Yule (Yule 1900) and is referred to as Yule's Q. It is
            based entirely on the joint conditional probabilities,
            and so is not influenced in any way by the marginal totals.

            ORSS= (ad-bc)/(ad+bc); 'a' -hits, 'b'-false alarm, 'c'-misses,
                & 'd'- correct negatives

    Inputs: obs- the observed values has to be a numpy array(or whatever
                                                                you decide)
            fcst - the forecast values
            th  - the threshold value for which the contingency table needs
                                to be created (floating point value please!!)
            By default obs, fcst, th are None. Instead of passing obs, fcst,
            and th values, you can pass 'ctg_table' kwarg as 2x2 matrix value.

    Outputs:

        Range: -1 to 1, 0 indicates no skill

        Perfect Score: 1

    Reference: Stephenson, D.B., 2000: Use of the "odds ratio" for diagnosing
                forecast skill. Wea. Forecasting, 15, 221-232.

    Links: http://www.cawcr.gov.au/projects/verification/

    Written by: Dileepkumar R,
                JRF, IIT Delhi

    Date: 24/02/2011

    """

    if 'ctg_table' in ctg:
        # user passed contigency table
        [[a, b], [c, d]] = ctg.get('ctg_table')
    else:
        if not obs:
            raise ValueError('You must pass obs value')
        if not fcst:
            raise ValueError('You must pass fcst value')
        if not th:
            raise ValueError('You must pass threshold value')
        # user passed obs, fcst, th values
        [[a, b], [c, d]] = contingency_table_2x2(obs, fcst, th)
    # end of if 'ctg_table' in ctg:
    denom = (a*d + b*c)
    if (denom == 0):
        if(a==a+b+c+d):
            return 1
        elif (d==a+b+c+d):
            return 1
        else:
            return 0
    else:
        return (a*d - b*c)/(a*d + b*c)
# end of def orss(obs=None, fcst=None, th=None, **ctg):

def eds(obs=None, fcst=None, th=None, **ctg):
    """
    :func:'eds':Extreme dependency score, converges to 2n-1 as event
            frequency approaches 0, where n is a parameter describing how
            fast the hit rate converges to zero for rarer events. EDS is
            independent of bias, so should be presented together with the
            frequency bias.

                EDS={2Log[(a+c)/(a+b+c+d)]/Log(a/(a+b+c+d))}-1; 'a' -hits,
                'b'-false alarm, 'c'-misses, & 'd'- correct negatives

    Inputs: obs- the observed values has to be a numpy array(or whatever
                                                                you decide)
            fcst - the forecast values
            th  - the threshold value for which the contingency table needs
                                to be created (floating point value please!!)
            By default obs, fcst, th are None. Instead of passing obs, fcst,
            and th values, you can pass 'ctg_table' kwarg as 2x2 matrix value.

    Outputs:

        Range: -1 to 1, 0 indicate no skill.

        Perfect Score: 1

    Reference: [1]Stephenson D.B., B. Casati, C.A.T. Ferro and
                C.A. Wilson, 2008: The extreme dependency score:
                a non-vanishing measure for forecasts of rare events.
                 Meteorol. Appl., 15, 41-50.

    Link:    http://www.cawcr.gov.au/projects/verification.

    Written by: Dileepkumar R,
                JRF, IIT Delhi

    Date: 24/02/2011

    """

    import math
    if 'ctg_table' in ctg:
        # user passed contigency table
        [[a, b], [c, d]] = ctg.get('ctg_table')
    else:
        if not obs:
            raise ValueError('You must pass obs value')
        if not fcst:
            raise ValueError('You must pass fcst value')
        if not th:
            raise ValueError('You must pass threshold value')
        # user passed obs, fcst, th values
        [[a, b], [c, d]] = contingency_table_2x2(obs, fcst, th)
    # end of if 'ctg_table' in ctg:
    N = a + b + c + d
    if (a == 0):
        return -1.0
    elif (a == N):
        return 1.0
    else:
        return (2*(math.log((a+c)/N))/(math.log(a/N)))-1
# end of def eds(obs=None, fcst=None, th=None, **ctg):
