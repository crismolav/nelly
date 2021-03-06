import spacy
from spacy import displacy
from pdb import set_trace
from customer import Order, Customer
from ingredients import ingredients_dict
from food_restrictions import food_restrictions_dict
import copy


def update_state(customer, parsed_tree, question_context={}):
    semantic_frame = determine_semantic_frame_from_parsed_tree(
        parsed_tree=parsed_tree, question_context=question_context)
    print("semantic_frame: %s" % semantic_frame)
    if semantic_frame == 'greeting':
        update_customer_with_greeting(customer=customer)
    elif semantic_frame == 'request_order_update':
        update_order_with_request(customer=customer, parsed_tree=parsed_tree)
    elif semantic_frame == 'request_ignore_food_type':
        update_order_with_request_ignore_food_type(
            customer=customer, question_context=question_context)
    elif semantic_frame == 'request_special_need':
        update_nutritional_restrictions(customer=customer, parsed_tree=parsed_tree)
    elif semantic_frame == "request_removal":
        update_order_with_removal_request(customer = customer, parsed_tree=parsed_tree)
    elif semantic_frame == "triggers_cancel":
        pass
    elif semantic_frame == "request_nelly_gender":
        pass
    elif semantic_frame == "request_no_food_restriction":
        update_customer_with_request_no_food_restriction(customer)
    elif semantic_frame == "accept_remove_suggested_items":
        update_order_with_removal_acceptance(
            customer = customer, question_context=question_context)
    else:
        pass


def update_order_with_removal_acceptance(customer, question_context):
    items_to_remove = question_context['items']
    for item_to_remove in items_to_remove:
        if item_to_remove in ingredients_dict['protein'].keys():
            customer.order.remove_protein_type(protein_type=item_to_remove)

        elif item_to_remove in ingredients_dict['vegetable'].keys():
            customer.order.remove_vegetable(vegetable=item_to_remove)

        elif item_to_remove in ingredients_dict['sauce'].keys():
            customer.order.remove_sauce(sauce=item_to_remove)

        elif item_to_remove in ingredients_dict['bread'].keys():
            customer.order.remove_bread_type(bread_type=item_to_remove)

        elif item_to_remove in ingredients_dict['sauce'].keys():
            customer.order.remove_cheese(cheese=item_to_remove)
        else:
            continue

        customer.feedback.setdefault('items_deleted', []).append(item_to_remove)

def update_customer_with_request_no_food_restriction(customer):
    customer.ignore_food_restriction = True


def update_customer_with_greeting(customer):
    customer.add_one_greeting()
    last_state_change = {}
    last_state_change.setdefault('semantic_frames', []).append('greeting')
    last_state_change['state_changed'] = {'number_of_greetings': customer.number_of_greetings}
    customer.last_state_change = last_state_change


def update_order_with_request(customer, parsed_tree):
    # TODO: use spacey labels ("PRODUCT")
    last_state_change = {}
    last_state_change.setdefault('semantic_frames', []).append('request_order_update')
    last_state_change['state_changed'] = {'order': {}}

    parsed_tree_copy = copy.deepcopy(parsed_tree)
    for token in parsed_tree:
        update_order_for_food_type(
            token, customer, parsed_tree=parsed_tree_copy,
            last_state_change=last_state_change)

    customer.last_state_change = last_state_change


def update_order_for_food_type(token, customer, parsed_tree, last_state_change):
    food_type = ''
    token_lemma = copy.deepcopy(str(token.lemma_))
    if token_lemma in ingredients_dict['protein'].keys():
        food_type = 'protein'
        customer.order.add_protein_type(protein_type=token_lemma)
        variable_name = 'protein'
    elif token_lemma in ingredients_dict['vegetable'].keys():
        food_type = 'vegetable'
        customer.order.add_vegetable(vegetable=token_lemma)
        variable_name = 'vegetable_list'
    elif token_lemma in ingredients_dict['sauce'].keys():
        food_type = 'sauce'
        customer.order.add_sauce(sauce=token_lemma)
        variable_name = 'sauce_list'
    elif "bread" in token_lemma:
        food_type = 'bread'
        if "_" not in token_lemma:
            token_lemma = get_food_type_strung(parsed_tree, "bread")
        customer.order.add_bread_type(bread_type=token_lemma)
        variable_name = 'bread_type'
    elif "cheese" in token_lemma:
        food_type = 'cheese'
        if "_" not in token_lemma:
            token_lemma = get_food_type_strung(parsed_tree, "cheese")
        customer.order.add_cheese(cheese=token_lemma)
        variable_name = 'cheese'
    elif (token_lemma in ingredients_dict['order_type'].keys()
          and token_lemma  != customer.order.order_type):
        customer.order.order_type = token_lemma
        variable_name = 'order_type'

    else:
        return
    if variable_name in ['sauce_list', 'vegetable_list']:
        last_state_change['state_changed']['order'].setdefault(variable_name, []).append(
            token_lemma)
    else:
        last_state_change['state_changed']['order'][variable_name] = token_lemma

    item_food_restrictions = check_item_food_restrictions(
        food_type=food_type, food_name=token_lemma,
        food_restrictions=customer.food_restrictions_list,
        ignored_food_restrictions_items=customer.ignored_food_restrictions_items
    )
    if item_food_restrictions != []:
        customer.feedback.setdefault('nutritional_violations',[]).append(token_lemma)
    # last_state_change['food_restriction_violation'].setdefault(token.lemma_, []).append()
    # set_trace()

