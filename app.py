import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import math
from scipy import stats
from statistics import mean

# --- Page Configuration ---
st.set_page_config(
    page_title="Indian Stock Analysis Strategies",
    page_icon="🇮🇳",
    layout="wide"
)

# --- Data Caching ---
# This decorator caches the output of the function, so the CSV is only loaded once.
@st.cache_data
def load_tickers():
    """Loads the list of tickers from the CSV file."""
    return pd.read_csv('top_50_indian_stocks.csv')

# --- Strategy 1: Equal Weight ---
def run_equal_weight_strategy(portfolio_size):
    """
    Calculates the number of shares to buy for a top-10 market cap portfolio with equal weighting.
    """
    tickers_df = load_tickers()
    tickers_list = tickers_df["Ticker"].head(10).tolist() # Optimization: only download top 10
    
    with st.spinner("Fetching market data for top 10 stocks..."):
        data = yf.download(tickers_list, period='2d', group_by='ticker', auto_adjust=False)
        
        stocks_data = []
        for ticker in tickers_list:
            try:
                market_cap_info = yf.Ticker(ticker).info
                market_cap = market_cap_info.get("marketCap", 0)
                latest_price = data[ticker]['Close'].iloc[-1]
                
                if market_cap > 0 and latest_price > 0:
                    stocks_data.append({
                        "Ticker": ticker, 
                        "Company Name": tickers_df[tickers_df['Ticker'] == ticker]['Company Name'].iloc[0],
                        "Market Cap": market_cap,
                        "Latest Price": latest_price,
                    })
            except Exception as e:
                st.warning(f"Could not fetch data for {ticker}: {e}")

    if not stocks_data:
        st.error("Could not fetch any stock data. Please try again later.")
        return pd.DataFrame()

    df = pd.DataFrame(stocks_data)
    df = df.sort_values(by="Market Cap", ascending=False).head(10)
    df.reset_index(inplace=True, drop=True)
    
    position_size = float(portfolio_size) / len(df.index)
    df['Number of Shares to Buy'] = df['Latest Price'].apply(
        lambda price: math.floor(position_size / price) if price > 0 else 0
    )
    
    # Format for better display
    df['Market Cap'] = df['Market Cap'].apply(lambda x: f"₹ {x/1e7:,.2f} Cr")
    df['Latest Price'] = df['Latest Price'].apply(lambda x: f"₹ {x:,.2f}")
    return df

# --- Strategy 2: Value Investing ---
def run_value_investing_strategy():
    """
    Ranks stocks based on a composite value score from multiple financial metrics.
    """
    with st.spinner('Fetching and analyzing financial data for 50 stocks... This may take a few moments.'):
        tickers_df = load_tickers()
        tickers_list = tickers_df['Ticker'].values.tolist()
        
        value_cols = ["Ticker", "Price", "PE-Ratio", "PB-Ratio", "PS-Ratio", "EV/EBITDA", "EV/GP"]
        value_df = pd.DataFrame(columns=value_cols)
        
        all_info = yf.Tickers(tickers_list)
        for ticker_str in tickers_list:
            stock = all_info.tickers[ticker_str]
            try:
                info = stock.info
                price = info.get("currentPrice", stock.history(period='2d')['Close'].iloc[-1])
                
                pe_ratio = info.get("forwardPE", np.nan)
                pb_ratio = info.get("priceToBook", np.nan)
                ps_ratio = info.get("priceToSalesTrailing12Months", np.nan)
                ev = info.get("enterpriseValue", np.nan)
                ebitda = info.get("ebitda", np.nan)
                evEbitda = ev / ebitda if ev and ebitda else np.nan
                gross_profit = info.get("grossProfits", np.nan)
                evGrossProfit = ev / gross_profit if ev and gross_profit else np.nan

                value_df.loc[len(value_df)] = [ticker_str, price, pe_ratio, pb_ratio, ps_ratio, evEbitda, evGrossProfit]
            except Exception:
                continue # Skip if a ticker fails

        # Handle missing values
        metric_cols = ["PE-Ratio", "PB-Ratio", "PS-Ratio", "EV/EBITDA", "EV/GP"]
        for col in metric_cols:
            value_df[col] = value_df[col].fillna(value_df[col].mean())
            
        # Calculate percentiles
        percentile_metrics = {col: f'{col}_Percentile' for col in metric_cols}
        for metric, percentile in percentile_metrics.items():
            value_df[percentile] = value_df[metric].rank(pct=True)

        # Calculate Value Score
        value_df['Value Score'] = value_df[[p for p in percentile_metrics.values()]].mean(axis=1)
        
        df = value_df.sort_values(by="Value Score", ascending=False).head(10)
        df.reset_index(drop=True, inplace=True)
    return df

