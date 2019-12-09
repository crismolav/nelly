import spacy
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr



r = sr.Recognizer()   #Speech recognition
with sr.Microphone() as source:
    print("Say something!")
    r.adjust_for_ambient_noise(source,duration=0.5)
    audio = r.listen(source)
    message = r.recognize_google(audio)
    print("Check: "+message)
try:
    print("User: " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))





tts = gTTS(text=message, lang='en')
tts.save("good.mp3")
playsound("good.mp3")
