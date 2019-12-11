import speech_recognition as sr
import random
import os
import spacy
from gtts import gTTS
from playsound import playsound
from spacy import displacy
from pdb import set_trace
from semantic_frames import Order, Customer
from ingredients import ingredients_dict
import sys
from spacy import displacy
from pdb import set_trace
from semantic_frames import Order, Customer
from ingredients import ingredients_dict
import nelly

################################################################################
def answer(frame):

    if frame == "greeting":
        answer = ['Hows your day going. What do you want to eat?', 'Hello my friend, what do you want to order?', 'Hello. My name is Nelly! What do you want to order?', 'Hi! Nice to meet you. Please proceed to order!']
        answer = random.choice(answer)

    elif frame == "not_greeting":
        answer = ['Well, as you did not answer, lets continue with your order, What do you want to eat?','Well friend, what you want to order today?','Answer bitch, why you so rude!, What you want to order?']
        answer = random.choice(answer)

    elif frame == "lactose_restriction": #(activated with cheese, milk, cream, etc)
        answer = ['Be carefull, this ingredient, contains dairy products!', 'You want to die bitch?', 'I would like to infrom you that, this ingredient contains lactose!', 'This product is not lactose free!']
        answer = random.choice(answer)

    elif frame == "no_lactose_restriction":
        answer = ['Oh!, nice you dont have any lactose restriction, now you can continue ordering!']
        answer = random.choice(answer)

    elif frame == "vegan_restriction": #(activated with bread, protein,beef, chicken, etc)
        answer = ['If you are vegan, you should not eat this!', 'This contains animal origin ingredient!', 'Not recommended, if you are vegan!']
        answer = random.choice(answer)

    elif frame == "no_vegan_restriction": #(activated with bread, protein,beef, chicken, etc)
        answer = ['Oh!, nice you are not vegan, you can continue ordering!']
        answer = random.choice(answer)

    elif frame == "gluten_restriction":
        answer = ['This is not gluten free', 'The ingredient contains gluten', 'Be Carefull my friend!, This product contains gluten.']
        answer = random.choice(answer)

    elif frame == "no_gluten_restriction":
        answer = ['Oh!, nice you dont have any gluten restriction, now you can continue ordering!']
        answer = random.choice(answer)

    elif frame == "answer_ingredient":
        answer = ['Yes! The sandwich contains that ingredient','Yes, it has some.']
        answer = random.choice(answer)

    elif frame == "no_answer_ingredient":
        answer = ['Sorry we dont have ingredients information for what you asked']
        answer = random.choice(answer)

    elif frame == "answer_price":
        answer = ['Its 5 euros in total! Thank you!','For you, I can leave it at 6 euros!', 'Its 10 euros. Have a nice day my friend.', 'Today, this sandwich is free for you!']
        answer = random.choice(answer)

    elif frame == "answer_goodbye":
        answer = ['Thank you, for buying in Nellys, have a nice day!','Thank you, for your order.', 'Bon apetit. Goodbye!']
        answer = random.choice(answer)

    elif frame == "silence":
        answer = ['Please. Answer to me!', 'Are you muted? I can not hear you!', 'Talk to me! Please my friend!', 'Listen my friend, you should answer my questions. If you want to eat today!']
        answer = random.choice(answer)

    else:
        answer = ['I dont have an answer for that, sorry.', 'I can not help you with that, amigo. Sorry.']
        answer = random.choice(answer)
    return answer
################################################################################
def answer_ingredient(ingredient_list):
    #FOR BETTER USER EXPERIENCE USE A LIST LIKE THIS ingredients= ['flour,', 'butter,', 'sugar,', 'salt,', 'yeast,']
    str1 = " "
    ingredient_list = str1.join(ingredient_list)
    answer = 'This food my friend, contains:' + ingredient_list
    return answer
################################################################################
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source,duration=0.5)
        audio = r.record(source, duration=5)
    try:
        message = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Could not understand audio")
        message = "silence"
    except sr.RequestError as e:
        print("Could not understand audio")
        message = "silence"
    print("Check: " + message)
    return  message
################################################################################
def text_to_speech(answer):
    tts = gTTS(text=answer, lang='en')
    tts.save("good2.mp3")
    playsound("good2.mp3")
    os.remove("good2.mp3")
    return 0
################################################################################

################################################################################
################################################################################
if __name__=="__main__":
    new_customer =  Customer()
    nlp = spacy.load("en_core_web_sm")
    message = speech_to_text()
    while message != "bye":
        while message == "silence":
                answer1= answer("silence")
                text_to_speech(answer1)
                message = speech_to_text()
        doc = nlp(message)
        nelly.update_state(customer=new_customer, parsed_tree=doc)
        frame = nelly.determine_semantic_frame_from_parsed_tree(doc)
        answer1= answer(frame)
        text_to_speech(answer1)
        message = speech_to_text()
    answer1= answer("answer_goodbye")
    text_to_speech(answer1)
