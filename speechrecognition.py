from flask import Flask, render_template, request, redirect
import speech_recognition as sr
import time
import pyaudio
import wave
import audiomentations
from scipy.io import wavfile
import pickle
import app


r = sr.Recognizer()




def micon(question, dur):
        model = pickle.load(open('models/model.pkl','rb'))
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source,duration=0.6)
            audio = r.listen(source)
            text = r.recognize_google(audio)
            ans = text
            text = [text]
            x = model.predict(text)
            return ans,x



if __name__ == "__main__":
    micon(1, 1)
