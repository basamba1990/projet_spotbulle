from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from werkzeug.utils import secure_filename
from models.transcriber import transcribe_video
from models.classifier import classify_pitch
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Créer l'application Flask
app = Flask(__name__)

# Configurer l'application avec les variables d'environnement
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")  
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///database.db")  
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "static/uploads")

# Créer le dossier d'upload s'il n'existe pas
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload")
def upload_page():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "Aucun fichier reçu"}), 400
    file = request.files["file"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # Transcrire la vidéo en texte
    text = transcribe_video(filepath)

    # Classifier le pitch basé sur la transcription
    category = classify_pitch(text)

    return jsonify({"transcription": text, "category": category})

@app.route("/feedback", methods=["GET", "POST"])
def feedback_page():
    if request.method == "POST":
        user_feedback = request.form.get("feedback")
        category = request.form.get("category")
        # Ici, vous pouvez stocker le feedback dans une base de données
        print(f"Feedback reçu : {user_feedback} pour la catégorie {category}")
        return redirect(url_for("index"))

    return render_template("feedback.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render fournit le port dynamiquement
    app.run(host="0.0.0.0", port=port, debug=True)
