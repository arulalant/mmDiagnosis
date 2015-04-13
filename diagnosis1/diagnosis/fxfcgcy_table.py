#####***************************************************************#######
#This program is for finding 4x4 & 2x2 condigency table weather prediction#
# From 2x2 condigency table we can find thse statistical scores           #
#Hit Rate(HR), Bias(BS), Threat Score(TS), Odd Rate(ODR)...etc            #
####****************************************************************#######
"""
.. module::ctgfunction
    :platform: Linux
   :synopsis:A useful module for calculating statistical score, from 4x4
			 contigency table. 

.. moduleauthor:: Dileepkumar R <dileepkunjaai@gmail.com>


"""

def contingency_table_4x4(obs, fcst, th, av, hy):

    """
	:func:`contingency_table_4x4`:	Contingency_table_4x4, for further 
			comprehensive study for the skill, Hit Rate(HR), Bias(BS), Threat 
			Score(TS),..etc and hit rates for different categories are calcul-
			ated.We categorise the 2x2 condigency table to 4x4 contigency 
			table. Hit rate for different categories moderate, heavy and very 
			heavy is calculated. The 2x2 contigency table useful for forecast
			verification. From 2x2 condigency table we can find the statistical 
			scores such as Hit Rate(HR), Bias(BS), Threat Score(TS), Odds Ratio
			(ODR)...etc
									 
	Inputs:
        obs -the observed values has to be a list(or whatever you decide)
        fcst-the forecast values
        th -the threshold value for which the contingency table needs to
                be created (floating point value please!!)
        av-the data points between 'th' and 'av' we say that data
                point is moderate value
        hy-the data points above 'hy' we say that the data point
                is higher value
        Outputs:
            A list of values [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p
            are entries of 4x4 contingency table
        where a = No of values such that both observed and
                                                        predicted < threshold
        b = No of values such that 'av'>observed is > threshold and
                                                        predicted < threshold
        c = No of values such that 'av'>observed is < 'hy'
                                                        predicted < threshold
        d = No of values such that observed is > 'hy'
                                                        predicted < threshold

        e =No of values such that  observed< threshold and
                                                   threshold<predicted < 'av'
        f =No of values such that  'av'>observed is > threshold and
                                                threshold<predicted < 'av'
        g =No of values such that 'av'>observed is < 'hy' and
                                                threshold<predicted < 'av'
        h =No of values such that observed is > 'hy'and
                                                threshold<predicted < 'av'

        i=No of values such that  observed< threshold and 'av'<predicted< 'hy'
        j=No of values such that  'av'>observed is > thresholdand and
                                                        'av'<predicted< 'hy'
        k=No of values such that 'av'>observed is < 'hy' and
                                                        'av'<predicted< 'hy'
        l=No of values such that observed is > 'hy'and 'av'<predicted< 'hy'

        m=No of values such that  observed< threshold and predicted> 'hy'
        n=No of values such that  'av'>observed is > thresholdand
                                                        and predicted> 'hy'
        o=No of values such that 'av'>observed is < 'hy' and
        p=No of values such that observed is > 'hy'and predicted> 'hy

        A list of values A, B, C, D are list are entries of
                                                        4x4 contigency table
        A = No of values such that both observed and predicted > threshold
        B = No of values such that observed is < threshold and
                                                        predicted > threshold
        C = No of values such that observed is > threshold and
                                                        predicted < threshold
        D = No of values such that both observed and predicted < threshold

        Usage: Comparing the statistical score, we can analyse the models
        example:
        From the contingency table the following statistics can be calculated.
        HR=(a+d)/(a+b+c+d) (for 2x2 contigency table)
        HR =(A+F+K+P)/N( for 4x4 contigency table, N is total all the
                                                                frequencies)
        ETS=a/(a+b+c)
        BS=(a+b)/(a+c)
        ODR= (a*d)/(b*c)

        N=(a+ b+ c+ d+ e+ f+ g+ h+ i+ j+ k+ l+ m+ n+ o+ p)
        N(Oi)= um of entries of i th column of 4x4 contingency table.
        N(Fi)= Sum of entries of i th row of 4x4 contingency table.

    Reference:

        "Statistical Methods in the Atmospheric Sciences",
        Daniel S Wilks, ACADEMIC PRESS

        "NCMRWF Report,  Monsoon-2009 Performance of T254L64 Global
                                                Assimilation-Forecast System"

    Written by:    Dileepkumar R,
                JRF, IIT Delhi

    Date: 29/02/2011
    """
    import numpy

    import numpy.ma as MA
    # If 'obs' or 'fcst' are not list then an assertion error will show
    #assert type(obs) is list," 'obs' is not a list"
    #assert type(fcst) is list," 'fcst' is not a list"

    obs=MA.array(obs)
    fcst= MA.array(fcst)
    #If we give 'obs' & 'fcst' of different dimention  an assertion
    #error will show
    assert (obs.shape == fcst.shape), \
    "Dimention of 'obs' and 'fcst' are different"

    # Defining threshold
    th = float(th)
    av = float(av)
    hy = float(hy)

    #We are masking the observation < threshold

    obs_1= MA.masked_where(obs<th, obs)
    obs_1_mask= MA.getmask(obs_1)

     # Masking the observation between "threshold" & "av"
    condition_1o= MA.logical_and(th<=obs, obs< av)
    obs_2 = MA.masked_where(condition_1o, obs)
    obs_2_mask = MA.getmask(obs_2)
    # Masking the observation between "av" & "hv"
    condition_2o= MA.logical_and(obs<hy, obs>= av)
    obs_3 = MA.masked_where(condition_2o, obs)
    obs_3_mask = MA.getmask(obs_3)
    # Masking the observation > hy

    obs_4=MA.masked_where(obs>=hy, obs)
    obs_4_mask = MA.getmask(obs_4)
    #Masking the forecast < threshold
    fcst_1= MA.masked_where(fcst<th, fcst)
    fcst_1_mask= MA.getmask(fcst_1)

    # Masking the forecast between "threshold" & "av"

    condition_1f= MA.logical_and(th<=fcst, fcst< av)
    fcst_2 = MA.masked_where(condition_1f, fcst)
    fcst_2_mask = MA.getmask(fcst_2)
    # Masking the forecast between "av" & "hv"
    condition_2f= MA.logical_and(fcst<hy, fcst>= av)
    fcst_3 = MA.masked_where(condition_2f, fcst)
    fcst_3_mask = MA.getmask(fcst_3)
    # Masking the forecast > hy
    fcst_4=MA.masked_where(fcst>=hy, fcst)
    fcst_4_mask = MA.getmask(fcst_4)
    #o1 , f1 ; less than threshold(Th) is no rain
    #o2, f2 ; greater than Th and less than 'av' is light to moderate rain
    #o3, f3 ; greater than 'av' and less than 'hy' is heavy rain
    #o4, f4 ; greater than 'hy' is very heavy rain.


    # Masking such that forcast < threshold vs other four condition
    # for observation

    f1o1=MA.logical_and(fcst_1_mask, obs_1_mask)# for a
    f1o2=MA.logical_and(fcst_1_mask, obs_2_mask)# for b
    f1o3=MA.logical_and(fcst_1_mask, obs_3_mask)# for c
    f1o4=MA.logical_and(fcst_1_mask, obs_4_mask)# for d
    # Masking such that forecast between "threshold" & "av" vs other four
    # condition for observation

    f2o1=MA.logical_and(fcst_2_mask, obs_1_mask)# for e
    f2o2=MA.logical_and(fcst_2_mask, obs_2_mask)# for f
    f2o3=MA.logical_and(fcst_2_mask, obs_3_mask)# for g
    f2o4=MA.logical_and(fcst_2_mask, obs_4_mask)# for h

    # Masking such that forecast between "av" & "hv" vs other four condition
    # for observation
    f3o1=MA.logical_and(fcst_3_mask, obs_1_mask)# for i
    f3o2=MA.logical_and(fcst_3_mask, obs_2_mask)# for j
    f3o3=MA.logical_and(fcst_3_mask, obs_3_mask)# for k
    f3o4=MA.logical_and(fcst_3_mask, obs_4_mask)# for l
    # Making an array of "1"s of order same as observed or predicted

    f4o1=MA.logical_and(fcst_4_mask, obs_1_mask)# for m
    f4o2=MA.logical_and(fcst_4_mask, obs_2_mask)# for n
    f4o3=MA.logical_and(fcst_4_mask, obs_3_mask)# for o
    f4o4=MA.logical_and(fcst_4_mask, obs_4_mask)# for p
    #Making an array of "1"s of order same as 'obs' or 'fcst'

    dummy = numpy.ones(obs.shape, numpy.int)
    # Calculating the total no. of entries
    total = float(numpy.sum(dummy))

    # Masking the entries of dummy array with respect to the above conditions
    a_mat = MA.array(dummy, mask=f1o1)
    b_mat = MA.array(dummy, mask=f1o2)
    c_mat = MA.array(dummy, mask=f1o3)
    d_mat = MA.array(dummy, mask=f1o4)

    e_mat = MA.array(dummy, mask=f2o1)
    f_mat = MA.array(dummy, mask=f2o2)
    g_mat = MA.array(dummy, mask=f2o3)
    h_mat = MA.array(dummy, mask=f2o4)

    i_mat = MA.array(dummy, mask=f3o1)
    j_mat = MA.array(dummy, mask=f3o2)
    k_mat = MA.array(dummy, mask=f3o3)
    l_mat = MA.array(dummy, mask=f3o4)

    m_mat = MA.array(dummy, mask=f4o1)
    n_mat = MA.array(dummy, mask=f4o2)
    o_mat = MA.array(dummy, mask=f4o3)
    p_mat = MA.array(dummy, mask=f4o4)

    # Subtact this from total (WHY???)--->Actually we are masking the needed
    # values, therefore to compute the actual value we have to substract it
    # from total
    a = total - numpy.sum(a_mat)
    b = total - numpy.sum(b_mat)
    c = total - numpy.sum(c_mat)
    d = total - numpy.sum(d_mat)

    e = total - numpy.sum(e_mat)
    f = total - numpy.sum(f_mat)
    g = total - numpy.sum(g_mat)
    h = total - numpy.sum(h_mat)

    i = total - numpy.sum(i_mat)
    j = total - numpy.sum(j_mat)
    k = total - numpy.sum(k_mat)
    l = total - numpy.sum(l_mat)

    m = total - numpy.sum(m_mat)
    n = total - numpy.sum(n_mat)
    o = total - numpy.sum(o_mat)
    p = total - numpy.sum(p_mat)
    #return [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o ,p]
    """
    From 4x4 contingency table we can create 2x2 contingency table
    """

    A = f+g+h+j+k+l+n+o+p #A is total no of values both observed and
    # forcast are > threshold
    B = e+i+m # B is total number of values such that observed< threshold &
    # predicted > threshold
    C = b+c+d #C is total number of values such that observed> threshold &
    # predicted < threshold
    D = a #D is total no of values such that both observed and
    # forcast are < threshold

    # We are changing the entries of 4x4 & 2x2 as float and represnt as
    # a matrix form

    tb4= ([[a, b, c, d], [e, f, g, h], [i, j, k, l], [m, n, o, p]])
    tb4 =numpy.array(tb4, dtype = float)
    tb2= ([A, B], [C, D])
    tb2 = numpy.array(tb2, dtype = float)

    return    tb4
