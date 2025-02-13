from flask import Flask, request, jsonify
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

nlp = spacy.load("fr_core_news_md")

pitchs_stockes = [
    "Plateforme pour l'éducation en ligne.",
    "Startup dans les énergies renouvelables.",
    "Application pour les jeunes entrepreneurs."
]

categories = {
    "Éducation": ["éducation", "apprentissage", "formation"],
    "Énergies renouvelables": ["solaire", "écologie"],
    "Technologie": ["IA", "robotique", "numérique"]
}

def categoriser_pitch(pitch):
    doc = nlp(pitch)
    for cat, mots in categories.items():
        if any(mot in doc.text.lower() for mot in mots):
            return cat
    return "Autre"

def calculer_similarite(nouveau_pitch):
    pitchs = pitchs_stockes + [nouveau_pitch]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(pitchs)
    similarites = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    return similarites.flatten().tolist()

@app.route('/analyse', methods=['POST'])
def analyser_pitch():
    data = request.json
    pitch = data.get("pitch")
    categorie = categoriser_pitch(pitch)
    similarites = calculer_similarite(pitch)
    return jsonify({"categorie": categorie, "similarites": similarites})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
