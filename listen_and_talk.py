from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import random
import os


################################################################################
def answer(frame):
    if frame == "greeting":
        answer = ['Hows your day going. What do you want to eat?', 'Hello my friend, what do you want to order?', 'Hello. My name is Nelly! What do you want to order?', 'Hi! Nice to meet you. Please proceed to order!']
        answer = random.choice(answer)
    elif frame == "lactose_restriction": #(activated with cheese, milk, cream, etc)
        answer = ['Be carefull, this ingredient, contains dairy products!', 'You want to die bitch?', 'I would like to infrom you that, this ingredient contains lactose!', 'This product is not lactose free!']
        answer = random.choice(answer)
    elif frame == "vegan_restriction": #(activated with bread, protein,beef, chicken, etc)
        answer = ['If you are vegan, you should not eat this!', 'This contains animal origin ingredient!', 'Not recommended, if you are vegan!']
        answer = random.choice(answer)
    elif frame == "gluten_restriction":
        answer = ['This is not gluten free', 'The ingredient contains gluten', 'Be Carefull my friend!, This product contains gluten.']
        answer = random.choice(answer)
    elif frame == "answer_ingredient":
        answer = ['Yes! The sandwich contains that ingredient','Yes, it has some.' ]
        answer = random.choice(answer)
    elif frame == "answer_price":
        answer = ['Its 5 euros in total! Thank you!','For you, I can leave it at 6 euros!', 'Its 10 euros. Have a nice day my friend.', 'Today, this sandwich is free for you!']
        answer = random.choice(answer)
    elif frame == "answer_goodbye":
        answer = ['Thank you, for buying in Nellys, have a nice day!','Thank you, for your order.', 'Bon apetit. Goodbye!']
        answer = random.choice(answer)
    elif frame == "answer_":
        answer = ['' ]
        answer = random.choice(answer)
    else:
        answer = ['a', 'b', 'c', 'd', 'e']
        answer = random.choice(answer)     
    return answer                                       
################################################################################
def answer_ingredient(ingredient_list):
    if frame == "greeting":
        answer = ['Hows your day going. What do you want to eat?', 'Hello my friend, what do you want to order?', 'Hello. My name is Nelly! What do you want to order?', 'Hi! Nice to meet you. Please proceed to order!']
        answer = random.choice(answer)
    elif frame == "lactose_restriction": #(activated with cheese, milk, cream, etc)
        answer = ['Be carefull, this ingredient, contains dairy products!', 'You want to die bitch?', 'I would like to infrom you that, this ingredient contains lactose!', 'This product is not lactose free!']
        answer = random.choice(answer)
    else:
        answer = ['a', 'b', 'c', 'd', 'e']
        answer = random.choice(answer)     
    return answer     
################################################################################
def speech_to_text():    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source,duration=0.5)
        audio = r.record(source, duration=5)
        message = r.recognize_google(audio)
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



frame= "greeting"
answer1= answer(frame)
text_to_speech(answer1)
frame= "gluten_restriction"
answer1= answer(frame)
text_to_speech(answer1)

