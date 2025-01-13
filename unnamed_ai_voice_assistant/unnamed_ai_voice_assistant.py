import openai
import pyttsx3 # for text-to-speech
import speech_recognition as sr # for speech-to-text 
import pywhatkit as kit # for system commands
import datetime # for getting time and date
import wikipedia # for deriving information from wikipedia
import pyjokes # for the personality :)
import os # for operating system based operations

# OpenAI API Key
openai.api_key = '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'

# setting up text-to-speech engine
engine = pyttsx3.init()

# function to make assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# function to listen to user's command
def listen():
    recognizer = sr.Recognizer() # to initialize the recognizer
    with sr.Microphone() as source: # use microphone as input source
        print("I hear you...")
        recognizer.adjust_for_ambient_noise(source) # adjust to background noise by adjusting sensitivity of recognizer
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio) # to recognize speech input using Google's speech recognition API
        print(f"I heard you say: {command}")
    except sr.UnknownValueError:
        speak("Sorry, come again, please?")
        return None 
    return command

# function to interact with OpenAI API
def openai_response(query):
    response = openai.Completion.create(
        model = "text-davinci-003", # can choose another model like "gpt-3.5-turbo" if necessary, this one was chosen for high-quality responses
        prompt = query,
        max_tokens = 200 # adjustable response length
    )
    return response.choices[0].text.strip() # returns first option of the response and strips text of leading/trailing spaces.

# function to tell date and time
def whats_the_time():
    current_time = datetime.datetime.now().strftime("%H:%M") # format time into HH:MM (in 24hr format)
    speak(f"The current time is {current_time}")

# function to tell a joke
def make_me_laugh():
    joke = pyjokes.get_joke()
    speak(joke)

# main
def roll_out():
    speak("Hey! I am your friendly neighbourhood virtual assistant, Talos! How can I help you today?")
    while True:
        command = listen()
        
        if command is None:
            continue
        
        if 'time' in command:
            whats_the_time()
        elif 'joke' in command:
            make_me_laugh()
        elif 'search' in command:
            search_query = command.replace('search', '')
            result = wikipedia.summary(search_query, sentences=1)
            speak(result)
        elif 'play' in command:
            song = command.replace('play', '')
            speak(f"Playing {song}")
            kit.playonyt(song) # fetches requested song from YouTube
        elif 'stop' in command:
            speak("See ya!")
            break 
        else:
            response = openai_response(command)
            speak(response)

# run code
if __name__ == "__main__":
    roll_out()