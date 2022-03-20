from dash import html
from dash import dcc
from dash import dash_table
import dash_bootstrap_components as dbc
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
    'WMT',
    'RTX'
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
        winners.append([ticker, gain_loss(ticker, '3mo')])        

losers.sort(key=lambda x: x[1])  # Can also define a def custom_sort() that returns x[1] and use key=custom_sort
winners.sort(key=lambda x: x[1], reverse=True)  
logging.debug("PRINTING WINNERS {} ".format(winners))

""" Convert winners and losers list to pd df """
winners_df = pd.DataFrame(winners, columns=['Ticker', 'Return'])
losers_df = pd.DataFrame(losers, columns=['Ticker', 'Return'])


""" Generate sparkline graph for each ticker in winner, loser list """
# Winners graphs - IS THERE A WAY TO TURN THIS INTO A FUNCTION OR CLASS? INSTEAD OF MULTIPLE figs 
# fig_w0 = graph.sparkline_graph(winners[0][0], '3mo')
winners_list = []
for i in range(len(winners_df)):
    winners_list.append(graph.sparkline_graph(winners[i][0], '3mo')) 

logging.debug(winners_list) 

# fig_w1 = graph.sparkline_graph(winners[1][0], '3mo')  # TO DO - If winners[1] doesn't exist because they were all in the red, will throw an error.  

# Losers graphs
fig_l0 = graph.sparkline_graph(losers[0][0], '3mo')
fig_l1 = graph.sparkline_graph(losers[1][0], '3mo')



""" Dash table arguments """
format = dash_table.FormatTemplate.percentage(2)
d_columns = [{'name': 'Ticker', 'id': 'Ticker'}, {'name': 'Return', 'id': 'Return', 'type': 'numeric', 'format': format}]

""" Layout template which is passed to children = [] in CONTENT and then to app.layout """

# -- Not required since not showing spark lines --- 
# table_header = [
# html.Thead(html.Tr(html.Th("Header 1")))
# ]

# row_w0 = html.Tr(html.Td(
#             dcc.Graph(id='fig_w0',
#                         figure = winners_list[0] # If winners_list[0] does not exist, will throw an error
#                     )                    
#             )
#         )   

# row_w1 = html.Tr(html.Td(
#             dcc.Graph(id='fig_w1',
#                     figure = winners_list[1]
#                     )                    
#             )
#         )   


# table_body_w = [
#     html.Tbody([row_w0, row_w1])
# ]
# -----------------------------------------------

layout = html.Div(
    [
        dbc.Row(
            [
                # Col for the table of winners - Col 1 of 4
                dbc.Col(children=[
                    dash_table.DataTable(
                        winners_df.to_dict('records'), 
                        d_columns,
                        style_cell={
                            'height': '75px'
                        }
                    )
                ]),

                # --  Decided to remove spark lines ------
                # Corresponding table of spark lines - Col 2 of 4
                # Uses dbc.Table bootstrap  
                # dbc.Col(children=[
                #     dbc.Table(table_header + table_body_w)    
                #  ]),
                # ---------------------------------------

                
                # Col for table of losers using bootstrap dbc.Table 
                dbc.Col(children=[
                    html.Div("two of four cols"),
                    dbc.Table.from_dataframe(losers_df)
                ]),    
                    # -- Replacing with bootstrap table --
                    # dash_table.DataTable(
                    #     losers_df.to_dict('records'), 
                    #     d_columns,
                    #     style_cell={
                    #         'height': '50px'
                    #     }
                    # )
                    
                
                # -- Removed spark lines. Different to 
                # table_header, table_body method using
                # dbc.Table method (bootstrap) -------
                # Corresponding table of spark lines 
                # dbc.Col(children=[
                #     html.Div("Two of two cols"),
                #     dcc.Graph(id='fig_l0',
                #                     figure = fig_l0
                #                     ),
                #     dcc.Graph(id='fig_l1',
                #                     figure = fig_l1
                #                     )   
                # ])              


                dbc.Col(children=[
                        html.Div("three of four cols"),
                        dbc.Table.from_dataframe(losers_df)    
                ]),    

                dbc.Col(children=[
                        html.Div("four of four cols"),
                        dbc.Table.from_dataframe(winners_df)    
                ])    
            ]
        )
    ]
)
