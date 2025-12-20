import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
#this is for practice

# --------------------------------------------------------
# Page Settings
# --------------------------------------------------------
st.set_page_config(page_title="Real-Time Crypto Dashboard", layout="wide")

# --------------------------------------------------------
# Auto Refresh
# --------------------------------------------------------
refresh_time = st.sidebar.slider("Auto Refresh (seconds)", 120, 240, 80)
st_autorefresh(interval=refresh_time * 1000, key="crypto_dashboard_refresh")

# --------------------------------------------------------
# Header
# --------------------------------------------------------
st.markdown(
    "<h2 style='text-align: center; color: #4CAF50;'>🚀 Real-Time Crypto Dashboard</h2>",
    unsafe_allow_html=True
)
st.markdown("---")

# --------------------------------------------------------
# Yahoo Symbols
# --------------------------------------------------------
st.sidebar.header("🔍 Filters")

crypto_map = {
    "bitcoin": "BTC-USD",
    "ethereum": "ETH-USD",
    "dogecoin": "DOGE-USD",
    "solana": "SOL-USD",
    "cardano": "ADA-USD",
    "xrp": "XRP-USD",
    "toncoin": "TON11466-USD",
    "avalanche": "AVAX-USD",
    "tron": "TRX-USD",
    "polkadot": "DOT-USD"
}

crypto_list = list(crypto_map.keys())
selected_crypto = st.sidebar.selectbox("Select Crypto", crypto_list)

# --------------------------------------------------------
# Currency Selector
# --------------------------------------------------------
currency = st.sidebar.selectbox(
    "Select Currency",
    ["USD", "EUR", "INR", "PKR"],
    index=0
)

yf_symbol = crypto_map[selected_crypto]

# --------------------------------------------------------
# Fetch Live Crypto Price (in USD)
# --------------------------------------------------------
try:
    ticker = yf.Ticker(yf_symbol)
    live = ticker.fast_info

    price_usd = live.last_price
    open_usd = live.open
    day_low_usd = live.day_low
    day_high_usd = live.day_high
    volume_24h = live.last_volume

    change_24h = price_usd - open_usd
    change_percent = (change_24h / open_usd) * 100

except Exception as e:
    st.error(f"⚠ Unable to fetch Yahoo Finance data: {e}")
    st.stop()

# --------------------------------------------------------
# Forex Conversion (using Yahoo Finance)
# --------------------------------------------------------
if currency == "USD":
    fx_rate = 1
else:
    fx_pair = f"{currency}=X"
    try:
        forex = yf.Ticker(fx_pair)
        fx_rate = forex.fast_info.last_price
    except:
        fx_rate = 1
        st.warning(f"⚠ Unable to fetch currency rate for {currency}. Using USD.")

# Convert values
price = price_usd * fx_rate
open_price = open_usd * fx_rate
day_low = day_low_usd * fx_rate
day_high = day_high_usd * fx_rate

# --------------------------------------------------------
# Marquee Ticker
# --------------------------------------------------------
st.markdown(
    f"""
    <marquee width="100%" direction="left">
        🚨 {selected_crypto.capitalize()} Price: {price:,.2f} {currency} |
        24h Change: {change_percent:.2f}%
    </marquee>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------------
# Info Section
# --------------------------------------------------------
st.write(f"📌 **Live data powered by Yahoo Finance — Prices converted to {currency}**")
st.markdown("---")

# --------------------------------------------------------
# KPIs — ROW 1
# --------------------------------------------------------
st.subheader("📊 Market Statistics")

row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)

# --------------------------------------------------------
# KPIs — ROW 1: Price & Open
# --------------------------------------------------------
st.subheader("📊 Market Statistics")

row1_col1, row1_col2 = st.columns(2)
row1_col1.metric("💰 Price", f"{price:,.2f} {currency}", f"{change_percent:.2f}%")
row1_col2.metric("📈 Open", f"{open_price:,.2f} {currency}")

# --------------------------------------------------------
# KPIs — ROW 2: Day Low & Day High
# --------------------------------------------------------
row2_col1, row2_col2 = st.columns(2)
row2_col1.metric("📉 Day Low", f"{day_low:,.2f} {currency}")
row2_col2.metric("📈 Day High", f"{day_high:,.2f} {currency}")

# --------------------------------------------------------
# KPIs — ROW 3: 24h Volume & 24h Change %
# --------------------------------------------------------
row3_col1, row3_col2 = st.columns(2)
row3_col1.metric("📦 24h Volume", f"{volume_24h:,.0f}")
row3_col2.metric("📊 24h Change %", f"{change_percent:.2f}%")


st.markdown("---")

# --------------------------------------------------------
# 30-Day Historical Chart
# --------------------------------------------------------
hist = ticker.history(period="1mo", interval="1d")
hist["Open"] *= fx_rate
hist["High"] *= fx_rate
hist["Low"] *= fx_rate
hist["Close"] *= fx_rate

st.subheader(f"📉 30-Day Price Chart - {selected_crypto.capitalize()} ({currency})")

fig = go.Figure(data=[
    go.Candlestick(
        x=hist.index,
        open=hist["Open"],
        high=hist["High"],
        low=hist["Low"],
        close=hist["Close"],
        name="Price"
    )
])

# Moving Averages
hist["MA7"] = hist["Close"].rolling(7).mean()
hist["MA25"] = hist["Close"].rolling(25).mean()

fig.add_trace(go.Scatter(x=hist.index, y=hist["MA7"], mode="lines", name="MA7"))
fig.add_trace(go.Scatter(x=hist.index, y=hist["MA25"], mode="lines", name="MA25"))

fig.update_layout(height=450)

st.plotly_chart(fig, use_container_width=True)
