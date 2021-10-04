from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import LinearAxis, Range1d, DatetimeTickFormatter
import pandas as pd
import numpy as np

df = pd.read_csv("C:/Users/rinez/Downloads/wpsu-7fer_raw_merged.csv")
df = df.dropna(axis=1, how='all')
df = df.sort_values(by=['timestamp'])
#df = df.set_index(df.timestamp.astype(np.datetime64))
data = df[df.station == "Long Beach"]
data = data[data.depth == 5]
time = pd.to_datetime(data['timestamp'], format="%Y-%m-%dT%H:%M:%S.000")


# oxy = data.dropna(axis=0 ,how='any', subset=['Dissolved Oxygen'])
# temp = data.dropna(axis=0, how='any', subset = ['Temperature'])
p = figure(plot_width= 1000, plot_height=400, x_axis_type="datetime",
           title = "Long Beach - Digby County",)
p.xaxis.formatter=DatetimeTickFormatter(
        hours=["%H:%M:%S"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],)
p.yaxis.axis_label = "Dissolved Oxygen (% saturation)"
p.extra_y_ranges = {"foo":Range1d(start=data.Temperature.min(), end=data.Temperature.max()),
                    "who":Range1d(start=data['Dissolved Oxygen'].min(), end = data['Dissolved Oxygen'].max())}
p.add_layout(LinearAxis(y_range_name="foo", axis_label="Temperature (Celsius)"), "right")
p.line(time, data['Dissolved Oxygen'], line_width=2,
        legend_label='Dissolved Oxygen at 5m Depth', y_range_name="who")
p.line(time, data['Temperature'], line_width=2
       ,line_color="green", y_range_name="foo", legend_label="Temperature at 5m Depth")
p.legend.location= 'top_right'
p.legend.click_policy='hide'

show(p)


