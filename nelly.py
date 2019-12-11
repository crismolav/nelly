import speech_recognition as sr
import os
import spacy
from spacy import displacy
from pdb import set_trace
from semantic_frames import Order, Customer
from ingredients import ingredients_dict
import sys
from spacy import displacy
from pdb import set_trace
from semantic_frames import Order, Customer
from ingredients import ingredients_dict
from food_restrictions import food_restrictions_dict


def update_state(customer, parsed_tree):
    semantic_frame = determine_semantic_frame_from_parsed_tree(parsed_tree)
    print("semantic_frame: %s" % semantic_frame)
    if semantic_frame == 'greeting':
        update_customer_with_greeting(customer=customer)
    elif semantic_frame == 'request_order_update':
        update_order_with_request(customer=customer, parsed_tree=parsed_tree)
    elif semantic_frame == 'request_for_information':
        provide_information(customer=customer, parsed_tree=parsed_tree)
    elif semantic_frame == 'request_special_need':
        update_nutritional_restrictions(customer=customer, parsed_tree=parsed_tree)
    else:
        pass

def update_customer_with_greeting(customer):
    customer.update_greeted_status(status=True)

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
            customer.order.add_bread_type(bread_type=token.lemma_)
        elif token.lemma_ in ingredients_dict['cheese'].keys():
            customer.order.add_cheese(cheese=token.lemma_)

def update_nutritional_restrictions(customer, parsed_tree):
    for token in parsed_tree:
        if token.lemma_ in food_restrictions_dict.keys():
            customer.food_restrictions_list.add_food_restriction(food_restriction=token.lemma_)


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
    if triggers_a_request_for_information(root_tuple=root_tuple, parsed_tree=parsed_tree):
        return "request_for_information"
    elif triggers_request_special_need(root_tuple=root_tuple, parsed_tree=parsed_tree):
        return 'request_special_need'
    elif triggers_request_order_update(root_tuple=root_tuple, parsed_tree=parsed_tree):
        return 'request_order_update'
    elif triggers_greeting(root_tuple=root_tuple, parsed_tree= parsed_tree):
        return "greeting"
    else:
        return False

def triggers_a_request_for_information(root_tuple, parsed_tree):
    root_lemma, root_text = root_tuple
    if root_lemma in ["tell", "know", "contain", "include"]:
        return True
    elif root_lemma in ["have", "want", "need", "would", "like", "be"]:

        for token in parsed_tree:
            if token.lemma_ in get_trigger_words_greeting():
                return False
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


def get_trigger_words_greeting():
    return ["hi", "hey", "hello", "morning", "afternoon", "evening", "night"]
def triggers_greeting(root_tuple, parsed_tree):
    trigger_words_greeting = get_trigger_words_greeting()
    for token in parsed_tree:
        if str(token.lemma_) in trigger_words_greeting:
            return True

    return False
    # root_lemma, root_text = root_tuple
    # if root_lemma in ["hi", "hey", "hello", "morning", "afternoon", "evening", "night"]:
    #     return True
    # if root_lemma == "be":
    #     for token in parsed_tree:
    #         if str(token.lemma_) in ["how"]:
    #             return True
    # return False

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
        if str(token.lemma_.lower()) in get_all_available_ingredients():
            return True

    return False

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
    return all_available_ingredients + ['sandwich']

def get_bread_type_strung(parsed_tree):
    bread_type_list = []
    bread_children = []
    for token in parsed_tree:
        if token.lemma_ == 'bread':
            bread_children = token.children
            break
    for bread_child in bread_children:
        if bread_child.pos_ == 'DET':
            continue
        bread_type_list.append(bread_child.lemma_)

    if bread_type_list != []:
        bread_type_list.append('bread')

    return '_'.join(bread_type_list)

if __name__=="__main__":
    new_customer =  Customer()
    nlp = spacy.load("en_core_web_sm")
    doc = nlp("I would like a sandwich with onions and beef")
    # doc = displacy.serve(doc, style="dep")
    # for token in doc:
    #     print(token.text, token.head,  token.lemma_, token.pos_, token.tag_, token.dep_,
    #           token.shape_, token.is_alpha, token.is_stop)

    update_state(customer=new_customer, parsed_tree=doc)
    print("*****")
    print("New order vegetables: %s"%new_customer.order.vegetable_list)
    print("New order protein: %s" % new_customer.order.protein)
    print("New order cheese: %s" % new_customer.order.cheese)
    print("New order bread: %s" % new_customer.order.bread_type)
    print("New order sauce: %s" % new_customer.order.sauce_list)
    print("*****")

    displacy.serve(doc, style="dep")
