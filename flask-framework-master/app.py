from flask import Flask, render_template, request, redirect
import pandas as pd
from pandas.io.json import json_normalize
import requests
import json
from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import file_html, components
from bokeh.models import ColumnDataSource

app = Flask(__name__)

# Alpha Vantage API KEY: E35E87068E5GF175

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/graph' , methods=['POST'])
def graph():
    symbol = request.form['symbol']

    if symbol == '':
        return render_template('index.html')

    apiData = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&apikey=E35E87068E5GF175&datatype=json' % symbol)

    # must handle error for an invalid stock symbol
    try:
        original = apiData.json()["Time Series (Daily)"]
    except KeyError:
        return render_template('index.html',error='Sorry, that stock is unavailable!')

    modified = [{'olddate':key,'close':value['4. close'], } for key, value in original.items()]
    df = json_normalize(modified)
    df['newDate'] = pd.to_datetime(df['olddate'])
    source = ColumnDataSource(data=df)

    plot = figure(x_axis_type='datetime')
    plot.line('newDate','close',source=source,line_color="purple", line_width = 3)
    plot.xaxis.axis_label = 'Date'
    plot.yaxis.axis_label = 'Share Price ($)'

    script, div = components(plot)

    return render_template('about.html',script=script,div=div,symbol=symbol)

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(port=33507)
