from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

VALID_API_KEY = "your-secret-key"

@app.route('/verify', methods=['POST'])
def verify_key():
    data = request.get_json()
    api_key = data.get('api_key')
    if api_key == VALID_API_KEY:
        return jsonify({"status": "success", "message": "Valid API Key!"})
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True)