def from_variable_name_to_food_type(variable_name):
    conv_dict = {
        'vegetable_list': 'vegetable',
        'sauce_list': 'sauce',
    }
    return conv_dict[variable_name]


def update_order_with_removal_request(customer, parsed_tree):
    last_state_change = {}
    last_state_change.setdefault('semantic_frames', []).append('request_removal')
    last_state_change['state_changed'] = {'order': {}}

    for token in parsed_tree:
        if token.lemma_ in ingredients_dict['protein'].keys():
            customer.order.remove_protein_type(protein_type=token.lemma_)
            last_state_change['state_changed']['order']['protein'] = token.lemma_
        elif token.lemma_ in ingredients_dict['vegetable'].keys():
            customer.order.remove_vegetable(vegetable=token.lemma_)
            last_state_change['state_changed']['order'].setdefault('vegetable_list', []).append(
                token.lemma_)
        elif token.lemma_ in ingredients_dict['sauce'].keys():
            customer.order.remove_sauce(sauce=token.lemma_)
            last_state_change['state_changed']['order'].setdefault('sauce_list', []).append(
                token.lemma_)
        elif token.lemma_ == "bread":
            token.lemma_ = get_food_type_strung(parsed_tree, "bread")
            customer.order.remove_bread_type(bread_type=token.lemma_)
            last_state_change['state_changed']['order']['bread_type'] = token.lemma_
        elif token.lemma_ == "cheese":
            token.lemma_ = get_food_type_strung(parsed_tree, "cheese")
            customer.order.remove_cheese(cheese=token.lemma_)
            last_state_change['state_changed']['order']['cheese'] = token.lemma_

    customer.last_state_change = last_state_change


def update_nutritional_restrictions(customer, parsed_tree):
    for token in parsed_tree:
        if token.lemma_ in food_restrictions_dict.keys():
            customer.add_food_restriction(food_restriction=token.lemma_)

    nutritional_inconsistencies = check_nutritional_inconsistencies(customer)
    # customer.feedback = {'nutritional_violations': nutritional_inconsistencies}


def check_nutritional_inconsistencies(customer):
    nutritional_inconsistencies = {}
    customer_restriction_list = customer.food_restrictions_list

    for food_restriction in customer_restriction_list:
        nutritional_inconsistencies[food_restriction] = \
            check_nutritional_inconsistencies_for_food_restriction(
                customer=customer, food_restriction=food_restriction)

    return nutritional_inconsistencies


