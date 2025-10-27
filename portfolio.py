import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

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
    tickers = list(holdings.keys())
    data = yf.download(tickers, period="1d")['Close'].iloc[-1]
    df_portfolio = pd.DataFrame()
    total_value = 0
    for ticker, qty in holdings.items():
        price = data[ticker]
        df_portfolio.loc[ticker, 'Quantity'] = qty
        df_portfolio.loc[ticker, 'Current Price'] = price
        df_portfolio.loc[ticker, 'Value'] = qty * price
        total_value += qty * price
    return df_portfolio, total_value

def plot_portfolio_pie(df_portfolio):
    fig = px.pie(df_portfolio, names=df_portfolio.index, values='Value',
                 color_discrete_sequence=px.colors.sequential.Viridis,
                 title="Udział akcji w portfelu")
    return fig
