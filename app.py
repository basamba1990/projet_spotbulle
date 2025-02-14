from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import requests

app = Flask(__name__)
CORS(app)

# 📌 Configuration de la base de données SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "uploads"
db = SQLAlchemy(app)

# 📌 Assurer que le dossier uploads existe
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# 📌 URL de l'API Google Colab pour l'analyse (Mettre à jour avec l'URL de ngrok)
COLAB_API_URL = "https://985a-34-169-105-177.ngrok-free.app"

# 📌 Modèle pour stocker les vidéos et leur analyse
class Pitch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    video_url = db.Column(db.String(255), nullable=False)
    transcription = db.Column(db.Text, nullable=True)
    feedback = db.Column(db.Text, nullable=True)

# 📌 Initialisation correcte de la base de données
with app.app_context():
    db.create_all()

# 📌 Route pour l’upload des vidéos et l’envoi à Google Colab
@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier trouvé"}), 400

    file = request.files['file']
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # 📌 Envoyer la vidéo à Google Colab pour analyse
    with open(file_path, "rb") as f:
        response = requests.post(COLAB_API_URL, files={"file": f})

    if response.status_code == 200:
        data = response.json()
        transcription = data.get("transcription", "")
        feedback = data.get("analysis", "")

        # 📌 Sauvegarde en BDD
        pitch = Pitch(user_id=1, video_url=file.filename, transcription=transcription, feedback=feedback)
        db.session.add(pitch)
        db.session.commit()

        return jsonify({"message": "Pitch enregistré !", "transcription": transcription, "feedback": feedback})
    else:
        return jsonify({"error": "Erreur lors de l'analyse"}), 500

# 📌 Route pour afficher la liste des vidéos stockées
@app.route('/videos', methods=['GET'])
def list_videos():
    videos = [{"id": pitch.id, "video_url": pitch.video_url, "transcription": pitch.transcription, "feedback": pitch.feedback} for pitch in Pitch.query.all()]
    return jsonify({"videos": videos})

# 📌 Route pour récupérer une vidéo
@app.route('/uploads/<filename>')
def get_video(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
