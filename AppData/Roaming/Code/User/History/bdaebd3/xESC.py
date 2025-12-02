from flask import Flask, request, jsonify

app = Flask(__name__)

# ✅ Correct credentials
VALID_EMAIL = "owner@supermarket.com"
VALID_PASSWORD = "OwnerStrongPass!2025"
VALID_KEY = "MySecretKey123"

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    if (
        data.get("email") == VALID_EMAIL
        and data.get("password") == VALID_PASSWORD
        and data.get("key") == VALID_KEY
    ):
        return jsonify({"status": "success", "message": "Access granted"})
    else:
        return jsonify({"status": "fail", "reason": "access_denied"}), 401

if __name__ == '__main__':
    app.run(debug=True)
python verify_key.py

