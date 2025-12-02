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
phone_col = input("📞 Enter the column name that has phone numbers: ").strip()
name_col = input("👤 Enter the column name for customer name (or press Enter to skip): ").strip()

# ✅ Optional category filtering
if "Segment" in df.columns:
    use_segment = input("🎯 Filter by category (Premium/Regular/Normal)? (y/n): ").lower()
    if use_segment == "y":
        seg = input("Enter category to send (e.g. Premium): ").strip()
        df = df[df["Segment"].str.lower() == seg.lower()]
        print(f"✅ Sending only to '{seg}' customers.")
else:
    print("ℹ️ No 'Segment' column found. Sending to all.")

print(f"\n📢 Total numbers found: {len(df)}")
confirm = input("Proceed to send SMS? (y/n): ").lower()

if confirm != "y":
    print("❌ Cancelled.")
    exit()

# ✅ Send SMS to each number
success, failed = 0, 0
for _, row in df.iterrows():
    name = row[name_col] if name_col and name_col in df.columns else "Customer"
    phone = str(row[phone_col]).strip()
    if not phone.startswith("+"):
        phone = f"+{phone}"

    msg = f"Hello {name}! 🎉 Exclusive offers waiting for you at Smart Supermarket. Visit us today!"

    try:
        client.messages.create(body=msg, from_=from_number, to=phone)
        print(f"✅ Sent to {name} ({phone})")
        success += 1
    except Exception as e:
        print(f"❌ Failed for {phone}: {e}")
        failed += 1

    time.sleep(1)

print(f"\n✅ SMS sent: {success}, ❌ Failed: {failed}")
backend/uploads/
