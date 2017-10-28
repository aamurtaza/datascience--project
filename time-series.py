#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd 
import os
import plotly
import plotly.graph_objs as go

import statsmodels.api as sm
import matplotlib.pyplot as plt
from pylab import rcParams

# Path
base_path = os.path.dirname(os.path.abspath('__file__'))

# Loading files
hotels_data = pd.read_csv(base_path + "/datasets/Finland_Hotels_Reviews.csv")

# Preprocessed rating_dates
hotels_data = hotels_data[hotels_data['rating_date'].notnull()]
hotels_data = hotels_data[hotels_data['rating'].notnull()]
hotels_data['rating_date'] = pd.to_datetime(hotels_data['rating_date'])

# Set figure size
rcParams['figure.figsize'] = 11, 9

###----------------------- Time series analysis of city vice hotels --------------------------###

# Time series analysis for Cluster 5 (Randomly selected) => GLO Hotel Kluuvi Helsinki, Klaus K Hotel
helsinki = hotels_data[hotels_data['name'] == "GLO Hotel Kluuvi Helsinki"]
helsinki = helsinki.set_index(pd.DatetimeIndex(helsinki['rating_date']))
helsinki_rating = helsinki['rating']
decomposition = sm.tsa.seasonal_decompose(helsinki_rating, freq=30, model='additive')
fig = decomposition.plot()
plt.title('GLO Hotel Kluuvi Helsinki')
plt.show()
fig.savefig(base_path + '/timeseries/helsinki_trends.png')


# Time series analysis for Cluster 6 (Randomly selected) => Holiday Club Saariselka, Santa Claus Holiday Village
rovaniemi = hotels_data[hotels_data['name'] == "Santa Claus Holiday Village"]
rovaniemi = rovaniemi.set_index(pd.DatetimeIndex(rovaniemi['rating_date']))
rovaniemi_rating = rovaniemi['rating']
decomposition = sm.tsa.seasonal_decompose(rovaniemi_rating, freq=8, model='additive')
fig = decomposition.plot()
plt.title('Santa Claus Holiday Village')
plt.show()
fig.savefig(base_path + '/timeseries/rovaniemi_trends.png')


saariselka = hotels_data[hotels_data['name'] == "Holiday Club Saariselka"]
saariselka = saariselka.set_index(pd.DatetimeIndex(saariselka['rating_date']))
saariselka_rating = saariselka['rating']
decomposition = sm.tsa.seasonal_decompose(saariselka_rating, freq=8, model='additive')
fig = decomposition.plot()
#fig.suptitle('Holiday Club Saariselka')
plt.title('Holiday Club Saariselka')
plt.show()
fig.savefig(base_path + '/timeseries/saariselka_trends.png')


###---------------------- Time seris using plotly --------------------------------------------###

trace_rovaniemi = go.Scatter(
                x=rovaniemi['rating_date'],
                y=rovaniemi['rating'],
                name = "Santa Claus Holiday Village",
                line = dict(color = '#17BECF'),
                opacity = 0.8)

trace_helsinki = go.Scatter(
                x=helsinki['rating_date'],
                y=helsinki['rating'],
                name = "GLO Hotel Kluuvi Helsinki",
                line = dict(color = '#A8ACB8'),
                opacity = 0.8)

trace_saariselka = go.Scatter(
                x=saariselka['rating_date'],
                y=saariselka['rating'],
                name = "Holiday Club Saariselka",
                line = dict(color = '#FEC77E'),
                opacity = 0.8)

data = [trace_rovaniemi,trace_helsinki, trace_saariselka]


# Date Range (2017-03-01 - 2017-09-30)
layout = dict(
    title = "Ratings trends of Hotels (2017-03-01 - 2017-09-30)",
    xaxis = dict(
        range = ['2017-03-01','2017-09-30'])
)

fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename = "Ratings trends Hotels")


# Date Range (2016-08-01 - 2017-02-28)
layout = dict(
    title = "Ratings trends of Hotels (2016-08-01 - 2017-02-28)",
    xaxis = dict(
        range = ['2016-08-01','2017-02-28'])
)

fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename = "Ratings trends Hotels")


# Date Range (2016-01-01 - 2016-07-31)
layout = dict(
    title = "Ratings trends of Hotels (2016-01-01 - 2016-07-31)",
    xaxis = dict(
        range = ['2016-01-01','2016-07-31'])
)

fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename = "Ratings trends Hotels")
