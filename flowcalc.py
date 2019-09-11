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
import math
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def calculate_well_area(fn, station_id):
    """Calculates Station area
        
    Parameters
    ----------
    fn: str
        the filename with well data
    station_id : str
        the station_id to calculate area for

    Returns
    -------
    well_area
    returns value of -1 on errors
    """
    stations = {}
    with open(fn) as csvDataFile:
        csvReader = csv.reader(csvDataFile, delimiter=',')
        for i, row in enumerate(csvReader):
            if i > 0: # skip first row
                stations[row[0]] = row[1]

    well_area = -1
    try:
        well_diameter = int(stations[station_id])/1000.0
        well_area = 3.14*((well_diameter/2.0)**2)
    except ValueError:
        measurements = stations[station_id].split('x') 
        well_length = float(measurements[0])
        well_width = float(measurements[1])
        well_area = well_width * well_length
    except KeyError:
        print("Missing dimensions for well: {}".format(station_id))
    return well_area

# /opt/python-3.7.4/bin/python3.7 flowcalc2.py reference_csv/ST200_pre_flow_calculation_2.csv well_details.csv 2
# /opt/python-3.7.4/bin/python3.7 flowcalc2.py reference_csv/ST004_pre_flow_calculation_2.csv well_details.csv 2
if __name__ =="__main__":
    # file with the dataset
    # make sure that the separator is comma, ','
    fn = sys.argv[1]
    # file with the well area
    wfn = sys.argv[2]
    # how to handle missing data
    # 0 - remove rows with missing data
    # 1 - interpolate linear
    # 2 - interpolate using time slices
    hd = int(sys.argv[3])

    data = pd.read_csv(fn, sep=',')

    data[data.columns[0]] = pd.to_datetime(data[data.columns[0]], format="%Y-%m-%d %H:%M:%S")
    data[data.columns[1:]] = data[data.columns[1:]].apply(pd.to_numeric)
	
	# handle missing data    
    if hd == 0:
        # Drop lines with no value
        print('Drop lines with no value')
        data = data.dropna()
        # need to reindex after droping rows
        data = data.reset_index().drop(columns='index')
    elif hd == 1:
        print('Interpolate using linear')
        # Interpolate the data using linear method 
        # considers each value equally spaces
        for column in data.columns:
            data[column].interpolate(method='linear', inplace=True)
    elif hd == 2:
        print('Interpolate using time')
        # Interpolate the data using time method 
        # it take into account the difference in time
        # need a time index
        data = data.set_index(data.columns[0])
        for column in data.columns:
            data[column].interpolate(method='time', inplace=True)
        # reindex the data
        data = data.reset_index()
    print(data)
    print(data.shape)
    

    base = os.path.basename(fn)
    station = os.path.splitext(base)[0].split("_")[0]
    
    well_area = calculate_well_area(wfn, station) 

    no_categoties = -1
    columns = data.columns[1:]

    # Compute categoriee and encodings
    # if p1_current == 0 and p2_current == 0 then category == 0
    # if p1_current  > 0 and p2_current == 0 then category == 1
    # if p1_current == 0 and p2_current  > 0 then category == 2
    # if p1_current  > 0 and p2_current  > 0 then category == 3
    if len(data.columns) == 4:
        new_cols = ['idx', 'start_date', 'end_date', 'category_column', 'encode1', 'encode2', 'flow']
        for elem in data.columns[2:]:
            new_cols.append(elem)
        no_categoties = 4
        print("categories")
        print("if p1_current == 0 and p2_current == 0 then category == ", 0)
        print("if p1_current  > 0 and p2_current == 0 then category == ", 1)
        print("if p1_current == 0 and p2_current  > 0 then category == ", 2)
        print("if p1_current  > 0 and p2_current  > 0 then category == ", 3)
        data['category_column'] = 0
        data['encode1'] = 0
        data['encode2'] = 0
        data.loc[data['p1_current'] > 0, 'category_column'] = 1
        data.loc[data['p1_current'] > 0, 'encode1'] = 1
        data.loc[data['p2_current'] > 0, 'category_column'] = 2
        data.loc[data['p2_current'] > 0, 'encode2'] = 1
        # test = (df['p1_current'] > 0 & df['p2_current'] > 0)
        # df['category_column'][ test ] = 3
        data.loc[(data['p1_current'] > 0) & (data['p2_current'] > 0), 'category_column'] = 3
    elif len(data.columns) == 3:
        no_categoties = 2
        new_cols = ['idx', 'start_date', 'end_date', 'category_column', 'encode', 'flow']
        for elem in data.columns[2:]:
            new_cols.append(elem)
        print("categories")
        print("if p1_current == 0 then category == ", 0)
        print("if p1_current  > 0 then category == ", 1)
        data['category_column'] = 0
        data['encode'] = 0
        data.loc[data['p1_current'] > 0, 'category_column'] = 1
        data.loc[data['p1_current'] > 0, 'encode'] = 1
    # compute the volume
    data['volume'] = data['station_level'] * well_area
    print(data)
    # Save the preprocessed data 
    # need the folder ResultsFlow
    data.to_csv("./ResultsFlow/" + station + "_processed.csv")
    
    # start computing the flow 
    n = data.shape[0]
    s = 0
    points = []
    current_interval = []
    intervals = []
    results = []
    flow_total = 0
    idx2date = {}
    date2idx = {}
    idx = 0
    p1_current = []
    p2_current = []

    # compute flow for working intervals
    for i in range(0, n-1):
        if data.iloc[i]['category_column'] == data.iloc[i + 1]['category_column']:
            end_date = data.iloc[i+1][0]
            start_date = data.iloc[i][0]
            diff_sec = (end_date - start_date).seconds
            flow = 1000*abs(data.iloc[i + 1]['volume'] - data.iloc[i]['volume'])/diff_sec
            flow_total += flow
            # print(start_date, end_date, flow, flow_total)
            points.append([start_date, end_date, flow, flow_total])
            current_interval.append(data.iloc[i][0])
            if no_categoties == 2:
                p1_current.append(data.iloc[i]['p1_current'])
            elif no_categoties == 4:
                p1_current.append(data.iloc[i]['p1_current'])
                p2_current.append(data.iloc[i]['p2_current'])
        else:
            end_date = data.iloc[i+1][0]
            start_date = data.iloc[i][0]
            diff_sec = (end_date - start_date).seconds
            flow = 1000*abs(data.iloc[i + 1]['volume'] - data.iloc[i]['volume'])/diff_sec
            flow_total += flow
            # print(start_date, end_date, flow, flow_total)
            points.append([start_date, end_date, flow, flow_total])

            # the case the change happens only for one value
            # e.g. pumps work, not work and again work
            if len(current_interval) == 0:    
                current_interval.append(data.iloc[i][0]) 

            current_interval.append(data.iloc[i+1][0])
            if no_categoties == 2:
                p1_current.append(data.iloc[i]['p1_current'])
            elif no_categoties == 4:
                p1_current.append(data.iloc[i]['p1_current'])
                p2_current.append(data.iloc[i]['p2_current'])
            if len(current_interval) != 0:
                if len(current_interval) == 1:
                    print(current_interval)
                start_date = current_interval[0]
                end_date = current_interval[len(current_interval)-1]
                tmp = str(start_date) + " to " + str(end_date) + " category " + str(data.iloc[i]['category_column'])
                idx2date[idx] = tmp
                date2idx[tmp] = idx
                intervals.append([date2idx[tmp], flow_total])
                if no_categoties == 2:
                    line = [date2idx[tmp], start_date, end_date, data.iloc[i]['category_column'], data.iloc[i]['encode'], flow, sum(p1_current)/len(p1_current) ] 
                elif no_categoties == 4:
                    line = [date2idx[tmp], start_date, end_date, data.iloc[i]['category_column'], data.iloc[i]['encode1'], data.iloc[i]['encode2'], flow, sum(p1_current)/len(p1_current), sum(p2_current)/len(p2_current) ] 
                results.append(line)
                flow_total = 0
                current_interval = []
                p1_current = []
                p2_current = []
                idx += 1
            else:
                print("not ok")
        
    # create graphs
    dfIntervals = pd.DataFrame(intervals, columns = ['Interval', 'Flow_Value_Total'])
    dfIntervals.plot(x=dfIntervals.columns[0], y=dfIntervals.columns[1], marker='o')
    plt.savefig("./ResultsFlow/" + station + "_intervals.png")
    plt.show()
    plt.close()
        
    # sve results for intervals
    dfResults = pd.DataFrame(results, columns = new_cols)
    dfResults.to_csv("./ResultsFlow/" + station + "_intervals.csv", index=False)
