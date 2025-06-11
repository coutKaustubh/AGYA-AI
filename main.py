import pyttsx3
import speech_recognition as sr
import datetime

engine = pyttsx3.init()
engine.setProperty('rate', 135)     # Speed of speech
engine.setProperty('volume', 1.0)   # Volume (0.0 to 1.0)

engine.say('Welcome to the world of QUANTA')
engine.runAndWait()

r = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        print("Say 'Hey Quanta' to activate...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        wake_command = r.recognize_google(audio).lower()
        print("You said (wake):", wake_command)

        if "hey quanta" in wake_command:
            engine.say("I'm listening...")
            engine.runAndWait()

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
            elif "exit" in command:
                engine.say("Goodbye!")
                engine.runAndWait()
                break
            else:
                engine.say("Sorry, I don't understand.")

            engine.runAndWait()

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError:
        print("Speech recognition service is down")
