import mysql.connector
import pandas as pd

# ── CONNECT TO MYSQL ──────────────────────────────────────
conn = mysql.connector.connect(
    host     = "localhost",
    user     = "root",
    password = "Purna040901@",  # ← your actual password
    database = "stock_dashboard"
)
print(" Connected to MySQL!")

# ── PULL ALL DATA FROM MYSQL ──────────────────────────────
query = """
    SELECT 
        ticker,
        trade_date,
        ROUND(close_price, 2)  AS close_price,
        ROUND(ma_50, 2)        AS ma_50,
        ROUND(ma_200, 2)       AS ma_200,
        ROUND(daily_return, 4) AS daily_return,
        CASE
            WHEN ma_50 > ma_200 THEN 'Bullish'
            WHEN ma_50 < ma_200 THEN 'Bearish'
            ELSE 'Neutral'
        END AS market_signal
    FROM stock_prices
    ORDER BY ticker, trade_date;
"""

df = pd.read_sql(query, conn)
print(f" Pulled {len(df)} rows from MySQL!")

# ── PREVIEW THE DATA ──────────────────────────────────────
print(df.head(10))
print(f"\nColumns: {list(df.columns)}")
print(f"Date range: {df['trade_date'].min()} → {df['trade_date'].max()}")

# ── EXPORT TO CSV ─────────────────────────────────────────
csv_path = "stock_data_for_tableau.csv"
df.to_csv(csv_path, index=False)
print(f"\n Exported successfully → {csv_path}")

conn.close()

print(" MySQL connection closed.")
