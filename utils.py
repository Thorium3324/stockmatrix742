import yfinance as yf
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator

def get_stock_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    if not df.empty:
        df['MA20'] = df['Close'].rolling(20).mean()
        df['MA50'] = df['Close'].rolling(50).mean()
        df['RSI'] = RSIIndicator(df['Close'], window=14).rsi()
        macd = MACD(df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_signal'] = macd.macd_signal()
    return df

def calculate_portfolio_value(holdings):
    df_portfolio = pd.DataFrame()
    total_value = 0
    for ticker, qty in holdings.items():
        price = yf.Ticker(ticker).history(period="1d")['Close'][-1]
        df_portfolio.loc[ticker, 'Quantity'] = qty
        df_portfolio.loc[ticker, 'Current Price'] = price
        df_portfolio.loc[ticker, 'Value'] = qty * price
        total_value += qty * price
    return df_portfolio, total_value

def parse_holdings(input_text):
    # np. "AAPL:10, TSLA:5"
    holdings = {}
    for item in input_text.split(","):
        try:
            ticker, qty = item.split(":")
            holdings[ticker.strip().upper()] = float(qty)
        except:
            continue
    return holdings
