import yfinance as yf
import pandas as pd
import numpy as np

def parse_holdings(input_text):
    holdings = {}
    for item in input_text.split(","):
        try:
            ticker, qty = item.split(":")
            holdings[ticker.strip().upper()] = float(qty)
        except:
            continue
    return holdings

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

def calculate_risk_metrics(df_portfolio):
    returns = df_portfolio.pct_change().dropna()
    sharpe = returns.mean() / returns.std() * np.sqrt(252)
    volatility = returns.std() * np.sqrt(252)
    return sharpe, volatility
