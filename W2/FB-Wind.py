from erddapy import ERDDAP
from bokeh.plotting import figure, output_file, show, save
from bokeh.io import export_png
import pandas as pd
import datetime as dt
from bokeh.models import DatetimeTickFormatter, ColumnDataSource
import panel.widgets as pnw


e = ERDDAP(server="https://www.smartatlantic.ca/erddap/",
  protocol="tabledap",)

e.response = "csv"
e.dataset_id = "DFO_Sutron_DOGIS"
e.constraints = {
    "time>=": "2021-09-09T00:00:00Z",
    "time<=": "2021-09-12T12:00:00Z",}
e.variables = [
    "time", "wind_spd_gust"]
df = e.to_pandas()
single_color = (229, 81, 98)
vars = df[df.columns[1:]]
vars=vars.to_numpy(dtype=float)
time = pd.to_datetime(df['time (UTC)'], format="%Y-%m-%dT%H:%M:%SZ")
print(df)
output_file("FB-Wind.html")
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
fig1.xaxis.major_tick_line_color = None
fig1.xaxis.major_label_text_font_size = '0pt'
fig1.line(time, df['wind_spd_gust (m s-1)']*3.6, line_width=2, color=single_color,
          legend_label='Wind Gust Speed km/h')
#fig1.line(time, df['wind_spd_max (m s-1)'], line_width=2, color='yellow',
          #legend_label='wind_spd_max m/s')
#fig1.line(time, vars[:,2], line_width=2, color='blue')
fig1.legend.location= 'top_left'
fig1.legend.click_policy='hide'
show(fig1)