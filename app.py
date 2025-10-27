import streamlit as st
from datetime import date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import get_stock_data, parse_holdings, calculate_portfolio_value

# --- Konfiguracja ---
st.set_page_config(page_title="StockMatrix", layout="wide", page_icon="💹")
st.markdown('<link rel="stylesheet" href="styles.css">', unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.image("assets/logo.png", use_column_width=True)
st.sidebar.title("StockMatrix")
tabs = st.sidebar.radio("Sekcje:", ["Analiza Akcji", "Porównanie Spółek", "Portfolio", "Symulacje", "Alerty"])

# --- Analiza Akcji ---
if tabs == "Analiza Akcji":
    st.title("📈 Analiza Akcji")
    ticker = st.text_input("Symbol spółki:", "AAPL").upper()
    start_date = st.date_input("Data początkowa:", date(2023, 1, 1))
    end_date = st.date_input("Data końcowa:", date.today())

    if ticker:
        df = get_stock_data(ticker, start_date, end_date)
        if not df.empty:
            st.subheader(f"Wykres cenowy {ticker}")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="Close"))
            fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name="MA20"))
            fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], name="MA50"))
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Wskaźniki techniczne")
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=df.index, y=df['RSI'], name="RSI"))
            fig2.add_trace(go.Scatter(x=df.index, y=df['MACD'], name="MACD"))
            fig2.add_trace(go.Scatter(x=df.index, y=df['MACD_signal'], name="MACD Signal"))
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("Brak danych dla podanego symbolu.")

# --- Porównanie Spółek ---
elif tabs == "Porównanie Spółek":
    st.title("📊 Porównanie Spółek")
    tickers = st.text_input("Symbole spółek (oddzielone przecinkami):", "AAPL,MSFT,TSLA").upper().replace(" ", "").split(",")
    start_date = st.date_input("Data początkowa:", date(2023, 1, 1), key="comp_start")
    end_date = st.date_input("Data końcowa:", date.today(), key="comp_end")

    if tickers:
        df_all = pd.DataFrame()
        for t in tickers:
            df_all[t] = get_stock_data(t, start_date, end_date)['Close']
        st.line_chart(df_all)

# --- Portfolio ---
elif tabs == "Portfolio":
    st.title("💼 Portfolio")
    portfolio_input = st.text_area("Wprowadź swoje akcje i ilość (np. AAPL:10, TSLA:5):", "AAPL:10, TSLA:5")
    holdings = parse_holdings(portfolio_input)
    if holdings:
        df_portfolio, total_value = calculate_portfolio_value(holdings)
        st.dataframe(df_portfolio.style.format({"Current Price": "${:,.2f}", "Value": "${:,.2f}"}))
        st.metric("Łączna wartość portfela", f"${total_value:,.2f}")

# --- Symulacje ---
elif tabs == "Symulacje":
    st.title("🧪 Symulacje Strategii")
    st.info("Możesz testować strategie np. średnie kroczące, RSI, MACD.")

# --- Alerty ---
elif tabs == "Alerty":
    st.title("🔔 Alerty")
    alert_ticker = st.text_input("Symbol:", "AAPL")
    alert_price = st.number_input("Cena alertu:", min_value=0.0, value=150.0)
    if st.button("Ustaw alert"):
        st.success(f"Alert ustawiony dla {alert_ticker} przy cenie ${alert_price}")
