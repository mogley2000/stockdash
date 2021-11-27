from flask import Flask, render_template, request, jsonify, send_file
import yfinance as yf
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from io import BytesIO  

# # symbol = request.args.get('symbol', default="AAPL")
# # period = request.args.get('period', default="1y")
# # interval = request.args.get('interval', default="1mo")
# #Pull the quote
# quote = yf.Ticker("AAPL")  
# period = "1y"
# interval = "1mo"
# #Use quote to pull historicals  
# hist = quote.history(period=period, interval=interval)
# data = hist.to_json()
# print(data)
# print(hist)

def get_closing_prices(symbol, period, interval):
    quote = yf.Ticker(symbol)
    hist = quote.history(period, interval)
    return hist["Close"]

def plot_graph(stock_ticker, stock_period, stock_interval): 
    """Plot graph in matplotlib. Function is called into app.py. 
    Master Figure changes done here 
    """
    # Call yfinance
    data = get_closing_prices(stock_ticker, stock_period, stock_interval) 
    
    # Instantiate object of Figure class. Can't use pyplot if sending graph to flask as png
    fig = Figure(figsize=(4,2))
    ax = fig.subplots()
    ax.plot(data.index, data, label=stock_ticker)
    ax.set_xticklabels(data.index, fontsize=8)
    ax.set_yticklabels(data, fontsize=8)
    ax.set_ylabel('Share price ($)', fontsize='x-small')
    ax.set_xlabel('Date', fontsize='x-small')
    ax.legend(loc='upper left', fontsize='x-small')
    fig.tight_layout()

    # Save to temp buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    return send_file(buf, mimetype='image/png')



# pyplot.plot(AAPL_closing_prices.index, AAPL_closing_prices)
# pyplot.show()


    
# x_axis = [1, 2, 3, 4, 5]
# y_axis = [10, 20, 30, 40, 50]
# pyplot.plot(x_axis, y_axis)
# pyplot.show()

