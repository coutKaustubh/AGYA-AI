import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser

engine = pyttsx3.init()
engine.setProperty('rate', 125)     # Speed of speech
engine.setProperty('volume', 1.0)   # Volume (0.0 to 1.0)

engine.say('Welcome to the world of QUANTA')
engine.runAndWait()

r = sr.Recognizer()
quanta_activate = False

while True:
    with sr.Microphone() as source:
        print("Say 'Hey Quanta' to activate...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        wake_command = r.recognize_google(audio).lower()
        print("You said (wake):", wake_command)
        if any(phrase in wake_command for phrase in ["hey quanta", "are you there" , "r u there" , "hello" , "listen" , "quanta"]):
            quanta_activate = True
            engine.say("I'm listening...")
            engine.runAndWait()

            while quanta_activate == True:
                with sr.Microphone() as source:
                    print("Listening for command...")
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = r.listen(source)

                command = r.recognize_google(audio).lower()
                print("You said (command):", command)

                if "time" in command:
                    now = datetime.datetime.now()
                    time_str = now.strftime("%I:%M %p")
                    engine.say(f"The current time is {time_str}")
                elif any(phrase in command for phrase in ["how are you", "how r u"]):
                    engine.say("Always operational.")
                elif "your name" in command:
                    engine.say("I am Quanta, your assistant.")
                elif any(phrase in command for phrase in ["stop","end","exit","thanks","thank you","over","sign out"]):
                    quanta_activate = False
                    engine.say("Thank you for using me")
                    engine.runAndWait()
                    break
                
                elif "open" in command:
                    try:
                        site_name = command.split("open")[1].strip()  # Get word after 'open'
                        url = f"https://www.{site_name}.com"
                        engine.say(f"Opening {site_name}")
                        engine.runAndWait()
                        webbrowser.open(url)
                    except Exception as e:
                        engine.say("Sorry, I couldn't open that website.")
                        engine.runAndWait()
                        print("Error:", e)
                        engine.say("Sorry, I don't understand.")

                

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError:
        print("Speech recognition service is down")
