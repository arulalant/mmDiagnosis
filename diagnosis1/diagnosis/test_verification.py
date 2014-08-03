'''
This program we can use for testing our codes for statistical score and other
evaluation values like MSE, RMSE...etc are correct or not according to our
sample data and its crresponding scores.
'''
import numpy
obs= numpy.loadtxt("test_data_obvs.txt", dtype= float, comments= '#',
                    delimiter= None, skiprows=0, usecols= None, unpack= False)
fcst = numpy.loadtxt("test_data_fcst.txt", dtype= float, comments= '#',
                    delimiter= None, skiprows=0, usecols= None, unpack= False)
PASS=1
FAIL=0
th=0.5
av=3.
hy=12.5
###********************TESTING 2X2 CONTIGENCY FUNCTION********************###

def test_contingency_table_2x2(obs, fcst, th):
    from ctgfunction import contingency_table_2x2
    PASS= 1
    FAIL= 0
    [a, b, c, d] = contingency_table_2x2(obs, fcst, th)

    if (a==36 and b==1 and c==3 and d==5):
        return PASS
    else:
        return FAIL

print "Test for 2x2 Contigency Table-", test_contingency_table_2x2(obs, fcst,\
                                                                          th)
###********************TESTING ACCURACY(HIT RATE)********************###

def test_accuracy(obs, fcst, th):
    from ctgfunction import accuracy
    import numpy as np
    PASS=1
    FAIL=0
    acry= accuracy(obs, fcst, th)
    acr= np.round(acry, 4)

    if (acr==0.9111):
        return PASS
    else:
        return FAIL
print "Test for Accuracy(Hit Rate)-", test_accuracy(obs, fcst, th)
###********************TESTING BIAS********************###

def test_bias_score(obs, fcst, th):
    from ctgfunction import bias_score
    import numpy as np
    bias= bias_score(obs, fcst, th)
    bias=np.round(bias, 4)
    PASS=1
    FAIL=0
    if (bias==0.9487):
        return PASS
    else:
        return FAIL

print "Test for Bias Score-", test_bias_score(obs, fcst, th)
###********************TESTING PROBABILITY OF DETECTION*******************###

def test_pod(obs, fcst, th):
    from ctgfunction import pod
    import numpy as np
    pod= pod(obs, fcst, th)
    pod=np.round(pod, 4)
    PASS=1
    FAIL=0

    if (pod==0.9231):
        return PASS
    else:
        return FAIL

print "Test for POD-", test_pod(obs, fcst, th)
###********************TESTING FALSE ALARM RATIO********************###

def test_far(obs, fcst, th):
    from ctgfunction import far
    import numpy as np
    far=far(obs, fcst, th)
    far=np.round(far, 4)
    PASS=1
    FAIL=0

    if (far==0.027):
        return PASS
    else:
        return FAIL

print "Test for FAR-", test_far(obs, fcst, th)
###*****************TESTING PROBABILITY OF FALSE DETECTION*****************###

def test_pofd(obs, fcst, th):
    from ctgfunction import pofd
    import numpy as np
    pofd= pofd(obs, fcst, th)
    pofd=np.round(pofd, 4)
    PASS=1
    FAIL=0
    if (pofd==0.1667):
        return PASS
    else:
        return FAIL


print "Test for PODF-", test_pofd(obs, fcst, th)
###********************TESTING THREAT SCORE********************###

def test_ts(obs, fcst, th):
    from ctgfunction import ts
    import numpy as np
    ts= ts(obs, fcst, th)
    ts=np.round(ts, 4)
    PASS=1
    FAIL=0
    if (ts==0.9000):
        return PASS
    else:
        return FAIL
print "Test for TS-", test_ts(obs, fcst, th)
###********************TESTING EQUITABLE THREAT SCORE********************###

def test_ets(obs, fcst, th):
    from ctgfunction import ets
    import numpy as np
    ets= ets(obs, fcst, th)
    ets=np.round(ets, 4)
    PASS=1
    FAIL=0
    if (ets==0.4958):
        return PASS
    else:
        return FAIL
