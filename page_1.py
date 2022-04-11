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

TICKERS = [
    'NVDA', 'MSFT','TWLO','NET','U','SQ','RTX','PYPL','SDGR','PLTR',
    'ETSY','GOOG','DIS','CRM','AMZN','TSM','LRCX','SWKS'
]

TICKERS_AU = [
   'ABB.AX','VGL.AX','EXP.AX','EML.AX','SHL.AX','CKF.AX','ALL.AX','REA.AX','HMD.AX','AD8.AX',
   'XRO.AX', 'PDN.AX'  
]



# ----- OLD gain_loss func which called yf everytime ------------------
# def gain_loss(ticker, period, interval):
#     """ Calculates % gain or loss over period 
#     valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max"""
#     quote = yf.Ticker(ticker)
#     hist = quote.history(period, interval)
#     df = hist.round(decimals=2)    
    
#     if period == '1d':  # If just 1d, cf df frmo Open and Close on same day/line 
#         return ((df.iloc[0, 3] / df.iloc[0, 0] - 1))
#     else:  # If more than 1d, cf Close from latest to first row 
#         return ((df.iloc[-1, 3] / df.iloc[0, 3] - 1))
# -------------------------------------------------------------


def gain_loss(data_set, ticker, period):
    """ Calc gain loss """
    close = data_set[ticker]['Close']
    
    if period == '5d':  # '5d' period dataset for 1d gain_loss 
        first_close = close.iloc[-2]
    else:
        first_close = close.iloc[0]
    
    latest_close = close.iloc[-1]

    gain_loss = (latest_close / first_close) - 1
    
    return gain_loss


def fifty_two_wk_high(data_set, ticker):
    """ Gets 52-week high and calc percentage var """
    fifty_two_high = data_set[ticker]['Close'].max()
    close_price = data_set[ticker]['Close'].iloc[-1]
    
    var = (close_price / fifty_two_high) - 1

    return var


# Variables for main() but not to be re-run everytime the main() code is pulled when clicking route 
run_counter = 0  # Counter to prevent data from pulling again if >= 1
losers_1d = []
losers_3mo = []
winners_1d = []
winners_3mo = []
fifty_two_wk_high_list = []

