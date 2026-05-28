# Moving Average Crossover Bot

import yfinance as yf
import pandas as pd

stock = "AAPL"

print(f"Fetching data for {stock}...")
data = yf.download(stock, period="2y", interval="1d", progress=False)

close = data["Close"]

# calculate the 50 and 200 day moving averages
ma50 = close.rolling(window=50).mean()
ma200 = close.rolling(window=200).mean()

signals = []

for i in range(1, len(close)):
    if ma50.iloc[i] > ma200.iloc[i] and ma50.iloc[i-1] <= ma200.iloc[i-1]:
        signals.append({"Date": close.index[i].date(), "Signal": "BUY", "Price": round(float(close.iloc[i]), 2)})
    elif ma50.iloc[i] < ma200.iloc[i] and ma50.iloc[i-1] >= ma200.iloc[i-1]:
        signals.append({"Date": close.index[i].date(), "Signal": "SELL", "Price": round(float(close.iloc[i]), 2)})

# convert signals list into a dataframe
df = pd.DataFrame(signals)
print(df)

