# WeightAnalyzer

 

 

This code is usable to analyze weight measurement data. As of now it is compatible with the Xiaomi Smart Sccale csv format.

It uses pandas to read the csv and filter it. The current filters are

- First measuremnt for each day.
- Lowest weight for each day
- Heighest wight for each day
- Weekly average
- Weekly average of lowest weight

 

It plots the each weight data and fits a line to each filtered datast.

It also plots a weight distribution histogram of all the data, which shows which weight interval is measured how often.

 ![Figure_1](https://user-images.githubusercontent.com/2387022/152677052-50920a7d-e1d7-46b2-962f-d8c41d0e3487.png)


