from dash import html
from dash import dcc
from dash import dash_table
import graph
import yfinance as yf 
import pandas as pd 
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')


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
    
    return ((df.iloc[-1, 0] / df.iloc[0, 0]) - 1) 

losers = []
winners = []

for ticker in ticker_list:
    if gain_loss(ticker, '3mo') < 0:
        losers.append([ticker, gain_loss(ticker, '3mo')])
    elif gain_loss(ticker, '3mo') >= 0:
        winners.append((ticker, gain_loss(ticker, '3mo')))        

losers.sort(key=lambda x: x[1])  # Can also define a def custom_sort() that returns x[1] and use key=custom_sort
winners.sort(key=lambda x: x[1], reverse=True)  

""" Convert winners and losers list to pd df """
winner_df = pd.DataFrame(winners, columns=['Ticker', 'Return'])

logging.debug(winner_df)


""" Generate sparkline graph for each ticker in winner, loser list """
fig_0 = graph.sparkline_graph(losers[0][0], '3mo')
fig_1 = graph.sparkline_graph(losers[1][0], '3mo')


""" Dash table arguments """
format = dash_table.FormatTemplate.percentage(2)
d_columns = [{'name': 'Ticker', 'id': 'Ticker'}, {'name': 'Return', 'id': 'Return', 'type': 'numeric', 'format': format}]

layout = html.Div([
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),

    dash_table.DataTable(winner_df.to_dict('records'), d_columns),
    
    dcc.Graph(id='fig_0',
                    figure = fig_0
                    ),
    
    dcc.Graph(id='fig_1',
                    figure = fig_1
                    )

])


