from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import LinearAxis, Range1d, DatetimeTickFormatter
import pandas as pd
import numpy as np
from erddapy import ERDDAP

e = ERDDAP(server="https://dev.cioosatlantic.ca/erddap",
                 protocol="tabledap", )
e.auth = ("cioosatlantic", "4oceans")
e.response = "csv"
e.dataset_id = 'wpsu-7fer'
df = e.to_pandas()
df = df.dropna(axis=1, how='all')
df = df.sort_values(by=['time (UTC)'])
data = df[df.waterbody_station == "St. Mary's Bay-Long Beach"]
data = data[data['depth (m)'] == 5]
time = pd.to_datetime(data['time (UTC)'], format="%Y-%m-%dT%H:%M:%SZ")

p = figure(plot_width= 1000, plot_height=400, x_axis_type="datetime",
           title = "Long Beach - Digby County",)
p.xaxis.formatter=DatetimeTickFormatter(
        hours=["%H:%M:%S"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],)
p.yaxis.axis_label = "Dissolved Oxygen (% saturation)"
p.extra_y_ranges = {"foo":Range1d(start=data['Temperature (degrees Celsius)'].min(),
                                  end=data['Temperature (degrees Celsius)'].max()),
                    "who":Range1d(start=data['Dissolved_Oxygen (% saturation)'].min(),
                                  end = data['Dissolved_Oxygen (% saturation)'].max())}
p.add_layout(LinearAxis(y_range_name="foo", axis_label="Temperature (°C)"), "right")
p.line(time, data['Dissolved_Oxygen (% saturation)'], line_width=2,
        legend_label='Dissolved Oxygen at 5m Depth', y_range_name="who")
p.line(time, data['Temperature (degrees Celsius)'], line_width=2
       ,line_color="green", y_range_name="foo", legend_label="Temperature at 5m Depth")
p.legend.location= 'top_right'
p.legend.click_policy='hide'

show(p)