#####**********************************************#########

def histogram():
    pass
    """
    Histogram:
        Plot relative frequencies of forcast and observed categories.
        Shows similarity between location, spread, and skewness of forecast
        and  observed distributions. Does not give information on the
        correspondence between the forecasts and observations.

    Reference: "Statistical Methods in the Atmospheric Sciences",
                Daniel S Wilks, ACADEMIC PRESS(Page No: 33-34)

    Links: http://www.cawcr.gov.au/projects/verification/

    Written by:    Dileepkumar R,
                JRF, IIT Delhi

    Date: 29/02/2011
    """
    return
#####**********************************************#########

def accuracy_mc(obs, fcst, th, av, hy):
    ([[a, b, c, d], [e, f, g, h], [i, j, k, l], [m, n, o, p]])=\
    contingency_table_4x4(obs, fcst, th, av, hy)
    N=(a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p)
    """
    :func:`accuracy_mc`:Accuracy, the average correspondence between individual 
		forecasts and the events they predict. Scalar measures of accuracy
		are meant to summarize, in a single number, the overall quality of a set
		of forecasts. Can be mislead, since it is heavily influenced by the most
        common category, usually "no event" in the case of rare weather. This 
        is similar to accuracy in 2x2 contigency table.

    			Accuracy=(a+f+k+p)/N; a, f, k, p are values defined as 
				in 4x4 contigency tableN is the total number of forecasts

	Inputs:
		obs -the observed values has to be a list(or whatever you decide)
		fcst-the forecast values
		th -the threshold value for which the contingency table needs to
                be created (floating point value please!!)
		av-the data points between 'th' and 'av' we say that data
                point is moderate value
		hy-the data points above 'hy' we say that the data point
                is higher value

    Range: 0 to 1

    Perfect Score: 1

    Reference: "NCMRWF Report,  Monsoon-2009 Performance of T254L64 Global
                Assimilation-Forecast System"

    Links: http://www.cawcr.gov.au/projects/verification/

    Written by: Dileepkumar R,
                JRF, IIT Delhi

    Date: 29/02/2011
    """
    return (a+f+k+p)/N