def check_nutritional_inconsistencies_for_food_restriction(customer, food_restriction):
    nutritional_inconsistencies = {}
    customer_restriction_list = customer.food_restrictions_list
    ignored_food_restrictions_items = customer.ignored_food_restrictions_items
    if customer.food_restrictions_list == []:
        return nutritional_inconsistencies
    # check bread
    bread_list = []
    if customer.order.bread_type is not None:
        if check_item_food_restriction(
                food_type='bread', food_name=customer.order.bread_type,
                food_restriction=food_restriction,
                ignored_food_restrictions_items=ignored_food_restrictions_items):
            bread_list.append(customer.order.bread_type)

    # check protein
    protein_inconsistencies = []
    if customer.order.protein is not None:
        if check_item_food_restriction(
                food_type='protein', food_name=customer.order.protein,
                food_restriction=food_restriction,
                ignored_food_restrictions_items=ignored_food_restrictions_items):
            protein_inconsistencies.append(customer.order.protein)

    # check cheese
    cheese_inconsistencies = []
    if customer.order.cheese is not None:
        if check_item_food_restriction(
                food_type='cheese', food_name=customer.order.cheese,
                food_restriction=food_restriction,
                ignored_food_restrictions_items=ignored_food_restrictions_items):
            cheese_inconsistencies.append(customer.order.cheese)

    # check vegetables
    vegetable_inconsistencies = []
    for vegetable in customer.order.vegetable_list:
        if check_item_food_restriction(
                food_type='vegetable', food_name=vegetable,
                food_restriction=food_restriction,
                ignored_food_restrictions_items=ignored_food_restrictions_items):
            vegetable_inconsistencies.append(vegetable)

    # check sauce
    sauce_inconsistencies = []
    for sauce in customer.order.sauce_list:
        if check_item_food_restriction(
                food_type='sauce', food_name=sauce,
                food_restriction=food_restriction,
                ignored_food_restrictions_items=ignored_food_restrictions_items):
            sauce_inconsistencies.append(sauce)

    return make_nutritional_inconsistencies_dict(
        bread_list=bread_list, protein_list=protein_inconsistencies,
        cheese_list=cheese_inconsistencies, vegetable_list=vegetable_inconsistencies,
        sauce_list=sauce_inconsistencies)


def make_nutritional_inconsistencies_dict(
        bread_list, protein_list, cheese_list, vegetable_list, sauce_list):
    nutritional_inconsistencies_dict = {}
    if bread_list != []:
        nutritional_inconsistencies_dict["bread"] = bread_list
    if protein_list != []:
        nutritional_inconsistencies_dict["protein"] = protein_list
    if cheese_list != []:
        nutritional_inconsistencies_dict["cheese"] = cheese_list
    if vegetable_list != []:
        nutritional_inconsistencies_dict["vegetable"] = vegetable_list
    if sauce_list != []:
        nutritional_inconsistencies_dict["sauce"] = sauce_list
    return nutritional_inconsistencies_dict


def check_item_food_restrictions(food_type, food_name, food_restrictions,
                                 ignored_food_restrictions_items):
    item_food_restrictions = []
    for food_restriction in food_restrictions:
        if check_item_food_restriction(food_type, food_name, food_restriction,
                                       ignored_food_restrictions_items):
            item_food_restrictions.append(food_restriction)

    return item_food_restrictions


def check_item_food_restriction(food_type, food_name, food_restriction,
                                ignored_food_restrictions_items):
    if food_name in ignored_food_restrictions_items.get(food_type, []):
        return False
    item_restriction_list = ingredients_dict.get(
        food_type, {}).get(food_name, {}).get("restriction", [])

    if food_restriction in item_restriction_list:
        return True
    else:
        return False
    # item_restriction_set = set(item_restriction_list)
    # customer_restriction_set = set(food_restriction)
    #
    # inconsistencies = list(item_restriction_set.intersection(customer_restriction_set))


def get_trigger_words_removal():
    return ["remove", "delete"]


def triggers_remove_item_from_the_order(root_tuple, parsed_tree, question_context={}):
    if question_context != {} and question_context['type'] == 'accept_remove_items':
        return False
    root_lemma, root_text = root_tuple
    trigger_words_removal = get_trigger_words_removal()

    for token in parsed_tree:
        if str(root_lemma) in get_trigger_words_removal() :
            if str(token.lemma_) in trigger_words_removal:
                return True
            if str(token.lemma_) in trigger_words_removal and str(token.dep_) == "neg":
                return False
        if str(root_lemma) == "want" and str(token.lemma_) in trigger_words_removal:
            return True
        if str(token.dep_) == "neg" and str(root_lemma) == "want":
            return False
    return False


def update_order_with_request_ignore_food_type(customer, question_context):
    food_type = question_context['type']
    customer.order.wants_food_type[food_type] = False

    last_state_change = {}
    last_state_change.setdefault('semantic_frames', []).append('request_ignore_food_type')
    last_state_change['state_changed'] = {'order': {}}
    last_state_change['state_changed']['order']['wants_food_type'] = food_type
    customer.last_state_change = last_state_change


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


