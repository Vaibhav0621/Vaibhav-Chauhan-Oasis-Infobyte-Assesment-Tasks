"""Listen for simple English commands and speak the result."""

import re
import webbrowser
from datetime import datetime
from urllib.parse import urlencode


def handle_command(command):
    """Return a response and whether the assistant should keep listening."""
    command = " ".join(command.split()).rstrip(".?!")
    words = command.lower()

    if words in {"exit", "stop", "quit", "goodbye"}:
        return "Goodbye!", False
    if words in {"hello", "hi", "hey"}:
        return "Hello! How can I help you?", True
    if words in {"time", "what time is it", "what is the time", "tell me the time"}:
        now = datetime.now()
        return f"The time is {now.strftime('%I:%M %p').lstrip('0')}.", True
    if words in {"date", "what is the date", "what day is it", "tell me the date"}:
        today = datetime.now()
        return f"Today is {today.strftime('%A, %B')} {today.day}, {today.year}.", True

    if words in {"search", "search for", "search the web", "search the web for"}:
        return "Try saying search for, followed by the topic.", True

    search = re.fullmatch(r"search(?: the web)?(?: for)? (.+)", command, re.IGNORECASE)
    if search:
        topic = search[1]
        url = "https://www.google.com/search?" + urlencode({"q": topic})
        try:
            opened = webbrowser.open_new_tab(url)
        except (webbrowser.Error, OSError):
            opened = False
        if opened:
            return f"I opened a search for {topic}.", True
        return "I could not open your browser. Check your default browser settings.", True

    return "Try saying hello, time, date, search for a topic, or stop.", True


def main():
    try:
        import pyttsx3
        import speech_recognition as sr
    except ImportError as error:
        print(f"Voice dependencies are unavailable ({error}). Install requirements.txt first.")
        return 1

    try:
        engine = pyttsx3.init()
    except Exception as error:
        # Speech drivers expose different exception types on each platform.
        print(f"Could not start text-to-speech: {error}")
        print("Check that a system text-to-speech voice is installed and available.")
        return 1

    def speak(message):
        print(message, flush=True)
        engine.say(message)
        engine.runAndWait()

    recognizer = sr.Recognizer()
    recognizer.operation_timeout = 10
    try:
        microphone = sr.Microphone()
        speak("Voice assistant ready. Say hello, time, date, search for a topic, or stop.")
        with microphone as source:
            print("Calibrating microphone. Stay quiet for a moment.", flush=True)
            recognizer.adjust_for_ambient_noise(source, duration=0.6)

        keep_listening = True
        while keep_listening:
            try:
                with microphone as source:
                    print("Listening...", flush=True)
                    audio = recognizer.listen(source, timeout=7, phrase_time_limit=8)
                command = recognizer.recognize_google(audio)
            except sr.WaitTimeoutError:
                speak("I did not hear anything. Please try again.")
                continue
            except sr.UnknownValueError:
                speak("I could not understand that. Please repeat.")
                continue
            except (sr.RequestError, TimeoutError):
                speak("Speech recognition is unavailable. Check your internet connection and try again.")
                continue

            response, keep_listening = handle_command(command)
            speak(response)
    except (AttributeError, OSError) as error:
        print(f"Audio error: {error}")
        speak("Check that a microphone is connected and permitted in your system settings.")
        return 1
    except KeyboardInterrupt:
        speak("Goodbye!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
