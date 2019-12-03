#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
import speech_recognition as sr
import spacy
import os
import sys
import pyttsx3
from spacy import displacy
from pdb import set_trace
from order import Order

def determine_semantic_frame_from_parsed_tree(parsed_tree):
    root_tuple = get_parse_tree_root_tuple(parsed_tree)
    if triggers_greeting(root_tuple=root_tuple):
        return "greeting"
    elif triggers_request_special_need(root_tuple=root_tuple, parsed_tree=parsed_tree):
        return 'request_special_need'
    elif triggers_request_order_update(root_tuple=root_tuple, parsed_tree=parsed_tree):
        return 'request_order_update'
    else:
        return False

def triggers_greeting(root_tuple):
    root_lemma, root_text = root_tuple
    if root_lemma in ["hi", "hey", "hello", "good morning"]:
        return True
    return False

def triggers_request_order_update(root_tuple, parsed_tree):
    root_lemma, root_text = root_tuple
    if root_lemma in ['sandwich', 'have', 'like', 'want', 'give', 'need']:
        return True
    return False

def triggers_request_special_need(root_tuple, parsed_tree):
    root_lemma, root_text = root_tuple
    if root_lemma in ['eat', 'drink', 'ingest', 'consume', 'tolerate', 'have', 'be']:
        if root_verb_is_negated(root_tuple, parsed_tree):
            if triggers_request_special_need_verb_with_negation(
                root_tuple=root_tuple, parsed_tree=parsed_tree):
                return True
        else:
            if triggers_request_special_need_verb_positive(
                root_tuple=root_tuple, parsed_tree=parsed_tree):
                return True

    return False

def triggers_request_special_need_verb_positive(root_tuple, parsed_tree):
    trigger_list = ['intolerance', 'allergy', 'disease']
    positive_list = ['vegan', 'vegetarian', 'celiac', 'lactose', 'gluten']
    root_lemma, root_text = root_tuple
    if root_lemma not in ['be', 'have']:
        return False

    for token in parsed_tree:
        if token_triggers_special_need_verb_positive(
                token=token, root_text=root_text, positive_list=positive_list,
                trigger_list=trigger_list):
            return True
    return False

def token_triggers_special_need_verb_positive(token, root_text, positive_list, trigger_list):
    parent = token.head
    if ((str(parent) == root_text and token.text in positive_list)
            or (str(parent) in trigger_list and str(parent.head) == root_text
                and token.text in positive_list)):
        return True
    else:
        return False

def root_verb_is_negated(root_tuple, parsed_tree):
    root_lemma, root_text = root_tuple
    for token in parsed_tree:
        if str(token.dep_) == 'neg' and str(token.head) == root_text:
            return True
    return False

def triggers_request_special_need_verb_with_negation(root_tuple, parsed_tree):
    root_lemma, root_text = root_tuple
    positive_list = ['celiac', 'lactose', 'noon']
    for token in parsed_tree:
        parent = token.head
        if str(parent) == root_text and token.text in positive_list:
            return True
    return True

def get_parse_tree_root_tuple(parsed_tree):
    for token in parsed_tree:
        if token.dep_ == 'ROOT':
            return token.lemma_, token.text

def modify_order(order, parsed_tree):
    semantic_frame = determine_semantic_frame_from_parsed_tree(parsed_tree)
    print("semantic_frame: %s" % semantic_frame)
    if semantic_frame == 'request_order_updated':
        update_order_with_request(order=order, parsed_tree=parsed_tree)
    else:
        pass

def update_order_with_request(order, parsed_tree):
    #TODO: use spacey labels ("PRODUCT")
    for token in parsed_tree:
        all_ingredients = order.get_all_avaible_ingredients()
        if token.lemma_ in order.available_protein_types():
            order.add_protein_type(protein_type=token.lemma_)
        elif token.lemma_ in order.available_vegetables():
            order.add_vegetable(vegetable=token.lemma_)
        elif token.lemma_ in order.available_sauces():
            order.add_sauce(sauce=token.lemma_)
#obligatory slots and optional slots.
#root?
if __name__=="__main__":
    # engine = pyttsx3.init()
    #     # #engine.setProperty('voice', en_voice_id)
    #     #
    #     # # Set properties _before_ you add things to say
    #     # engine.setProperty('rate', 100)    # Speed percent (can go over 100)
    #     # engine.setProperty('volume', 0.9)  # Volume 0-1
    #     # engine.say("Thank you")
    #     # engine.runAndWait()

    # en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
    new_order = Order()
    # new_order.add_bread_type("regular")
    # new_order.add_vegetable("tomato")
    # new_order.add_vegetable("lettuce")
    # print(new_order.vegetable_list)

    nlp = spacy.load("en_core_web_sm")
    # doc = nlp("I would like a sandwich")
    # doc = nlp("is this gluten free?")
    # doc = nlp("A sandwich with bacon and lettuce")
    doc = nlp("I have gluten allergy")


    modify_order(order=new_order, parsed_tree=doc)
    print("*****")
    print("New order vegetables: %s"%new_order.vegetable_list)
    print("New order protein: %s" % new_order.protein)
    print("*****")
    # for token in doc:
    #     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
    #           token.shape_, token.is_alpha, token.is_stop)
    displacy.serve(doc, style="dep")
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


