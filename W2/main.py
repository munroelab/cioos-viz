from erddapy import ERDDAP
from bokeh.plotting import figure, output_file, show
import pandas as pd
import datetime as dt
from bokeh.models import DatetimeTickFormatter

e = ERDDAP(
  server="https://cioosatlantic.ca/erddap",
  protocol="tabledap",
)

e.response = "csv"
e.dataset_id = "SMA_red_island_shoal"
e.constraints = {
    "time>=": "2021-08-11T00:00:00Z",
    "time<=": "2021-09-11T12:00:00Z",
    "latitude>=": 47.24438,
    "latitude<=": 47.39998333,
    "longitude>=": -54.36902167,
    "longitude<=": -53.91570333,
}
e.variables = [
    "time", "wind_spd_avg", "surface_temp_avg"
]

df = e.to_pandas()
print(df)
time = pd.to_datetime(df['time (UTC)'], format="%Y-%m-%dT%H:%M:%SZ")
print(time)
wind_spd_avg = df['wind_spd_avg (m s-1)']

output_file("index.html")

p = figure(
    title='Average Wind Speed SMA_red_island_shoal',
    x_axis_type="datetime",
    x_axis_label = 'Time',
    y_axis_label = 'Average Wind Speed (ms^-1)'
)
p.xaxis.formatter=DatetimeTickFormatter(
        hours=["%H:%M:%S"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
p.xaxis.major_label_orientation = 45
p.line(time, wind_spd_avg, line_width=2)

show(p)