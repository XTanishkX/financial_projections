# Algorithmic Trading Strategies for the Indian Stock Market

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Libraries](https://img.shields.io/badge/Libraries-Pandas%20%7C%20YFinance-green)
![Data](https://img.shields.io/badge/Data-NSE%20Top%2050-yellow)

This project uses Python to implement and test three different algorithmic trading strategies on the top 50 stocks of the Indian National Stock Exchange (NSE). The scripts fetch live financial data using the `yfinance` library to analyze and select stocks based on predefined rules.

---

## 📈 Strategies Implemented

This repository contains notebooks for three distinct investment strategies:

### 1. Equal Weight Strategy (`01_equal_weights.ipynb`)
[cite_start]This strategy invests in the largest companies in the market by splitting capital evenly among them[cite: 1].

* **Logic:**
    1.  [cite_start]Fetches the market capitalization for the top 50 Indian stocks[cite: 1].
    2.  Selects the **top 10 largest companies**.
    3.  Takes a total investment amount as input.
    4.  [cite_start]Divides the investment equally across the 10 stocks and calculates the number of shares to buy for each[cite: 1].

### 2. Value Investing Strategy (`02_value_investing.ipynb`)
[cite_start]This strategy aims to find stocks that are potentially undervalued based on their financial health[cite: 2].

* **Logic:**
    1.  [cite_start]Fetches key valuation metrics like **P/E (Price-to-Earnings)**, **P/B (Price-to-Book)**, and **EV/EBITDA** for each stock[cite: 2].
    2.  Each stock is ranked on every metric using percentile scores.
    3.  A final **"Value Score"** is calculated by averaging the ranks.
    4.  [cite_start]Stocks are sorted by this score to identify the top value opportunities[cite: 2].

### 3. Dividend Investing Strategy (`03_dividend_based_investing.ipynb`)
This strategy focuses on identifying stocks that provide good, sustainable dividend income.

* **Logic:**
    1.  Gathers dividend-related data such as **Dividend Yield**, **Payout Ratio**, and **5-Year Average Yield**.
    2.  Each metric is normalized and then combined into a weighted **"Dividend Score"**.
    3.  The weights prioritize factors like yield (30%) and sustainability (payout ratio, 20%).
    4.  Stocks are ranked by this final score to find the best dividend-paying companies.

---

## 🚀 How to Run

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```

2.  **Install Required Libraries**
    ```bash
    pip install pandas numpy yfinance scipy jupyterlab
    ```

3.  **Run the Jupyter Notebooks**
    ```bash
    jupyter lab
    ```
