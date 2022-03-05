# Code source: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/

import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import yfinance as yf

import page_1

external_stylesheets = [dbc.themes.CYBORG] #DARKLY

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    # "background-color": "#4C4C4C",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#060606"
}

SIDEBAR = html.Div(
    [
        html.H2("Sidebard / Stocks", className="display-4"),
        html.Hr(),
        html.P(
            "Number of students per education level", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Test", href="/test", active="exact"),
                dbc.NavLink("NVDA", href="/NVDA", active="exact"),
                dbc.NavLink("MSFT", href="/MSFT", active="exact"),
                dbc.NavLink("AAPL", href="/AAPL", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


CONTENT = html.Div(id="page-content", children=[], style=CONTENT_STYLE)  # Graph goes inside children via call back 

CALLBACK = html.Div([   
                dcc.RadioItems(
                    id='period-selector',
                    options = [
                        {'label': '1 mth', 'value': '1mo'},
                        {'label': '3 mth', 'value': '3mo'},
                        {'label': '6 mth', 'value': '6mo'},
                        {'label': '1 yr', 'value': '1y'},
                        {'label': '5 yr', 'value': '5y'}
                    ],
                    value = "6mo",

                    #labelStyle is done in CSS 
                    labelStyle={
                        'textAlign': 'center',
                        'display': 'inline-block', 
                        'color': 'white',
                        'font-family': 'Arial',
                        'font-size' : '15px',
                        'padding-right': '30px'
                    },

                    style={
                        'textAlign': 'center'
                    }
                )
                ])

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    SIDEBAR,
    CONTENT,
    CALLBACK
])



""" Plotly graph """
@app.callback(
    Output("page-content", "children"),
    Output("period-selector", "style"),
    Input("url", "pathname"),
    Input('period-selector', 'value')
)

def render_page_content(pathname, period_selector):
    """ App routing from sidebar to content depending on path """

    hidden_style = {'display': 'none'}
    #  It would be best to make visible_style a module level variable.
    #  Use it for both the app layout and this callback function.
    #  That way if you want to change its location or look you only have to edit one location.
    visible_style = {'textAlign': 'center'} 

    if pathname == '/':
        return page_1.layout, hidden_style
    
    if pathname == '/test':
        return 'Test', hidden_style
    
    else:  # If pathname isn't defined above, assume is stock ticker and calls graph below 
        interval = '1d'

        quote = yf.Ticker(pathname)
        hist = quote.history(period_selector, interval)
        df = hist.round(decimals=2)
        
        last_price = df.iloc[-1, 0] # return first row (-1)

        #Performance over period calc
        performance_calc = ((df.iloc[-1, 0] / df.iloc[0, 0]) - 1) * 100
        if performance_calc >= 0:
            performance = '+' + str(round(performance_calc,2))
        else:
            performance = str(round(performance_calc,2))
        
        #Define color of performance % 
        performance_int = (round(performance_calc,2))
        
        if performance_int >= 0:
            perf_color = 'lime'
        else:
            perf_color = 'red'
        
        fig = px.line(df, 
            x=df.index, y=df["Close"], 
            title='NVDA',
            template="plotly_dark",
            color_discrete_sequence=['lime'],
            labels = {'Date': ''}
            )
        
        if interval == '1mo':
            d_tick='604800000'  #7 days in milliseconds. Datetime format requires ms input. 
        elif interval == '5y':
            d_tick = 'M12'
        else:
            d_tick='M1'

        fig.update_xaxes(
            dtick=d_tick,
            showgrid=False,            
        )

        fig.update_yaxes(
            showgrid=False,
            visible=False
        )
        #Last price annotation 
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

        #Performance annotation 
        fig.add_annotation(dict(font=dict(color=perf_color,size=25, family='Arial'),
            x=0.14,
            y=1.12,
            showarrow=False,
            text=str(performance) + '%',
            textangle=0,
            xanchor='left',
            xref="paper",
            yref="paper")
        )

        fig.update_traces(hovertemplate=None)
        
        fig.update_layout(
            plot_bgcolor='#060606',
            paper_bgcolor='#060606',
            font_color='white',
            title=dict(   
                y = 0.82,  #Adjust location of stock ticker title 
                x = 0.92,
                xanchor = 'center',
                yanchor = 'top',
                font=dict(
                    family="Arial",
                    size=25,
                    color='white'
                    )
            ),
            hovermode = 'x',
            # xaxis_tickformat = '%b'
        )

        # Return below into children tag above 
        return [
                html.H1(pathname,
                        style={'textAlign':'center'}),
                dcc.Graph(id='stock-chart',
                    figure = fig
                    )
                ], visible_style

if __name__=='__main__':
    app.run_server(debug=True, port=3000)