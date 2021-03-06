import speech_recognition as sr
import random
import os
import spacy
from gtts import gTTS
from playsound import playsound
from customer import Order, Customer
from ingredients import ingredients_dict
import nelly
from pdb import set_trace


################################################################################
def answer(frame, customer=None):

    if frame == "greeting":
        answer = ['Welcome to Nellys!', 'Hello my friend. Welcome to my restaurant!', 'Hello. My name is Nelly!', 'Hi! Nice to meet you!']
        answer = random.choice(answer)

    elif frame == "request_no_food_restriction":
        answer = ['Perfect my friend. Lets continue with the order!','Awesome!', 'Okay. What do you want to order?']
        answer = random.choice(answer)

    elif frame == "two_times_greeting":
        answer = ['Hello, again, my friend!','It looks like, you enjoy greeting me!']
        answer = random.choice(answer)

    elif frame == "lactose_restriction": #(activated with cheese, milk, cream, etc)
        answer = ['Be careful, this ingredient, contains dairy products!', 'You want to get sick?', 'I would like to infrom you that, this ingredient contains lactose!', 'This product is not lactose free!']
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
        answer = ['Oh!, nice you do not have any gluten restriction, now you can continue ordering!']
        answer = random.choice(answer)

    elif frame == "answer_ingredient":
        answer = ['Yes! The sandwich contains that ingredient','Yes, it has some.']
        answer = random.choice(answer)

    elif frame == "no_answer_ingredient":
        answer = ['Sorry we dont have ingredients information for what you asked']
        answer = random.choice(answer)

    elif frame == "request_goodbye":
        answer = ['Thank you, for buying in Nellys, have a nice day!','Thank you, for your order.', 'Bon apetit. Goodbye!']
        answer = random.choice(answer)

    elif frame == "silence":
        answer = ['Please. Answer to me!', 'Check your microphone. I can not hear you!', 'Talk to me! Please my friend!', 'Listen my friend, you should answer my questions. If you want to eat today!', 'Well, as you did not answer, lets continue with your order, What do you want to eat?']
        answer = random.choice(answer)

    elif frame == "request_order_update":
        answer = ['Sure!, Now your order is: + spacystring()']
        answer = random.choice(answer)

    elif frame == "request_cancel":
        answer = ['Sure! I am cancelling the order. Have a nice day!', 'Okay. I hope, i did not do, something wrong my friend!']
        answer = random.choice(answer)

    elif frame == "answer_bread":
        answer = ['Please tell me which kind of bread do you want for your sandwich', 'Which of the bread options you want my friend?']
        answer = random.choice(answer)

    elif frame == "answer_NO_bread":
        answer = ['You can not have a sandwich whithout bread my friend', 'If you take your sandwich without bread we can call it a salad!','Dont try to trick me. You can not have a breadless sandwich!', 'Please!, Tell me which bread you want!']
        answer = random.choice(answer)

    elif frame == "answer_protein":
        answer = ['Please tell me which protein do you want in your sandwich', 'Would you want any protein for your sandwich?']
        answer = random.choice(answer)

    elif frame == "answer_NO_protein":
        answer = ['Oh, what a shame you dont like to add any protein to your sandwich','Oh! No protein kind of people!. Nice!.', 'Ok, lets continue without proteins then']
        answer = random.choice(answer)

    elif frame == "answer_vegetable":
        answer = ['Would you like to add any vegetables', 'Dont you like vegetables?. Add some vegetables to your order']
        answer = random.choice(answer)

    elif frame == "answer_NO_vegetable":
        answer = ['Oh Friend you should eat your veggies!, but its ok for today', 'No vegetables, perfect!', 'Okay, roger that!, No veggies.']
        answer = random.choice(answer)

    elif frame == "answer_sauce":
        answer = ['Please tell me which sauces do you want', 'If you add sauce it tastes better. Please tell me which sauce you want to add.']
        answer = random.choice(answer)

    elif frame == "answer_NO_sauce":
        answer = ['Nice! Without sauce its a good fitness option!','Ok, No sauce, I will write that down right now!', 'So, a fitness sandwich for you, without sauces']
        answer = random.choice(answer)

    elif frame == "answer_cheese":
        answer = ['Please tell me which kind of cheese do you want', 'Dear friend, please tell me which cheese you want in the sandwich!']
        answer = random.choice(answer)

    elif frame == "answer_NO_cheese":
        answer = ['Nice, I am not adding cheese to your order!','No cheese, for the friend, here!', 'George!, Prepare the sandwich without cheese please.' ]
        answer = random.choice(answer)

    elif frame == "request_ignore_food_type":
        answer = ['Okay my friend.', 'Okay, noted', 'Got it' ]
        answer = random.choice(answer)

    elif frame == "request_removal":
        answer = ['Of course my friend. I am removing this ingredient', 'Sure! Removed!', 'Okay. I am removing it right now!' ]
        answer = random.choice(answer)

    elif frame == "request_special_need":
        answer = ['Thanks for the information! What do you want to order?', 'Okay. I will have that in mind! What do you want to eat?' ]
        answer = random.choice(answer)

    elif frame == "request_nelly_gender":
        answer = ["That's a very personal question. Anyway, I identify myself as non binary. Even though I am a machine. Isn't that ironic" ]
        answer = random.choice(answer)

    elif frame == "restate_last_state_change":
        answer = [","]
        answer = random.choice(answer)

    elif frame == "accept_remove_suggested_items":
        answer = ["Got it. Items removed!"]
        answer = random.choice(answer)

    elif frame == "deny_remove_suggested_items":
        answer = ["Got it"]
        answer = random.choice(answer)

    else:
        answer = ['HA HA HA HA! I can not understand you!', 'I can not help you with that, amigo. Sorry.']
        answer = random.choice(answer)
    return answer

