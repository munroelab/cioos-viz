from bokeh.plotting import figure
from bokeh.io import show
#from bokeh.models import LinearAxis, Range1d, DatetimeTickFormatter,  Legend
import datetime as dt
import pandas as pd
import numpy as np
from erddapy import ERDDAP
import scipy.signal
import os
import matplotlib.pyplot as plt
#
# print("dataset loading")
# if os.path.exists("dataset.csv"):
#     df = pd.read_csv("dataset.csv")
# else:
e = ERDDAP(server="https://dev.cioosatlantic.ca/erddap",
                 protocol="tabledap", )
e.auth = ("cioosatlantic", "4oceans")
e.response = "csv"
e.dataset_id = 'wpsu-7fer'
df = e.to_pandas()
#df.to_csv("dataset.csv")


print("dataset loaded, filtering...")
df = df.dropna(axis=1, how='all')
df = df.sort_values(by=['time (UTC)'])
df['time (UTC)'] = pd.to_datetime(df['time (UTC)'], format="%Y-%m-%dT%H:%M:%SZ")
df = df.set_index(df['time (UTC)'].astype(np.datetime64))
data = df[df.waterbody_station == "St. Mary's Bay-Long Beach"]
data = data[data['depth (m)'] == 5]
data = data.loc['2020-8-1':'2020-8-31']
data = data[['time (UTC)','Temperature (degrees Celsius)','Dissolved_Oxygen (% saturation)']]
data['time (UTC)'] = (data["time (UTC)"]-dt.datetime(1970,1,1)).dt.total_seconds()
data['time (UTC)'] -= data['time (UTC)'].min()
data = data.rename(columns={'time (UTC)': "time (s)"})
inter_sample_time = data['time (s)'][1]-data["time (s)"][0]
sampling_frequency = 1/inter_sample_time
print("# of samples =", len(data))
print("sample time interval =", inter_sample_time, 's')
print("sampling frequency =", sampling_frequency, 'hz')
print("dataset filtered")

f, psd= scipy.signal.periodogram(data['Temperature (degrees Celsius)'], fs=sampling_frequency)
f = 1/f/3600

indexes = [1,2,3,4,5,6,7,8,9]
psd = np.delete(psd, indexes, axis=0)
f = np.delete(f, indexes, axis=0)

plt.plot(f,psd)
plt.xlabel("Period (hours)")
plt.ylabel("Power Spectral Density")
plt.show()


