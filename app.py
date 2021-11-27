""" app.py is being run by Flask as a webserver and looking to app.py. 
Can't run usual Python code here i.e. print("Hello World") 
"""

from flask import Flask, render_template, request, jsonify, send_file # Flask is a Class inside flask library 
import yfinance as yf
from matplotlib import pyplot as plt
from matplotlib.figure import Figure # Import Figure Class 
from plot import get_closing_prices, plot_graph # Must important functions from another module. 
                                                # App module is for routing only 
from io import BytesIO


# Instantiate Class by assigning Flask to a variable 
app = Flask(__name__) #Flask is a Class


#Define the root route
@app.route('/') #Which URL should trigger the function? app is an instance of Flask class which has the method .route 
def home():
    """ Serve webpage """
    return render_template("index.html")


@app.route('/about') # NB: when you use url_for tag it looks for the 'url for' function which = '/about' in this case. 
                     # Allows you to change the '/about' without changing it in each .html 
def about():
    """ Serve webpage """
    return render_template("about.html")


@app.route('/dash')
def dash():
    return render_template("dash.html")    


@app.route('/dash_overview')
def dash_overview():
    return render_template("dash_overview.html")


# Plot defaults 
stock_period_default = '3mo'
stock_interval_default='1d'

#Plot routes below 
@app.route('/plot_graph_NVDA')
#def dash():
# """ get query string parameters per args inputted in URL e.g. localhost/dash?symbol=TSLA 
# request object is sent by client and received by Flask as server. synbol is contained in url as arg """
    # symbol = request.args.get('symbol', default="AAPL")
    # period = request.args.get('period', default="1y")
    # interval = request.args.get('interval', default="1mo")
def plot_graph_NVDA():
    return plot_graph('NVDA', stock_period_default, stock_interval_default)


@app.route('/plot_graph_AAPL')
def plot_graph_AAPL():
    return plot_graph('AAPL', stock_period_default, stock_interval_default)


@app.route('/plot_graph_REA')
def plot_graph_REA():
    return plot_graph('REA.AX', stock_period_default, stock_interval_default)



