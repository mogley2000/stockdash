# Code source: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import pandas as pd 


import page_1  # Importing the whole sheet and downloading the df data on app.py startup 
import graph

external_stylesheets = [dbc.themes.CYBORG] #DARKLY

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
                        {'label': '1 day', 'value': '5d'},  # 1d return needs 5d data set to calculate close from day before
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
        return page_1.main(), hidden_style  # first return maps to Output("Page-content"), hidden_style to ("period-selector")
    
    if pathname == '/test':
        return 'Test', hidden_style
    
    else:  # If pathname isn't defined above, assume is stock ticker and calls graph below 
        fig = graph.large_graph(pathname, period_selector)
        info_table = graph.info(pathname)
        # Return below into children tag above 
        return  [
                html.Div([
                html.H1(pathname,
                        style={'textAlign':'center'}),
                dcc.Graph(id='stock-chart',
                    figure = fig
                    )
                ]),
                html.Div([
                    dbc.Row(
                        [
                            # Col for .info table
                        dbc.Col(children=[
                            html.Div("info table"),
                            
                            dash_table.DataTable(
                                info_table.to_dict('records') 
                                # d_columns,
                                # style_cell=style_cell,
                                # style_data_conditional=style_data_conditional_green,
                                # style_header=style_header,
                                # style_data=style_data,
                                # style_as_list_view=True,
                                # style_table=style_table
                            )
                        ])
                    ])
                ])
        ], visible_style

if __name__=='__main__':
    app.run_server(debug=True, port=3000)


