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
@app.route('/index') #Which URL should trigger the function? app is an instance of Flask class which has the method .route 
def index():
    """ Serve webpage """
    return render_template("index.html")


@app.route('/about') # NB: when you use url_for tag it looks for the 'url for' function which = '/about' in this case. 
                     # Allows you to change the '/about' without changing it in each .html 
def about():
    """ Serve webpage """
    return render_template("about.html")



# Main code starts here
@app.route('/')
def home():
    for k, v in stock_period_dict.items():
        if k == stock_period_default:
            stock_period_default_expanded = v

    return render_template("home.html", stock_period_default_expanded=stock_period_default_expanded)


# Plot defaults 
stock_period_default = '6mo'
stock_interval_default='1d'

stock_period_dict = {'1mo':'1 month', '3mo':'3 months', '6mo':'6 months'}

# Plot routes below 

@app.route('/plot_graph_TWLO')
def plot_graph_TWLO():
    return plot_graph('TWLO', stock_period_default, stock_interval_default)

@app.route('/plot_graph_U')
def plot_graph_U():
    return plot_graph('U', stock_period_default, stock_interval_default)

@app.route('/plot_graph_SQ')
def plot_graph_SQ():
    return plot_graph('SQ', stock_period_default, stock_interval_default)

@app.route('/plot_graph_PYPL')
def plot_graph_PYPL():
    return plot_graph('PYPL', stock_period_default, stock_interval_default)

@app.route('/plot_graph_SDGR')
def plot_graph_SDGR():
    return plot_graph('SDGR', stock_period_default, stock_interval_default)

@app.route('/plot_graph_PLTR')
def plot_graph_PLTR():
    return plot_graph('PLTR', stock_period_default, stock_interval_default)

@app.route('/plot_graph_ETSY')
def plot_graph_ETSY():
    return plot_graph('ETSY', stock_period_default, stock_interval_default)

@app.route('/plot_graph_NVDA')
def plot_graph_NVDA():
    return plot_graph('NVDA', stock_period_default, stock_interval_default)

@app.route('/plot_graph_GOOG')
def plot_graph_GOOG():
    return plot_graph('GOOG', stock_period_default, stock_interval_default)

@app.route('/plot_graph_DIS')
def plot_graph_DIS():
    return plot_graph('DIS', stock_period_default, stock_interval_default)

@app.route('/plot_graph_CRM')
def plot_graph_CRM():
    return plot_graph('CRM', stock_period_default, stock_interval_default)

@app.route('/plot_graph_RTX')
def plot_graph_RTX():
    return plot_graph('RTX', stock_period_default, stock_interval_default)

@app.route('/plot_graph_AMZN')
def plot_graph_AMZN():
    return plot_graph('AMZN', stock_period_default, stock_interval_default)

@app.route('/plot_graph_TSM')
def plot_graph_TSM():
    return plot_graph('TSM', stock_period_default, stock_interval_default)

@app.route('/plot_graph_LRCX')
def plot_graph_LRCX():
    return plot_graph('LRCX', stock_period_default, stock_interval_default)

@app.route('/plot_graph_MSFT')
def plot_graph_MSFT():
    return plot_graph('MSFT', stock_period_default, stock_interval_default)

@app.route('/plot_graph_SWKS')
def plot_graph_SWKS():
    return plot_graph('SWKS', stock_period_default, stock_interval_default)

@app.route('/plot_graph_ABB')
def plot_graph_ABB():
    return plot_graph('ABB.AX', stock_period_default, stock_interval_default)

@app.route('/plot_graph_VGL')
def plot_graph_VGL():
    return plot_graph('VGL.AX', stock_period_default, stock_interval_default)

@app.route('/plot_graph_EXP')
def plot_graph_EXP():
    return plot_graph('EXP.AX', stock_period_default, stock_interval_default)

@app.route('/plot_graph_EML')
def plot_graph_EML():
    return plot_graph('EML.AX', stock_period_default, stock_interval_default)

@app.route('/plot_graph_SHL')
def plot_graph_SHL():
    return plot_graph('SHL.AX', stock_period_default, stock_interval_default)

@app.route('/plot_graph_CKF')
def plot_graph_CKF():
    return plot_graph('CKF.AX', stock_period_default, stock_interval_default)

@app.route('/plot_graph_ALL')
def plot_graph_ALL():
    return plot_graph('ALL.AX', stock_period_default, stock_interval_default)

@app.route('/plot_graph_REA')
def plot_graph_REA():
    return plot_graph('REA.AX', stock_period_default, stock_interval_default)

@app.route('/plot_graph_HMD')
def plot_graph_HMD():
    return plot_graph('HMD.AX', stock_period_default, stock_interval_default)

@app.route('/plot_graph_AD8')
def plot_graph_AD8():
    return plot_graph('AD8.AX', stock_period_default, stock_interval_default)

@app.route('/plot_graph_XRO')
def plot_graph_XRO():
    return plot_graph('XRO.AXX', stock_period_default, stock_interval_default)

@app.route('/plot_graph_PDN')
def plot_graph_PDN():
    return plot_graph('PDN.AX', stock_period_default, stock_interval_default)


# Launch flask
if __name__ == '__main__':
    app.run(host='0.0.0.0')
