echo import pandas as pd
echo import os, time, glob
echo from twilio.rest import Client
echo from dotenv import load_dotenv
echo.
echo load_dotenv()
echo.
echo account_sid = os.getenv("TWILIO_ACCOUNT_SID")
echo auth_token = os.getenv("TWILIO_AUTH_TOKEN")
echo from_number = os.getenv("TWILIO_PHONE_NUMBER")
echo client = Client(account_sid, auth_token)
echo.
echo UPLOAD_FOLDER = os.path.join("backend", "uploads")
echo csv_files = glob.glob(os.path.join(UPLOAD_FOLDER, "*.csv"))
echo if not csv_files:
echo.    print("❌ No CSV files found in backend/uploads/. Please upload a dataset from the app first.")
echo.    exit()
echo.
echo latest_file = max(csv_files, key=os.path.getctime)
echo print(f"📂 Using latest uploaded file: {os.path.basename(latest_file)}")
echo.
echo try:
echo.    df = pd.read_csv(latest_file, encoding='utf-16')
echo except Exception:
echo.    df = pd.read_csv(latest_file, encoding='utf-8')
echo.
echo print("\n📋 Columns found:", df.columns.tolist())
echo print(df.head(), "\n")
echo.
echo phone_col = input("📞 Enter the column name that has phone numbers: ").strip()
echo name_col = input("👤 Enter the column name for customer name (or press Enter to skip): ").strip()
echo.
echo if "Segment" in df.columns:
echo.    use_segment = input("🎯 Filter by category (Premium/Regular/Normal)? (y/n): ").lower()
echo.    if use_segment == "y":
echo.        seg = input("Enter category to send (e.g. Premium): ").strip()
echo.        df = df[df["Segment"].str.lower() == seg.lower()]
echo.        print(f"✅ Sending only to '{seg}' customers.")
echo else:
echo.    print("ℹ️ No 'Segment' column found. Sending to all.")
echo.
echo print(f"\n📢 Total numbers found: {len(df)}")
echo confirm = input("Proceed to send SMS? (y/n): ").lower()
echo if confirm != "y":
echo.    print("❌ Cancelled.")
echo.    exit()
echo.
echo success, failed = 0, 0
echo for _, row in df.iterrows():
echo.    name = row[name_col] if name_col and name_col in df.columns else "Customer"
echo.    phone = str(row[phone_col]).strip()
echo.    if not phone.startswith("+"):
echo.        phone = f"+{phone}"
echo.    msg = f"Hello {name}! 🎉 Exclusive offers waiting for you at Smart Supermarket. Visit us today!"
echo.    try:
echo.        client.messages.create(body=msg, from_=from_number, to=phone)
echo.        print(f"✅ Sent to {name} ({phone})")
echo.        success += 1
echo.    except Exception as e:
echo.        print(f"❌ Failed for {phone}: {e}")
echo.        failed += 1
echo.    time.sleep(1)
echo.
echo print(f"\n✅ SMS sent: {success}, ❌ Failed: {failed}")