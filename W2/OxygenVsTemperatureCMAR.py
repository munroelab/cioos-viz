from bokeh.plotting import figure
from bokeh.io import show
from bokeh.models import LinearAxis, Range1d, DatetimeTickFormatter
import datetime as dt
import pandas as pd
import numpy as np
from erddapy import ERDDAP
from scipy.optimize import curve_fit
import os
import matplotlib.pyplot as plt

print("dataset loading")
if os.path.exists("dataset.csv"):
    df = pd.read_csv("dataset.csv")
else:
    e = ERDDAP(server="https://dev.cioosatlantic.ca/erddap",
                 protocol="tabledap", )
    e.auth = ("cioosatlantic", "4oceans")
    e.response = "csv"
    e.dataset_id = 'wpsu-7fer'
    df = e.to_pandas()
    df.to_csv("dataset.csv")


print("dataset loaded, filtering...")
df = df.dropna(axis=1, how='all')
df = df.sort_values(by=['time (UTC)'])
df['time (UTC)'] = pd.to_datetime(df['time (UTC)'], format="%Y-%m-%dT%H:%M:%SZ")
df = df.set_index(df['time (UTC)'].astype(np.datetime64))
data = df[df.waterbody_station == "St. Mary's Bay-Long Beach"]
data = data[data['depth (m)'] == 5]
data = data.loc['2020-8-1':'2020-8-30']
data = data[['Temperature (degrees Celsius)','Dissolved_Oxygen (% saturation)']]
data = data.resample('D').mean()
temp = data['Temperature (degrees Celsius)'].values
oxygen = data['Dissolved_Oxygen (% saturation)'].values
print("dataset filtered")
p= figure( plot_width=600, plot_height=400, output_backend="webgl", tools="pan,wheel_zoom,box_zoom,reset,hover",
           x_axis_type = 'datetime')
p.xaxis.formatter = DatetimeTickFormatter(
        hours=["%H:%M"],
        days=["%a %b %d"],
        months=["%b %Y"],
        years=["%Y"], )
p.circle(temp, oxygen, size =5, color = 'blue')
p.xaxis.axis_label = 'Temperature (C)'
p.yaxis.axis_label = 'Oxygen Saturation (%)'

#p.circle(data.index, temp, size =5, color ='red')
show(p)
# def f(oxy,c0,c1,c2,c3):
#     return c0+c1*oxy-c2*np.exp(-c3*oxy)
#
# c, cov = curve_fit(f,temp, oxygen)
