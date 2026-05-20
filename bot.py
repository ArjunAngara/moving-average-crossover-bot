# Moving Average Crossover Bot

import yfinance as yf
import pandas as pd

stock = "AAPL"

print(f"Fetching data for {stock}...")
data = yf.download(stock, period="1y", interval="1d", progress=False)

close = data["Close"]

# calculate the 50 and 200 day moving averages
ma50 = close.rolling(window=50).mean()
ma200 = close.rolling(window=200).mean()

# check if 50 day is above or below 200 day
latest_ma50 = float(ma50.iloc[-1])
latest_ma200 = float(ma200.iloc[-1])

if latest_ma50 > latest_ma200:
    print(f"50-day MA ({round(latest_ma50, 2)}) is ABOVE 200-day MA ({round(latest_ma200, 2)})")
    print("Bullish signal")
else:
    print(f"50-day MA ({round(latest_ma50, 2)}) is BELOW 200-day MA ({round(latest_ma200, 2)})")
    print("Bearish signal")
