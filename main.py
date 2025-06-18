from imports import *
from gemini import *

# TTS Setup 
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

# Wake Message 
speak_now("Aapka swagat hai agya AI me")

# Speech Recognition 
r = sr.Recognizer()
agya_activate = False

while True:
    with sr.Microphone() as source:
        print("Call out my name or listen to activate...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        wake_command = r.recognize_google(audio).lower()
        print("You said (wake):", wake_command)
        
        if any(phrase in wake_command for phrase in ["hey", "agya", "hey agya", "are you there", "r u there", "hello", "listen", "agya"]):
            agya_activate = True
            speak_now("Mai sun rahi hoon. Whats your question?")

            while agya_activate:
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
                        speak_now("I am agya, aapki sathi.")

                    elif any(phrase in command for phrase in ["badhiya", "achi" , "maza aagya" , "good" , "appreciate"]):
                        speak_now("I am very thankful . Shukriya !")

                    elif any(phrase in command for phrase in ["kharab", "bekar" , "need to be better" , "bad" , "kill"]):
                        speak_now("I am in a developing phase. I will correct myself")

                    elif any(phrase in command for phrase in ["stop", "end", "exit", "thanks", "thank" "thank you", "over", "sign out"]):
                        agya_activate = False
                        speak_now("Thanks for using me")
                        break

                    elif "open" in command:
                        try:
                            site_name = command.split("open")[1].strip()
                            url = f"https://www.{site_name}.com"
                            speak_now(f"apna browser check kro {site_name} khul gya h")
                            webbrowser.open(url)
                        except Exception as e:
                            print("Error:", e)
                            speak_now("Sorry, I couldn't open that website.")

                    elif "play" in command:
                        try:
                            site_name = command.split("play")[1].strip()
                            url = f"https://www.youtube.com/results?search_query={site_name}"
                            speak_now(f"apna youtube check kro {site_name} ke results khul gye h")
                            webbrowser.open(url)
                        except Exception as e:
                            print("Error:", e)
                            speak_now("Sorry, I couldn't open that website.")

                    
                    else:
                        reply = ask_gemini(command)
                        speak_now(reply)


                except sr.UnknownValueError:
                    print("Some error ! please speak again")
                    speak_now("Please dobara bolo .. I didn't understand")
                except sr.RequestError:
                    print("Speech recognition service is down.")
                    speak_now("Sorry, Lagta h meri battery gyiiiiiiiiiiiiii.")
                    agya_activate = False

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError:
        print("Speech recognition service is down")
    
