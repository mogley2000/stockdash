from dash import html
from dash import dcc
import graph
import yfinance as yf 


""" Setup list of stock winners and losers """

ticker_list = [
    'NVDA',
    'AAPL',
    'MSFT',
    'NFLX',
    'COST',
    'JNJ',
    'WMT'
]

def gain_loss(ticker, period):
    """ Calculates % gain or loss over period """
    quote = yf.Ticker(ticker)
    hist = quote.history(period, '1d')
    df = hist.round(decimals=2)    
    
    return ((df.iloc[-1, 0] / df.iloc[0, 0]) - 1) * 100

losers = []
winners = []

for ticker in ticker_list:
    if gain_loss(ticker, '3mo') < 0:
        losers.append([ticker, gain_loss(ticker, '3mo')])
    elif gain_loss(ticker, '3mo') >= 0:
        winners.append((ticker, gain_loss(ticker, '3mo')))        

losers.sort(key=lambda x: x[1])  # Can also define a def custom_sort() that returns x[1] and use key=custom_sort
winners.sort(key=lambda x: x[1], reverse=True)  


""" Generate sparkline graph for each ticker in winner, loser list """
fig_0 = graph.sparkline_graph(losers[0][0], '3mo')
fig_1 = graph.sparkline_graph(losers[1][0], '3mo')

layout = html.Div([
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
    
    dcc.Graph(id='fig_0',
                    figure = fig_0
                    ),
    
    dcc.Graph(id='fig_1',
                    figure = fig_1
                    )

])


