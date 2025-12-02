import yfinance as yf
import pymysql
import time
from datetime import datetime

# ✅ MySQL connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="pass123",   # ⚠️ change to your actual MySQL password
    database="stockdb"
)
cursor = db.cursor()

# ✅ Company tickers (Yahoo Finance codes)
tickers = {
    "INFY": "Infosys",
    "TCS.NS": "TCS",
    "HCLTECH.NS": "HCL",
    "CAP.PA": "Capgemini",
    "CTSH": "Cognizant",
    "AMZN": "Amazon"
}

# ✅ Company Logos
logos = {
    "Infosys": "https://companieslogo.com/img/orig/INFY-7d81e9f9.png?t=1727713249",
    "TCS": "https://companieslogo.com/img/orig/TCS.NS-05e47c64.png?t=1727713274",
    "HCL": "https://companieslogo.com/img/orig/HCLTECH.NS-4c06c14f.png?t=1727713304",
    "Capgemini": "https://companieslogo.com/img/orig/CAP.PA-3f8ce40d.png?t=1727713336",
    "Cognizant": "https://companieslogo.com/img/orig/CTSH-6f352118.png?t=1727713362",
    "Amazon": "https://companieslogo.com/img/orig/AMZN-d94c8719.png?t=1727713393"
}

def fetch_and_store():
    for symbol, name in tickers.items():
        try:
            data = yf.download(symbol, period="1d", interval="1m")
            if not data.empty:
                latest = data.tail(1)  # get latest row
                for index, row in latest.iterrows():
                    cursor.execute("""
                        INSERT INTO stocks (company, datetime, open, high, low, close, volume, logo_url)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (
                        name,
                        index.to_pydatetime(),
                        float(row["Open"]),
                        float(row["High"]),
                        float(row["Low"]),
                        float(row["Close"]),
                        int(row["Volume"]),
                        logos[name]   # ✅ add logo here
                    ))
                    db.commit()
                print(f"[{datetime.now()}] ✅ {name} data inserted with logo!")
            else:
                print(f"[{datetime.now()}] ⚠️ No data for {name}")
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Error fetching {name}: {e}")

print("🚀 Starting real-time stock fetcher with logos...")

# ✅ Run every 1 second
while True:
    fetch_and_store()
    time.sleep(1)
