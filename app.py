from flask import Flask, request, jsonify
import os, json

app = Flask(__name__)

# ملف البيانات المحلي
DATA_FILE = "data.json"

# تحميل البيانات
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# حفظ البيانات
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# المسارات
@app.route("/api/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "Aucun fichier envoyé"}), 400
    file = request.files["file"]
    file.save(DATA_FILE)
    return jsonify({"status": "ok", "message": "Fichier sauvegardé"})

@app.route("/api/download/<filename>", methods=["GET"])
def download(filename):
    if not os.path.exists(DATA_FILE):
        return jsonify({"status": "error", "message": "Fichier inexistant"}), 404
    return app.send_static_file(DATA_FILE)

@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify(load_data())

@app.route("/api/add", methods=["POST"])
def add():
    data = request.json
    if not data or "ref" not in data or "description" not in data:
        return jsonify({"status": "error", "message": "Données invalides"}), 400
    all_data = load_data()
    all_data.append(data)
    save_data(all_data)
    return jsonify({"status": "ok", "message": "Ajouté", "data": data})

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API fonctionne"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
