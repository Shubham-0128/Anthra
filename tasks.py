import webbrowser
import pywhatkit

def run_command(command):
    if "open youtube" in command:
        voice.speak("Opening YouTube")
        print("🤖 Opening YouTube...")
        webbrowser.open("https://www.youtube.com")
    elif "search for" in command:
        query = command.split("search for")[-1].strip()
        if query:
            voice.speak(f"Searching for {query}")
            print(f"🤖 Searching for {query}...")
            webbrowser.open(f"https://www.google.com/search?q={query}")
    elif "play" in command:
        song = command.split("play")[-1].strip()
        if song:
            voice.speak(f"Playing {song} on YouTube")
            print(f"🤖 Playing {song} on YouTube...")
            pywhatkit.playonyt(song)
    else:
        print("🤖 Command not recognized.")
