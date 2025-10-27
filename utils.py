import streamlit as st
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.volatility import BollingerBands

@st.cache_data(ttl=3600)
def get_stock_data_cached(ticker, start, end):
    """
    Pobiera dane akcji i oblicza wskaźniki techniczne.
    Bezpieczne dla pojedynczych i wielu tickerów.
    """
    df = yf.download(ticker, start=start, end=end)
    if df.empty:
        return df

    # upewnij się, że Close jest 1D Series
    close_series = df['Close']
    if isinstance(close_series, pd.DataFrame):
        close_series = close_series.iloc[:,0]

    df['MA20'] = SMAIndicator(close_series, 20).sma_indicator()
    df['EMA20'] = EMAIndicator(close_series, 20).ema_indicator()
    df['RSI'] = RSIIndicator(close_series, 14).rsi()
    macd = MACD(close_series)
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()
    bb = BollingerBands(close_series, window=20, window_dev=2)
    df['BB_upper'] = bb.bollinger_hband()
    df['BB_lower'] = bb.bollinger_lband()
    return df

@st.cache_data(ttl=3600)
def get_multiple_stock_data(tickers, start, end):
    """
    Pobiera ceny Close dla wielu tickerów.
    """
    df_all = yf.download(tickers, start=start, end=end)['Close']
    # jeśli tylko jeden ticker, wymuszenie Series
    if isinstance(df_all, pd.Series):
        df_all = df_all.to_frame()
    return df_all