################################################################################
def answer_ingredient(ingredient_list):
    str1 = " "
    ingredient_list = str1.join(ingredient_list)
    answer = 'This food my friend, contains:' + ingredient_list
    return answer
################################################################################
def answer_price():

    price = 0

    if ("avocado" in new_customer.order.vegetable_list):
        price = price + 2

    if (len(new_customer.order.vegetable_list) > 5):
        price = len(new_customer.order.vegetable_list - 5)*1 + price

    if (new_customer.order.protein):
        price = price + 3

    if (new_customer.order.cheese):
        price = price + 1

    price =str(price)
    answer = "Its, " + price +  ", euros. Have a nice day my friend."

    answer = [answer, 'Today, this order is free for you!']
    answer = random.choice(answer)

    return answer
################################################################################
def answer_order(vegetable_list,sauce_list,bread,protein,cheese, order_type):
    str1 = " "
    str2 = " "

    if vegetable_list:
        vegetable_list = ','.join(vegetable_list)
        vegetable = vegetable_list
    else:
        vegetable= " "

    if sauce_list:
        sauce_list = ','.join(sauce_list)
        sauce = sauce_list
    else:
        sauce= " "

    if bread and order_type == 'sandwich':
        bread=bread.replace("_", ",")
    else:
        bread= ""

    if cheese:
        cheese=cheese.replace("_", ",")
    else:
        cheese= " "

    if protein:
        protein=protein.replace("_", ",")
    else:
        protein= " "

    answer = 'Dear friend, you have ordered a %s which contains.'%order_type + bread + '.' + protein + '.' + vegetable + ',' + sauce + ',' + cheese
    return answer