print "Test for ETS-", test_ets(obs, fcst, th)
###*****TESTING HANSSEN  AND KUIPERS DISCRIMINANT(KUIPERS SKILL SCORE)****###

def test_kss(obs, fcst, th):
    from ctgfunction import kss
    import numpy as np
    kss=kss(obs, fcst, th)
    kss= np.round(kss, 4)
    PASS=1
    FAIL=0

    if (kss==0.7564):
        return PASS
    else:
        return FAIL
print "Test for KSS-", test_kss(obs, fcst, th)
###********************TESTING HEIDKE SKILL SCORE********************###

def test_hss(obs, fcst, th):
    from ctgfunction import hss
    import numpy as np
    hss=hss(obs, fcst, th)
    hss= np.round(hss, 4)
    PASS=1
    FAIL=0


    if (hss==0.6629):
        return PASS
    else:
        return FAIL

print "Test for HSS-", test_hss(obs, fcst, th)
###********************TESTING ODDS RATIO********************###

def test_odr(obs, fcst, th):
    from ctgfunction import odr
    import numpy as np
    odr=odr(obs, fcst, th)
    odr=np.round(odr, 4)
    PASS=1
    FAIL=0
    if (odr==60.0):
        return PASS
    else:
        return FAIL

print "Test for ODR-", test_odr(obs, fcst, th)
###********************TESTING ODDS RATIO SKILL SCORE********************###

def test_orss(obs, fcst, th):
    from ctgfunction import orss
    import numpy as np
    orss= orss(obs, fcst, th)
    orss=np.round(orss, 4)
    PASS=1
    FAIL=0

    if (orss==60.0):
        return PASS
    else:
        return FAIL

print "Test for ORSS-", test_odr(obs, fcst, th)
###********************TESTING LOG ODDS RATIO********************###

def test_logodr(obs, fcst, th):
    from ctgfunction import logodr
    import numpy as np
    logodr=logodr(obs, fcst, th)
    logodr=np.round(logodr, 4)
    PASS=1
    FAIL=0

    if (logodr==4.0943):
        return PASS
    else:
        return FAIL
print "Test for LOG ODR-", test_logodr(obs, fcst, th)
###********************TESTING EXTREME DEPENDENCY SCORE********************###

def test_eds(obs, fcst, th):
    from ctgfunction import eds
    import numpy as np
    eds=eds(obs, fcst, th)
    eds = np.round(eds, 4)
    PASS=1
    FAIL=0
    if (eds==0.2826):
        return PASS
    else:
        return FAIL


print "Test for EDS-", test_eds(obs, fcst, th)
#######****************************************************************#######
###********************TESTING 4x4 CONTIGENCY FUNCTION********************###
#######****************************************************************#######

def test_contingency_table_4x4(obs, fcst, th, av, hy):
    from fxfcgcy_table import contingency_table_4x4
    ([[a, b, c, d], [e, f, g, h], [i, j, k, l], [m, n, o, p]])=\
                                contingency_table_4x4(obs, fcst, th, av, hy)
    if (a==5 and b==3 and c==0 and d==0 and e==1 and f==25 and g==5 and h==1
    and i==0 and j==0 and k==4 and l==0 and m==0 and n==0 and o==0 and p==1):
        return PASS
    else:
        return FAIL
print "Test for 4x4 Contigency Table-", test_contingency_table_4x4(obs, fcst,
                                                                   th, av, hy)
###********************TESTING ACCURACY(HIT RATE)************************###

def test_accuracy_4x4(obs, fcst, th, av, hy):
    from fxfcgcy_table import contingency_table_4x4
    from fxfcgcy_table import accuracy_mc
    import numpy as np
    ([[a, b, c, d], [e, f, g, h], [i, j, k, l], [m, n, o, p]])=\
                                contingency_table_4x4(obs, fcst, th, av, hy)
    acry= accuracy_mc(obs, fcst, th, av, hy)
    acr= np.round(acry, 4)
    if (acr==0.7778):
        return PASS
    else:
        return FAIL
print "Test for Accuracy of 4x4 Contigency Table-", test_accuracy_4x4(obs,
                                                             fcst, th, av, hy)
###*********************TESTING HEIDKE SKILL SCORE*********************###

