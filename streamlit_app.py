import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from app.indicators import calculate_sma, calculate_rsi
from app.ml_model import predict_trend
from app.ai_explainer import generate_ai_explanation


st.set_page_config(page_title="AI Stock Analysis Platform", layout="wide")
st.title("📈 AI-Powered Stock Analysis Platform")

st.sidebar.header("⚙️ Analysis Settings")

analysis_mode = st.sidebar.radio(
    "Analysis Mode",
    ["Short-term ML (Recommended)", "Intraday (1 Day View)"]
)

sma_window = st.sidebar.slider("SMA Window", 10, 50, 20)
rsi_window = st.sidebar.slider("RSI Window", 7, 30, 14)

# Fixed interval
interval = "5m"

# Period logic
if analysis_mode == "Intraday (1 Day View)":
    period = "1d"
else:
    period = "5d"


# -------------------------------
# Stock symbol input
# -------------------------------
symbol = st.text_input(
    "Enter Stock Symbol (e.g. AAPL, MSFT, RELIANCE.NS)",
    value="MSFT"
)


# -------------------------------
# Cached data loader
# -------------------------------
@st.cache_data(ttl=300)
def load_stock_data(symbol, period, interval):
    data = yf.download(
        tickers=symbol,
        period=period,
        interval=interval,
        progress=False
    )

    # Fix columns
    if not data.empty and isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # FALLBACK FOR INTRADAY
    if data.empty and period == "1d":
        fallback_data = yf.download(
            tickers=symbol,
            period="5d",
            interval=interval,
            progress=False
        )

        if not fallback_data.empty:
            if isinstance(fallback_data.columns, pd.MultiIndex):
                fallback_data.columns = fallback_data.columns.get_level_values(0)

            return fallback_data.dropna()

    return data.dropna()

if st.button("Analyze"):
    with st.spinner("Fetching data and running analysis..."):

        # 1. Fetch data
        data = load_stock_data(symbol, period, interval)

        if data.empty:
            st.error("No data found for this symbol.")
            st.stop()

        if analysis_mode == "Intraday (1 Day View)" and period == "1d":
            st.info(
                "Intraday data may be unavailable outside market hours. "
                "Showing recent data instead."
            )
        # 2. Indicators (MUST come before ML / fallback)
        data["SMA"] = calculate_sma(data["Close"], sma_window)
        data["RSI"] = calculate_rsi(data["Close"], rsi_window)

        # Drop NaNs after indicators
        data = data.dropna()
        if data.empty:
            st.warning(
                "Not enough data after applying indicators. "
                "Try reducing indicator window sizes or switching mode."
            )
            st.stop()

        # 3. ML prediction
        trend, confidence = predict_trend(data)

        # 4. Rule-based fallback
        if trend is None:
            latest = data.iloc[-1]

            if latest["Close"] > latest["SMA"]:
                trend = "UP"
            else:
                trend = "DOWN"

            confidence = 0.55

            st.info(
                "ML model did not have enough data. "
                "Showing rule-based trend using technical indicators."
            )

        # 5. AI explanation
        latest_row = data.iloc[-1]
        ai_explanation = generate_ai_explanation(
            symbol,
            trend,
            confidence,
            latest_row
        )

        # 6. Plotly chart
        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.08,
            row_heights=[0.7, 0.3],
            subplot_titles=("Price & SMA", "RSI")
        )

        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                name="Price"
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["SMA"],
                mode="lines",
                name=f"SMA {sma_window}"
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["RSI"],
                mode="lines",
                name=f"RSI {rsi_window}"
            ),
            row=2, col=1
        )

        fig.update_layout(
            xaxis_rangeslider_visible=False,
            height=700
        )

        # 7. Display
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📊 Model Prediction")
        st.write(f"**Trend:** {trend}")
        st.write(f"**Confidence:** {confidence:.2f}")
        st.progress(int(confidence * 100))

        st.caption(f"⏱ Prediction horizon: next {interval} candle")

        if analysis_mode == "Intraday (1 Day View)":
            st.warning(
                "Intraday mode uses limited historical data. "
                "Predictions may be less stable."
            )

        st.subheader("🧠 AI Explanation")
        st.markdown(ai_explanation)

        st.caption("⚠️ Educational purpose only. Not financial advice.")
