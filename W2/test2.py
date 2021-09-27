from erddapy import ERDDAP
from bokeh.plotting import figure, output_file, show
import pandas as pd
import datetime as dt
from bokeh.models import DatetimeTickFormatter, ColumnDataSource
import matplotlib.pyplot as plt


e = ERDDAP(server="https://cioosatlantic.ca/erddap",
  protocol="tabledap",)

e.response = "csv"
e.dataset_id = "SMA_red_island_shoal"
e.constraints = {
    "time>=": "2021-08-11T00:00:00Z",
    "time<=": "2021-09-11T12:53:01Z",}
e.variables = [
    "time", "wind_spd_avg", "wind_spd_max", "wave_ht_max",
    "wave_ht_sig", "wave_period_max", "curr_spd_avg"]
df = e.to_pandas()

#time = pd.to_datetime(df['time (UTC)'], format="%Y-%m-%dT%H:%M:%SZ")
def TimeTrend(start, stop):
    timeFrame = df[df.columns[:1]]
    timeRange = timeFrame[start:stop]
    pd.to_datetime(timeRange['time (UTC)'], format="%Y-%m-%dT%H:%M:%SZ")
    x = timeRange.to_numpy(dtype='datetime64[m]')

    varFrame = df[df.columns[1:]]
    columns=list(varFrame)

    fig, ax = plt.subplots(figsize=(20, 10))

    for i in range(len(columns)):
        tag = varFrame[varFrame.columns[i:i + 1:1]]
        varRange = tag[start:stop]
        y = varRange.to_numpy(dtype=float)
        plt.subplot(len(columns), 1, i + 1)
        plt.plot(x, y, linewidth=0.5, linestyle='-', color='r', )
        plt.xlabel("")
        plt.ylabel(columns[i], rotation=0)
        plt.tick_params(labelrotation=45)
        if i < (len(columns) - 1):
            plt.xticks([])
            plt.grid(axis='x')
            i += 1
        else:
            plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9,
                                top=0.9, wspace=0.2, hspace=0.2)
            fig.suptitle("High Density Time Trend", fontsize=25)
            plt.yticks([])
            fig.text(0.5, 0.01, 'Time Range', fontsize=10)
            plt.show()
    return fig

TimeTrend(0,400)