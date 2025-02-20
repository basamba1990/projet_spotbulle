import speech_v1p1beta1

model = speech_v1p1beta1.load_model("base")

def transcribe_video(video_path):
    result = model.transcribe(video_path)
    return result["text"]
