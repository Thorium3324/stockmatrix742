import streamlit as st
from datetime import date
import plotly.graph_objects as go
import plotly.express as px
from utils import get_stock_data_cached, get_multiple_stock_data
from portfolio import parse_holdings, calculate_portfolio_value, plot_portfolio_pie
from strategies import sma_crossover

st.set_page_config(page_title="StockMatrix Ultra EVO", layout="wide", page_icon="💹")
st.markdown('<link rel="stylesheet" href="styles.css">', unsafe_allow_html=True)

st.sidebar.title("StockMatrix Ultra EVO 2.0")
tabs = st.sidebar.radio("Sekcje:", ["Analiza Akcji", "Porównanie", "Portfolio", "Symulacje", "Alerty", "Heatmapa"])

# --- Analiza Akcji ---
if tabs == "Analiza Akcji":
    st.title("📈 Analiza Akcji Premium")
    ticker = st.text_input("Symbol:", "AAPL").upper()
    start_date = st.date_input("Start:", date(2023,1,1))
    end_date = st.date_input("End:", date.today())
    if ticker:
        df = get_stock_data_cached(ticker, start_date, end_date)
        if not df.empty:
            show_indicators = st.checkbox("Pokaż wskaźniki techniczne")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="Close", line=dict(color="#0d6efd")))
            if show_indicators:
                fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name="MA20", line=dict(color="orange")))
                fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], name="EMA20", line=dict(color="green")))
                fig.add_trace(go.Scatter(x=df.index, y=df['BB_upper'], name="BB Upper", line=dict(color="red", dash="dot")))
                fig.add_trace(go.Scatter(x=df.index, y=df['BB_lower'], name="BB Lower", line=dict(color="red", dash="dot")))
            st.plotly_chart(fig, use_container_width=True)

# --- Porównanie spółek ---
elif tabs == "Porównanie":
    st.title("📊 Porównanie spółek")
    tickers = st.text_input("Symbole:", "AAPL,MSFT,TSLA").upper().replace(" ","").split(",")
    start_date = st.date_input("Start:", date(2023,1,1), key="comp_start")
    end_date = st.date_input("End:", date.today(), key="comp_end")
    if tickers:
        df_all = get_multiple_stock_data(tickers, start_date, end_date)
        st.line_chart(df_all)

# --- Portfolio ---
elif tabs == "Portfolio":
    st.title("💼 Portfolio")
    portfolio_input = st.text_area("Akcje i ilości:", "AAPL:10,TSLA:5")
    holdings = parse_holdings(portfolio_input)
    if holdings:
        df_portfolio, total_value = calculate_portfolio_value(holdings)
        st.dataframe(df_portfolio.style.format({"Current Price":"${:,.2f}","Value":"${:,.2f}"}))
        st.metric("Łączna wartość portfela", f"${total_value:,.2f}")
        st.plotly_chart(plot_portfolio_pie(df_portfolio), use_container_width=True)

# --- Symulacje ---
elif tabs == "Symulacje":
    st.title("🧪 Backtesting strategii")
    ticker = st.text_input("Symbol do strategii:", "AAPL", key="strategy")
    start_date = st.date_input("Start:", date(2023,1,1), key="str_start")
    end_date = st.date_input("End:", date.today(), key="str_end")
    df = get_stock_data_cached(ticker, start_date, end_date)
    df = sma_crossover(df)
    fig = px.line(df, y='Equity', title=f"SMA Crossover Equity Curve: {ticker}", line_shape="spline")
    st.plotly_chart(fig, use_container_width=True)

# --- Alerty ---
elif tabs == "Alerty":
    st.title("🔔 Alerty")
    alert_ticker = st.text_input("Symbol:", "AAPL")
    alert_price = st.number_input("Cena alertu:", min_value=0.0, value=150.0)
    if st.button("Ustaw alert"):
        st.success(f"Alert ustawiony dla {alert_ticker} przy cenie ${alert_price}")

# --- Heatmapa ---
elif tabs == "Heatmapa":
    st.title("🔥 Heatmapa zmian dziennych")
    tickers = st.text_input("Symbole:", "AAPL,MSFT,TSLA").upper().replace(" ","").split(",")
    df = get_multiple_stock_data(tickers, start=date.today().replace(day=1), end=date.today()).pct_change()
    fig = px.imshow(df.T, text_auto=True, aspect="auto", color_continuous_scale="RdYlGn", origin="lower")
    st.plotly_chart(fig, use_container_width=True)
