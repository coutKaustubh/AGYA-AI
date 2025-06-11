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

    tts = edge_tts.Communicate(text, voice="en-IN-NeerjaNeural")
    await tts.save(temp_path)
    playsound(temp_path)

    # Clean up the temporary file
    os.remove(temp_path)

def speak_now(text):
    asyncio.run(speak(text))

# ========== Wake Message ========== #
speak_now("Aapka swagat hai nova AI me")

# ========== Speech Recognition ========== #
r = sr.Recognizer()
nova_activate = False

while True:
    with sr.Microphone() as source:
        print("Call out my name or listen to activate...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        wake_command = r.recognize_google(audio).lower()
        print("You said (wake):", wake_command)
        
        if any(phrase in wake_command for phrase in ["hey", "nova", "hey nova", "are you there", "r u there", "hello", "listen", "nova"]):
            nova_activate = True
            speak_now("I'm listening...")

            while nova_activate:
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
                        speak_now(f"The current time is {time_str}")

                    elif any(phrase in command for phrase in ["how are you", "how r u"]):
                        speak_now("Always operational.")

                    elif "your name" in command:
                        speak_now("I am nova, your assistant.")

                    elif any(phrase in command for phrase in ["stop", "end", "exit", "thanks", "thank you", "over", "sign out"]):
                        nova_activate = False
                        speak_now("Thank you for using me")
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
                    nova_activate = False

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError:
        print("Speech recognition service is down")
    
