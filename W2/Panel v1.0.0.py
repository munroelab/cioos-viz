import param
import bokeh.plotting
from bokeh.plotting import show
import holoviews as hv
import panel as pn
import numpy as np
import bokeh.io
from erddapy import ERDDAP
import pandas as pd
import datetime as dt
hv.extension('bokeh')
pn.extension()

# erddap1 = ERDDAP(server="https://dev.cioosatlantic.ca/erddap",
#                  protocol="tabledap", )
# erddap1.auth = ("cioosatlantic", "4oceans")
# erddap1.response = "csv"
# erddap1.dataset_id = "wpsu-7fer"
# erddap1.constraints = {
#     "time>=": "2020-12-05T00:00:00Z",
#     "time<=": "2020-12-12T12:15:00Z",}
# dfdigby = erddap1.to_pandas()
#
# erddap2 = ERDDAP(server="https://dev.cioosatlantic.ca/erddap",
#                  protocol="tabledap", )
# erddap2.auth = ("cioosatlantic", "4oceans")
# erddap2.response = "csv"
# erddap2.dataset_id = "knwz-4bap"
# erddap2.constraints = {
#         "time>=": "2020-12-05T00:00:00Z",
#         "time<=": "2020-12-12T12:15:00Z", }
# dfAnnapolis = erddap2.to_pandas()
# df = pd.concat([dfdigby, dfAnnapolis], axis=0)
# df=df.dropna(axis=1, how='all')
dfDigbey = pd.read_csv("C:/Users/rinez/Downloads/wpsu-7fer_raw_merged.csv")
dfAnnapolis = pd.read_csv("C:/Users/rinez/Downloads/knwz-4bap_raw_merged.csv")
df = pd.concat([dfDigbey, dfAnnapolis], axis=0)
df = df.dropna(axis=1, how='all')

opts = dict(show_grid=True,  color="#1f77b3", frame_height=300, frame_width=300)

varFrame = df.drop(["timestamp"], axis=1)
varlist = list(varFrame.columns)
bodyFrame = df['waterbody'].unique()
bodylist = list(sorted(bodyFrame))
time = pd.to_datetime(df['timestamp'], format="%Y-%m-%dT%H:%M:%S.000")

var_selector = pn.widgets.Select(name="Variable", options=varlist)

body_selector = pn.widgets.Select(name = "WaterBody", options= bodylist)

@pn.depends(body_selector.param.value,var_selector.param.value)
def choicePlot(bodyname, varname):
    data = 