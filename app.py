from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from werkzeug.utils import secure_filename
from models.transcriber import transcribe_video
from models.classifier import classify_pitch

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "Aucun fichier reçu"}), 400
    file = request.files["file"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # Transcription
    text = transcribe_video(filepath)

    # Catégorisation
    category = classify_pitch(text)

    return jsonify({"transcription": text, "category": category})

@app.route("/feedback", methods=["POST"])
def feedback():
    user_feedback = request.form.get("feedback")
    category = request.form.get("category")
    # Ici, vous pouvez stocker le feedback dans une base de données
    print(f"Feedback reçu : {user_feedback} pour la catégorie {category}")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
