# voice.py
import whisper
import sounddevice as sd
import numpy as np
import queue
import tempfile
import os
import pyttsx3
import scipy.io.wavfile

# Load Whisper model (tiny/base/small/medium/large)
model = whisper.load_model("base")

# TTS engine setup
engine = pyttsx3.init()
engine.setProperty('rate', 170)  # Speech rate

# Audio queue
q = queue.Queue()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def audio_callback(indata, frames, time, status):
    if status:
        print("Recording error:", status)
    q.put(indata.copy())

def recognize_speech(duration=5, samplerate=16000):
    print("🎤 Listening for", duration, "seconds...")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        filename = f.name

        with sd.InputStream(samplerate=samplerate, channels=1, callback=audio_callback):
            audio = []
            for _ in range(int(duration * samplerate / 1024)):
                data = q.get()
                audio.append(data)
            audio_np = np.concatenate(audio, axis=0)

        # Save recorded audio
        scipy.io.wavfile.write(filename, samplerate, audio_np)

    # Transcribe using Whisper
    print("🧠 Transcribing...")
    result = model.transcribe(filename, language="en")
    text = result["text"].strip()

    print("🗣️ You said:", text)
    os.remove(filename)
    return text

