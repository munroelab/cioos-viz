from erddapy import ERDDAP
from bokeh.plotting import figure, output_file, show, save
from bokeh.io import export_png
import pandas as pd
import datetime as dt
from bokeh.models import DatetimeTickFormatter, ColumnDataSource, Legend, LegendItem
import panel.widgets as pnw

e = ERDDAP(server="https://cioosatlantic.ca/erddap",
  protocol="tabledap",)

e.response = "csv"
e.dataset_id = "DFO_Sutron_NHARB"
e.constraints = {
    "time>=": "2021-09-09T00:00:00Z",
    "time<=": "2021-09-12T12:00:00Z",}
e.variables = [
    "time", "water_pressure"]
df = e.to_pandas()
single_color = (241, 226, 104)
vars = df[df.columns[1:]]
vars=vars.to_numpy(dtype=float)
time = pd.to_datetime(df['time (UTC)'], format="%Y-%m-%dT%H:%M:%SZ")
print(df)
output_file("PB-Pressure.html")
fig1 = figure(
              x_axis_type='datetime',
              plot_width=955, plot_height=275,toolbar_location=None)
fig1.xaxis.formatter=DatetimeTickFormatter(
        hours=["%H:%M:%S"],
        days=["%b %d"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],)
fig1.xaxis.major_label_text_font_size = "15pt"
fig1.yaxis.major_label_text_font_size = "15pt"
fig1.xgrid.grid_line_color = None
fig1.ygrid.grid_line_color = None
fig1.xaxis.major_tick_line_color = None
fig1.xaxis.major_label_text_font_size = '0pt'
fig1.yaxis.axis_label = "decibars"
fig1.yaxis.axis_label_text_font_size = "15pt"
fig1.outline_line_color=None
fig1.line(time, df['water_pressure (mbar)']/100, line_width=5, color=single_color,
          legend_label='Water Pressure at 3m Depth')
fig1.legend.location= 'top_left'
fig1.legend.label_text_font_size = "21pt"
fig1.legend.click_policy='hide'


show(fig1)