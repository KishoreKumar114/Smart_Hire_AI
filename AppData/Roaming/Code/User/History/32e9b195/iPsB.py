import yfinance as yf
import pymysql
import time
from datetime import datetime

# ✅ MySQL connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="pass123",   # ⚠️ your actual MySQL password
    database="stockdb"
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

# ✅ Company Logos
logos = {
    "Infosys": "https://logo.clearbit.com/infosys.com",
    "TCS": "https://logo.clearbit.com/tcs.com",
    "HCL": "https://logo.clearbit.com/hcltech.com",
    "Capgemini": "https://logo.clearbit.com/capgemini.com",
    "Cognizant": "https://logo.clearbit.com/cognizant.com",
    "Amazon": "https://logo.clearbit.com/amazon.com"
}

# ✅ CEO Images
ceo_images = {
    "Infosys": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Salil_Parekh.jpg",
    "TCS": "https://qph.cf2.quoracdn.net/main-qimg-59d1a3f9b03b77278cbaa9f2b6b1efad",
    "HCL": "https://upload.wikimedia.org/wikipedia/commons/1/16/C_Vijayakumar_HCL.jpg",
    "Capgemini": "https://media.licdn.com/dms/image/C4E03AQEBuVtN0pVQ_g/profile-displayphoto-shrink_200_200/0/1597935526882",
    "Cognizant": "https://upload.wikimedia.org/wikipedia/commons/9/9c/Ravi_Kumar_S.jpg",
    "Amazon": "https://upload.wikimedia.org/wikipedia/commons/0/05/Andy_Jassy.jpg"
}

# ✅ Company Extra Details (HQ + Coordinates)
company_details = {
    "Infosys": {
        "ceo": "Salil Parekh", "sector": "IT Services", "hq": "Bengaluru, India",
        "lat": 12.9716, "lon": 77.5946
    },
    "TCS": {
        "ceo": "K. Krithivasan", "sector": "IT Services", "hq": "Mumbai, India",
        "lat": 19.0760, "lon": 72.8777
    },
    "HCL": {
        "ceo": "C. Vijayakumar", "sector": "IT Services", "hq": "Noida, India",
        "lat": 28.5355, "lon": 77.3910
    },
    "Capgemini": {
        "ceo": "Aiman Ezzat", "sector": "IT Consulting", "hq": "Paris, France",
        "lat": 48.8566, "lon": 2.3522
    },
    "Cognizant": {
        "ceo": "Ravi Kumar S", "sector": "IT Consulting", "hq": "Teaneck, USA",
        "lat": 40.8976, "lon": -74.0163
    },
    "Amazon": {
        "ceo": "Andy Jassy", "sector": "E-Commerce", "hq": "Seattle, USA",
        "lat": 47.6062, "lon": -122.3321
    }
}

def fetch_and_store():
    for symbol, name in tickers.items():
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1d", interval="1m")
            if not data.empty:
                latest = data.tail(1)
                info = stock.info

                for index, row in latest.iterrows():
                    cursor.execute("""
                        INSERT INTO stocks 
                        (company, datetime, open, high, low, close, volume, logo_url,
                         sector, ceo, headquarters, currency, disclaimer, market_cap, pe_ratio,
                         ceo_img_url, latitude, longitude)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (
                        name,
                        index.to_pydatetime(),
                        float(row["Open"]),
                        float(row["High"]),
                        float(row["Low"]),
                        float(row["Close"]),
                        int(row["Volume"]),
                        logos[name],
                        company_details[name]["sector"],
                        company_details[name]["ceo"],
                        company_details[name]["hq"],
                        info.get("currency", "N/A"),
                        "⚠️ Educational Purpose Only",
                        info.get("marketCap", None),
                        info.get("trailingPE", None),
                        ceo_images[name],
                        company_details[name]["lat"],
                        company_details[name]["lon"]
                    ))
                    db.commit()
                print(f"[{datetime.now()}] ✅ {name} data inserted with map coordinates!")
            else:
                print(f"[{datetime.now()}] ⚠️ No data for {name}")
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Error fetching {name}: {e}")

print("🚀 Starting real-time stock fetcher with logos, CEO images & map coordinates...")

while True:
    fetch_and_store()
    time.sleep(5)
