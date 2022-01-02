import dash 
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import yfinance as yf 


app = dash.Dash(__name__)  # Instantiate Dash app 

# Yfinance module
def get_closing_prices(symbol, period, interval):
    quote = yf.Ticker(symbol)
    hist = quote.history(period, interval)
    return pd.DataFrame(hist["Close"].round(decimals=2))



# stock_period = '3mo'
# stock_interval = '1d'

# if stock_period == '3mo':
#     tickformat_var = '%b'
#     dtick_var = 'M1'
# elif stock_period == '1mo':
#     tickformat_var = '%d %b'
#     dtick_var = 'D1'

def plot_graph(stock_ticker, stock_period, stock_interval): 
    """Plot graph in matplotlib. Function is called into app.py. 
    Master Figure changes done here 
    """
    # Call yf func and populate df 
    df = get_closing_prices(stock_ticker, stock_period, stock_interval) 

    last_price = df.iloc[-1, 0] # Separates thousands with , and 2 decimal places 

    colors = {
        'background': '#111111',
        'text': 'white'
    }

    fig = px.line(df, 
                x=df.index, y=df['Close'], 
                title=stock_ticker,
                template="plotly_dark",
                color_discrete_sequence=['lime'],
                labels = {'Date': ''}
            
                )

    fig.update_xaxes(
        dtick='M1',
        tickformat='%b',
        showgrid=False,
        
    )

    # fig.for_each_trace(lambda trace: trace.update(fillcolor = 'rgba(50, 205, 50, 0.25)'))

    fig.update_yaxes(
        showgrid=False,
        visible=False
    )

    fig.add_annotation(dict(font=dict(color='white',size=40, family='Arial Black'),
        x=0,
        y=1.2,
        showarrow=False,
        text=str(last_price),
        textangle=0,
        xanchor='left',
        xref="paper",
        yref="paper")
    )

    
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        title={      
            'y':0.85,
            'x':0.93,
            'xanchor': 'center',
            'yanchor': 'top'}
    )

    # Main app layout 

    app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H1(
            children='Hello Dash',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.Div(children='Dash: A web application framework for your data.', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

        dcc.Graph(
            id='example-graph-2',
            figure=fig
        )
    ])


    # Launch server 
    if __name__ == '__main__':
        app.run_server(debug=True)


# Call plot_graph func for stock tickers 
NVDA = plot_graph('NVDA', '3mo', '1d')