from google.cloud import speech_v1p1beta1 as speech
import os

def transcribe_video(video_path: str) -> str:
    """ Transcrit l'audio d'une vidéo en texte avec Google Speech-to-Text. """
    client = speech.SpeechClient()
    
    with open(video_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="fr-FR",
    )

    response = client.recognize(config=config, audio=audio)
    
    transcription = " ".join(result.alternatives[0].transcript for result in response.results)
    
    return transcription.strip()
