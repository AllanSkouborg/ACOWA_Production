# coding: utf-8

"""
 *
 * Copyright (C) 2018 Ciprian-Octavian Truică <ciprian.truica@cs.pub.ro>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
"""

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2019, Aarhus University"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.au.dk"
__status__ = "Production"

import pandas as pd
import matplotlib.pyplot as plt 
import sys
import os
import numpy as np
import ruptures as rpt

# Binary Segmenetation
# J. Bai. Estimating multiple breaks one at a time. Econometric Theory, 13(3):315–352, 1997.
# P. Fryzlewicz. Wild binary segmentation for multiple change-point detection. The Annals of Statistics, 42(6):2243–2281, 2014. doi:10.1214/14-AOS1245.
#
# Bottom-up segmentation
# Piotr Fryzlewicz. Unbalanced Haar Technique for Nonparametric Function Estimation. Journal of the American Statistical Association, 102(480):1318–1327, 2007. doi:10.1198/016214507000000860.
# E. Keogh, S. Chu, D. Hart, and M. Pazzani. An online algorithm for segmenting time series. In Proceedings of the IEEE International Conference on Data Mining (ICDM), 289–296. 2001.
# 

# RUN
# python3.7 cpd.py ResultsFlow/ST003_processed.csv 1
# python3.7 cpd.py ResultsMA/ST003_SMA.csv 1
# python3.7 cpd.py ResultsFlow/ST003_intervals.csv 1
 
if __name__ == "__main__":
    # data file
    fn = sys.argv[1]
    # number of breaking points to search for
    n_bkps = int(sys.argv[2])
    df = pd.read_csv(fn, sep=',')
    # need ResultsTrend 
    ofn = "./ResultsCPD/" + os.path.basename(fn).split(".")[0]

    no_cases = len(df['category_column'].unique())
    df[df.columns[0]] = df[df.columns[0]].apply(pd.to_numeric)
    df[df.columns[1]] = pd.to_datetime(df[df.columns[1]], format="%Y-%m-%d %H:%M:%S")
    df[df.columns[2]] = pd.to_datetime(df[df.columns[2]], format="%Y-%m-%d %H:%M:%S")
    df[df.columns[3:]] = df[df.columns[3:]].apply(pd.to_numeric)
  
    df = df.set_index(df[df.columns[0]])
    for category in df['category_column'].unique():
        if category == 1:
            X = df.loc[df['category_column'] == category]['p1_current'].values
            indexes = df.loc[df['category_column'] == category].index.values
            
            algo = rpt.BottomUp(model="l2")
            result = algo.fit_predict(X, n_bkps=n_bkps)
            x = []
            for idx in result[:-1]:
                x.append(indexes[idx])
            y = []
            for idx in x:
                y.append(df.loc[df.index == idx]['p1_current'].values[0]) 

            plt.plot(df.loc[df['category_column'] == category].index, df.loc[df['category_column'] == category]['p1_current'], label='normal')
            plt.scatter(x, y, label='outlier', color='red', marker='o')
            plt.title("Change Finder Bottom Up p1_current")
            plt.xlabel('Date Time')
            plt.ylabel('p1_current')
            plt.savefig( ofn + "_BottomUp_p1_current.png")
            plt.show()
            plt.close()

            algo = rpt.Window(model="l2")
            result = algo.fit_predict(X, n_bkps=n_bkps)
            x = []
            for idx in result[:-1]:
                x.append(indexes[idx])
            y = []
            for idx in x:
                y.append(df.loc[df.index == idx]['p1_current'].values[0]) 

            plt.plot(df.loc[df['category_column'] == category].index, df.loc[df['category_column'] == category]['p1_current'], label='normal')
            plt.scatter(x, y, label='outlier', color='red', marker='o')
            plt.title("Change Finder Window Segmentation p1_current")
            plt.xlabel('Date Time')
            plt.ylabel('p1_current')
            plt.savefig(ofn + "_Window_p1_current.png")
            plt.show()
            plt.close()

            algo = rpt.Binseg(model="l2")
            result = algo.fit_predict(X, n_bkps=n_bkps)
            x = []
            for idx in result[:-1]:
                x.append(indexes[idx])
            y = []
            for idx in x:
                y.append(df.loc[df.index == idx]['p1_current'].values[0]) 

            plt.plot(df.loc[df['category_column'] == category].index, df.loc[df['category_column'] == category]['p1_current'], label='normal')
            plt.scatter(x, y, label='outlier', color='red', marker='o')
            plt.title("Change Finder Binseg p1_current")
            plt.xlabel('Date Time')
            plt.ylabel('p1_current')
            plt.savefig(ofn + "_BinarySeg_p1_current.png")
            plt.show()
            plt.close()
            
        if category == 2:
            X = df.loc[df['category_column'] == category]['p2_current'].values
            indexes = df.loc[df['category_column'] == category].index.values
            

            algo = rpt.BottomUp(model="l2")
            result = algo.fit_predict(X, n_bkps=n_bkps)
            x = []
            for idx in result[:-1]:
                x.append(indexes[idx])
            y = []
            for idx in x:
                y.append(df.loc[df.index == idx]['p2_current'].values[0]) 

            plt.plot(df.loc[df['category_column'] == category].index, df.loc[df['category_column'] == category]['p2_current'], label='normal')
            plt.scatter(x, y, label='outlier', color='red', marker='o')
            plt.title("Change Finder Bottom Up p2_current")
            plt.xlabel('Date Time')
            plt.ylabel('p2_current')
            plt.savefig(ofn + "_BottomUp_p2_current.png")
            plt.show()
            plt.close()

            algo = rpt.Window(model="l2")
            result = algo.fit_predict(X, n_bkps=n_bkps)
            x = []
            for idx in result[:-1]:
                x.append(indexes[idx])
            y = []
            for idx in x:
                y.append(df.loc[df.index == idx]['p2_current'].values[0]) 

            plt.plot(df.loc[df['category_column'] == category].index, df.loc[df['category_column'] == category]['p2_current'], label='normal')
            plt.scatter(x, y, label='outlier', color='red', marker='o')
            plt.title("Change Finder Window p2_current")
            plt.xlabel('Date Time')
            plt.ylabel('p2_current')
            plt.savefig(ofn + "_Window_p2_current.png")
            plt.show()
            plt.close()
            
            algo = rpt.Binseg(model="l2")
            result = algo.fit_predict(X, n_bkps=n_bkps)
            x = []
            for idx in result[:-1]:
                x.append(indexes[idx])
            y = []
            for idx in x:
                y.append(df.loc[df.index == idx]['p2_current'].values[0]) 

            plt.plot(df.loc[df['category_column'] == category].index, df.loc[df['category_column'] == category]['p2_current'], label='normal')
            plt.scatter(x, y, label='outlier', color='red', marker='o')
            plt.title("Change Finder Binary Segmentation p2_current")
            plt.xlabel('Date Time')
            plt.ylabel('p2_current')
            plt.savefig(ofn + "_BinarySeg_p2_current.png")
            plt.show()
            plt.close()