# --- Strategy 3: Dividend Investing ---
def run_dividend_investing_strategy():
    """
    Ranks stocks based on a weighted dividend score.
    """
    with st.spinner('Fetching dividend and growth data for 50 stocks...'):
        tickers_df = load_tickers()
        tickers_list = tickers_df['Ticker'].values.tolist()
        
        cols = ["Ticker", "Dividend Yield(%)", "Dividend Rate", "Payout Ratio(%)", "5 Year Avg Dividend Yield(%)", "Earning Growth(%)"]
        dividend_df = pd.DataFrame(columns=cols)

        all_info = yf.Tickers(tickers_list)
        for stock_str in tickers_list:
            try:
                info = all_info.tickers[stock_str].info
                dividend_yield = info.get("dividendYield", np.nan) * 100
                dividend_rate = info.get("dividendRate", np.nan)
                payout_ratio = info.get("payoutRatio", np.nan) * 100
                five_year_avg_yield = info.get("fiveYearAvgDividendYield", np.nan)
                earning_growth = info.get("earningsGrowth", np.nan) * 100
                dividend_df.loc[len(dividend_df)] = [stock_str, dividend_yield, dividend_rate, payout_ratio, five_year_avg_yield, earning_growth]
            except Exception:
                continue

        # Fill NaNs before normalization
        dividend_df.fillna(0, inplace=True)

        # Normalize metrics
        numeric_cols = ["Dividend Yield(%)", "Dividend Rate", "Payout Ratio(%)", "5 Year Avg Dividend Yield(%)", "Earning Growth(%)"]
        for col in numeric_cols:
            norm_col_name = f"{col} Normalised"
            if col == "Payout Ratio(%)": # Lower is better
                dividend_df[norm_col_name] = 1 - ((dividend_df[col] - dividend_df[col].min()) / (dividend_df[col].max() - dividend_df[col].min()))
            else: # Higher is better
                dividend_df[norm_col_name] = (dividend_df[col] - dividend_df[col].min()) / (dividend_df[col].max() - dividend_df[col].min())
        
        # Handle cases where max == min -> results in NaN
        dividend_df.fillna(0, inplace=True)
        
        # Calculate weighted score
        weights = {
            "Dividend Yield(%) Normalised": 0.3, "Dividend Rate Normalised": 0.2, "Payout Ratio(%) Normalised": 0.2,
            "5 Year Avg Dividend Yield(%) Normalised": 0.2, "Earning Growth(%) Normalised": 0.1
        }
        dividend_df["Dividend Score"] = dividend_df[list(weights.keys())].mul(list(weights.values())).sum(axis=1)
        
        df = dividend_df.sort_values(by="Dividend Score", ascending=False).head(10)
        df.reset_index(drop=True, inplace=True)
    return df

# --- Streamlit UI ---
st.title("🇮🇳 Algorithmic Trading Strategies for Indian Stocks")
st.write("This app demonstrates three quantitative strategies to analyze and select stocks from the top 50 companies on the NSE.")

st.sidebar.header("Controls")
strategy = st.sidebar.selectbox(
    "Choose a Strategy",
    ["Select a Strategy", "Equal Weight Strategy", "Value Investing Strategy", "Dividend Investing Strategy"]
)

if strategy == 'Equal Weight Strategy':
    st.header("⚖️ Equal Weight Strategy")
    st.markdown("This strategy identifies the **top 10 largest companies** by market capitalization and suggests an equal monetary allocation for each.")
    
    portfolio_size = st.sidebar.number_input(
        "Enter Your Portfolio Size (INR)", 
        min_value=50000, max_value=100000000, value=100000, step=25000,
        help="Enter the total amount you want to invest."
    )
    
    if st.sidebar.button("Run Strategy"):
        result_df = run_equal_weight_strategy(portfolio_size)
        st.dataframe(result_df, use_container_width=True)

elif strategy == 'Value Investing Strategy':
    st.header("💎 Value Investing Strategy")
    st.markdown("This strategy screens for **undervalued stocks** by calculating a composite 'Value Score' from key financial ratios. A higher score indicates a potentially better value investment.")
    
    if st.sidebar.button("Run Strategy"):
        result_df = run_value_investing_strategy()
        st.dataframe(result_df, use_container_width=True)

elif strategy == 'Dividend Investing Strategy':
    st.header("💰 Dividend Investing Strategy")
    st.markdown("This strategy ranks stocks to find the **best dividend payers** based on a weighted score of yield, rate, sustainability (payout ratio), and growth.")
    
    if st.sidebar.button("Run Strategy"):
        result_df = run_dividend_investing_strategy()
        st.dataframe(result_df, use_container_width=True)
else:
    st.info("Please select a strategy from the sidebar on the left to get started.")