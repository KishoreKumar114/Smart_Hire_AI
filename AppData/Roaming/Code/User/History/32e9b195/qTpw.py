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
    logos = {
    "Infosys": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Infosys_logo.svg/2560px-Infosys_logo.svg.png",
    "TCS": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Tata_Consultancy_Services_Logo.svg/1280px-Tata_Consultancy_Services_Logo.svg.png",
    "HCL": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/HCL_Technologies_Logo.svg/1280px-HCL_Technologies_Logo.svg.png",
    "Capgemini": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Capgemini_201x_logo.svg/1280px-Capgemini_201x_logo.svg.png",
    "Cognizant": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Cognizant_logo_2022.svg/2560px-Cognizant_logo_2022.svg.png",
    "Amazon": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/1024px-Amazon_logo.svg.png"
}

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
