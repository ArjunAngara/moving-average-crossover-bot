# Moving Average Crossover Bot

import yfinance as yf

stock = "AAPL"

print(f"Fetching data for {stock}...")
data = yf.download(stock, period="1y", interval="1d", progress=False)

close = data["Close"]
print(f"Got {len(close)} days of price data")
print(f"Latest price: ${round(float(close.iloc[-1]), 2)}")
