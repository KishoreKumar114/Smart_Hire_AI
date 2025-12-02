from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ✅ Route for verifying login
@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    key = data.get('key')

    if email == "owner@supermarket.com" and password == "OwnerStrongPass!2025" and key == "MySecretKey123":
        return jsonify({"status": "success", "message": "Access granted"})
    else:
        return jsonify({"status": "error", "message": "Access denied"}), 401


if __name__ == '__main__':
    app.run(debug=True)
