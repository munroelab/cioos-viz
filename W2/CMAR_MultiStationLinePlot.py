from bokeh.plotting import figure
from bokeh.models import LinearAxis, Range1d, DatetimeTickFormatter,  Legend
import pandas as pd
import numpy as np
from erddapy import ERDDAP
import panel as pn
from bokeh.palettes import Category10_10
pn.extension()

e = ERDDAP(server="https://dev.cioosatlantic.ca/erddap",
                 protocol="tabledap", )
e.auth = ("cioosatlantic", "4oceans")
e.response = "csv"
e.dataset_id = 'wpsu-7fer'
df = e.to_pandas()
df = df.dropna(axis=1, how='all')
df = df.sort_values(by=['time (UTC)'])
df['time (UTC)'] = pd.to_datetime(df['time (UTC)'], format="%Y-%m-%dT%H:%M:%SZ")
print("dataset loaded")

depthlist = list(sorted(df["depth (m)"].unique()))
depth_selector = pn.widgets.Select(name="Depth", options = depthlist)

def plot(depth):
    data = df[df["depth (m)"] == depth]
    fig = figure(title="Digby County", x_axis_type='datetime', output_backend="webgl",
                 plot_width=1000, plot_height=300)
    for (name, group), color in zip(data.groupby('waterbody_station'), Category10_10):
        fig.line(x=group['time (UTC)'], y=group['Temperature (degrees Celsius)'],
    legend_label=str(name), color=color)
    fig.xaxis.formatter = DatetimeTickFormatter(
        hours=["%H:%M:%S"],
        days=["%b %d"],
        months=["%d %B %Y"],
        years=["%d %B %Y"], )
    fig.yaxis.axis_label = "Temperature (°C)"
    fig.legend.location= 'top_left'
    fig.legend.click_policy='hide'
    fig.legend.visible=False
    legend=Legend(items=list(fig.legend[0].items), title = "Station",)
    fig.add_layout(legend, 'right')
    return fig

chartpane = pn.pane.Bokeh(plot(depth_selector.value))
#callback(s)
def update(target, event):
    target.object = plot(event.new)

depth_selector.link(chartpane, callbacks={"value":update})

widgets = pn.Row(chartpane, depth_selector)
widgets.show()