# 🔥 Real-Time Crypto Dashboard

A live cryptocurrency tracking dashboard built with **Python** and **Streamlit**. This application fetches real-time market data from **Yahoo Finance** and visualizes it using interactive **Plotly** charts.

It is designed to help users track price trends, analyze volatility with Bollinger Bands, and monitor key metrics for top cryptocurrencies like Bitcoin (BTC) and Ethereum (ETH).

## ✨ Key Features
* **📡 Live Data:** Fetches real-time crypto prices using the `yfinance` library.
* **📊 Interactive Charts:**
    * **Candlestick Charts:** For detailed price tracking (Open, High, Low, Close).
    * **Bollinger Bands:** To visualize market volatility.
* **⚡ Auto-Refresh:** Dashboard updates automatically every 30 seconds (Live Mode).
* **🎛️ User Controls:** Filter by Coin (BTC, ETH, SOL) and Time Range (1 Day, 1 Month, 1 Year).
* **📈 Key Metrics:** Displays current price, price change ($ and %), and high/lows.

## 🛠️ Tech Stack
* **Language:** [Python 3.10+](https://www.python.org/)
* **Frontend:** [Streamlit](https://streamlit.io/)
* **Data Source:** [YFinance](https://pypi.org/project/yfinance/)
* **Visualization:** [Plotly](https://plotly.com/python/)
* **Data Manipulation:** [Pandas](https://pandas.pydata.org/)

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/crypto-dashboard.git](https://github.com/your-username/crypto-dashboard.git)
cd crypto-dashboard
