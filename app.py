import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import math
from scipy import stats

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Indian Stock Analysis",
    page_icon="🇮🇳",
    layout="wide"
)

# --- CACHING THE DATA LOADING ---
# Caching ensures that the data is loaded only once, making the app faster.
@st.cache_data
def load_tickers():
    return pd.read_csv('top_50_indian_stocks.csv')

# --- STRATEGY FUNCTIONS ---
# It's best practice to put the logic for each strategy into its own function.

def run_equal_weight_strategy(portfolio_size):
    tickers_df = load_tickers()
    tickers_list = tickers_df["Ticker"].values.tolist()
    
    # Fetch data (simplified from your notebook)
    data = yf.download(tickers_list, period='1d')['Close']
    stocks_data = []
    for ticker in tickers_list:
        market_cap = yf.Ticker(ticker).info.get("marketCap", 0)
        latest_price = data[ticker].iloc[-1] if not data[ticker].empty else 0
        if market_cap > 0 and latest_price > 0:
            stocks_data.append({
                "Ticker": ticker,
                "Market Cap": market_cap,
                "Latest Price": latest_price,
            })
    
    df = pd.DataFrame(stocks_data)
    df = df.sort_values(by="Market Cap", ascending=False).head(10)
    df.reset_index(drop=True, inplace=True)
    
    position_size = portfolio_size / len(df.index)
    df['Number of Shares to buy'] = df['Latest Price'].apply(
        lambda price: math.floor(position_size / price) if price > 0 else 0
    )
    return df

def run_value_investing_strategy():
    # This can be slow, so we show a spinner
    with st.spinner('Fetching and analyzing data for 50 stocks... This might take a moment.'):
        tickers_df = load_tickers()
        tickers_list = tickers_df['Ticker'].values.tolist()
        
        # --- Your value investing logic from notebook 02 goes here ---
        # (This is a simplified placeholder)
        # For the real app, copy/paste the functions from your notebook.
        st.info("Note: The full Value Investing logic from the notebook should be implemented here.")
        # As a placeholder, we'll just show the list of tickers.
        return tickers_df.head(10)

def run_dividend_investing_strategy():
    with st.spinner('Fetching dividend data for 50 stocks...'):
        tickers_df = load_tickers()
        
        # --- Your dividend investing logic from notebook 03 goes here ---
        st.info("Note: The full Dividend Investing logic from the notebook should be implemented here.")
        # As a placeholder, we'll show the list of tickers.
        return tickers_df.head(10)


# --- UI LAYOUT ---
st.title("🇮🇳 Algorithmic Trading Strategies for Indian Stocks")
st.write("This app analyzes the top 50 NSE stocks to demonstrate different quantitative investment strategies.")

st.sidebar.header("Controls")
strategy = st.sidebar.selectbox(
    "Choose a Strategy",
    ["Equal Weight Strategy", "Value Investing Strategy", "Dividend Investing Strategy"]
)

if strategy == 'Equal Weight Strategy':
    st.header("Equal Weight Strategy")
    st.write("This strategy invests an equal amount of money into the top 10 largest companies by market cap.")
    
    portfolio_size = st.sidebar.number_input(
        "Enter Your Portfolio Size (INR)", 
        min_value=50000, 
        max_value=10000000, 
        value=100000, 
        step=50000
    )
    
    if st.sidebar.button("Run Strategy"):
        result_df = run_equal_weight_strategy(portfolio_size)
        st.dataframe(result_df)

elif strategy == 'Value Investing Strategy':
    st.header("Value Investing Strategy")
    st.write("This strategy screens for potentially undervalued stocks based on financial ratios.")
    if st.sidebar.button("Run Strategy"):
        result_df = run_value_investing_strategy()
        st.dataframe(result_df)

elif strategy == 'Dividend Investing Strategy':
    st.header("Dividend Investing Strategy")
    st.write("This strategy finds the best dividend-paying stocks based on a weighted score.")
    if st.sidebar.button("Run Strategy"):
        result_df = run_dividend_investing_strategy()
        st.dataframe(result_df)