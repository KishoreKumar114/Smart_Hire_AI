import yfinance as yf
import pymysql
import time
from datetime import datetime
import warnings
import os

# Suppress warnings
warnings.filterwarnings("ignore")

# -------------------- CONFIG --------------------

# MySQL connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="pass123",
    database="stockdb",
    charset='utf8mb4'
)
cursor = db.cursor()

# Folder with CEO images (already downloaded manually)
SAVE_DIR = "ceo_images"
STATIC_BASE_URL = "http://localhost/ceo_images"

# -------------------- DATA --------------------

tickers = {
    "INFY.NS": "Infosys",
    "TCS.NS": "TCS",
    "HCLTECH.NS": "HCL",
    "CAP.PA": "Capgemini",
    "CTSH": "Cognizant",
    "AMZN": "Amazon"
}

company_info = {
    "Infosys": {
        "logo_url": "https://img.logo.dev/infosys.com",
        "ceo": "Salil Parekh",
        "ceo_img_url": f"{STATIC_BASE_URL}/Infosys.jpg",
        "headquarters": "Bangalore, India",
        "sector": "Information Technology",
        "currency": "INR",
        "disclaimer": "Data fetched from Yahoo Finance",
        "latitude": 12.9716,
        "longitude": 77.5946
    },
    "TCS": {
        "logo_url": "https://img.logo.dev/tcs.com",
        "ceo": "K. Krithivasan",
        "ceo_img_url": f"{STATIC_BASE_URL}/TCS.jpg",
        "headquarters": "Mumbai, India",
        "sector": "Information Technology",
        "currency": "INR",
        "disclaimer": "Data fetched from Yahoo Finance",
        "latitude": 19.0760,
        "longitude": 72.8777
    },
    "HCL": {
        "logo_url": "https://img.logo.dev/hcltech.com",
        "ceo": "C. Vijayakumar",
        "ceo_img_url": f"{STATIC_BASE_URL}/HCL.jpg",
        "headquarters": "Noida, India",
        "sector": "Information Technology",
        "currency": "INR",
        "disclaimer": "Data fetched from Yahoo Finance",
        "latitude": 28.5355,
        "longitude": 77.3910
    },
    "Capgemini": {
        "logo_url": "https://img.logo.dev/capgemini.com",
        "ceo": "Aiman Ezzat",
        "ceo_img_url": f"{STATIC_BASE_URL}/Capgemini.jpg",
        "headquarters": "Paris, France",
        "sector": "Consulting and IT Services",
        "currency": "EUR",
        "disclaimer": "Data fetched from Yahoo Finance",
        "latitude": 48.8566,
        "longitude": 2.3522
    },
    "Cognizant": {
        "logo_url": "https://img.logo.dev/cognizant.com",
        "ceo": "Ravi Kumar S",
        "ceo_img_url": f"{STATIC_BASE_URL}/Cognizant.jpg",
        "headquarters": "Teaneck, New Jersey, USA",
        "sector": "Information Technology",
        "currency": "USD",
        "disclaimer": "Data fetched from Yahoo Finance",
        "latitude": 40.8976,
        "longitude": -74.0167
    },
    "Amazon": {
        "logo_url": "https://img.logo.dev/amazon.com",
        "ceo": "Andy Jassy",
        "ceo_img_url": f"{STATIC_BASE_URL}/Amazon.jpg",
        "headquarters": "Seattle, USA",
        "sector": "E-commerce / Cloud",
        "currency": "USD",
        "disclaimer": "Data fetched from Yahoo Finance",
        "latitude": 47.6062,
        "longitude": -122.3321
    }
}

# -------------------- FUNCTIONS --------------------

def fetch_and_store():
    for symbol, name in tickers.items():
        try:
            # Get latest stock data (1-minute interval)
            data = yf.download(symbol, period="1d", interval="1m", progress=False)
            if data is None or data.empty:
                print(f"[{datetime.now()}] ⚠️ No data for {name}")
                continue

            latest = data.tail(1)
            for index, row in latest.iterrows():
                info = company_info[name]

                insert_tuple = (
                    name,
                    index.to_pydatetime(),
                    float(row["Open"]),
                    float(row["High"]),
                    float(row["Low"]),
                    float(row["Close"]),
                    int(row["Volume"]) if row["Volume"] is not None else 0,
                    info["logo_url"],
                    info["ceo"],
                    info["ceo_img_url"],
                    info["headquarters"],
                    info["sector"],
                    info["currency"],
                    info["disclaimer"],
                    info["latitude"],
                    info["longitude"]
                )

                sql = """
                INSERT INTO stocks 
                (company, datetime, open, high, low, close, volume, 
                logo_url, ceo, ceo_img_url, headquarters, sector, currency, 
                disclaimer, latitude, longitude)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
                cursor.execute(sql, insert_tuple)
                db.commit()
                print(f"[{datetime.now()}] ✅ {name} inserted!")

        except Exception as e:
            print(f"[{datetime.now()}] ❌ Error fetching {name}: {e}")

# -------------------- MAIN LOOP --------------------

print("🚀 Starting real-time stock fetcher (local CEO images)...")

while True:
    fetch_and_store()
    time.sleep(1)  # 1-minute interval




