# Stock-Market-Dashboard
FAANG Stock Analysis | 5-Year Performance Dashboard | Python, MySQL, Tableau | Moving Averages, Golden Cross Signals & 5-Year Returns


**Problem Statement**
Investors need a clear visual system to track stock performance, identify buy/sell signals and compare returns across multiple companies over time.

**What I Built**
A complete stock analytics pipeline that downloads 5 years of FAANG stock data, stores it in MySQL, runs technical analysis queries and visualizes everything in an interactive Tableau dashboard.

**Dataset**
Source   : Yahoo Finance API (yfinance)
Stocks   : META, AAPL, AMZN, NFLX, GOOGL
Period   : 5 years of daily trading data
Rows     : 6,300+ records

**Key Findings**
META had the strongest 5-year return
Golden Cross signals identified buy opportunities
2022 showed weakest performance across all stocks
Moving average crossovers detected trend changes

**Dashboard Features**
Price trend lines for all 5 stocks
MA50 vs MA200 overlay with dual axis
Market signal table (Bullish/Bearish/Neutral)
5-Year return comparison bar chart
Interactive ticker filter

**Project Structure**
stock_data_collector.py  → downloads FAANG data via API
export_for_tableau.py    → exports cleaned CSV for Tableau

## How to Run
pip install yfinance pandas mysql-connector-python
python stock_data_collector.py
python export_for_tableau.py

**Dashboard**
[View on Tableau Public](https://public.tableau.com/views/FAANGStockMarketPerformanceDashboard/FAANGStockMarketPerformanceDashboard20192024?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

## Tools Used
Python | yfinance | pandas | MySQL | Tableau Public
