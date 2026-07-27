# Moving Average Crossover Bot

import yfinance as yf
import pandas as pd
import os
import datetime
import statistics


def get_stock_data(stock, period="2y"):
    print(f"Fetching {period} of data for {stock}...")
    data = yf.download(stock, period=period, interval="1d", progress=False)
    return data["Close"]


def calculate_signals(close, short_window=50, long_window=200):
    ma_short = close.rolling(window=short_window).mean()
    ma_long = close.rolling(window=long_window).mean()

    signals = []
    for i in range(1, len(close)):
        if ma_short.iloc[i] > ma_long.iloc[i] and ma_short.iloc[i-1] <= ma_long.iloc[i-1]:
            signals.append({"Date": close.index[i].date(), "Signal": "BUY", "Price": round(float(close.iloc[i]), 2)})
        elif ma_short.iloc[i] < ma_long.iloc[i] and ma_short.iloc[i-1] >= ma_long.iloc[i-1]:
            signals.append({"Date": close.index[i].date(), "Signal": "SELL", "Price": round(float(close.iloc[i]), 2)})
    return pd.DataFrame(signals)


def calculate_pnl(df):
    total_pnl = 0
    buy_price = None
    buy_date = None  # bug: storing buy date but never using it correctly
    trades = []

    for _, row in df.iterrows():
        if row["Signal"] == "BUY":
            buy_price = row["Price"]
            buy_date = row["Date"]
        elif row["Signal"] == "SELL" and buy_price is not None:
            pnl = round(row["Price"] - buy_price, 2)
            total_pnl += pnl
            # bug: appending buy_date instead of sell date for the trade record
            trades.append({"Date": buy_date, "PnL": pnl, "Buy": buy_price, "Sell": row["Price"]})
            buy_price = None

    return trades, round(total_pnl, 2)


def calculate_sharpe(trades, risk_free_rate=0.05):
    pnls = [t["PnL"] for t in trades]
    if len(pnls) < 2:
        return 0
    avg_return = sum(pnls) / len(pnls)
    std_return = statistics.stdev(pnls)
    return round((avg_return - risk_free_rate) / std_return, 2) if std_return != 0 else 0


def save_csv(df, stock):
    os.makedirs("output", exist_ok=True)
    filename = datetime.datetime.now().strftime(f"{stock}_signals_%Y%m%d_%H%M%S.csv")
    filepath = os.path.join("output", filename)
    df.to_csv(filepath, index=False)


def print_summary(stock, trades, total_pnl):
    wins = len([t for t in trades if t["PnL"] > 0])
    losses = len([t for t in trades if t["PnL"] <= 0])
    win_rate = round((wins / len(trades)) * 100, 2) if trades else 0
    avg_win = round(sum(t["PnL"] for t in trades if t["PnL"] > 0) / wins, 2) if wins > 0 else 0
    avg_loss = round(sum(t["PnL"] for t in trades if t["PnL"] <= 0) / losses, 2) if losses > 0 else 0
    risk_reward = round(abs(avg_win / avg_loss), 2) if avg_loss != 0 else 0
    sharpe = calculate_sharpe(trades)

    print("=" * 40)
    print(f"BACKTEST RESULTS — {stock}")
    print("=" * 40)
    print(f"Total Trades: {len(trades)}")
    print(f"Wins: {wins} — Losses: {losses}")
    print(f"Win Rate: {win_rate}%")
    print(f"Average Win: ${avg_win}")
    print(f"Average Loss: ${avg_loss}")
    print(f"Risk/Reward Ratio: {risk_reward}")
    print(f"Sharpe Ratio: {sharpe}")
    print(f"Total P&L: ${total_pnl}")


stocks = ["AAPL", "MSFT", "TSLA", "NVDA", "SPY"]
best_stock = None
best_pnl = float("-inf")
all_results = []

for stock in stocks:
    close = get_stock_data(stock)
    df = calculate_signals(close, short_window=50, long_window=200)
    trades, total_pnl = calculate_pnl(df)
    save_csv(df, stock)
    print_summary(stock, trades, total_pnl)
    print()

    wins = len([t for t in trades if t["PnL"] > 0])
    sharpe = calculate_sharpe(trades)
    all_results.append({
        "Stock": stock,
        "Total P&L": total_pnl,
        "Trades": len(trades),
        "Wins": wins,
        "Losses": len(trades) - wins,
        "Sharpe Ratio": sharpe
    })

    if total_pnl > best_pnl:
        best_pnl = total_pnl
        best_stock = stock

summary_df = pd.DataFrame(all_results)
summary_df.to_csv("output/summary.csv", index=False)
print(f"Best performing stock: {best_stock} with total P&L of ${best_pnl}")
