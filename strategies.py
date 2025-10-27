import pandas as pd
import numpy as np

def sma_crossover(df, short_window=20, long_window=50):
    df['SMA_short'] = df['Close'].rolling(short_window).mean()
    df['SMA_long'] = df['Close'].rolling(long_window).mean()
    df['Signal'] = 0
    df['Signal'][short_window:] = np.where(df['SMA_short'][short_window:] > df['SMA_long'][short_window:], 1, -1)
    df['Equity'] = (df['Signal'].shift(1) * df['Close'].pct_change()).cumsum()
    return df
