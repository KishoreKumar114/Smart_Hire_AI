import yfinance as yf
import pymysql
import time
from datetime import datetime
import warnings
import requests
import os

# Suppress warnings
warnings.filterwarnings("ignore")

# ✅ MySQL connection — edit password / host if needed
db = pymysql.connect(
    host="localhost",
    user="root",
    password="pass123",
    database="stockdb",
    charset='utf8mb4'
)
cursor = db.cursor()

# ✅ Company tickers
tickers = {
    "INFY.NS": "Infosys",
    "TCS.NS": "TCS",
    "HCLTECH.NS": "HCL",
    "CAP.PA": "Capgemini",
    "CTSH": "Cognizant",
    "AMZN": "Amazon"
}

# ✅ Company info (logos + CEO photos)
company_info = {
    "Infosys": {
        "logo_url": "https://img.logo.dev/infosys.com",
        "ceo": "Salil Parekh",
        "ceo_img_url": "https://upload.wikimedia.org/wikipedia/commons/1/15/Salil_Parekh_Infosys.jpg",
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
        "ceo_img_url": "https://upload.wikimedia.org/wikipedia/commons/6/6e/K_Krithivasan_TCS.jpg",
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
        "ceo_img_url": "https://upload.wikimedia.org/wikipedia/commons/d/d5/C_Vijayakumar_HCL.jpg",
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
        "ceo_img_url": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Aiman_Ezzat_Capgemini.jpg",
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
        "ceo_img_url": "https://upload.wikimedia.org/wikipedia/commons/a/af/Ravi_Kumar_S_Cognizant.jpg",
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
        "ceo_img_url": "https://upload.wikimedia.org/wikipedia/commons/1/1e/Andy_Jassy_2021.jpg",
        "headquarters": "Seattle, USA",
        "sector": "E-commerce / Cloud",
        "currency": "USD",
        "disclaimer": "Data fetched from Yahoo Finance",
        "latitude": 47.6062,
        "longitude": -122.3321
    }
}

# ✅ Folder + URL setup for CEO images
SAVE_DIR = "ceo_images"  # local folder
STATIC_BASE_URL = "http://localhost/ceo_images"  # for XAMPP / local web server
os.makedirs(SAVE_DIR, exist_ok=True)

# ✅ Placeholder if no image available
PLACEHOLDER_IMG = f"{STATIC_BASE_URL}/placeholder_ceo.png"

# --- Helper Functions ---

def is_image_url_valid(url, timeout=10):
    """Quick check if URL returns valid image"""
    try:
        r = requests.head(url, allow_redirects=True, timeout=timeout)
        ct = r.headers.get("Content-Type", "")
        return r.status_code == 200 and "image" in ct.lower()
    except Exception:
        return False


def download_image_and_host(name, url, save_dir=SAVE_DIR):
    """Download image and return hosted URL (or None)"""
    try:
        r = requests.get(url, stream=True, timeout=15)
        r.raise_for_status()
        ct = r.headers.get("Content-Type", "").lower()
        ext = ".jpg" if "jpeg" in ct or "jpg" in ct else ".png"
        filename = f"{name.replace(' ','_')}{ext}"
        path = os.path.join(save_dir, filename)
        with open(path, "wb") as f:
            for chunk in r.iter_content(1024):
                if chunk:
                    f.write(chunk)
        return f"{STATIC_BASE_URL}/{filename}"
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Image download failed for {name}: {e}")
        return None


def prepare_ceo_url(name, original_url):
    """Return reliable CEO image URL"""
    if original_url and is_image_url_valid(original_url):
        return original_url
    hosted = download_image_and_host(name, original_url)
    if hosted:
        return hosted
    return PLACEHOLDER_IMG


# --- Fetch + Store Loop ---

def fetch_and_store():
    for symbol, name in tickers.items():
        try:
            data = yf.download(symbol, period="1d", interval="1m", progress=False)
            if data is None or data.empty:
                print(f"[{datetime.now()}] ⚠️ No data for {name} ({symbol})")
                continue

            latest = data.tail(1)
            for index, row in latest.iterrows():
                info = company_info[name]
                original_ceo_url = info.get("ceo_img_url", "")
                final_ceo_url = prepare_ceo_url(name, original_ceo_url)

                insert_tuple = (
                    name,
                    index.to_pydatetime(),
                    float(row["Open"]),
                    float(row["High"]),
                    float(row["Low"]),
                    float(row["Close"]),
                    int(row["Volume"]) if row["Volume"] is not None else 0,
                    info.get("logo_url"),
                    info.get("ceo"),
                    final_ceo_url,
                    info.get("headquarters"),
                    info.get("sector"),
                    info.get("currency"),
                    info.get("disclaimer"),
                    info.get("latitude"),
                    info.get("longitude")
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
                print(f"[{datetime.now()}] ✅ {name} data inserted! (CEO image: {final_ceo_url})")

        except Exception as e:
            print(f"[{datetime.now()}] ❌ Error fetching {name}: {e}")


print("🚀 Starting real-time stock fetcher with reliable CEO image handling...")

# ✅ Run loop every 60 sec
while True:
    fetch_and_store()
    time.sleep(2)


