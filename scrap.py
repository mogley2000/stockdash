import yfinance as yf


quote = yf.Ticker('AAPL')
hist = quote.history('6mo', '1d')
df = hist.iloc[-1, 3]
print(df)



