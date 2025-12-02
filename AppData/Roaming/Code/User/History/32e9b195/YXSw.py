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
    "INFY.NS": "Infosys",
    "TCS.NS": "TCS",
    "HCLTECH.NS": "HCL",
    "CAP.PA": "Capgemini",
    "CTSH": "Cognizant",
    "AMZN": "Amazon"
}

# ✅ Extra Company Info (with working CEO image URLs)
company_info = {
    "Infosys": {
        "logo_url": "https://logo.clearbit.com/infosys.com",
        "ceo": "Salil Parekh",
        "ceo_img_url": "https://i.imgur.com/9qXW2nl.jpg",   # ✅ working JPG
        "headquarters": "Bangalore, India",
        "sector": "IT Services",
        "currency": "INR",
        "disclaimer": "Data for educational use only",
        "latitude": 12.9716,
        "longitude": 77.5946
    },
    "TCS": {
        "logo_url": "https://logo.clearbit.com/tcs.com",
        "ceo": "K. Krithivasan",
        "ceo_img_url": "https://i.imgur.com/FYox0pM.jpg",   # ✅ working JPG
        "headquarters": "Mumbai, India",
        "sector": "IT Services",
        "currency": "INR",
        "disclaimer": "Data for educational use only",
        "latitude": 19.0760,
        "longitude": 72.8777
    },
    "HCL": {
        "logo_url": "https://logo.clearbit.com/hcltech.com",
        "ceo": "C. Vijayakumar",
        "ceo_img_url": "https://i.imgur.com/eov4g7b.jpg",   # ✅ working JPG
        "headquarters": "Noida, India",
        "sector": "IT Services",
        "currency": "INR",
        "disclaimer": "Data for educational use only",
        "latitude": 28.5355,
        "longitude": 77.3910
    },
    "Capgemini": {
        "logo_url": "https://logo.clearbit.com/capgemini.com",
        "ceo": "Aiman Ezzat",
        "ceo_img_url": "https://i.imgur.com/6HyK4yv.jpg",   # ✅ working JPG
        "headquarters": "Paris, France",
        "sector": "IT Consulting",
        "currency": "EUR",
        "disclaimer": "Data for educational use only",
        "latitude": 48.8566,
        "longitude": 2.3522
    },
    "Cognizant": {
        "logo_url": "https://logo.clearbit.com/cognizant.com",
        "ceo": "Ravi Kumar S",
        "ceo_img_url": "https://i.imgur.com/zT7FRAl.jpg",   # ✅ working JPG
        "headquarters": "Teaneck, USA",
        "sector": "IT Services",
        "currency": "USD",
        "disclaimer": "Data for educational use only",
        "latitude": 40.8976,
        "longitude": -74.0159
    },
    "Amazon": {
        "logo_url": "https://logo.clearbit.com/amazon.com",
        "ceo": "Andy Jassy",
        "ceo_img_url": "https://i.imgur.com/3Fe8f1M.jpg",   # ✅ working JPG
        "headquarters": "Seattle, USA",
        "sector": "E-commerce & Cloud",
        "currency": "USD",
        "disclaimer": "Data for educational use only",
        "latitude": 47.6062,
        "longitude": -122.3321
    }
}

def fetch_and_store():
    for symbol, name in tickers.items():
        try:
            data = yf.download(symbol, period="1d", interval="1m")
            if not data.empty:
                latest = data.tail(1)  # get latest row
                for index, row in latest.iterrows():
                    info = company_info[name]
                    cursor.execute("""
                        INSERT INTO stocks 
                        (company, datetime, open, high, low, close, volume, 
                        logo_url, ceo, ceo_img_url, headquarters, sector, currency, 
                        disclaimer, latitude, longitude)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (
                        name,
                        index.to_pydatetime(),
                        float(row["Open"]),
                        float(row["High"]),
                        float(row["Low"]),
                        float(row["Close"]),
                        int(row["Volume"]),
                        info["logo_url"],
                        info["ceo"],
                        info["ceo_img_url"],
                        info["headquarters"],
                        info["sector"],
                        info["currency"],
                        info["disclaimer"],
                        info["latitude"],
                        info["longitude"]
                    ))
                    db.commit()
                print(f"[{datetime.now()}] ✅ {name} data inserted with full details!")
            else:
                print(f"[{datetime.now()}] ⚠️ No data for {name}")
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Error fetching {name}: {e}")

print("🚀 Starting real-time stock fetcher with full company details...")

# ✅ Run every 1 min
while True:
    fetch_and_store()
    time.sleep(60)



