import yfinance as yf
import pymysql
import time
from datetime import datetime
import warnings
import os

# -------------------- CONFIG --------------------
warnings.filterwarnings("ignore")

# MySQL connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="pass123",
    database="stockdb",
    charset='utf8mb4'
)
cursor = db.cursor()

# Folder with CEO images (already downloaded)
SAVE_DIR = "C:/xampp/htdocs/ceo_images"  # Windows XAMPP folder
STATIC_BASE_URL = "http://localhost/ceo_images"

# Placeholder if any CEO image is missing
PLACEHOLDER_IMG = f"{STATIC_BASE_URL}/placeholder_ceo.png"

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
        "ceo_img_file": "Infosys.jpg",
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
        "ceo_img_file": "TCS.jpg",
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
        "ceo_img_file": "HCL.jpg",
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
        "ceo_img_file": "Capgemini.jpg",
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
        "ceo_img_file": "Cognizant.jpg",
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
        "ceo_img_file": "Amazon.jpg",
        "headquarters": "Seattle, USA",
        "sector": "E-commerce / Cloud",
        "currency": "USD",
        "disclaimer": "Data fetched from Yahoo Finance",
        "latitude": 47.6062,
        "longitude": -122.3321
    }
}

# -------------------- FUNCTIONS --------------------

def get_ceo_url(file_name):
    """Return full URL for CEO image or placeholder if missing"""
    path = os.path.join(SAVE_DIR, file_name)
    if os.path.exists(path):
        return f"{STATIC_BASE_URL}/{file_name}"
    else:
        return PLACEHOLDER_IMG

def fetch_and_store():
    for symbol, name in tickers.items():
        try:
            # Fetch 1-minute interval data for today
            data = yf.download(symbol, period="1d", interval="1m", progress=False)
            if data is None or data.empty:
                print(f"[{datetime.now()}] ⚠️ No data for {name}")
                continue

            latest = data.tail(1)
            for index, row in latest.iterrows():
                info = company_info[name]
                ceo_url = get_ceo_url(info.get("ceo_img_file", ""))

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
                    ceo_url,
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
                print(f"[{datetime.now()}] ✅ {name} inserted! (CEO image: {ceo_url})")

        except Exception as e:
            print(f"[{datetime.now()}] ❌ Error fetching {name}: {e}")

# -------------------- MAIN LOOP --------------------
print("🚀 Starting real-time stock fetcher (local CEO images)...")

while True:
    fetch_and_store()
    time.sleep(1)  # 1-minute interval





