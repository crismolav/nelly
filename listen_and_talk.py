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
        answer = ['Yes! The sandwich contains that ingredient','Yes, it has some.']
        answer = random.choice(answer)
    elif frame == "answer_price":
        answer = ['Its 5 euros in total! Thank you!','For you, I can leave it at 6 euros!', 'Its 10 euros. Have a nice day my friend.', 'Today, this sandwich is free for you!']
        answer = random.choice(answer)
    elif frame == "answer_goodbye":
        answer = ['Thank you, for buying in Nellys, have a nice day!','Thank you, for your order.', 'Bon apetit. Goodbye!']
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
def update_state(customer, parsed_tree):
    semantic_frame = determine_semantic_frame_from_parsed_tree(parsed_tree)
    print("semantic_frame: %s" % semantic_frame)
    if semantic_frame == 'request_order_update':
        update_order_with_request(customer=customer, parsed_tree=parsed_tree)
    elif semantic_frame == 'request_for_information':
        provide_information(customer, parsed_tree=parsed_tree)
    else:
        pass

def update_order_with_request(customer, parsed_tree):
    #TODO: use spacey labels ("PRODUCT")
    for token in parsed_tree:
        if token.lemma_ in ingredients_dict['protein'].keys():
            customer.order.add_protein_type(protein_type=token.lemma_)
        elif token.lemma_ in ingredients_dict['vegetable'].keys():
            customer.order.add_vegetable(vegetable=token.lemma_)
        elif token.lemma_ in ingredients_dict['sauce'].keys():
            customer.order.add_sauce(sauce=token.lemma_)
        elif token.lemma_ in ingredients_dict['bread'].keys():
            customer.order.add_bread(bread=token.lemma_)
        elif token.lemma_ in ingredients_dict['cheese'].keys():
            customer.order.add_cheese(cheese=token.lemma_)

def provide_information(customer, parsed_tree):
    root_lemma, root_text = get_parse_tree_root_tuple(parsed_tree)
    queried_list = determine_what_ingredient_is_being_queried(parsed_tree)
    if is_yes_or_no(root_lemma):
        pass

def is_yes_or_no(root_lemma):
    if root_lemma in ['be']:
        return True

def determine_what_ingredient_is_being_queried(parsed_tree):
    queried_list = []
    for token in parsed_tree:
        if token.lemma_ in get_all_available_ingredients():
            queried_list.append(token.lemma_)
    return queried_list

def determine_semantic_frame_from_parsed_tree(parsed_tree):
    root_tuple = get_parse_tree_root_tuple(parsed_tree)
    if triggers_greeting(root_tuple=root_tuple):
        return "greeting"
    elif triggers_a_request_for_information(root_tuple=root_tuple, parsed_tree=parsed_tree):
        return "request_for_information"
    elif triggers_request_special_need(root_tuple=root_tuple, parsed_tree=parsed_tree):
        return 'request_special_need'
    elif triggers_request_order_update(root_tuple=root_tuple, parsed_tree=parsed_tree):
        return 'request_order_update'
    else:
        return False

def triggers_a_request_for_information(root_tuple, parsed_tree):
    root_lemma, root_text = root_tuple
    if root_lemma in ["tell", "know", "contain", "include"]:
        return True
    elif root_lemma in ["have", "want", "need", "would", "like", "be"]:
        for token in parsed_tree:
            if str(token.head.lemma_) == 'be':
                # E.g. "I am vegan"
                if str(token.dep_) == 'nsubj':
                    return False
                # E.g. "Is this bread vegan"
                else:
                    return True
            if str(token.lemma_) in ["do", "tell", "know", "contain", "include", "find", "inquire"]:
                return True
    return False

def triggers_greeting(root_tuple):
    root_lemma, root_text = root_tuple
    if root_lemma in ["hi", "hey", "hello", "morning", "afternoon", "evening", "night"]:
        return True
    return False

def triggers_request_order_update(root_tuple, parsed_tree):
    root_lemma, root_text = root_tuple
    modal_verbs = ['would', 'like']
    there_is_a_verb = is_there_a_verb(parsed_tree)

    if there_is_a_verb and root_lemma not in ['sandwich', 'have', 'like', 'want',
                                              'give', 'need', "add", "order"]:
        return False
    for token in parsed_tree:
        if there_is_a_verb:
            if root_lemma in modal_verbs:
                if str(token.head) == root_text and str(token.lemma_) in ['know', 'inquire', 'find']:
                    return False
        else:
            if str(token.lemma_) in get_all_available_ingredients():
                return True

    return True

def is_there_a_verb(parsed_tree):
    for token in parsed_tree:
        if token.pos_ == 'VERB':
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
    positive_list = ['celiac', 'lactose', 'dairy', 'wheat', 'peanuts', 'nuts', 'meat', 'animal']
    for token in parsed_tree:
        parent = token.head
        granparent = parent.head
        if (str(parent) == root_text or str(granparent) == root_text) \
                and token.text in positive_list:
            return True
    return False

def get_parse_tree_root_tuple(parsed_tree):
    for token in parsed_tree:
        if token.dep_ == 'ROOT':
            return token.lemma_, token.text


def get_all_available_ingredients():
    all_available_ingredients = []
    for food_type, food_type_dict in ingredients_dict.items():
        all_available_ingredients +=ingredients_dict[food_type].keys()
    return all_available_ingredients
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
if __name__=="__main__":
    new_customer =  Customer()
    nlp = spacy.load("en_core_web_sm")
    message=speech_to_text()
    doc = nlp(message)
    # doc = displacy.serve(doc, style="dep")
    # for token in doc:
    #     print(token.text, token.head,  token.lemma_, token.pos_, token.tag_, token.dep_,
    #           token.shape_, token.is_alpha, token.is_stop)

    update_state(customer=new_customer, parsed_tree=doc)
    print("*****")
    print("New order vegetables: %s"%new_customer.order.vegetable_list)
    print("New order protein: %s" % new_customer.order.protein)
    print("*****")

    displacy.serve(doc, style="dep")


    frame = determine_semantic_frame_from_parsed_tree(doc)
    answer1= answer(frame)
    text_to_speech(answer1)
