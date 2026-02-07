import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="HK Stock Viewer", layout="wide")

# Title
st.title("📈 Hong Kong Stock Price Viewer")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Stock_HK.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# Sidebar
st.sidebar.header("🔎 Filters")

# Stock selector
stock_list = sorted(df["Stock"].unique())
selected_stock = st.sidebar.selectbox(
    "Select Stock",
    stock_list
)

# Filter stock
stock_df = df[df["Stock"] == selected_stock]

# Date range selector
start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [stock_df["Date"].min(), stock_df["Date"].max()]
)

# Apply date filter
mask = (stock_df["Date"] >= pd.to_datetime(start_date)) & \
       (stock_df["Date"] <= pd.to_datetime(end_date))
stock_df = stock_df[mask]

# Show basic stats
st.subheader(f"📊 {selected_stock} Overview")
col1, col2, col3 = st.columns(3)

col1.metric("Start Price", f"{stock_df.Close.iloc[0]:.2f}")
col2.metric("End Price", f"{stock_df.Close.iloc[-1]:.2f}")
col3.metric("Max Price", f"{stock_df.Close.max():.2f}")

# Plot
st.subheader("📉 Closing Price Trend")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(stock_df["Date"], stock_df["Close"])
ax.set_xlabel("Date")
ax.set_ylabel("Close Price")
ax.set_title(f"{selected_stock} Closing Price")

st.pyplot(fig)

# Show data
with st.expander("📄 View Raw Data"):
    st.dataframe(stock_df)
