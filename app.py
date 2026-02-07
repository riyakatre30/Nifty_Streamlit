import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

# ---------------- TITLE ----------------
st.markdown(
    "<h1 style='text-align:center;'>📊 Interactive Stock Dashboard</h1>",
    unsafe_allow_html=True
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("Stock_HK.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Controls")

stock_name = st.sidebar.selectbox(
    "Select Stock",
    sorted(df["Stock"].unique())
)

chart_type = st.sidebar.radio(
    "Chart Type",
    ["Line Chart", "Candlestick"]
)

show_volume = st.sidebar.checkbox("Show Volume", True)

ma20 = st.sidebar.checkbox("Moving Average 20", True)
ma50 = st.sidebar.checkbox("Moving Average 50")
ma200 = st.sidebar.checkbox("Moving Average 200")

# ---------------- FILTER DATA ----------------
stock_df = df[df["Stock"] == stock_name].sort_values("Date")

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [stock_df["Date"].min(), stock_df["Date"].max()]
)

stock_df = stock_df[
    (stock_df["Date"] >= pd.to_datetime(start_date)) &
    (stock_df["Date"] <= pd.to_datetime(end_date))
]

# ---------------- METRICS ----------------
st.subheader(f"📌 {stock_name} Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Open", f"{stock_df['Open'].iloc[0]:.2f}")
c2.metric("Close", f"{stock_df['Close'].iloc[-1]:.2f}")
c3.metric("High", f"{stock_df['High'].max():.2f}")
c4.metric("Low", f"{stock_df['Low'].min():.2f}")

# ---------------- MOVING AVERAGES ----------------
if ma20:
    stock_df["MA20"] = stock_df["Close"].rolling(20).mean()
if ma50:
    stock_df["MA50"] = stock_df["Close"].rolling(50).mean()
if ma200:
    stock_df["MA200"] = stock_df["Close"].rolling(200).mean()

# ---------------- PRICE CHART ----------------
st.subheader("📈 Price Chart")

fig = go.Figure()

if chart_type == "Candlestick":
    fig.add_trace(go.Candlestick(
        x=stock_df["Date"],
        open=stock_df["Open"],
        high=stock_df["High"],
        low=stock_df["Low"],
        close=stock_df["Close"],
        name="Price"
    ))
else:
    fig.add_trace(go.Scatter(
        x=stock_df["Date"],
        y=stock_df["Close"],
        mode="lines",
        name="Close Price"
    ))

if ma20:
    fig.add_trace(go.Scatter(
        x=stock_df["Date"],
        y=stock_df["MA20"],
        name="MA 20"
    ))
if ma50:
    fig.add_trace(go.Scatter(
        x=stock_df["Date"],
        y=stock_df["MA50"],
        name="MA 50"
    ))
if ma200:
    fig.add_trace(go.Scatter(
        x=stock_df["Date"],
        y=stock_df["MA200"],
        name="MA 200"
    ))

fig.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Date",
    yaxis_title="Price",
    legend=dict(orientation="h", y=1.05)
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- VOLUME CHART ----------------
if show_volume and "Volume" in stock_df.columns:
    st.subheader("📊 Trading Volume")

    vol_fig = go.Figure()
    vol_fig.add_trace(go.Bar(
        x=stock_df["Date"],
        y=stock_df["Volume"],
        name="Volume"
    ))

    vol_fig.update_layout(
        template="plotly_dark",
        height=250
    )

    st.plotly_chart(vol_fig, use_container_width=True)

# ---------------- DATA TABLE ----------------
with st.expander("📄 Show Data Table"):
    st.dataframe(stock_df)

# ---------------- DOWNLOAD ----------------
st.download_button(
    label="⬇️ Download Filtered Data",
    data=stock_df.to_csv(index=False),
    file_name=f"{stock_name}_data.csv",
    mime="text/csv"
)
