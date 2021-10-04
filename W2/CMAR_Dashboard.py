from bokeh.io import show
from bokeh.plotting import figure
from bokeh.models import LinearAxis, Range1d, DatetimeTickFormatter, Legend
from bokeh.models.tickers import MonthsTicker, DaysTicker, DatetimeTicker
import pandas as pd
import numpy as np
from bokeh.transform import factor_cmap
from bokeh.palettes import Viridis6
import panel as pn
from erddapy import ERDDAP
pn.extension()


e = ERDDAP(server="https://dev.cioosatlantic.ca/erddap",
                 protocol="tabledap", )
e.auth = ("cioosatlantic", "4oceans")
e.response = "csv"
e.dataset_id = 'wpsu-7fer'
df = e.to_pandas()
df = df.dropna(axis=1, how='all')
df = df.sort_values(by=['time (UTC)'])

stationlist = list(sorted(df["waterbody_station"].unique()))
station_selector = pn.widgets.Select(name="Station", options=stationlist, value = stationlist[0])

def tempScatterPlot(station):

    data = df[df.waterbody_station == station]
    data['time (UTC)'] = pd.to_datetime(data['time (UTC)'],
                                       format="%Y-%m-%dT%H:%M:%SZ")
    data['depth (m)'] = data['depth (m)'].astype(str)
    p = figure(plot_width=600, plot_height=300, x_axis_type="datetime",
               title=station ,)

    p.xaxis.formatter = DatetimeTickFormatter(
        hours=["%H:%M"],
        days=["%a %b %d"],
        months=["%b %Y"],
        years=["%Y"], )
    p.yaxis.axis_label = "Temperature (°C)"

    p.scatter('time (UTC)', 'Temperature (degrees Celsius)', source=data, legend_group='depth (m)',
                fill_alpha=0.4, size=1, color=factor_cmap('depth (m)', palette=Viridis6,
                factors=sorted(list(data['depth (m)'].unique())), end=1), )
    p.legend.visible = False
    legend = Legend(items=list(p.legend.items), title="Depth(m)", )
    p.add_layout(legend, 'right')
    return p

def oxygenPlot(station):
    data = df[df.waterbody_station == station]
    data['time (UTC)'] = pd.to_datetime(data['time (UTC)'],
                                        format="%Y-%m-%dT%H:%M:%SZ")
    data['depth (m)'] = data['depth (m)'].astype(str)
    p2 = figure(plot_width=600, plot_height=300, x_axis_type="datetime",
               title=station, )

    p2.xaxis.formatter = DatetimeTickFormatter(
        hours=["%H:%M"],
        days=["%a %b %d"],
        months=["%b %Y"],
        years=["%Y"], )
    p2.yaxis.axis_label = "Dissolved Oxygen (% Saturation)"

    p2.scatter('time (UTC)', 'Dissolved_Oxygen (% saturation)', source=data, legend_group='depth (m)',
              fill_alpha=0.4, size=1, color=factor_cmap('depth (m)', palette=Viridis6,
              factors=sorted(list(data['depth (m)'].unique())), end=1), )
    p2.legend.visible = False

    return p2



temppane = pn.pane.Bokeh(tempScatterPlot(station_selector.value))
oxypane = pn.pane.Bokeh(oxygenPlot(station_selector.value))

def tempstation(target, event):
    target.object = tempScatterPlot(event.new)
def oxystation(target, event):
    target.object = oxygenPlot(event.new)

station_selector.link(temppane, callbacks={"value":tempstation})
station_selector.link(oxypane, callbacks={"value":oxystation})

widgets = pn.Column(pn.Spacer(height=0), station_selector, width=400)
charts = pn.Column(temppane, pn.Spacer(height=0), oxypane, pn.Spacer(height=0))
dashboard = pn.Row(charts, pn.Spacer(width=0), widgets)
dashboard.show()