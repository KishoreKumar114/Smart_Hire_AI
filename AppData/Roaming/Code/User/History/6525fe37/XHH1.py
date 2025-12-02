import pandas as pd
import os, time, glob
from twilio.rest import Client
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)

# ✅ Look for latest uploaded CSV in backend/uploads/
UPLOAD_FOLDER = os.path.join("backend", "uploads")
csv_files = glob.glob(os.path.join(UPLOAD_FOLDER, "*.csv"))

if not csv_files:
    print("❌ No CSV files found in backend/uploads/. Please upload a dataset from the app first.")
    exit()

latest_file = max(csv_files, key=os.path.getctime)
print(f"📂 Using latest uploaded file: {os.path.basename(latest_file)}")

# ✅ Load dataset
try:
    df = pd.read_csv(latest_file, encoding='utf-16')
except Exception:
    df = pd.read_csv(latest_file, encoding='utf-8')

print("\n📋 Columns found:", df.columns.tolist())
print(df.head(), "\n")

# ✅ Ask which columns to use
phone_col = input("📞 Enter th_
