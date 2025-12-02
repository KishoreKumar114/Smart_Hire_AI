from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    key = data.get("key")

    # ✅ Check values (use your real ones here)
    if email == "owner@supermarket.com" and password == "OwnerStrongPass!2025" and key == "MySecretKey123":
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "failed"})

if __name__ == "__main__":
    app.run(debug=True)
cd C:\Users\Lenovo\Downloads\smart-supermarket-analytics-dashboard\frontend
npm run dev
