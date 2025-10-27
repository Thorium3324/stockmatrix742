import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator, EMAIndicator
from ta.volatility import BollingerBands

def get_stock_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    if not df.empty:
        df['MA20'] = SMAIndicator(df['Close'], 20).sma_indicator()
        df['EMA20'] = EMAIndicator(df['Close'], 20).ema_indicator()
        df['RSI'] = RSIIndicator(df['Close'], 14).rsi()
        macd = MACD(df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_signal'] = macd.macd_signal()
        bb = BollingerBands(df['Close'], window=20, window_dev=2)
        df['BB_upper'] = bb.bollinger_hband()
        df['BB_lower'] = bb.bollinger_lband()
    return df
