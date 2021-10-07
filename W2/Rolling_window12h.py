from bokeh.plotting import figure
from bokeh.io import show
from bokeh.models import LinearAxis, Range1d, DatetimeTickFormatter
import datetime as dt
import pandas as pd
import numpy as np
from erddapy import ERDDAP
import scipy.signal
import os
#import matplotlib.pyplot as plt

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
data = data.resample('0.5D').mean()
#mindata = data.resample('0.5D').min()
print("dataset filtered and resampled")
p= figure( plot_width=600, plot_height=400, output_backend="webgl")
p.xaxis.formatter=DatetimeTickFormatter(
        hours=["%H:%M"],
        days=["%a %b %d"],
        months=["%b %Y"],
        years=["%Y"],)
p.yaxis.axis_label = "Temperature Peaks per 12 hours (°C)"
p.circle(data.index, data['Temperature (degrees Celsius)'], size=5, color='red')
p.circle(data.index, data['Dissolved_Oxygen (% saturation)'], size = 5, color='blue')
show(p)
print("dataset resampled")