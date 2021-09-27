import param
import bokeh.plotting
from bokeh.plotting import show
import holoviews as hv
import panel as pn
import numpy as np
import bokeh.io
from erddapy import ERDDAP
hv.extension(bokeh)

class A(param.Parameterized):
    title = param.String(default="sum", doc="Title for the result")


class B(A):
    a = param.Integer( bounds=(0, 10), doc="First addend")
    b = param.Integer(3, bounds=(0, 10), doc="Second addend")

    def __call__(self):
        return print(self.title + ": " + str(self.a + self.b))
object = B(b=5, title="this here is")
object.a=10
object()

opts = dict(show_grid=True,  color="#1f77b3")

mu_slider = pn.widgets.FloatSlider(
    name="m", start=-5, end=5, step=0.1, value=0
)
sigma_slider = pn.widgets.FloatSlider(
    name="b", start=0.1, end=5, step=0.1, value=1
)

pn.extension()

@pn.depends(mu_slider.param.value, sigma_slider.param.value)
def plot_normal_pdf(mu=0, sigma=1):
    x = np.linspace(0, 100, 200, endpoint=True)
    y = mu+sigma*x
    return hv.Curve(data=(x, y)).opts(
        **opts
    )
#plot_normal_pdf(0, 1)
widgets = pn.Column(
    pn.Spacer(height=30),
    mu_slider,
    pn.Spacer(height=15),
    sigma_slider,
    width=200,
)
plotnormalpdfPanel = pn.Row(plot_normal_pdf, pn.Spacer(width=15), widgets)
plotnormalpdfPanel.servable()