def determine_semantic_frame_from_parsed_tree(parsed_tree, question_context={}):
    root_tuple = get_parse_tree_root_tuple(parsed_tree)
    # if triggers_a_request_for_information(
    #         root_tuple=root_tuple, parsed_tree=parsed_tree):
    #     return "request_for_information"
    if triggers_request_special_need(
            root_tuple=root_tuple, parsed_tree=parsed_tree):
        return 'request_special_need'
    elif triggers_remove_item_from_the_order(
            root_tuple=root_tuple, parsed_tree= parsed_tree, question_context=question_context):
        return "request_removal"
    elif triggers_request_order_update(
            root_tuple=root_tuple, parsed_tree=parsed_tree, question_context=question_context):
        return 'request_order_update'
    elif triggers_request_ignore_food_type(
            parsed_tree=parsed_tree, question_context=question_context):
        return 'request_ignore_food_type'
    elif triggers_greeting(
            root_tuple=root_tuple, parsed_tree=parsed_tree):
        return "greeting"
    elif triggers_request_goodbye(
            root_tuple=root_tuple, parsed_tree=parsed_tree):
        return "request_goodbye"
    elif triggers_request_cancel(
            root_tuple=root_tuple, parsed_tree=parsed_tree):
        return "request_cancel"
    elif triggers_nelly_gender(
            parsed_tree=parsed_tree):
        return "request_nelly_gender"
    elif triggers_request_no_food_restriction(
            parsed_tree=parsed_tree, question_context=question_context):
        return "request_no_food_restriction"
    elif triggers_accept_remove_suggested_items(
            parsed_tree=parsed_tree, question_context=question_context):
        return "accept_remove_suggested_items"
    elif triggers_deny_remove_suggested_items(
            parsed_tree=parsed_tree, question_context=question_context):
        return "deny_remove_suggested_items"
    # elif triggers_remove_item_from_the_order(root_tuple=root_tuple, parsed_tree= parsed_tree):
    #     return "request_removal"
    else:
        return "False"

#
# def triggers_request_sandwich_or_salad(parsed_tree, question_context):
#     if question_context == {} or 'sandwich_or_salad' not in question_context.get('type', {}):
#         return False
#     for token in parsed_tree:
#         set_trace()
#         if token.lemma_ in ['sandwich', 'salad'] and [x for x in token.children][0].dep_ !='neg':
#             return True
#
#     return False

def triggers_deny_remove_suggested_items(parsed_tree, question_context):
    if question_context == {} or 'accept_remove_items' not in question_context.get('type', {}):
        return False
    for token in parsed_tree:
        if token.i == 0 and token.lemma_.lower() == 'no':
            return True
        if token.i == 0 and token.lemma_.lower() == 'yes':
            return False
        if (str(token.dep_) == 'neg'
                and str(token.head) in ['do', 'have']):
            return True

    return True

def triggers_accept_remove_suggested_items(parsed_tree, question_context):
    if question_context == {} or 'accept_remove_items' not in question_context.get('type', {}):
        return False
    for token in parsed_tree:
        if token.i == 0 and token.lemma_.lower() == 'yes':
            return True
        if token.i == 0 and token.lemma_.lower() == 'no':
            return False
        if (str(token.dep_) == 'neg'
                and str(token.head) in ['do', 'have']):
            return False

    return True


def triggers_request_no_food_restriction(parsed_tree, question_context):
    if question_context == {} or 'food_restriction' not in question_context.get('type', {}):
        return False

    for token in parsed_tree:
        if token.i == 0 and token.lemma_.lower() == 'no':
            return True
        if (str(token.dep_) == 'neg'
                and str(token.head) in ['do', 'have']):
            return True

    return False


def triggers_nelly_gender(parsed_tree):
    for token in parsed_tree:
        if token.lemma_ == 'gender':
            return True

    return False


def triggers_a_request_for_information(root_tuple, parsed_tree):
    root_lemma, root_text = root_tuple

    if root_lemma in ["tell", "know", "contain", "include"]:
        if not root_verb_is_negated(root_tuple=root_tuple, parsed_tree=parsed_tree):
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
            if str(token.lemma_) in ["tell", "know", "contain", "include", "find", "inquire"]:
                return True
            elif str(token.lemma_) == 'do' and token.i == 0:
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


def get_trigger_words_goodbye():
    return ["bye", "goodbye", "ciao", "au-revoir"]


def triggers_request_goodbye(root_tuple, parsed_tree):
    trigger_words_goodbye = get_trigger_words_goodbye()
    for token in parsed_tree:
        if str(token.lemma_) in trigger_words_goodbye:
            return True
    return False


def get_trigger_words_cancel():
    return ["cancel", "stop"]


def triggers_request_cancel(root_tuple, parsed_tree):
    root_lemma, root_text = root_tuple
    trigger_words_cancel = get_trigger_words_cancel()
    for token in parsed_tree:
        if str(token.lemma_) in trigger_words_cancel:
            return True
        if str(token.lemma_) in trigger_words_cancel and str(token.dep_) == "neg":
            return False

    return False


