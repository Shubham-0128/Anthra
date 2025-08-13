
import whisper
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wav
from tasks import run_command
import voice

# Load the Whisper model
model = whisper.load_model("base")  # You can try "small" or "medium" too
voice.speak("Hello, I am your voice assistant. How can I help you today?")

# Function to record audio and save it temporarily
def record_audio(duration=5, fs=16000):
    print("🎤 Listening...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        wav.write(f.name, fs, recording)
        return f.name

# Continuous loop to listen → transcribe → respond
while True:
    audio_file = record_audio()
    result = model.transcribe(audio_file)
    text = result["text"].strip()

    print("You said:", text)

    if text:
        run_command(text.lower())


