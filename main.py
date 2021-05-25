import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
import wolframalpha
import json
import requests
import pyowm
import Word
import spacy
import bern

current_time = datetime.datetime.now()
def wishMe():
    hour = datetime.datetime.now().hour         #checks for current time and displays appropiate greeting
    if hour>=0 and hour<12:                     #uses datetime class to get time in 24 hour cycle
        print("Hello,Good Morning")
    elif hour>=12 and hour<18:
        print("Hello,Good Afternoon")
    else:
        print("Hello,Good Evening")

def speak():
    r=sr.Recognizer()                           #used to call upon recognizer class and set it to r
    with sr.Microphone() as source:             # assigns michrophone as source for easy calling
        print("Listening...")
        audio=r.listen(source)                  #microphone input put into audio

        try:
            user =r.recognize_google(audio,language='en-in')   #call on google speech to check input


        except Exception as e:                  #makes sure the program does not crash if user takes to long to talk
            print("I'm sorry i did not catch that")
            return "None"
        return user


wishMe()


if __name__=='__main__':
    print("How can I help you today")
    while True:
        user = speak().lower()         #call speak
        if "bye" in user:
            print("goodbye")
            break
        if "hello" in user:
            Word.greeting()

        if "open" in user:
            if "notepad" in user:
                os.system("notepad")
            elif "google" in user:
                webbrowser.open_new_tab("https://www.google.com")

        if "joke" in user:
            Word.joke()
        if "weather" in user:               #call on weather api to get weather for selected city.
            print("Which city")
            user = speak().lower()
            APIKEY = '736c03a82b35e11f971e65ea10cbfb99'
            OpenWMap = pyowm.OWM(APIKEY)
            Weather = OpenWMap.weather_at_place(user)
            Data = Weather.get_weather()
        if "time" in user:
            print(current_time)
        if 'files' in user:
            user = user.replace("search", "")
            webbrowser.open_new_tab(user)
        if 'search' in user:                #uses wikipidia python libary to search wikipidia for simple answers.
            user = user.replace("search", "")
            results = wikipedia.summary(user, sentences=3)
            print(results)
time.sleep(3)