def main():
    """ Setup various dfs for tickers based on losers and winners """
    global run_counter 
    global losers_1d
    global losers_3mo
    global winners_1d
    global winners_3mo
    global fifty_two_wk_high_list

    if run_counter == 0:  # Don't run if alraedy run once to prevent re-downloading data 
        run_counter += 1
        
        # Download the data sets if running for first time
        # AU data_set needs to be downlaoded separately due to time difference and mixing AU tickers returns a NaN in US date
        # i.e. 6th April is NaN for US tickers when AU is 6th April
        download_5d = yf.download(TICKERS, period='5d', interval='1d', group_by='ticker', threads=True)
        download_5d_AU = yf.download(TICKERS_AU, period='5d', interval='1d', group_by='ticker', threads=True)
        
        # logging.debug('PRINT download_5d')
        # logging.debug(download_5d)
        download_3mo = yf.download(TICKERS, period='3mo', interval='1d', group_by='ticker', threads=True)
        download_3mo_AU = yf.download(TICKERS_AU, period='3mo', interval='1d', group_by='ticker', threads=True)
        download_52high = yf.download(TICKERS, period="1y", interval='1d', group_by='ticker', threads=True)
        download_52high_AU = yf.download(TICKERS_AU, period="1y", interval='1d', group_by='ticker', threads=True)


        for ticker in TICKERS:
            if gain_loss(download_5d, ticker, '5d') < 0:
                losers_1d.append([ticker, gain_loss(download_5d, ticker, '5d')])
            if gain_loss(download_3mo, ticker, '3mo') < 0:
                losers_3mo.append([ticker, gain_loss(download_3mo, ticker, '3mo')])
            if gain_loss(download_5d, ticker, '5d') >= 0:
                winners_1d.append([ticker, gain_loss(download_5d, ticker, '5d')])
            if gain_loss(download_3mo, ticker, '3mo') >= 0:
                winners_3mo.append([ticker, gain_loss(download_3mo, ticker, '3mo')])   
            
            fifty_two_wk_high_list.append([ticker, fifty_two_wk_high(download_52high, ticker)])

        for ticker in TICKERS_AU:  
            if gain_loss(download_5d_AU, ticker, '5d') < 0:
                losers_1d.append([ticker, gain_loss(download_5d_AU, ticker, '5d')])
            if gain_loss(download_3mo_AU, ticker, '3mo') < 0:
                losers_3mo.append([ticker, gain_loss(download_3mo_AU, ticker, '3mo')])
            if gain_loss(download_5d_AU, ticker, '5d') >= 0:
                winners_1d.append([ticker, gain_loss(download_5d_AU, ticker, '5d')])
            if gain_loss(download_3mo_AU, ticker, '3mo') >= 0:
                winners_3mo.append([ticker, gain_loss(download_3mo_AU, ticker, '3mo')])   
            
            fifty_two_wk_high_list.append([ticker, fifty_two_wk_high(download_52high_AU, ticker)])


    losers_1d.sort(key=lambda x: x[1])  # Can also define a def custom_sort() that returns x[1] and use key=custom_sort
    losers_3mo.sort(key=lambda x: x[1])  # Can also define a def custom_sort() that returns x[1] and use key=custom_sort

    winners_1d.sort(key=lambda x: x[1], reverse=True)  
    winners_3mo.sort(key=lambda x: x[1], reverse=True)  

    fifty_two_wk_high_list.sort(key=lambda x: x[1])

    # logging.debug(losers_1d)

    """ Convert winners and losers list to pd df """
    winners_1d_df = pd.DataFrame(winners_1d, columns=['Ticker', 'Return'])
    winners_3mo_df = pd.DataFrame(winners_3mo, columns=['Ticker', 'Return'])
    # logging.debug("PRINTING WINNERS_1D_df")
    # logging.debug(winners_1d_df)
    # logging.debug("PRINING Winners_3mo_df")
    # logging.debug(winners_3mo_df)

    losers_1d_df = pd.DataFrame(losers_1d, columns=['Ticker', 'Return'])
    losers_3mo_df = pd.DataFrame(losers_3mo, columns=['Ticker', 'Return'])
    # logging.debug("PRINTING losers_1D_df")
    # logging.debug(losers_1d_df)
    # logging.debug("PRINING losers_3mo_df")
    # logging.debug(losers_3mo_df)

    fifty_two_wk_high_list_df = pd.DataFrame(fifty_two_wk_high_list, columns=['Ticker', 'Return'])


    """ Generate sparkline graph for each ticker in winner, loser list """
    # Winners graphs - IS THERE A WAY TO TURN THIS INTO A FUNCTION OR CLASS? INSTEAD OF MULTIPLE figs 
    # fig_w0 = graph.sparkline_graph(winners[0][0], '3mo')
    # winners_list = []
    # for i in range(len(winners_df)):
    #     winners_list.append(graph.sparkline_graph(winners[i][0], '3mo')) 



    # fig_w1 = graph.sparkline_graph(winners[1][0], '3mo')  # TO DO - If winners[1] doesn't exist because they were all in the red, will throw an error.  

    # Losers graphs
    # fig_l0 = graph.sparkline_graph(losers[0][0], '3mo')
    # fig_l1 = graph.sparkline_graph(losers[1][0], '3mo')



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

    """ Dash table arguments """
    format = dash_table.FormatTemplate.percentage(2)

    d_columns = [{'name': 'Ticker', 'id': 'Ticker'}, {'name': 'Return', 'id': 'Return', 'type': 'numeric', 'format': format}]

    style_cell = {
        'height': '50px',
        'textAlign': 'left',
        'font_family': 'Arial',
        'font_size': '24px',
        'text_align': 'center'
    }

    style_header={
        'backgroundColor': '#060606',
        'color': 'white',
        'font-weight': 'bold',
        'border': 'none'
    }
                            
    style_data={
        'backgroundColor': '#060606',
        'color': 'white',
        'border': 'none'
    }

    style_data_conditional_green = [
        {
            'if': {
                'column_id': 'Return',
            },
            'backgroundColor': '#060606',
            'color': 'lime'
        }
    ]

    style_data_conditional_red = [
        {
            'if': {
                'column_id': 'Return',
            },
            'backgroundColor': '#060606',
            'color': 'red'
        }
    ]

    style_table = {
        'height': '300px', 
        'overflowY': 'auto'
        }
    


    """ Layout template which is passed to children = [] in CONTENT and then to app.layout. Function returns layout.  """

    """ Main page layout """
    layout = html.Div(
        [
            dbc.Row(
                [
                    # Col for the table of winners - Col 1 of 4
                    dbc.Col(children=[
                        html.Div("1 Day Winners"),
                        
                        dash_table.DataTable(
                            winners_1d_df.to_dict('records'), 
                            d_columns,
                            style_cell=style_cell,
                            style_data_conditional=style_data_conditional_green,
                            style_header=style_header,
                            style_data=style_data,
                            style_as_list_view=True,
                            style_table=style_table
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
                        html.Div("1 Day Losers"),
                        
                        dash_table.DataTable(
                            losers_1d_df.to_dict('records'), 
                            d_columns,
                            style_cell=style_cell,
                            style_data_conditional=style_data_conditional_red,
                            style_header=style_header,
                            style_data=style_data,
                            style_as_list_view=True,
                            style_table=style_table
                        )
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
                        html.Div("3mo Winners"),
                        
                        dash_table.DataTable(
                            winners_3mo_df.to_dict('records'), 
                            d_columns,
                            style_cell=style_cell,
                            style_data_conditional=style_data_conditional_green,
                            style_header=style_header,
                            style_data=style_data,
                            style_as_list_view=True,
                            style_table=style_table
                        )
                    ]),
                    
                    dbc.Col(children=[
                        html.Div("3mo Losers"),
                        
                        dash_table.DataTable(
                            losers_3mo_df.to_dict('records'), 
                            d_columns,
                            style_cell=style_cell,
                            style_data_conditional=style_data_conditional_red,
                            style_header=style_header,
                            style_data=style_data,
                            style_as_list_view=True,
                            style_table=style_table
                        )
                    ]),

                    dbc.Col(children=[
                        html.Div("52-wk high"),
                        
                        dash_table.DataTable(
                            fifty_two_wk_high_list_df.to_dict('records'), 
                            d_columns,
                            style_cell=style_cell,
                            style_data_conditional=style_data_conditional_red,
                            style_header=style_header,
                            style_data=style_data,
                            style_as_list_view=True,
                            style_table=style_table
                        )
                    ])
                    
                ]
            )
        ]
    )

    return layout


if __name__ == '__main__':
    main()