def triggers_request_ignore_food_type(parsed_tree, question_context):
    if question_context == {} or question_context['type'] in ['food_restriction', 'accept_remove_items']:
        return False

    for token in parsed_tree:
        if token.i == 0 and token.lemma_.lower() == 'no':
            return True
        if (str(token.dep_) == 'neg'
                and str(token.head) in ['want', 'eat', 'like', 'need', 'add', 'have']):
            return True

    return False


def triggers_request_order_update(root_tuple, parsed_tree, question_context={}):
    root_lemma, root_text = root_tuple
    modal_verbs = ['would', 'like']
    there_is_a_verb = is_there_a_verb(parsed_tree)

    if there_is_a_verb and root_lemma not in ['sandwich', 'salad', 'have', 'like', 'want',
                                              'give', 'need', "add", "order"] + get_all_available_ingredients():
        return False

    for token in parsed_tree:
        if there_is_a_verb:
            if root_lemma in modal_verbs:
                if str(token.head) == root_text and str(token.lemma_) in ['know', 'inquire',
                                                                          'find']:
                    return False
        if token.lemma_ in ["bread", "cheese"]:
            token.lemma_ = get_food_type_strung(parsed_tree, token.lemma_)

        if str(token.lemma_.lower()) in get_all_available_ingredients():
            return True

    return False


def is_there_a_verb(parsed_tree):
    for token in parsed_tree:
        if token.lemma_ in ["bread", "cheese"]:
            token.lemma_ = get_food_type_strung(parsed_tree, token.lemma_)
        if token.lemma_ in get_all_available_ingredients():
            continue
        if token.pos_ == 'VERB':
            return True
    return False


def triggers_request_special_need(root_tuple, parsed_tree):
    root_lemma, root_text = root_tuple
    if root_lemma in ['eat', 'drink', 'ingest', 'consume', 'tolerate', 'have', 'be', 'vegan', 'vegetarian', "gluten"]:
        if root_lemma in ['vegan', 'vegetarian',"gluten"]:
            return True
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
    trigger_list = ['intolerance', 'intolerant', 'allergy', 'disease']
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
        all_available_ingredients += ingredients_dict[food_type].keys()
    return all_available_ingredients + ['sandwich', 'salad']


def get_food_type_strung(parsed_tree, food_type):
    food_type_list = []
    food_children = []
    for token in parsed_tree:
        if token.lemma_ == food_type:
            if token.i >0 and token.head.lemma_ in ['oregano']:
                food_children.append(token.head)
            else:
                food_children += token.children
            break
    filtered_food_children = filter_food_type_children(
        children=food_children, food_type=food_type)

    for food_child in filtered_food_children:
        if food_child.pos_ == 'DET':
            continue
        food_type_list.append(food_child.lemma_)

    if food_type_list != []:
        food_type_list.append(food_type)

    return '_'.join(food_type_list)


def filter_food_type_children(children, food_type):
    bread_list = ["wheat", "whole", "rice", "sourdough", "oregano", "pita"]
    cheese_list = ["regular", "vegan", "cheddar", "cottage", "cream"]
    filter_in_list = bread_list if food_type == 'bread' else cheese_list
    filtered_list = []
    for child in children:
        if str(child) in filter_in_list:
            filtered_list.append(child)

    return filtered_list


def return_last_elements_added_to_the_order(customer):
    customer_dict = customer.last_state_change

    values_clean = []

    for keys, i in customer_dict["state_changed"]["order"].items():

        if keys in ["vegetable_list", "sauce_list"]:
            values_clean += i
        else:
            if "_" in keys:
                values_clean.append(i.replace("_", " "))
            else:
                values_clean.append(i)

    return values_clean


if __name__ == "__main__":
    new_customer = Customer()
    nlp = spacy.load("en_core_web_sm")
    doc = nlp("i want a sandwich with tomato lettuce and onions and beef")
    print(doc)

    update_state(customer=new_customer, parsed_tree=doc)
    print("*****")
    print("New order vegetables: %s" % new_customer.order.vegetable_list)
    print("New order protein: %s" % new_customer.order.protein)
    print("New order cheese: %s" % new_customer.order.cheese)
    print("New order bread: %s" % new_customer.order.bread_type)
    print("New order sauce: %s" % new_customer.order.sauce_list)
    print("*****")

    print("you just added", return_last_elements_added_to_the_order(new_customer))
