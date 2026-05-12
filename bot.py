# Moving Average Crossover Bot

import yfinance as yf

stock = "AAPL"

print(f"Fetching data for {stock}...")
data = yf.download(stock, period="1y", interval="1d", progress=False)

print(data.tail())