#####**********************************************#########

def hss_mc(obs, fcst, th, av, hy):
    """
	:func:`hss_mc`: Heidke skill score (Cohen's k) ,the reference accuracy 
	measure in the Heidke score is the hit rate that would be achieved by
	random forecasts, subject to the constraint that the marginal distributions 
	of forecasts and observations characterizing the contingency table for the 
	random forecasts, P(Yi) and p(oj), are the same as the marginal distributions 
	in the actual verification data set. This is similar to HSS in 2x2 conti-
	gency table.

    HSS={[(a+f+k+p)/N]-(1/N*N)(sum of(N(Oi)*N(Fi))}/(1-(1/N*N)*(sum of(N(Oi)*N(Fi))

	a, f, k, p are values defined as in 4x4 contigency table

	N(Fi) denotes the total number of forecasts in category i, 
	N(Oj) denotes the total number of observations in category j, and N is the
	total number of forecasts. 				
	N(Fi) denotes the total number of forecasts in category i, 
	N(Oj) denotes the total number of observations in category j, 
	and N is the total number of forecasts. 

	Inputs:
		obs -the observed values has to be a list(or whatever you decide)
		fcst-the forecast values
		th -the threshold value for which the contingency table needs to
                be created (floating point value please!!)
		av-the data points between 'th' and 'av' we say that data
                point is moderate value
		hy-the data points above 'hy' we say that the data point
                is higher value


    Range: -infinity to 1, 0 indicates no skill.

    Perfect score: 1.

    Reference:[1] "Statistical Methods in the Atmospheric Sciences",
                    Daniel S Wilks, ACADEMIC PRESS(Page No: 248-249)

               [2]"NCMRWF Report,  Monsoon-2009 Performance of T254L64 Global
                                                Assimilation-Forecast System"

    Links: http://www.cawcr.gov.au/projects/verification/

    Written by:    Dileepkumar R,
                JRF, IIT Delhi

    Date: 29/02/2011
    """
    ([[a, b, c, d], [e, f, g, h], [i, j, k, l], [m, n, o, p]])=\
    contingency_table_4x4(obs, fcst, th, av, hy)
    N=(a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p)
    NF1=a+b+c+d
    NF2=e+f+g+h
    NF3=i+j+k+l
    NF4=m+n+o+p
    NO1=a+e+i+m
    NO2=b+f+j+n
    NO3=c+g+k+o
    NO4=d+h+l+p
    acr=(1/N)*(a+f+k+p)
    ss=(1/(N*N))*(NF1*NO1+NF2*NO2+NF3*NO3+NF4*NO4)

    HSS= (acr-ss)/(1-ss)

    return HSS
