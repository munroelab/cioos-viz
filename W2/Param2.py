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

e = ERDDAP(server="https://dev.cioosatlantic.ca/erddap",
               protocol="tabledap", )
e.auth = ("cioosatlantic", "4oceans")
e.response = "csv"
e.dataset_id = "DFO_Sutron_KLUMI"
e.constraints = {
        "time>=": "2021-09-09T00:00:00Z",
        "time<=": "2021-09-12T12:00:00Z", }
e.variables = [
        "time", "wind_spd_gust", "wind_spd_avg"]

df = e.to_pandas()
varList = list(df.columns[1:])

opts = dict(show_grid=True,  color="#1f77b3", frame_height=300, frame_width=300)
values = (dt.datetime(2021, 3, 2, 12, 10), dt.datetime(2021, 3, 2, 12, 22))
#datetime_rangeslider = pn.widgets.DatetimeRangePicker(
#  name="Time Range", start=dt.datetime(2021, 9, 9, 0, 0), end=dt.datetime(2019, 9, 12, 0, 0), value=values
#)
var_selector = pn.widgets.Select(
    name="Variable",
    options=varList,
    value="wind_spd_gust (m s-1)",
)

pn.extension()

@pn.depends(var_selector.param.value)
def plotData(varName='wind_spd_gust (m s-1)'):
    time = pd.to_datetime(df['time (UTC)'], format="%Y-%m-%dT%H:%M:%SZ")
    vartoplot = df[varName]
    return hv.Curve(data=(time, vartoplot)).opts(
        **opts
    )

widgets = pn.Column(
    pn.Spacer(height=0),
    var_selector,
    width=400,
)
plotDataPanel = pn.Row(plotData, pn.Spacer(width=0), widgets)
plotDataPanel.show()