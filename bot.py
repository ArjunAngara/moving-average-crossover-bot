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
trades = []

for _, row in df.iterrows():
    if row["Signal"] == "BUY":
        buy_price = row["Price"]
    elif row["Signal"] == "SELL" and buy_price is not None:
        pnl = round(row["Price"] - buy_price, 2)
        total_pnl += pnl
        trades.append(pnl)
        buy_price = None

wins = len([t for t in trades if t > 0])
losses = len([t for t in trades if t <= 0])
win_rate = round((wins / len(trades)) * 100, 2) if trades else 0
avg_win = round(sum(t for t in trades if t > 0) / wins, 2) if wins > 0 else 0
avg_loss = round(sum(t for t in trades if t <= 0) / losses, 2) if losses > 0 else 0

# calculate risk reward ratio
risk_reward = round(abs(avg_win / avg_loss), 2) if avg_loss != 0 else 0

print(f"Total P&L: ${round(total_pnl, 2)}")
print(f"Total Trades: {len(trades)}")
print(f"Wins: {wins} — Losses: {losses}")
print(f"Win Rate: {win_rate}%")
print(f"Average Win: ${avg_win}")
print(f"Average Loss: ${avg_loss}")
print(f"Risk/Reward Ratio: {risk_reward}")
