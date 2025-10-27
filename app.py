import streamlit as st
from datetime import date
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils import get_stock_data
from portfolio import parse_holdings, calculate_portfolio_value
from strategies import sma_crossover

st.set_page_config(page_title="StockMatrix Ultimate EVO", layout="wide", page_icon="💹")
st.markdown('<link rel="stylesheet" href="styles.css">', unsafe_allow_html=True)

# Sidebar
st.sidebar.image("assets/logo.png", use_column_width=True)
st.sidebar.title("StockMatrix EVO 5873487 + Hybrid")
tabs = st.sidebar.radio("Sekcje:", ["Analiza Akcji", "Porównanie Spółek", "Portfolio", "Symulacje", "Alerty", "Heatmapa"])

# --- Analiza Akcji ---
if tabs == "Analiza Akcji":
    st.title("📈 Analiza Akcji Premium")
    ticker = st.text_input("Symbol spółki:", "AAPL").upper()
    start_date = st.date_input("Data początkowa:", date(2023,1,1))
    end_date = st.date_input("Data końcowa:", date.today())

    if ticker:
        df = get_stock_data(ticker, start_date, end_date)
        if not df.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="Close"))
            fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name="MA20"))
            fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], name="EMA20"))
            fig.add_trace(go.Scatter(x=df.index, y=df['BB_upper'], name="BB Upper"))
            fig.add_trace(go.Scatter(x=df.index, y=df['BB_lower'], name="BB Lower"))
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Wskaźniki techniczne")
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=df.index, y=df['RSI'], name="RSI"))
            fig2.add_trace(go.Scatter(x=df.index, y=df['MACD'], name="MACD"))
            fig2.add_trace(go.Scatter(x=df.index, y=df['MACD_signal'], name="MACD Signal"))
            st.plotly_chart(fig2, use_container_width=True)

# --- Porównanie Spółek ---
elif tabs == "Porównanie Spółek":
    st.title("📊 Porównanie Spółek")
    tickers = st.text_input("Symbole (oddzielone przecinkami):", "AAPL,MSFT,TSLA").upper().replace(" ","").split(",")
    start_date = st.date_input("Start:", date(2023,1,1), key="comp_start")
    end_date = st.date_input("End:", date.today(), key="comp_end")
    df_all = pd.DataFrame()
    for t in tickers:
        df_all[t] = get_stock_data(t, start_date, end_date)['Close']
    st.line_chart(df_all)

# --- Portfolio ---
elif tabs == "Portfolio":
    st.title("💼 Portfolio Premium")
    portfolio_input = st.text_area("Wprowadź akcje i ilości (AAPL:10,TSLA:5):", "AAPL:10,TSLA:5")
    holdings = parse_holdings(portfolio_input)
    if holdings:
        df_portfolio, total_value = calculate_portfolio_value(holdings)
        st.dataframe(df_portfolio.style.format({"Current Price":"${:,.2f}","Value":"${:,.2f}"}))
        st.metric("Łączna wartość portfela", f"${total_value:,.2f}")

# --- Symulacje ---
elif tabs == "Symulacje":
    st.title("🧪 Backtesting Strategii")
    ticker = st.text_input("Symbol do strategii:", "AAPL", key="strategy")
    start_date = st.date_input("Start:", date(2023,1,1), key="str_start")
    end_date = st.date_input("End:", date.today(), key="str_end")
    df = get_stock_data(ticker, start_date, end_date)
    df = sma_crossover(df)
    fig = px.line(df, y='Equity', title=f"SMA Crossover Equity Curve: {ticker}")
    st.plotly_chart(fig, use_container_width=True)

# --- Alerty ---
elif tabs == "Alerty":
    st.title("🔔 Alerty Premium")
    alert_ticker = st.text_input("Symbol:", "AAPL")
    alert_price = st.number_input("Cena alertu:", min_value=0.0, value=150.0)
    if st.button("Ustaw alert"):
        st.success(f"Alert ustawiony dla {alert_ticker} przy cenie ${alert_price}")

# --- Heatmapa ---
elif tabs == "Heatmapa":
    st.title("🔥 Heatmapa zmian dziennych")
    tickers = st.text_input("Symbole:", "AAPL,MSFT,TSLA").upper().replace(" ","").split(",")
    df = pd.DataFrame()
    for t in tickers:
        df[t] = get_stock_data(t, start_date=date.today().replace(day=1), end=date.today())['Close'].pct_change()
    import seaborn as sns
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    sns.heatmap(df.T, annot=True, cmap="RdYlGn", center=0, ax=ax)
    st.pyplot(fig)
