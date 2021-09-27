from erddapy import ERDDAP
from bokeh.plotting import figure, output_file, show, save
from bokeh.io import export_png
import pandas as pd
import datetime as dt
from bokeh.models import DatetimeTickFormatter, ColumnDataSource
import panel.widgets as pnw

e1 = ERDDAP(server="https://cioosatlantic.ca/erddap",
            protocol="tabledap", )

e1.response = "csv"
e1.dataset_id = "SMA_MouthofPlacentiaBayBuoy"
e1.constraints = {
    "time>=": "2021-09-09T00:00:00Z",
    "time<=": "2021-09-12T12:00:00Z",}
e1.variables = [
    "time", "wave_ht_max"]
df1 = e1.to_pandas()
time1 = pd.to_datetime(df1['time (UTC)'], format="%Y-%m-%dT%H:%M:%SZ")

e = ERDDAP(server="https://cioosatlantic.ca/erddap",
  protocol="tabledap",)

e.response = "csv"
e.dataset_id = "SMA_red_island_shoal"
e.constraints = {
    "time>=": "2021-09-09T00:00:00Z",
    "time<=": "2021-09-12T12:00:00Z",}
e.variables = [
    "time", "wave_ht_max"]
df = e.to_pandas()
time = pd.to_datetime(df['time (UTC)'], format="%Y-%m-%dT%H:%M:%SZ")

single_color = (86, 220, 190)

print(df)
output_file("PB-Wave.html")
fig1 = figure(
              x_axis_type='datetime',
              plot_width=955, plot_height=275,toolbar_location=None)
fig1.xaxis.formatter=DatetimeTickFormatter(
        hours=["%H:%M:%S"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],)
fig1.xgrid.grid_line_color = None
fig1.ygrid.grid_line_color = None
fig1.line(time, df['wave_ht_max (m)'], line_width=2, color=single_color,
         legend_label='Maximum Wave Height (m)')
fig1.line(time1, df1['wave_ht_max (m)'], line_width=2, color=single_color,
          legend_label='Maximum Wave Height (m)')

fig1.legend.location= 'top_left'
fig1.legend.click_policy='hide'
show(fig1)