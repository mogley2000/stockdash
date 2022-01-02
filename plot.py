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
    return hist["Close"].round(decimals=2)

def plot_graph(stock_ticker, stock_period, stock_interval): 
    """Plot graph in matplotlib. Function is called into app.py. 
    Master Figure changes done here 
    """
    # Call yfinance
    data = get_closing_prices(stock_ticker, stock_period, stock_interval) 
    last_price = '{:,.2f}'.format(data[-1]) # Separates thousands with , and 2 decimal places 

    # Format performance label based on +ve or -ve 
    performance_calc = ((data[-1] / data[0]) - 1) * 100
    if performance_calc >= 0:
        performance = '+' + str(round(performance_calc,2))
    else:
        performance = str(round(performance_calc,2))

    # Format performance label by color 
    performance_int = (round(performance_calc,2))
    
    if performance_int >= 0:
        colors = 'lime'
    else:
        colors = 'red'

    # Other ax colors
    bg_color = 'black'
    label_color = 'white'
    

    
    # fig.text x co-ord based on length of last_price to manage horiz spacing 
    if len(last_price) > 6:
        x_coord = 0.3
    else:
        x_coord = 0.27 

  
    
    # Instantiate object of Figure class. Can't use pyplot if sending graph to flask as png
    fig = Figure(figsize=(6,2))
    fig.patch.set_facecolor(bg_color)
    ax = fig.subplots()

    ax.patch.set_facecolor(bg_color)
    ax.plot(data.index, data, label=stock_ticker, color=colors)
    # fig.suptitle(stock_ticker)
    fig.subplots_adjust(top=0.75)
    
    fig.text(0.125, 0.90, last_price, fontsize='x-large', fontweight='bold', color=label_color)
    fig.text(x_coord, 0.90, '{}%'.format(performance), fontsize='large', fontweight='bold', color=colors)
    ax.set_title(stock_ticker, loc='left', pad=4, fontsize='x-large', fontweight='bold', color=label_color)
    ax.set_xticks(data.index[::20])  # Slices list to include all values but indexjump every 20 
    #ax.set_yticks(data[::20])
    ax.set_xticklabels(data.index.strftime('%b')[::20], color=label_color)  # set_xticklabels must preceded by set_xticks with same range
    ax.set_yticklabels(data[::20], fontsize=8, color=label_color)
    ax.tick_params(axis='both', labelsize=8, color=label_color)
    # ax.set_ylabel('Share price ($)', fontsize='x-small')
    # ax.set_xlabel('Date', fontsize='x-small')
    # ax.legend(loc='upper left', fontsize='x-small')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_color('gray')
    ax.spines['left'].set_color('gray')
    # fig.tight_layout()

    # Save to temp buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    return send_file(buf, mimetype='image/png')


def small_plot(stock_ticker, stock_period, stock_interval):
    """ Small graph for scroll nav bar"""
    # Call yfinance
    data = get_closing_prices(stock_ticker, stock_period, stock_interval) 
    last_price = '{:,.2f}'.format(data[-1]) # Separates thousands with , and 2 decimal places 

    # Format performance label based on +ve or -ve 
    performance_calc = ((data[-1] / data[0]) - 1) * 100
    if performance_calc >= 0:
        performance = '+' + str(round(performance_calc,2))
    else:
        performance = str(round(performance_calc,2))

    # Format performance label by color 
    performance_int = (round(performance_calc,2))
    
    if performance_int >= 0:
        colors = 'lime'
    else:
        colors = 'red'

    # Other ax colors
    bg_color = 'black'
    label_color = 'white'
    

    
    # fig.text x co-ord based on length of last_price to manage horiz spacing 
    if len(last_price) > 6:
        x_coord = 0.3
    else:
        x_coord = 0.27 

  
    
    # Instantiate object of Figure class. Can't use pyplot if sending graph to flask as png
    fig = Figure(figsize=(6,2))
    fig.patch.set_facecolor(bg_color)
    ax = fig.subplots()

    ax.patch.set_facecolor(bg_color)
    ax.plot(data.index, data, label=stock_ticker, color=colors)
    # fig.suptitle(stock_ticker)
    fig.subplots_adjust(top=0.75)
    
    fig.text(0.125, 0.90, last_price, fontsize='x-large', fontweight='bold', color=label_color)
    fig.text(x_coord, 0.90, '{}%'.format(performance), fontsize='large', fontweight='bold', color=colors)
    ax.set_title(stock_ticker, loc='left', pad=4, fontsize='x-large', fontweight='bold', color=label_color)
    #ax.set_xticks(data.index[::20])  # Slices list to include all values but indexjump every 20 
    #ax.set_yticks(data[::20])
    #ax.set_xticklabels(data.index.strftime('%b')[::20], color=label_color)  # set_xticklabels must preceded by set_xticks with same range
    #ax.set_yticklabels(data[::20], fontsize=8, color=label_color)
    #ax.tick_params(axis='both', labelsize=8, color=label_color)
    # ax.set_ylabel('Share price ($)', fontsize='x-small')
    # ax.set_xlabel('Date', fontsize='x-small')
    # ax.legend(loc='upper left', fontsize='x-small')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    #ax.spines['bottom'].set_color('gray')
    #ax.spines['left'].set_color('gray')
    # fig.tight_layout()

    # Save to temp buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    return send_file(buf, mimetype='image/png')
