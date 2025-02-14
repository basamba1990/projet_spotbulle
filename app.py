from flask import Flask, request, render_template, jsonify
from pyngrok import ngrok
import whisper
import google.generativeai as genai
import os

# Initialiser l'application Flask
app = Flask(__name__)

# Vérifier que le dossier uploads existe
os.makedirs("uploads", exist_ok=True)

# Charger les modèles IA
whisper_model = whisper.load_model("base")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-2.0-flash')

# Route d'accueil qui renvoie le formulaire HTML
@app.route('/')
def home():
    return render_template('form.html')  # Assurez-vous que le fichier form.html est dans le dossier "templates"

# Route pour analyser les fichiers audio/vidéo envoyés
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier trouvé"}), 400

    file = request.files['file']
    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    # Transcrire la vidéo ou l'audio
    result = whisper_model.transcribe(filepath)
    transcription = result["text"]

    # Analyser le pitch
    response = gemini_model.generate_content(f"Analyse ce pitch : {transcription}")

    # Retourner la transcription et l'analyse
    return jsonify({"transcription": transcription, "analysis": response.text})

# Lancer Flask avec Ngrok pour avoir un tunnel public
public_url = ngrok.connect(5000)
print(f"Ngrok Tunnel URL: {public_url}")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
