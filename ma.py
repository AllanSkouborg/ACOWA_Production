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

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

# Compute Exponential Moving Averages (EMA)
def ExponentialMovingAverages(df, span=200, adjust=False):
    ema = df.ewm(span=span, adjust=adjust).mean()
    return ema

# Compute Simple Moving Averages (SMA)
def SimpleMovingAverages(df, ws=200):
    sma = df.rolling(window=ws).mean()
    return sma



# Creates CSV on interval data using Moving Averages
# /opt/python-3.7.4/bin/python3.7 adf.py ResultsFlow/ST004_intervals.csv
if __name__ == "__main__":
    fn = sys.argv[1]
    # sep = sys.argv[2]
    df = pd.read_csv(fn, sep=',')

    # outputs the results in folder ResultsMA
    ofn = "./ResultsMA/" + os.path.basename(fn).split("_")[0]

    no_cases = len(df['category_column'].unique())
    df[df.columns[0]] = df[df.columns[0]].apply(pd.to_numeric)
    df[df.columns[1]] = pd.to_datetime(df[df.columns[1]], format="%Y-%m-%d %H:%M:%S")
    df[df.columns[2]] = pd.to_datetime(df[df.columns[2]], format="%Y-%m-%d %H:%M:%S")
    df[df.columns[3:]] = df[df.columns[3:]].apply(pd.to_numeric)
    
    l_idx = []
    for column in df.columns[0:3]:
        l_idx.append(column)
    df = df.set_index(l_idx)
    l_sma = []
    l_ema = []
    for category in df['category_column'].unique():
        print("====================================")
        print("==========Category " + str(category) + "=================")
        print("====================================")
    
    
        dfma = pd.DataFrame(df.loc[df['category_column'] == category], columns = df.columns)
        n_row, n_col =  dfma.shape
        ws = int(n_row * 0.1)
        print(n_row, n_col)
        sma = SimpleMovingAverages(dfma, ws=ws)
        l_sma.append(sma)
        ema = ExponentialMovingAverages(dfma, span=ws)
        l_ema.append(ema)

    sma_result = pd.concat(l_sma, sort=True)
    sma_result.sort_index(inplace=True)
    sma_result = sma_result.dropna()

    ema_result = pd.concat(l_ema, sort=True)
    ema_result.sort_index(inplace=True)
    ema_result = ema_result.dropna()  

    for category in df['category_column'].unique():
        if category == 1:
            column = 'p1_current'
            plt.plot(df.loc[df['category_column'] == category].index.get_level_values(0), df.loc[df['category_column'] == category][column], label=column)
            plt.plot(sma_result.loc[sma_result['category_column'] == category].index.get_level_values(0), sma_result.loc[sma_result['category_column'] == category][column], label='SMA ' + column)
            plt.plot(ema_result.loc[ema_result['category_column'] == category].index.get_level_values(0), ema_result.loc[ema_result['category_column'] == category][column], label='EMA ' + column)
            plt.title("MA p1_current")
            plt.xlabel('Date Time')
            plt.ylabel('p1_current')
            plt.legend()
            plt.savefig(ofn + "_" + column + "_ma.png")
            plt.show()
            plt.close()
        if category == 2:
            column = 'p2_current'
            plt.plot(df.loc[df['category_column'] == category].index.get_level_values(0), df.loc[df['category_column'] == category][column], label=column)
            plt.plot(sma_result.loc[sma_result['category_column'] == category].index.get_level_values(0), sma_result.loc[sma_result['category_column'] == category][column], label='SMA ' + column)
            plt.plot(ema_result.loc[ema_result['category_column'] == category].index.get_level_values(0), ema_result.loc[ema_result['category_column'] == category][column], label='EMA ' + column)
            plt.title("MA p2_current")
            plt.xlabel('Date Time')
            plt.ylabel('p2_current')
            plt.legend()
            plt.savefig(ofn + "_" + column + "_ma.png")
            plt.show()
            plt.close()



    sma_result.to_csv(ofn + "_SMA.csv")
    ema_result.to_csv(ofn + "_EMA.csv")