import yfinance as yf
import pandas as pd
import logging
import datetime

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

""" List of tickers to analyse """
tickers = [
    'NVDA',
    'MSFT',
    'TWLO',
    'U',
    'NET'
]

""" Get 52 week high """
end = datetime.datetime.now()
start = end - datetime.timedelta(weeks=52)

for t in tickers:
    ticker = yf.Ticker()
logging.debug(msft.financials)

