# Jarvis - Python Virtual Assistant

A voice-controlled virtual assistant written in Python. This is an excellent project for learning about Speech Recognition, Text-to-Speech (TTS), and system automation. It can perform tasks like opening applications, searching Wikipedia, opening websites, playing music, and more.

## Features
- **Voice Recognition**: Understands your voice commands using `SpeechRecognition`.
- **Text-to-Speech**: Speaks back to you using `pyttsx3`.
- **Wikipedia Lookups**: Summarizes Wikipedia articles and reads them aloud.
- **Web Browsing**: Automatically opens YouTube, Google, StackOverflow, Instagram, etc.
- **Application Launcher**: Can open VS Code, Sublime Text, Android Studio, and games.
- **System Tasks**: Tells you the current time.

## System Requirements
- Python 3.7+
- A working microphone
- Internet connection (for Speech Recognition and Web features)
- Windows OS (recommended, due to `sapi5` TTS engine and `os.startfile`)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/jarvis.git
   cd jarvis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: If you run into issues installing `PyAudio` on Windows, you may need to install it from a pre-compiled wheel using `pipwin install pyaudio` or by downloading the appropriate `.whl` file from [lfd.uci.edu](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).*

3. **Configure the application**
   - Copy `config.example.json` to `config.json`
   - Open `config.json` and change the paths to match your PC's application directories.
   - Update your email address and password if you plan to use the email feature.
   *(Note: For Gmail, you may need to use an "App Password" due to security restrictions).*

4. **Run Jarvis**
   ```bash
   python jarvis.py
   ```

## Customization
To add new applications, update the `config.json` file with the absolute path of the `.exe` file, and add an `elif` condition in `jarvis.py` following the existing format.

## Troubleshooting
- **Microphone not picking up audio**: Ensure your default system microphone is correctly set. You might want to tweak the `r.energy_threshold` value in `takeCommand()` if there is too much background noise.
- **`os.startfile` error**: Make sure the application paths in your `config.json` are exact absolute paths.
