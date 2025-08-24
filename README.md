# Algorithmic Trading Strategies for the Indian Stock Market

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Libraries](https://img.shields.io/badge/Libraries-Pandas%20%7C%20YFinance-green)

---

### 🚀 [**Check out the live Streamlit App!**]([https://your-streamlit-app-url.streamlit.app/](https://financialprojections-vaaz4bfg6apw8rznnxzzq8.streamlit.app/))

---

## ## Overview

This project implements three distinct quantitative stock-picking strategies for the top 50 companies on the Indian National Stock Exchange (NSE). The logic, originally developed in Jupyter Notebooks, is now presented as an interactive web application built with Streamlit. The app fetches real-time financial data using the `yfinance` library to provide actionable insights.

## ## Key Features

* **Interactive Dashboard**: A user-friendly interface built with Streamlit to select and run strategies.
* **Three Unique Strategies**: Implements Equal Weight, Value Investing, and Dividend Investing models.
* **Real-Time Data**: Fetches the latest stock prices, market cap, and financial ratios directly from Yahoo Finance.
* **Actionable Output**: Provides clear outputs, such as the number of shares to buy or a ranked list of top stocks.

---

## ## Strategies Implemented

1.  **⚖️ Equal Weight Strategy**:
    * Identifies the top 10 largest companies by market capitalization.
    * Calculates the number of shares to buy for each, based on an equal monetary allocation from a user-defined portfolio size.

2.  **💎 Value Investing Strategy**:
    * Screens all 50 stocks using key valuation metrics (P/E, P/B, EV/EBITDA, etc.).
    * Ranks stocks based on a composite "Value Score" to find the most undervalued opportunities.

3.  **💰 Dividend Investing Strategy**:
    * Analyzes stocks based on dividend yield, payout ratio, and historical growth.
    * Ranks stocks using a weighted "Dividend Score" to identify the top income-generating investments.

---

## ## Project Structure
* `app.py`: The main Streamlit application file.
* `requirements.txt`: Lists all the Python libraries needed to run the project.
* `top_50_indian_stocks.csv`: Contains the list of the top 50 NSE stock tickers.
* `01_equal_weights.ipynb`: Jupyter Notebook for the Equal Weight strategy.
* `02_value_investing.ipynb`: Jupyter Notebook for the Value Investing strategy.
* `03_dividend_based_investing.ipynb`: Jupyter Notebook for the Dividend Investing strategy.

---
## ## How to Run Locally

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```

2.  **Install Dependencies**
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit App**
    ```bash
    streamlit run app.py
    ```
    Your app will now be running in your web browser. The Jupyter notebooks are also available for a detailed, cell-by-cell breakdown of the logic.

### ### `requirements.txt`
pandas
numpy
yfinance
scipy
streamlit