#####**********************************************#########

def kss_mc(obs, fcst, th, av, hy):
    """
	:func:`kss_mc`:	Hanssen and Kuipers discriminant(Kuipers Skill Score),
    the contribution made to the Kuipers score by a correct "no" or "yes" 
    forecast increases as the event is more or less likely, respectively.
    A drawback of this score is that it tends to converge to the POD for rare
    events,because the value of "d" becomes very large.

    HK= {[(a+f+k+p)/N]-(1/N*N)(sum of(N(Oi)*N(Fi))}/(1-(1/N*N)*(sum of(N(Oi)*N(Oi))

	a, f, k, p are values defined as in 4x4 contigency table

	N(Fi) denotes the total number of forecasts in category i, 
	N(Oj) denotes the total number of observations in category j, and N is the
	total number of forecasts. N(Fi) denotes the total number of forecasts in
	category i, 
	N(Oj) denotes the total number of observations in category j, and N is the 
	total number of forecasts. 

	Inputs:
		obs -the observed values has to be a list(or whatever you decide)
		fcst-the forecast values
		th -the threshold value for which the contingency table needs to
                be created (floating point value please!!)
		av-the data points between 'th' and 'av' we say that data
                point is moderate value
		hy-the data points above 'hy' we say that the data point
                is higher value


    Range:-1 to 1 , 0 indicate no skill.

    Perfect Score: 1

    Reference:[1] "Statistical Methods in the Atmospheric Sciences",
                    Daniel S Wilks, ACADEMIC PRESS(Page No: 249-250)
              [2]"NCMRWF Report,  Monsoon-2009 Performance of T254L64 Global
                            Assimilation-Forecast System"(Page No: 117-119)

    Links: http://www.cawcr.gov.au/projects/verification/

    Written by: Dileepkumar R,
                JRF, IIT Delhi

    Date: 29/02/2011
    """
    ([[a, b, c, d], [e, f, g, h], [i, j, k, l], [m, n, o, p]])=\
    contingency_table_4x4(obs, fcst, th, av, hy)
    N=(a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p)
    NF1=a+b+c+d
    NF2=e+f+g+h
    NF3=i+j+k+l
    NF4=m+n+o+p
    NO1=a+e+i+m
    NO2=b+f+j+n
    NO3=c+g+k+o
    NO4=d+h+l+p
    acr=(1/N)*(a+f+k+p)
    ss=(1/(N*N))*(NF1*NO1+NF2*NO2+NF3*NO3+NF4*NO4)
    so=(1/(N*N))*(NO1*NO1+NO2*NO2+NO3*NO3+NO4*NO4)
    kss= (acr-ss)/(1-so)
    return kss
#####**********************************************#########
