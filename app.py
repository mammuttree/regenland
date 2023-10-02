from flask import Flask, render_template
import pandas as pd
import numpy as np
import json
import plotly
import plotly.express as px

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import WMTSTileSource

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chart1')
def chart1():
  df = pd.DataFrame({
      "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
      "Amount": [4, 1, 2, 2, 4, 5],
      "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
  })

  fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  header="Fruit in North America"
  description = """
  A academic study of the number of apples, oranges and bananas in the cities of
  San Francisco and Montreal would probably not come up with this chart.
  """

  html = render_template(
    'example_chart.html', 
    graphJSON=graphJSON, 
    header=header,
    description=description
    )

  return html 


@app.route('/chart2')
def chart2():
  df = pd.DataFrame({
      "Vegetables": ["Lettuce", "Cauliflower", "Carrots", "Lettuce", "Cauliflower", "Carrots"],
      "Amount": [10, 15, 8, 5, 14, 25],
      "City": ["London", "London", "London", "Madrid", "Madrid", "Madrid"]
  })

  fig = px.bar(df, x="Vegetables", y="Amount", color="City", barmode="stack")

  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  header="Vegetables in Europe"
  description = """
  The rumor that vegetarians are having a hard time in London and Madrid can probably not be
  explained by this chart.
  """

  html = render_template(
    'example_chart.html', 
    graphJSON=graphJSON, 
    header=header,
    description=description
    )

  return html 


@app.route('/bokeh_brtiles')
def bokeh_brtiles():
  tile_provider = WMTSTileSource(
      url='http://tiles.buienradar.nl/tiles-eu-v2/{Z}/{X}/{Y}.png',
      attribution='Tested'
  )

  # range bounds supplied in web mercator coordinates
  fig = figure(x_range=(230000, 880000), y_range=(6750000, 6900000),
            x_axis_type="mercator", y_axis_type="mercator")
  fig.add_tile(tile_provider)

  # grab the static resources
  js_resources = INLINE.render_js()
  css_resources = INLINE.render_css()

  # render template
  script, div = components(fig)
  html = render_template(
      'bokeh.html',
      plot_script=script,
      plot_div=div,
      js_resources=js_resources,
      css_resources=css_resources,
  )

  return html

# if __name__ == "__main__":
#   app.run()