import google.generativeai as genai

genai.configure(api_key="VOTRE_CLE_GEMINI")

def classify_pitch(text):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Classifie ce pitch en catégorie (Tech, Santé, Éducation, Finance) : {text}"
    response = model.generate_content(prompt)
    return response.text