################################################################################
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=0.4)
        print("Say something!")
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
    enter_value=0
    inside=0
    entering=0
    nlp = spacy.load("en_core_web_sm")
    message = speech_to_text()
    doc = nlp(message)
    nelly.update_state(customer=new_customer, parsed_tree=doc)
    frame = nelly.determine_semantic_frame_from_parsed_tree(doc)
    while frame != 'request_goodbye' and frame != 'request_cancel':

        while message == "silence":
            answer1 = answer("silence")
            text_to_speech(answer1)
            message = speech_to_text()
            if message != "silence":
                doc = nlp(message)
                nelly.update_state(customer=new_customer, parsed_tree=doc)
                frame = nelly.determine_semantic_frame_from_parsed_tree(doc)


        question_context = {}



        if frame != "request_goodbye":




            if (frame == "request_order_update") or (frame == "False" and enter_value==1) or (frame == "request_ignore_food_type") or (frame == "request_removal") or (frame == "accept_remove_items") or (frame == "deny_remove_suggested_items") or(frame =="accept_remove_suggested_items"):


                if entering==0:
                    text_to_speech("First of all. Do you have any food restriction?")
                    message = speech_to_text()
                    doc = nlp(message)
                    nelly.update_state(customer=new_customer, parsed_tree=doc, question_context = {'type': 'food_restriction'})
                    frame = nelly.determine_semantic_frame_from_parsed_tree(doc,question_context = {'type': 'food_restriction'})
                    while frame != 'request_no_food_restriction' and frame != 'request_special_need':
                        text_to_speech("You have to answer me. Its important! Do you have any food restriction?")
                        message = speech_to_text()
                        doc = nlp(message)
                        nelly.update_state(customer=new_customer, parsed_tree=doc, question_context = {'type': 'food_restriction'})
                        frame = nelly.determine_semantic_frame_from_parsed_tree(doc,question_context = {'type': 'food_restriction'})
                    entering=1

                if frame =="accept_remove_suggested_items" or frame=="deny_remove_suggested_items":
                    answer1= answer(frame)
                    text_to_speech(answer1)

                if frame == "request_order_update" and enter_value == 1:
                    answer1 =  answer(frame='restate_last_state_change', customer=new_customer)
                    answer1  = answer1.join(nelly.return_last_elements_added_to_the_order(new_customer))
                    answer1 = "Ok I added, " + answer1.replace("_", " ")
                    text_to_speech(answer1)


                if frame == "request_ignore_food_type" or frame == "request_removal":
                    answer1 = answer(frame)
                    text_to_speech(answer1)


                if frame == "request_special_need" and entering==1:
                    text_to_speech("Please my friend, lets continue with the order!")
                    enter_value=0


                if frame == "False" and enter_value==1:
                    answer1= answer(frame)
                    text_to_speech(answer1)
                    text_to_speech("Please my friend, lets continue with the order!")
                    enter_value=0


                if new_customer.order.bread_type == None and new_customer.order.order_type == 'sandwich':
                    answer1= answer("answer_bread")
                    text_to_speech(answer1)
                    message = speech_to_text()
                    enter_value = 1


                elif new_customer.order.wants_food_type['protein'] and new_customer.order.protein == None:
                    answer1 = answer("answer_protein")
                    text_to_speech(answer1)
                    message = speech_to_text()
                    question_context = {'type': 'protein'}
                    enter_value = 1


                elif new_customer.order.wants_food_type['vegetable'] and not new_customer.order.vegetable_list:
                    answer1 = answer("answer_vegetable")
                    text_to_speech(answer1)
                    message = speech_to_text()
                    question_context = {'type': 'vegetable'}
                    enter_value = 1


                elif new_customer.order.wants_food_type['sauce'] and not new_customer.order.sauce_list:
                    answer1 = answer("answer_sauce")
                    text_to_speech(answer1)
                    message = speech_to_text()
                    question_context = {'type': 'sauce'}
                    enter_value = 1


                elif new_customer.order.wants_food_type['cheese'] and new_customer.order.cheese == None:
                    answer1 = answer("answer_cheese")
                    text_to_speech(answer1)
                    message = speech_to_text()
                    question_context = {'type': 'cheese'}
                    enter_value = 1


                else:
                    enter_value = 0
                    answer1 = answer_order(
                        vegetable_list=new_customer.order.vegetable_list,
                        sauce_list=new_customer.order.sauce_list,
                        bread=new_customer.order.bread_type,
                        protein=new_customer.order.protein,
                        cheese=new_customer.order.cheese,
                        order_type=new_customer.order.order_type)
                    text_to_speech(answer1)
                    answer1 = answer_price()
                    text_to_speech(answer1)
                    message = speech_to_text()



            elif frame == "request_special_need":
                    answer1 = answer(frame)
                    text_to_speech(answer1)
                    entering=1
                    message = speech_to_text()



            else:
                if new_customer.number_of_greetings > 1:
                    if  frame == "greeting":
                        answer1 = answer("two_times_greeting")
                        text_to_speech(answer1)
                        message = speech_to_text()
                    else:
                        answer1 = answer(frame)
                        text_to_speech(answer1)
                        message = speech_to_text()
                else:
                    answer1 = answer(frame)
                    text_to_speech(answer1)
                    if entering==0:
                        text_to_speech("Dear friend. Do you have any food restriction?")
                        message = speech_to_text()
                        doc = nlp(message)
                        nelly.update_state(customer=new_customer, parsed_tree=doc, question_context = {'type': 'food_restriction'})
                        frame = nelly.determine_semantic_frame_from_parsed_tree(doc,question_context = {'type': 'food_restriction'})
                        while frame != 'request_no_food_restriction' and frame != 'request_special_need':
                            text_to_speech("You have to answer me. Its important! Do you have any food restriction?")
                            message = speech_to_text()
                            doc = nlp(message)
                            nelly.update_state(customer=new_customer, parsed_tree=doc, question_context = {'type': 'food_restriction'})
                            frame = nelly.determine_semantic_frame_from_parsed_tree(doc,question_context = {'type': 'food_restriction'})
                        entering=1
                        answer1 = answer(frame)
                        text_to_speech(answer1)

                    message = speech_to_text()


        doc = nlp(message)
        nelly.update_state(customer=new_customer, parsed_tree=doc, question_context=question_context)
        frame = nelly.determine_semantic_frame_from_parsed_tree(doc,question_context=question_context)
        if ("avocado" in new_customer.order.vegetable_list) and inside==0:
            text_to_speech("You have added Avocado. Be carefull it is, expensive! Costs two extra euros.")
            inside = 1

        if new_customer.ignore_food_restriction == False:
            # set_trace()
            if new_customer.feedback:
                if 'nutritional_violations' in new_customer.feedback:
                    a=new_customer.feedback['nutritional_violations']
                    answer1= a[0]
                    if "_"  in answer1:
                        answer1=answer1.replace("_", ",")
                    # answer1= "You should remove, " + answer1 + ", because of your food restriction."
                    answer1 = "Be careful, " + answer1 + ", violates your food restrictions. Would you like me to remove it from your order"
                    text_to_speech(answer1)
                    question_context = {'type': 'accept_remove_items', 'items':new_customer.feedback['nutritional_violations']}
                    message = speech_to_text()

                    doc = nlp(message)
                    nelly.update_state(customer=new_customer, parsed_tree=doc,  question_context=question_context)
                    frame = nelly.determine_semantic_frame_from_parsed_tree(doc, question_context=question_context)

                # elif 'items_deleted' in new_customer.feedback:
                #     answer1 = "Got it. Items removed"
                #     text_to_speech(answer1)
                new_customer.feedback = {}

    answer1 = answer(frame)
    text_to_speech(answer1)
