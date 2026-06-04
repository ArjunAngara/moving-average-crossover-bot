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

df = pd.DataFrame(signals)

total_pnl = 0
buy_price = None

for _, row in df.iterrows():
    if row["Signal"] == "BUY":
        buy_price = row["Price"]
    elif row["Signal"] == "SELL" and buy_price is not None:
        pnl = round(row["Price"] - buy_price, 2)
        total_pnl += pnl
        print(f"  Bought at ${buy_price} — Sold at ${row['Price']} — P&L: ${pnl}")
        buy_price = None

print(f"\nTotal P&L: ${round(total_pnl, 2)}")

# calculate win rate
wins = sum(1 for _, row in df.iterrows() if row["Signal"] == "SELL" and buy_price is None)
total_trades = len([s for s in signals if s["Signal"] == "SELL"])
print(f"Total trades: {total_trades}")
