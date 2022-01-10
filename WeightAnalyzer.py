import csv
import dateutil.parser as dparser
import io
import pandas as pd
from pandas.core import groupby
import numpy as np
from pandas.core.algorithms import mode

TestSulyFilePath = "./weight/2022-01-10-suly.csv"



df = pd.read_csv(TestSulyFilePath, sep=',', parse_dates=[0], usecols=['time', 'weight'])
#df['time'] = pd.to_datetime(df['time'])
#[d for d in range(len(datum)) if datum[d]]
print(df.head())
print(df.groupby(pd.Grouper(key='time', axis=0, freq='D')).count().head())
print(df.dtypes)

LowestWeightForEachDate = df.loc[df.groupby(df.time.dt.date, as_index=False).weight.idxmin()]
print('LowestWeightForEachDate')
print(LowestWeightForEachDate['weight'].groupby(LowestWeightForEachDate.time.dt.date).count())

FirstWeightForEachDay = df.sort_values(by=['time']).drop_duplicates(keep='first')
FirstWeightForEachDay = FirstWeightForEachDay.loc[FirstWeightForEachDay.groupby(FirstWeightForEachDay.time.dt.date, as_index=False).time.idxmin()]
print('FirstWeightForEachDay')
print(FirstWeightForEachDay.groupby(pd.Grouper(key='time', axis=0, freq='D')).count().head())
print(FirstWeightForEachDay)
# print(FirstWeightForEachDay.loc[FirstWeightForEachDay.groupby(pd.Grouper(key='time', axis=0, freq='D')).idxmin()])

import matplotlib.pyplot as plt

# Initialise the subplot function using number of rows and columns
figure, axis = plt.subplots(2, 1)

axis[0].plot(FirstWeightForEachDay.time.dt.to_pydatetime(), FirstWeightForEachDay['weight'], label="First measurement of the day")
axis[0].scatter(FirstWeightForEachDay.time.dt.to_pydatetime(), FirstWeightForEachDay.weight, label=None)
axis[0].plot(LowestWeightForEachDate.time.dt.to_pydatetime(), LowestWeightForEachDate['weight'], label="lowest weight of the day")
axis[0].scatter(LowestWeightForEachDate.time.dt.to_pydatetime(), LowestWeightForEachDate.weight, label=None)
m, b = np.polyfit(df.index, df.weight, 1)
axis[0].plot(df.time.dt.to_pydatetime(), m*df.index+b, label="Fit Line to all data")
m, b = np.polyfit(LowestWeightForEachDate.index, LowestWeightForEachDate.weight, 1)
axis[0].plot(df.time.dt.to_pydatetime(), m*df.index+b, label="Fit Line to lowest weight of each day")
m, b = np.polyfit(FirstWeightForEachDay.index, FirstWeightForEachDay.weight, 1)
axis[0].plot(df.time.dt.to_pydatetime(), m*df.index+b, label="Fit Line to first measurement of each day")

axis[0].legend(loc='best')
axis[0].set_title("Morning weight and Daily Minimum Weight")
axis[0].set_xlabel("Date")
axis[0].set_ylabel("Weight (kg)")
# axis[0].xlabel("Date")
# axis[0].ylabel("Weight (kg)")
# axis[0].xticks(rotation='vertical')

bins = [82,83,84,85,86]
axis[1].hist(df.weight, bins=bins, edgecolor='k')
bins2 = [82.5,83,83.5,84,84.5,85,85.5,86]
axis[1].hist(df.weight, bins=bins2, edgecolor='k')
bins2 = [82.25,82.5,82.75,83,83.25,83.5,83.75,84,84.25,84.5,84.75,85,85.25,85.5,85.75,86]
axis[1].hist(df.weight, bins=bins2, edgecolor='k')
axis[1].set_title("Distribution of All Measurements")
axis[1].set_xlabel("Weight (kg)")
axis[1].set_ylabel("Number of Occurances")

plt.show()

