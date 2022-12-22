import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[0].id)                        # make voices[0].id to get male voice 
engine.setProperty('voice', voices[0].id)   # make voices[1].id to get female voice 


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=4 and hour<12:
        speak("Good Morning!")
    
    elif hour>=12 and hour<16:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("Hi, I am Your Virtual Assistant, How may I help you?")

def takeCommand():
    #It takes microphone inputs from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 700            # ---------- for saying the commands louder so that background voices won't be captured
        r.pause_threshold = 1               # ---------- break to end command in seconds
        audio = r.listen(source)
        

    try:
        print("Recognizion...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said :  {query}\n")

    except Exception as e:
        print("Say that again please...")
        return "none"
    
    return query


def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("dummymail@gmail.com", "passwordInputHere")      #password to put in a file for security reasons
    server.sendmail("dummymail@gmail.com", to, content)
    server.close()

if __name__ == "__main__":
    speak("hello user")
    wishMe()
    
    while True:
        query = takeCommand().lower()
        #query = input("enter command ")                        #to take commands while typing
        #logic for executing task based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)     #change sentences = 1 for one line 
            speak("According to Wikipedia") 
            print(results)
            speak(results)
        
        elif "open youtube" in query:
            webbrowser.open('youtube.com')

        elif "open google" in query:
            webbrowser.open('google.com')

        elif "open instagram" in query:
            webbrowser.open('instagram.com')

        elif "open stackoverflow" in query:
            webbrowser.open('stackoverflow.com')

        elif "open facebook" in query:
            webbrowser.open('facebook.com')

        elif "open gmail" in query:
            webbrowser.open('gmail.com')



        elif "play music" in query:
            music_dir = "C:\\Users\\Admin\\Desktop\\One Direction"
            songs =  os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))             #can use random function here

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        

        elif "open vs code" in query:
            #how to get path? right click on application > choose 'show in folder' > copy the path of .exe file and done.
            vsCodePath = "C:\\Users\\Admin\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(vsCodePath)

        elif "open sublime" in query:
            sublimePath = "C:\\Program Files\\Sublime Text 3\\sublime_text.exe"
            os.startfile(sublimePath)

        elif "open eclipse" in query:
            javaPath = "C:\\Users\\Admin\\eclipse\\jee-2020-12\\eclipse\\eclipse.exe"
            os.startfile(javaPath)

        elif "open netbeans" in query:
            netbeansPath = "C:\Program Files\NetBeans 8.2\bin\netbeans64.exe"
            os.startfile(netbeansPath)

        elif "open python idle" in query:
            pyPath = "C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python39\\pythonw.exe"
            os.startfile(pyPath)

        elif "open android studio" in query:
            andrPath = "C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe"
            os.startfile(andrPath)

        elif "open san andreas" in query:
            gtaSaPath = "C:\\Program Files (x86)\\Mr DJ\\Grand Theft Auto San Andreas\\gta_sa.exe"
            os.startfile(gtaSaPath)

        elif "open cs" in query:
            csPath = "C:\\Games\\Counter-Strike WaRzOnE\\CS16Launcher.exe"
            os.startfile(csPath)



        #work in process
        elif "email to person_name" in query:
            try:
                speak("What should I write?")
                content = takeCommand()
                to = "person_email@gmail.com"            #to the person can take user input for future scope
                sendEmail(to, content)
                speak("Email has been sent.")           #feedback
            except Exception as e:
                print(e)
                speak("Email not sent")
