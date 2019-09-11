### Description 

#### Flow intervals calculation (flowcalc.py)

Interpolation types:
* 0 - Drop lines with no value
* 1 - Interpolate using linear
* 2 - Interpolate using time

Construct 2 or 4 types of categories depending on the number of pumps for a well:
* if p1_current == 0 and p2_current == 0 then category == 0
* if p1_current  > 0 and p2_current == 0 then category == 1
* if p1_current == 0 and p2_current  > 0 then category == 2
* if p1_current  > 0 and p2_current  > 0 then category == 3

Calculate flow:
* computed the volume for each data point (time point) as V = h x A, where h - station level and A - well area
* computed the flow on intervals using the category
* for a sequence of points wihin the same category that contains k intervals:
	* for each two sequantial point [t, t+1]  (an interval i) in the sequence I compute the flow[i] = 1000 x ( V[t+1] -V[t])/ (seconds (t+1, t) ) - formula taken from ACOWA code
	* compute the total flow for the sequence as Sum(flow(i))

Input:
* file with preflow calculations
* wale details file
* the type of interpolation

Run:
* python3.7 flowcalc2.py reference_csv/ST200_pre_flow_calculation.csv well_details.csv 2
* python3.7 flowcalc2.py reference_csv/ST004_pre_flow_calculation.csv well_details.csv 2

#### Moving Averages Calculation (ma.py)

Computes Moving Averages on the intervals

Methods used:

* Simple Moving Averages (SMA)
* Exponatial Moving Averages (EMA)

Input:
* Flow intervals data

The algorithm computes automatically the window size as 10% of the number of values for a category.

Run:
* python3.7 ma.py ResultsFlow/ST003_intervals.csv


#### Change Point Detection (cdp.py)

Algorithms for change point detection. 
* Binary Segmentation [1,2]
* Bottom-up segmentation [3,4]
* Window-based change point detection [5]

Input
* Simple Moving Averages applied on flow intervals.
* Exponantial Moving Averages applied on flow intervals.
* The flow intervals.
* The processed data

Need to set the number of points to detect.

Only works on intervals that either have pump p1 running or pump p2 running.

Run: 
* python3.7 cpd.py ResultsFlow/ST003_processed.csv 1
* python3.7 cpd.py ResultsMA/ST003_SMA.csv 1
* python3.7 cpd.py ResultsMA/ST003_EMA.csv 1
* python3.7 cpd.py ResultsFlow/ST003_intervals.csv 1

[1] J. Bai. Estimating multiple breaks one at a time. Econometric Theory, 13(3):315–352, 1997.
[2] P. Fryzlewicz. Wild binary segmentation for multiple change-point detection. The Annals of Statistics, 42(6):2243–2281, 2014. doi:10.1214/14-AOS1245.
[3] Piotr Fryzlewicz. Unbalanced Haar Technique for Nonparametric Function Estimation. Journal of the American Statistical Association, 102(480):1318–1327, 2007. doi:10.1198/016214507000000860.
[4] E. Keogh, S. Chu, D. Hart, and M. Pazzani. An online algorithm for segmenting time series. In Proceedings of the IEEE International Conference on Data Mining (ICDM), 289–296. 2001.
[5] D. Kifer, Shai Ben-David, and Johannes Gehrke. Detecting change in data streams. In VLDB, 2004

=== packages ===

* pandas
* matplotlib
* numpy
* ruptures 

