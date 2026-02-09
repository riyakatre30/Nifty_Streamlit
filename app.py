import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Hong Kong Stock Market Analysis",
    layout="wide"
)

# ---------------- CUSTOM DARK THEME ----------------
st.markdown(
    """
    <style>
    body {
        background-color: #000000;
        color: white;
    }
    .stApp {
        background-color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- TITLE ----------------
st.title("📈 Hong Kong Stock Market Analysis")
st.write("Interactive stock price visualization with trading-style charts")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("Stock_HK.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# ---------------- SIDEBAR CONTROLS ----------------
st.sidebar.header("🔧 Controls")

stock_list = df["Stock"].unique()
selected_stock = st.sidebar.selectbox("Select Stock", stock_list)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["Date"].min(), df["Date"].max()]
)

# ---------------- FILTER DATA ----------------
filtered_df = df[
    (df["Stock"] == selected_stock) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

# ---------------- LINE CHART (TRADING STYLE) ----------------
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=filtered_df["Date"],
        y=filtered_df["Close"],
        mode="lines",
        name="Close Price",
        line=dict(color="#00ffcc", width=2)
    )
)

fig.update_layout(
    title=f"{selected_stock} Closing Price",
    xaxis_title="Date",
    yaxis_title="Price",
    template="plotly_dark",
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font=dict(color="white"),
    xaxis=dict(
        rangeslider=dict(visible=True),
        showgrid=False
    ),
    yaxis=dict(showgrid=False),
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- BASIC STATS ----------------
st.subheader("📊 Stock Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Max Price", f"{filtered_df['Close'].max():.2f}")
col2.metric("Min Price", f"{filtered_df['Close'].min():.2f}")
col3.metric("Average Price", f"{filtered_df['Close'].mean():.2f}")

# ---------------- DATA PREVIEW ----------------
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_df)
