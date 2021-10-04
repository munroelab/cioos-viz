import param
import bokeh.plotting
from bokeh.plotting import show
import holoviews as hv
import hvplot.pandas
import panel as pn
import numpy as np
import bokeh.io
from erddapy import ERDDAP
import pandas as pd
import datetime as dt
import requests
import io

hv.extension('bokeh')
pn.extension(loading_spinner='dots', loading_color='#00aa41',)

dfDigbey = pd.read_csv("C:/Users/rinez/Downloads/wpsu-7fer_raw_merged.csv")
dfAnnapolis = pd.read_csv("C:/Users/rinez/Downloads/knwz-4bap_raw_merged.csv")
df = pd.concat([dfDigbey, dfAnnapolis], axis=0)
df = df.dropna(axis=1, how='all')
df = df.sort_values(by=['timestamp'])
df = df.set_index(df.timestamp.astype(np.datetime64))
# pd.to_datetime(df['timestamp'], format="%Y-%m-%dT%H:%M:%S.000")
# df = df.sort_index(ascending = True)
df = df['2019-10-20':'2019-11-01']

opts = dict(show_grid=True,  color="#1f77b3", frame_height=300, frame_width=300)

timeVariables = df.drop(['waterbody','latitude','longitude','deployment_start_date',
                         'deployment_end_date', 'station', 'sensor', 'timestamp'], axis = 1)
varlist = list(timeVariables.columns)
bodyFrame = df['waterbody'].unique()
bodylist = list(sorted(bodyFrame))



var_selector = pn.widgets.Select(name="Variable", options=varlist)

body_selector = pn.widgets.Select(name = "WaterBody", options= bodylist)

date_range_slider = pn.widgets.DateRangeSlider(
    name="Show between",
    start=df.index.min(),
    end=df.index.max(),
    value=(df.index.min(), df.index.max()),
)

def choicePlot(bodyname, varName, xlim):
    data = df[df.waterbody == bodyname]
    return data.hvplot(y=varName, xlim=xlim).opts(**opts)

df_choicePlot = pn.pane.HoloViews(choicePlot(body_selector.value, var_selector.value, date_range_slider.value))

def trim(target, event):
    target.object = choicePlot(body_selector.value, var_selector.value, event.new)

def updatebody(target, event):
    target.object = choicePlot(event.new, var_selector.value, date_range_slider.value)

def updatevar(target, event):
    target.object = choicePlot(body_selector.value, event.new, date_range_slider.value)

date_range_slider.link(df_choicePlot, callbacks = {"value":trim})
body_selector.link(df_choicePlot, callbacks = {"value":updatebody})
var_selector.link(df_choicePlot, callbacks = {"value":updatevar})

widgets = pn.Column(
    pn.Spacer(height=30),
    body_selector, pn.Spacer(height=30), var_selector, pn.Spacer(height=30), date_range_slider,
    width=400,)

expanel = pn.Row(df_choicePlot, pn.Spacer(width = 10), widgets)
expanel.show()