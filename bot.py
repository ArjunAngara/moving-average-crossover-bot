# Moving Average Crossover Bot

import yfinance as yf
import pandas as pd

stock = "AAPL"

print(f"Fetching data for {stock}...")
data = yf.download(stock, period="1y", interval="1d", progress=False)

close = data["Close"]

# calculate the 50 day moving average
ma50 = close.rolling(window=50).mean()

print("50-day moving average (last 5 days):")
print(ma50.tail())
