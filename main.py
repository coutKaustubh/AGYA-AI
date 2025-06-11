import os
import asyncio
import edge_tts
from playsound import playsound
import speech_recognition as sr
import webbrowser
import datetime
import tempfile

# ========== TTS Setup ========== #
async def speak(text):
    # Generate a temporary mp3 file to avoid permission errors
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_path = fp.name

    tts = edge_tts.Communicate(text, voice="hi-IN-SwaraNeural")
    await tts.save(temp_path)
    playsound(temp_path)

    # Clean up the temporary file
    os.remove(temp_path)

def speak_now(text):
    asyncio.run(speak(text))

# ========== Wake Message ========== #
speak_now("Aapka swagat hai navya AI me")

# ========== Speech Recognition ========== #
r = sr.Recognizer()
navya_activate = False

while True:
    with sr.Microphone() as source:
        print("Call out my name or listen to activate...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        wake_command = r.recognize_google(audio).lower()
        print("You said (wake):", wake_command)
        
        if any(phrase in wake_command for phrase in ["hey", "navya", "hey navya", "are you there", "r u there", "hello", "listen", "navya"]):
            navya_activate = True
            speak_now("Mai sun rahi hoon. mai koi bhi app khol sakti hoon and time bhi bta sakti hoon")

            while navya_activate:
                try:
                    with sr.Microphone() as source:
                        print("Listening for command...")
                        r.adjust_for_ambient_noise(source, duration=0.5)
                        audio = r.listen(source)

                    command = r.recognize_google(audio).lower()
                    print("You said (command):", command)

                    if "time" in command:
                        now = datetime.datetime.now()
                        time_str = now.strftime("%I:%M %p")
                        speak_now(f"{time_str} ho raha h")

                    elif any(phrase in command for phrase in ["how are you", "how r u"]):
                        speak_now("Always operational.")

                    elif any(phrase in command for phrase in ["tumhara naam", "nam" , "your name"]):
                        speak_now("I am navya, aapki sathi.")

                    elif any(phrase in command for phrase in ["badhiya", "achi" , "maza aagya" , "good" , "appreciate"]):
                        speak_now("I am very thankful . Shukriya !")

                    elif any(phrase in command for phrase in ["kharab", "bekar" , "need to be better" , "bad" , "kill"]):
                        speak_now("I am in a developing phase. I will correct myself")

                    elif any(phrase in command for phrase in ["stop", "end", "exit", "thanks", "thank you", "over", "sign out"]):
                        navya_activate = False
                        speak_now("Mujhe use krne ke liye dhanyawad. aapka din shubh ho")
                        break

                    elif "open" in command:
                        try:
                            site_name = command.split("open")[1].strip()
                            url = f"https://www.{site_name}.com"
                            speak_now(f"Opening {site_name}")
                            webbrowser.open(url)
                        except Exception as e:
                            print("Error:", e)
                            speak_now("Sorry, I couldn't open that website.")
                    
                    else:
                        speak_now("Sorry, I didn't understand that.")

                except sr.UnknownValueError:
                    print("Could not understand command. Listening again...")
                    speak_now("Sorry, I didn't catch that.")
                except sr.RequestError:
                    print("Speech recognition service is down.")
                    speak_now("Sorry, I'm having trouble connecting.")
                    navya_activate = False

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError:
        print("Speech recognition service is down")
    