def test_hss_mc(obs, fcst, th, av, hy):
    from fxfcgcy_table import contingency_table_4x4
    from fxfcgcy_table import hss_mc
    import numpy as np
    ([[a, b, c, d], [e, f, g, h], [i, j, k, l], [m, n, o, p]])=\
                                  contingency_table_4x4(obs, fcst, th, av, hy)
    hss=hss_mc(obs, fcst, th, av, hy)
    hss=np.round(hss, 4)
    if (hss==0.5686):
        return PASS
    else:
        return FAIL
print "Test for HSS of 4x4 Contigency Table-", test_hss_mc(obs, fcst, th,
                                                                      av, hy)
###****TESTING HANSSEN  AND KUIPERS DISCRIMINANT(KUIPERS SKILL SCORE)****###

def test_kss_mc(obs, fcst, th, av, hy):
    from fxfcgcy_table import contingency_table_4x4
    from fxfcgcy_table import kss_mc
    import numpy as np
    ([[a, b, c, d], [e, f, g, h], [i, j, k, l], [m, n, o, p]])=\
                                contingency_table_4x4(obs, fcst, th, av, hy)
    kss=kss_mc(obs, fcst, th, av, hy)
    kss= np.round(kss, 4)
    if (kss==0.5295):
        return PASS
    else:
        return FAIL
print "Test for KSS of 4x4 Contigency Table-", test_kss_mc(obs, fcst, th,
                                                                      av, hy)
###*******************************************************************###
###*******METHODS FOR FORCAST OF CONTINUES RANDOM VARIABLES***********###
###*******************************************************************###

###*************************TESTING MEAN ERROR************************###

def test_me(obs, fcst):
    from methods_for_foreasts_of_continuous_variables import me
    import numpy as np
    mean_err=me(obs, fcst)

    mean_err=np.round(mean_err, 4)

    if (mean_err==0.9182):
        return PASS
    else:
        return FAIL
print "Test for Mean Error-", test_me(obs, fcst)
###*********************TESTING (MULTIPLICATIVE)BIAS*********************###

def test_mbias(obs, fcst):
    from methods_for_foreasts_of_continuous_variables import mbias
    import numpy as np
    m_bias=mbias(obs, fcst)
    m_bias=np.round(m_bias, 4)
    if (m_bias==0.6451):
        return PASS
    else:
        return FAIL

print "Test for (Multiplicative)Bias-", test_mbias(obs, fcst)
###*********************TESTING MEAN ABSOLUTE ERROR*********************###

def test_mae(obs, fcst):
    from methods_for_foreasts_of_continuous_variables import mae
    import numpy as np
    mean_abs_err=mae(obs, fcst)
    mean_abs_err=np.round(mean_abs_err, 4)
    if (mean_abs_err==1.0862):
        return PASS
    else:
        return FAIL
print "Test for Mean Absolute Error(MAE)-", test_mae(obs, fcst)
###********************TESTING ROOT MEAN SQURED ERROR********************###

def test_rmse(obs, fcst):
    from methods_for_foreasts_of_continuous_variables import rmse
    import numpy as np
    r_mse=rmse(obs, fcst)
    r_mse=np.round(r_mse, 4)
    if (r_mse==2.7926):
        return PASS
    else:
        return FAIL
print "Test for Root Mean Squred Error(RMSE)-", test_rmse(obs, fcst)
###*********************TESTING MEAN SQURED ERROR*********************###

def test_mse(obs, fcst):
    from methods_for_foreasts_of_continuous_variables import mse
    import numpy as np
    mserr=mse(obs, fcst)
    mserr=np.round(mserr, 4)
    if (mserr==7.7987):
        return PASS
    else:
        return FAIL
print "Test for Mean Squred Error(MSE)-", test_mse(obs, fcst)
###*****************************************************************####

def test_rmsf(obs, fcst):
    pass
    from methods_for_foreasts_of_continuous_variables import rmsf
    import numpy as np
    rms_f=rmsf(obs, fcst)
    rms_f=np.round(rms_f, 4)
    if (rms_f=='xxxxxx'):
        return PASS
    else:
        return FAIL
