from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

DATA_FILE = "data.json"

# تأكد أن الملف موجود
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

@app.route("/")
def home():
    return jsonify({"message": "Bienvenue sur l'API Oscaro"})

@app.route("/api/upload", methods=["POST"])
def upload_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    file.save(DATA_FILE)
    return jsonify({"status": "OK", "message": "File uploaded"})

@app.route("/api/download/<filename>", methods=["GET"])
def download_data(filename):
    if os.path.exists(DATA_FILE):
        return app.send_static_file(DATA_FILE)
    return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
