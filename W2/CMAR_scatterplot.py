from bokeh.io import show
from bokeh.plotting import figure
from bokeh.models import LinearAxis, Range1d, DatetimeTickFormatter, Legend
from bokeh.models.tickers import MonthsTicker, DaysTicker, DatetimeTicker
import pandas as pd
import numpy as np
from bokeh.transform import factor_cmap
from bokeh.palettes import Viridis5

df = pd.read_csv("C:/Users/rinez/Downloads/wpsu-7fer_raw_merged.csv")
df = df.dropna(axis=1, how='all')
df = df.sort_values(by=['timestamp'])

data = df[df.station == "Long Island"]
data['timestamp']= pd.to_datetime(data['timestamp'], format="%Y-%m-%dT%H:%M:%S.000")
data.depth= data.depth.astype(str) + ' m'
p = figure(plot_width= 1000, plot_height=400, x_axis_type="datetime",
           title="Long Island - Digby County", output_backend="webgl")

p.xaxis.formatter=DatetimeTickFormatter(
        hours=["%H:%M"],
        days=["%a %b %d"],
        months=["%b %Y"],
        years=["%Y"],)
# p.xaxis.ticker = MonthsTicker(list(range(0,12,3)))
p.yaxis.axis_label = "Temperature (°C)"

p.scatter('timestamp', 'Temperature', source=data, legend_group='depth',
fill_alpha=0.4, size=1, color = factor_cmap('depth', palette=Viridis5,
factors=sorted(data.depth.unique(), reverse=True),end=1), )
p.legend.visible=False
legend=Legend(items=list(p.legend[0].items), title = "Depth(m)",)
p.add_layout(legend, 'right')
show(p)