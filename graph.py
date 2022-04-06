import yfinance as yf
import plotly.express as px

def large_graph(pathname, period_selector):
    """ Main plotly graph  """
    interval = '1d'

    quote = yf.Ticker(pathname)
    hist = quote.history(period_selector, interval)
    df = hist.round(decimals=2)
    
    last_price = df.iloc[-1, 3] # return first row (-1)

    #Performance over period calc
    if period_selector == '5d':
        performance_calc = ((df.iloc[-1, 3] / df.iloc[-2, 3] - 1)) * 100 
    else:
        performance_calc = ((df.iloc[-1, 3] / df.iloc[0, 3]) - 1) * 100
    
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
        color_discrete_sequence=[perf_color],
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

    return fig 


def sparkline_graph(pathname, period_selector):
    """ Sparkline graph  """
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
        title=pathname,
        template="plotly_dark",
        color_discrete_sequence=[perf_color],
        labels = {'Date': ''},
        height=75,
        width=200
        )
    
    if interval == '1mo':
        d_tick='604800000'  #7 days in milliseconds. Datetime format requires ms input. 
    elif interval == '5y':
        d_tick = 'M12'
    else:
        d_tick='M1'

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)

    fig.update_layout(annotations=[], overwrite=True)

    fig.update_traces(hovertemplate=None)
    
    fig.update_layout(
        showlegend=False,
        margin=dict(t=10,l=10,b=10,r=10),
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
                ))
        )

    return fig 