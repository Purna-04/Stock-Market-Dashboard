import yfinance as yf
import pandas as pd
import mysql.connector

# ── CONNECT TO MYSQL ──────────────────────────────────────
conn = mysql.connector.connect(
    host     = "localhost",
    user     = "root",
    password = "Purna040901@",  # ← YOUR password here
    database = "stock_dashboard"
)
cursor = conn.cursor()
print("✅ Connected to MySQL successfully!")

# ── DOWNLOAD STOCK DATA ───────────────────────────────────
tickers = ['META', 'AAPL', 'AMZN', 'NFLX', 'GOOGL']
print("📥 Downloading stock data from Yahoo Finance...")
df = yf.download(tickers, start='2019-01-01', end='2024-12-31')
df = df['Close'].reset_index()

df_long = df.melt(id_vars='Date', var_name='ticker', value_name='close_price')
df_long.rename(columns={'Date': 'trade_date'}, inplace=True)
df_long.dropna(inplace=True)
print(f"✅ Downloaded {len(df_long)} rows of stock data!")

# ── CALCULATE MOVING AVERAGES ─────────────────────────────
df_long.sort_values(['ticker', 'trade_date'], inplace=True)

df_long['ma_50'] = df_long.groupby('ticker')['close_price'] \
    .transform(lambda x: x.rolling(50).mean())

df_long['ma_200'] = df_long.groupby('ticker')['close_price'] \
    .transform(lambda x: x.rolling(200).mean())

df_long['daily_return'] = df_long.groupby('ticker')['close_price'] \
    .pct_change() * 100

# ── CLEAN NaN VALUES PROPERLY ─────────────────────────────
# Convert all NaN to None (MySQL only accepts None as NULL)
df_long = df_long.astype(object).where(pd.notnull(df_long), None)

print("✅ Moving averages and daily returns calculated!")

# ── INSERT INTO MYSQL ─────────────────────────────────────
insert_query = """
    INSERT INTO stock_prices 
        (ticker, trade_date, close_price, ma_50, ma_200, daily_return)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

print("📤 Inserting data into MySQL... please wait...")
rows_inserted = 0
for _, row in df_long.iterrows():

    # Manually force each value to None if it is NaN
    ticker       = row['ticker']
    trade_date   = str(row['trade_date'])[:10]
    close_price  = None if pd.isna(row['close_price'])  else float(row['close_price'])
    ma_50        = None if pd.isna(row['ma_50'])         else float(row['ma_50'])
    ma_200       = None if pd.isna(row['ma_200'])        else float(row['ma_200'])
    daily_return = None if pd.isna(row['daily_return'])  else float(row['daily_return'])

    cursor.execute(insert_query, (
        ticker,
        trade_date,
        close_price,
        ma_50,
        ma_200,
        daily_return
    ))
    rows_inserted += 1

conn.commit()
print(f"✅ {rows_inserted} rows inserted into MySQL successfully!")

cursor.close()
conn.close()
print("🔒 MySQL connection closed.")