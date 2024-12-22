import whisper

def transcribe_audio(audio_file):
    model = whisper.load_model("medium")
    result = model.transcribe(audio_file)
    return result["text"]

if __name__ == "__main__":
    audio_file = "/app/input.m4a"
    result = transcribe_audio(audio_file)
    print("Transcription: ", result)

