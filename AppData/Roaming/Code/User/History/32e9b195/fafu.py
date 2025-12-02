
import yfinance as yf
import pymysql
import time
from datetime import datetime
import warnings
import os

# Suppress warnings
warnings.filterwarnings("ignore")

# ---------------- CONFIG ----------------

# MySQL connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="pass123",
    database="stockdb",
    charset='utf8mb4'
)
cursor = db.cursor()

# Local folder with CEO and logo images
IMAGE_DIR = "ceo_images"
STATIC_BASE_URL = "http://localhost/ceo_images"  # XAMPP local server

# Ensure folder exists
os.makedirs(IMAGE_DIR, exist_ok=True)

# ---------------- DATA ----------------

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
        "logo_url": f"{STATIC_BASE_URL}/infosys_logo.png",
        "ceo": "Salil Parekh",
        "ceo_img_url": f"{STATIC_BASE_URL}/infosys_ceo.png",
        "headquarters": "Bangalore, India",
        "sector": "IT Services",
        "currency": "INR",
        "disclaimer": "Data for educational use only",
        "latitude": 12.9716,
        "longitude": 77.5946
    },
    "TCS": {
        "logo_url": f"{STATIC_BASE_URL}/tcs_logo.png",
        "ceo": "K. Krithivasan",
        "ceo_img_url": f"{STATIC_BASE_URL}/tcs_ceo.png",
        "headquarters": "Mumbai, India",
        "sector": "IT Services",
        "currency": "INR",
        "disclaimer": "Data for educational use only",
        "latitude": 19.0760,
        "longitude": 72.8777
    },
    "HCL": {
        "logo_url": f"{STATIC_BASE_URL}/hcl_logo.png",
        "ceo": "C. Vijayakumar",
        "ceo_img_url": f"{STATIC_BASE_URL}/hcl_ceo.png",
        "headquarters": "Noida, India",
        "sector": "IT Services",
        "currency": "INR",
        "disclaimer": "Data for educational use only",
        "latitude": 28.5355,
        "longitude": 77.3910
    },
    "Capgemini": {
        "logo_url": f"{STATIC_BASE_URL}/capgemini_logo.png",
        "ceo": "Aiman Ezzat",
        "ceo_img_url": f"{STATIC_BASE_URL}/capgemini_ceo.png",
        "headquarters": "Paris, France",
        "sector": "IT Consulting",
        "currency": "EUR",
        "disclaimer": "Data for educational use only",
        "latitude": 48.8566,
        "longitude": 2.3522
    },
    "Cognizant": {
        "logo_url": f"{STATIC_BASE_URL}/cognizant_logo.png",
        "ceo": "Ravi Kumar S",
        "ceo_img_url": f"{STATIC_BASE_URL}/cognizant_ceo.png",
        "headquarters": "Teaneck, USA",
        "sector": "IT Services",
        "currency": "USD",
        "disclaimer": "Data for educational use only",
        "latitude": 40.8976,
        "longitude": -74.0159
    },
    "Amazon": {
        "logo_url": f"{STATIC_BASE_URL}/amazon_logo.png",
        "ceo": "Andy Jassy",
        "ceo_img_url": f"{STATIC_BASE_URL}/amazon_ceo.png",
        "headquarters": "Seattle, USA",
        "sector": "E-commerce & Cloud",
        "currency": "USD",
        "disclaimer": "Data for educational use only",
        "latitude": 47.6062,
        "longitude": -122.3321
    }
}

# ---------------- FUNCTIONS ----------------

def fetch_and_store():
    for symbol, name in tickers.items():
        try:
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
                    int(row["Volume"]) if row["Volume"] else 0,
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
                print(f"[{datetime.now()}] ✅ {name} inserted with local images!")

        except Exception as e:
            print(f"[{datetime.now()}] ❌ Error fetching {name}: {e}")

# ---------------- MAIN LOOP ----------------

print("🚀 Starting real-time stock fetcher with local CEO/logo images...")

while True:
    fetch_and_store()
    time.sleep(1)  # fetch every 1 min


