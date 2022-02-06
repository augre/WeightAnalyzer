import csv
import dateutil.parser as dparser
import io
from numpy.lib.function_base import average
import pandas as pd
from pandas.core import groupby
import numpy as np
from pandas.core.algorithms import mode

TestSulyFilePath = "./weight/2022-02-06-suly.csv"


# Read the time and weight colums from the csv file w/ pandas
df = pd.read_csv(TestSulyFilePath, sep=',', parse_dates=[0], usecols=['time', 'weight'])

# Print some info
print(df.head())
print(df.groupby(pd.Grouper(key='time', axis=0, freq='D')).count().head())
print(df.dtypes)

# Filter for the lowest weight on each day
LowestWeightForEachDate = df.loc[df.groupby(df.time.dt.date, as_index=False).weight.idxmin()]
# print('LowestWeightForEachDate')
# print(LowestWeightForEachDate['weight'].groupby(LowestWeightForEachDate.time.dt.date).count())

# Filter for the heighest weight each day
HeighestWeightEachDate = df.loc[df.groupby(df.time.dt.date, as_index=False).weight.idxmax()]

# Filter for average of each day
AverageOfEachDay = df.groupby(df.time.dt.date, as_index=False).weight.mean()

# Filter weekly average
WeeklyAverage = df.resample('W', on='time').weight.mean()
print(WeeklyAverage)

# Filter for weekly average of daily minimum
WeeklyAverageOfDailyMin = LowestWeightForEachDate.resample('W', on='time').weight.mean()

# Filter for the earliest measurement on each day
FirstWeightForEachDay = df.sort_values(by=['time']).drop_duplicates(keep='first')
FirstWeightForEachDay = FirstWeightForEachDay.loc[FirstWeightForEachDay.groupby(FirstWeightForEachDay.time.dt.date, as_index=False).time.idxmin()]
# print('FirstWeightForEachDay')
# print(FirstWeightForEachDay.groupby(pd.Grouper(key='time', axis=0, freq='D')).count().head())
# print(FirstWeightForEachDay)

# Plot the data
import matplotlib.pyplot as plt

# Initialise the subplot function using number of rows and columns
figure, axis = plt.subplots(2, 1)

# axis[0].plot(FirstWeightForEachDay.time.dt.to_pydatetime(), FirstWeightForEachDay['weight'], label="First measurement of the day")
# axis[0].scatter(FirstWeightForEachDay.time.dt.to_pydatetime(), FirstWeightForEachDay.weight, label=None)

# axis[0].plot(LowestWeightForEachDate.time.dt.to_pydatetime(), LowestWeightForEachDate['weight'], label="Lowest weight of the day")
# axis[0].scatter(LowestWeightForEachDate.time.dt.to_pydatetime(), LowestWeightForEachDate.weight, label=None)

# axis[0].plot(HeighestWeightEachDate.time.dt.to_pydatetime(), HeighestWeightEachDate['weight'], label="Heighest weight of the day")
# axis[0].scatter(HeighestWeightEachDate.time.dt.to_pydatetime(), HeighestWeightEachDate.weight, label=None)

# axis[0].plot(HeighestWeightEachDate.time.dt.to_pydatetime(), AverageOfEachDay, label="average")
# axis[0].scatter(HeighestWeightEachDate.time.dt.to_pydatetime(), AverageOfEachDay, label=None)

axis[0].plot(WeeklyAverage.index, WeeklyAverage, label="weekly average")
axis[0].plot(WeeklyAverageOfDailyMin.index, WeeklyAverageOfDailyMin, label="weekly average of the min of each day")


# Fit line on each dataset and plot them too
m, b = np.polyfit(df.index, df.weight, 1)
xAxis = np.linspace(df.index.min(), df.index.max(), len(df.index))
axis[0].plot(df.time.dt.to_pydatetime(), m*xAxis+b, label="Fit Line to all data")
m, b = np.polyfit(LowestWeightForEachDate.index, LowestWeightForEachDate.weight, 1)
axis[0].plot(df.time.dt.to_pydatetime(), m*xAxis+b, label="Fit Line to lowest weight of each day")
m, b = np.polyfit(FirstWeightForEachDay.index, FirstWeightForEachDay.weight, 1)
axis[0].plot(df.time.dt.to_pydatetime(), m*xAxis+b, label="Fit Line to first measurement of each day")
m, b = np.polyfit(HeighestWeightEachDate.index, HeighestWeightEachDate.weight, 1)
axis[0].plot(df.time.dt.to_pydatetime(), m*xAxis+b, label="Fit Line to heighest weight of each day")
m, b = np.polyfit(HeighestWeightEachDate.index, AverageOfEachDay, 1)
axis[0].plot(df.time.dt.to_pydatetime(), m*xAxis+b, label="Fit Line to average weight of each day")

axis[0].legend(loc='best')
axis[0].set_title("Morning weight and Daily Minimum Weight")
axis[0].set_xlabel("Date")
axis[0].set_ylabel("Weight (kg)")

#Create the histogram
bins = np.arange(df.weight.min(), df.weight.max(), 1)
axis[1].hist(df.weight, bins=bins, edgecolor='k')
bins = np.arange(df.weight.min(), df.weight.max(), 0.5)
axis[1].hist(df.weight, bins=bins, edgecolor='k')
bins = np.arange(df.weight.min(), df.weight.max(), 0.1)
axis[1].hist(df.weight, bins=bins, edgecolor='k')

axis[1].set_title("Distribution of All Measurements")
axis[1].set_xlabel("Weight (kg)")
axis[1].set_ylabel("Number of Occurances")

plt.show()

