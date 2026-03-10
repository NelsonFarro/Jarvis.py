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
import logging
from typing import Dict, Any, Callable, Optional

# ==========================================
# SETUP LOGGING
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("Jarvis")

class JarvisAssistant:
    def __init__(self, config_file: str = 'config.json'):
        """Initializes the Jarvis Assistant with configuration and TTS engine."""
        self.config: Dict[str, Any] = self._load_config(config_file)
        self.engine: pyttsx3.Engine = self._init_engine()
        
        # Command Registry: Maps command triggers (strings) to handler functions
        self.commands: Dict[str, Callable[[str], bool]] = {}
        self._register_default_commands()

    # ------------------------------------------
    # CONFIGURATION & INITIALIZATION
    # ------------------------------------------
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Loads user-specific configurations."""
        try:
            with open(config_file, 'r') as f:
                logger.info(f"Successfully loaded configuration from {config_file}")
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"{config_file} not found! Please create one using config.example.json.")
            sys.exit(1)
        except json.JSONDecodeError:
            logger.error(f"{config_file} is not a valid JSON file.")
            sys.exit(1)

    def _init_engine(self) -> pyttsx3.Engine:
        """Initializes the text-to-speech engine."""
        try:
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id) # Index 0 for Male, 1 for Female
            logger.info("TTS Engine initialized successfully.")
            return engine
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            sys.exit(1)

    # ------------------------------------------
    # COMMAND REGISTRATION (STRATEGY PATTERN)
    # ------------------------------------------
    def register_command(self, trigger: str, handler: Callable[[str], bool]) -> None:
        """Registers a new voice command."""
        self.commands[trigger.lower()] = handler
        logger.debug(f"Registered command: '{trigger}'")

    def _register_default_commands(self) -> None:
        """Registers all built-in commands."""
        # Core Web Search
        self.register_command("wikipedia", self.cmd_wikipedia)
        self.register_command("open youtube", self.cmd_open_youtube)
        self.register_command("open google", self.cmd_open_google)
        self.register_command("open stackoverflow", self.cmd_open_stackoverflow)
        
        # Local System Tasks
        self.register_command("the time", self.cmd_time)
        self.register_command("play music", self.cmd_play_music)
        
        # Application Launchers
        self.register_command("open code editor", self.cmd_open_vscode)
        self.register_command("open vs code", self.cmd_open_vscode)
        
        # External API Examples
        self.register_command("email", self.cmd_email)
        
        # Control & Exit
        self.register_command("quit", self.cmd_quit)
        self.register_command("exit", self.cmd_quit)
        self.register_command("stop", self.cmd_quit)

    # ------------------------------------------
    # CORE ASSISTANT FUNCTIONS
    # ------------------------------------------
    def speak(self, text: str) -> None:
        """Converts a text string to speech."""
        logger.info(f"Jarvis speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def wish_me(self) -> None:
        """Greets the user based on the current time of day."""
        hour = datetime.datetime.now().hour
        if 4 <= hour < 12:
            self.speak("Good Morning!")
        elif 12 <= hour < 16:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")

        self.speak("Hi, I am Your Virtual Assistant. How may I help you?")

    def take_command(self) -> str:
        """
        Takes microphone input from the user and returns a string output.
        """
        r = sr.Recognizer()
        with sr.Microphone() as source:
            logger.info("Listening...")
            r.energy_threshold = 700            
            r.pause_threshold = 1               
            audio = r.listen(source)
            
        try:
            logger.info("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            logger.info(f"User said: {query}")
            return query.lower()
        except Exception as e:
            logger.warning("Audio not recognized clearly.")
            print("Say that again please...")
            return "none"

    def send_email(self, to_address: str, content: str) -> bool:
        """Sends an email using configured credentials."""
        email_config = self.config.get("email", {})
        sender_email = email_config.get("address")
        sender_password = email_config.get("password")

        if not sender_email or not sender_password:
            logger.error("Email configuration is missing from config.json")
            self.speak("Email configuration is missing.")
            return False

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_address, content)
            server.close()
            logger.info(f"Email sent successfully to {to_address}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    # ------------------------------------------
    # COMMAND HANDLERS
    # ------------------------------------------
    # Note: Handlers return True if the assistant should continue running,
    # or False if it should exit the main loop.
    
    def cmd_wikipedia(self, query: str) -> bool:
        self.speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "").strip()
        try:
            results = wikipedia.summary(query, sentences=2)
            self.speak("According to Wikipedia") 
            print(results)
            self.speak(results)
        except Exception as e:
            logger.error(f"Wikipedia search failed: {e}")
            self.speak("Failed to search Wikipedia. Please try again.")
        return True

    def cmd_open_youtube(self, query: str) -> bool:
        webbrowser.open('youtube.com')
        return True

    def cmd_open_google(self, query: str) -> bool:
        webbrowser.open('google.com')
        return True

    def cmd_open_stackoverflow(self, query: str) -> bool:
        webbrowser.open('stackoverflow.com')
        return True

    def cmd_time(self, query: str) -> bool:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.speak(f"The time is {str_time}")
        return True

    def cmd_play_music(self, query: str) -> bool:
        music_dir = self.config.get("paths", {}).get("music_dir", "")
        if os.path.exists(music_dir):
            songs = os.listdir(music_dir)
            if songs:
                logger.info(f"Playing a random song from: {music_dir}")
                os.startfile(os.path.join(music_dir, random.choice(songs)))
            else:
                self.speak("No songs found in the directory.")
        else:
            self.speak("Music directory not found. Please check your config file.")
        return True

    def cmd_open_vscode(self, query: str) -> bool:
        path = self.config.get("paths", {}).get("vs_code")
        if path and os.path.exists(path):
            os.startfile(path)
        else:
            self.speak("Code Editor path not configured. Please add it to config.json.")
        return True

    def cmd_email(self, query: str) -> bool:
        self.speak("What should I write?")
        content = self.take_command()
        # TODO: Implement a contact dictionary mapping names to emails
        self.speak("Routing to default testing address.")
        to = "test_receiver@gmail.com"  
        if self.send_email(to, content):
            self.speak("Email has been sent.")
        else:
            self.speak("Email was not sent.")
        return True

    def cmd_quit(self, query: str) -> bool:
        self.speak("Goodbye! Have a nice day.")
        return False # Returning False breaks the main loop

    # ------------------------------------------
    # MAIN LOOP
    # ------------------------------------------
    def run(self) -> None:
        """The main loop that listens for and executes commands."""
        self.wish_me()
        
        while True:
            query = self.take_command()
            
            if query == 'none':
                continue

            command_executed = False
            
            # Iterate through registered commands and check if the trigger is in the user's query
            for trigger, handler in self.commands.items():
                if trigger in query:
                    logger.debug(f"Trigger matched: '{trigger}'")
                    should_continue = handler(query)
                    command_executed = True
                    
                    if not should_continue:
                        return # Exit the assistant
                    break # Stop checking other commands once a match is found
            
            if not command_executed:
                logger.debug(f"No command matched for query: '{query}'")


if __name__ == "__main__":
    assistant = JarvisAssistant()
    assistant.run()
