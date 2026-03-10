import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import json
import random
import sys

# ==========================================
# CONFIGURATION LOADER
# ==========================================
def load_config():
    """
    Loads user-specific configurations such as API keys, custom paths,
    and credentials from a config.json file. This keeps the main codebase
    clean and secure.
    """
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found! Please create one by copying config.example.json.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: config.json is not a valid JSON file.")
        sys.exit(1)

config = load_config()

# ==========================================
# INITIALIZE TEXT-TO-SPEECH ENGINE
# ==========================================
engine = pyttsx3.init('sapi5') # sapi5 is Microsoft's Speech API
voices = engine.getProperty('voices')

# Set Voice Type:
# voices[0].id -> Male Voice
# voices[1].id -> Female Voice
engine.setProperty('voice', voices[0].id)   


def speak(audio):
    """Converts a text string to speech"""
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """Greets the user based on the current time of day"""
    hour = int(datetime.datetime.now().hour)
    if hour >= 4 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 16:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("Hi, I am Your Virtual Assistant. How may I help you?")

def takeCommand():
    """
    Takes microphone input from the user and returns a string output.
    This function uses Google's Speech Recognition API.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 700            # Adjust for ambient background noise
        r.pause_threshold = 1               # Seconds of no speech before a phrase is considered complete
        audio = r.listen(source)
        
    try:
        print("Recognizing...")
        # Using Google Speech Recognition (requires an internet connection)
        query = r.recognize_google(audio, language='en-in')
        print(f"User said :  {query}\n")
    except Exception as e:
        # Happens when audio isn't clear or there's an internet issue
        print("Say that again please...")
        return "none"
    
    return query


def sendEmail(to, content):
    """
    Sends an email using dummy credentials loaded from config.json.
    Note: You may need to generate an 'App Password' for Gmail to allow this.
    """
    email_config = config.get("email", {})
    sender_email = email_config.get("address")
    sender_password = email_config.get("password")

    if not sender_email or not sender_password:
        print("Email configuration is missing from config.json")
        speak("Email configuration is missing.")
        return

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to, content)
        server.close()
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise e

# ==========================================
# MAIN EXECUTION LOOP
# ==========================================
def main():
    speak("Hello user")
    wishMe()
    
    while True:
        # Take user command and convert to lowercase for easier string matching
        query = takeCommand().lower()
        
        # Uncomment below line to take text input instead of voice (good for debugging)
        # query = input("Enter command: ").lower()     

        if 'none' in query:
            continue

        # ------------------------------------------
        # 1. CORE WEB SEARCH FEATURES
        # ------------------------------------------
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia") 
                print(results)
                speak(results)
            except Exception as e:
                speak("Failed to search Wikipedia. Please try again.")
        
        elif "open youtube" in query:
            webbrowser.open('youtube.com')

        elif "open google" in query:
            webbrowser.open('google.com')

        elif "open stackoverflow" in query:
            webbrowser.open('stackoverflow.com')

        # ------------------------------------------
        # 2. LOCAL SYSTEM TASKS
        # ------------------------------------------
        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif "play music" in query:
            # Reads the music directory path from config.json
            music_dir = config.get("paths", {}).get("music_dir", "")
            if os.path.exists(music_dir):
                songs = os.listdir(music_dir)
                if songs:
                    print(f"Playing a random song from: {music_dir}")
                    os.startfile(os.path.join(music_dir, random.choice(songs)))
                else:
                    speak("No songs found in the directory.")
            else:
                speak("Music directory not found. Please check your config file.")

        # ------------------------------------------
        # 3. APPLICATION LAUNCHERS
        # ------------------------------------------
        # Example: How to open an application based on a path from config.json
        # Add your own custom application launchers here!
        elif "open code editor" in query or "open vs code" in query:
            # Look up the "vs_code" key inside the "paths" object in config.json
            path = config.get("paths", {}).get("vs_code")
            if path and os.path.exists(path):
                os.startfile(path)
            else:
                speak("Code Editor path not configured. Please add it to config.json.")

        # ------------------------------------------
        # 4. EXTERNAL API EXAMPLES (Email)
        # ------------------------------------------
        elif "email" in query:
            try:
                speak("What should I write?")
                content = takeCommand()
                # TODO: Implement a contact dictionary mapping names to emails
                to = "test_receiver@gmail.com"  
                sendEmail(to, content)
                speak("Email has been sent.")
            except Exception as e:
                print(e)
                speak("Email was not sent.")
                
        # ------------------------------------------
        # 5. CONTROL & EXIT
        # ------------------------------------------
        elif "quit" in query or "exit" in query or "stop" in query:
            speak("Goodbye! Have a nice day.")
            break

if __name__ == "__main__":
    main()
