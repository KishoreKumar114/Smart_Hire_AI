import yfinance as yf
import mysql.connector
import schedule, time
import pymysql


from datetime import datetime

# MySQL connection
import pymysql

db = pymysql.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="stockdb"
)
cursor = db.cursor()


# Company tickers (Yahoo Finance codes)
tickers = {
    "INFY": "Infosys",
    "TCS.NS": "TCS",
    "HCLTECH.NS": "HCL",
    "CAP.PA": "Capgemini",
    "CTSH": "Cognizant",
    "AMZN": "Amazon"
}

def fetch_and_store():
    for symbol, name in tickers.items():
        data = yf.download(symbol, period="1d", interval="1m")
        latest = data.tail(1)  # latest record
        for index, row in latest.iterrows():
            cursor.execute("""
                INSERT INTO stocks (company, datetime, open, high, low, close, volume)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (name, index.to_pydatetime(), row["Open"], row["High"],
                  row["Low"], row["Close"], int(row["Volume"])))
            db.commit()
        print(f"{name} data inserted!")

# Schedule every 1 minute
schedule.every(1).minutes.do(fetch_and_store)

print("Starting real-time stock fetcher...")
while True:
    schedule.run_pending()
    time.sleep(1)
