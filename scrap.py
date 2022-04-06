import yfinance as yf

from page_1 import TICKERS


# msft = yf.Ticker('MSFT')
# history = msft.history()
# info = msft.info
# 

TICKERS = ['NVDA', 'MSFT', 'GOOG', 'TWLO', 'NET']


# close = download['NET']['Close']
# gain = close.iloc[0]
# last = close.iloc[-1]

download_1d = yf.download(TICKERS, period='1d', interval='1d', group_by='ticker', threads=True)
download_5d = yf.download(TICKERS, period='5d', interval='1d', group_by='ticker', threads=True)
download_3mo = yf.download(TICKERS, period='3mo', interval='1d', group_by='ticker', threads=True)
download_6mo = yf.download(TICKERS, period='6mo', interval='1d', group_by='ticker', threads=True)



def gain_loss(data_set, ticker, period):
    """ Calc gain loss """
    close = data_set[ticker]['Close']
    
    if period == '1d':
        first_close = close.iloc[-2]
    else:
        first_close = close.iloc[0]
    
    latest_close = close.iloc[-1]

    gain_loss = latest_close / first_close - 1
    
    return gain_loss


# print(download_3mo['NVDA'])
# print(gain_loss(download_3mo, 'NVDA', '3mo'))

# print(download_1d['NVDA'])
# print(gain_loss(download_1d, 'NVDA', '1d'))

data = download_3mo['NVDA']
print(data)
print(gain_loss(download_3mo, 'NVDA', '3mo'))

for ticker in TICKERS:
    print(gain_loss(download_3mo, ticker, '3mo'))


