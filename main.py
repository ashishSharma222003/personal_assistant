import pyttsx3
import speech_recognition as sr
from agent import reactAgent


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# # Set the speech rate (words per minute)
# rate = engine.getProperty('rate')  # Get the current rate
# engine.setProperty('rate', rate) 

# Set the volume (0.0 to 1.0)
volume = engine.getProperty('volume')  # Get the current volume
engine.setProperty('volume', volume + 0.1) 

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio).lower()
        print(f"You said: {text}")

        # Process the command if it contains specific keywords
        if "exit" in text:
            speak("Exiting")
            return False 
            # Add additional actions here if needed
        else:
            # To exit the loop if needed
            response=reactAgent.chat(text)
            speak(response)

    except sr.UnknownValueError:
        # speak("Sorry, I did not understand that.")
        return True
    except sr.RequestError:
        print("Sorry, there was an error with the speech recognition service.")
        return True

    return True 
def listen_for_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake-up word...")
        recognizer.adjust_for_ambient_noise(source)

        while True:
            print("Listening for wake-up word...")
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio).lower()
                print(f"Heard: {text}")

                # If the wake-up word is detected, start listening for commands
                if "hey google" in text:
                    speak("Listening for commands")
                    while listen_for_command():
                        pass  # Keep listening for commands until 'exit' is said
                if "vandalize" in text:
                    break
            except sr.UnknownValueError:
                # Optional: handle cases where the wake-up word is not understood
                pass
            except sr.RequestError:
                print("Sorry, there was an error with the speech recognition service.")


if __name__=="__main__":
    listen_for_wake_word()