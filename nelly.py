#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

import speech_recognition as sr
import spacy
import os
import sys
import pyttsx3
from spacy import displacy
from pdb import set_trace

class Order:
    def __init__(self):
        self.bread_type = None
        self.protein = None
        self.sauce_list = []
        self.vegetable_list = []
    def add_bread_type(self, bread_type):
        self.bread_type = bread_type
    def available_bread_types(self):
        return ['vegan', 'whole-wheat', 'regular']
    def add_protein_type(self, protein_type):
        self.protein = protein_type
    def available_protein_types(self):
        return ['tofu', 'chicken', 'beef', 'pork']
    def add_vegetable(self, vegetable):
        self.vegetable_list.append(vegetable)
    def available_vegetables(self):
        return ['lettuce', 'tomato', 'cucumber', 'olive', 'onion']
    def add_sauce(self, sauce):
        self.sauce_list.append(sauce)
    def available_sauces(self):
        return ['barbecue', 'ketchup', 'mustard', 'nelly_sauce']

def determine_semantic_frame_from_tree_root(parse_tree):
    parse_tree_root = get_parse_tree_root(parse_tree)
    if parse_tree_root in ['sandwich', 'have', 'like', 'want','give', 'need']:
        return 'request'
    else:
        return False

def get_parse_tree_root(parse_tree):
    for token in parse_tree:
        if token.dep_ == 'ROOT':
            return token.lemma_

if __name__=="__main__":
    engine = pyttsx3.init()
    #engine.setProperty('voice', en_voice_id)

    # Set properties _before_ you add things to say
    engine.setProperty('rate', 100)    # Speed percent (can go over 100)
    engine.setProperty('volume', 0.9)  # Volume 0-1
    engine.say("Thank you")
    engine.runAndWait()

    # en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
    new_order = Order()
    new_order.add_bread_type("regular")
    new_order.add_vegetable("tomato")
    new_order.add_vegetable("lettuce")

    nlp = spacy.load("en_core_web_sm")
    doc = nlp("Can I have a sandwich with tofu and tomato")
    doc = nlp("I would like a sandwich")
    doc = nlp("is this gluten free?")
    # doc = nlp("A sandwich with bacon and lettuce")
    semantic_frame = determine_semantic_frame_from_tree_root(parse_tree=doc)

    print("tree_root_str: %s"%tree_root_str)
    print("semantic_frame: %s"%semantic_frame)
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
              token.shape_, token.is_alpha, token.is_stop)
    # displacy.serve(doc, style="dep")
    # Record Audio
    # r = sr.Recognizer()
    # with sr.Microphone() as source:
    #     print("Say something!")
    #     audio = r.listen(source)
    #
    # # Speech recognition using Google Speech Recognition
    # try:
    #     # for testing purposes, we're just using the default API key
    #     # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    #     # instead of `r.recognize_google(audio)`
    #     print("You said: " + r.recognize_google(audio))
    #     doc = nlp(r.recognize_google(audio))
    #     for chunk in doc.noun_chunks:
    #         print (chunk)
    # except sr.UnknownValueError:
    #     print("Google Speech Recognition could not understand audio")
    # except sr.RequestError as e:
    #     print("Coud not request results from Google Speech Recognition service; {0}".format(e))


