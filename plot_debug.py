import yfinance as yf
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

def get_closing_prices(symbol, period, interval):
    quote = yf.Ticker(symbol)
    hist = quote.history(period, interval)
    return hist["Close"].round(decimals=2)

def main():
    """ Generate basic plt.plot() """

    data = get_closing_prices('AAPL', '6mo', '1d') 

    print(data)
    print()

    print(data.index)

    plt.plot(data.index, data)
    plt.show()

def figure():
    """ Generate plot using figure method """

    data = get_closing_prices('AAPL', '6mo', '1d') 

    fig = Figure(figsize=(5,3))
    ax = fig.subplots()
    ax.plot(data.index, data, label='AAPL')
    ax.set_xticks(data.index)
    ax.set_xticklabels(data.index.strftime('%d/%m'), fontsize=8)
    ax.set_yticklabels(data, fontsize=8)
    ax.set_ylabel('Share price ($)', fontsize='x-small')
    ax.set_xlabel('Date', fontsize='x-small')
    ax.legend(loc='upper left', fontsize='x-small')
    fig.tight_layout()
    
    fig.show()


if __name__ == '__main__':
    figure()

