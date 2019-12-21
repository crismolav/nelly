import unittest
import spacy
import nelly
import customer as sf
from pdb import set_trace

nlp = spacy.load("en_core_web_sm")
class NellyTests(unittest.TestCase):
    def test_determine_semantic_frame_from_parsed_tree__triggers_accept_remove_suggested_items_True(self):
        parsed_tree = nlp("Yes remove it")
        question_context = {'type': 'accept_remove_items',
                            'items': ['whole_wheat_bread']}

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree, question_context=question_context)
        expected = 'accept_remove_suggested_items'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__cheese_update(self):
        parsed_tree = nlp("can I have vegan cheese")
        question_context = {}

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree, question_context=question_context)
        expected = 'request_order_update'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__oregano_bread__update(self):
        parsed_tree = nlp("can I have oregano bread")
        question_context = {}

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree, question_context=question_context)
        expected = 'request_order_update'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__no_verb(self):
        parsed_tree = nlp("tomato and avocado please")
        question_context = {}
        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree, question_context=question_context)
        expected = 'request_order_update'

        self.assertEqual(expected, result)

    def test_triggers_request_special_need__True(self):
        parsed_tree = nlp("I'm lactose intolerant")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_request_special_need(
            parsed_tree=parsed_tree, root_tuple=root_tuple)

        self.assertTrue(result)

    # def test_triggers_request_sandwich_or_salad__True(self):
    #     parsed_tree = nlp("I want a salad")
    #     question_context = {'type': 'sandwich_or_salad'}
    #
    #     result = nelly.triggers_request_sandwich_or_salad(
    #         parsed_tree=parsed_tree, question_context=question_context)
    #
    #     self.assertTrue(result)
    #
    # def test_triggers_request_sandwich_or_salad__False(self):
    #     parsed_tree = nlp("I don't want a salad")
    #     question_context = {'type': 'sandwich_or_salad'}
    #
    #     result = nelly.triggers_request_sandwich_or_salad(
    #         parsed_tree=parsed_tree, question_context=question_context)
    #
    #     self.assertFalse(result)
    # def test_triggers_request_sandwich_or_salad__True(self):
    #     parsed_tree = nlp("I want a salad")
    #     question_context = {'type': 'sandwich_or_salad'}
    #
    #     result = nelly.triggers_request_sandwich_or_salad(
    #         parsed_tree=parsed_tree, question_context=question_context)
    #
    #     self.assertTrue(result)

    def test_determine_semantic_frame_from_parsed_tree__triggers_accept_remove_suggested_items_False(self):
        parsed_tree = nlp("No")
        question_context = {'type': 'accept_remove_items',
                            'items': ['whole_wheat_bread']}

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree, question_context=question_context)
        expected = 'deny_remove_suggested_items'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__request_special_need__have(self):
        parsed_tree = nlp("I have gluten allergy")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = 'request_special_need'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__request_no_food_restriction(self):
        parsed_tree = nlp("I don't")
        question_context = {'type': 'food_restriction'}

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree, question_context=question_context)
        expected = 'request_no_food_restriction'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__False(self):
        parsed_tree = nlp("I do")
        question_context = {'type': 'food_restriction'}

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree, question_context=question_context)
        expected = 'False'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__accept_remove_suggested_items(self):
        parsed_tree = nlp("I do")
        question_context = {'type': 'accept_remove_items'}

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree, question_context=question_context)
        expected = 'accept_remove_suggested_items'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__accept_remove_suggested_items_False(self):
        parsed_tree = nlp("I don't")
        question_context = {'type': 'remove_suggested_items'}

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree, question_context=question_context)
        expected = 'False'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__greeting_simple(self):
        parsed_tree = nlp("Hello")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = 'greeting'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__greeting_extended(self):
        parsed_tree = nlp("Hello Nelly, how are you?")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = 'greeting'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__request_ignore_food_type(self):
        parsed_tree = nlp("I don't want vegetables")
        question_context =  {'type':'vegetable'}

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree, question_context=question_context)
        expected = 'request_ignore_food_type'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__greeting_with_name(self):
        parsed_tree = nlp("Hello Nelly")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = 'greeting'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__greeting_with_order__request_order_update(self):
        parsed_tree = nlp("Hello Nelly a sandwich with tomato")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = 'request_order_update'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__request_special_need__be_celiac(self):
        parsed_tree = nlp("I am celiac")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = 'request_special_need'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__request_special_need__be_vegan(self):
        parsed_tree = nlp("I am vegan")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = 'request_special_need'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__request_special_need__negated_verb__dairy(self):
        parsed_tree = nlp("I can't eat dairy")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = 'request_special_need'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__request_special_need__negated_verb__animals(self):
        parsed_tree = nlp("I do not eat any animal products")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = 'request_special_need'

        self.assertEqual(expected, result)

    # def test_determine_semantic_frame_from_parsed_tree__request_for_information(self):
    #     parsed_tree = nlp("does my sandwich has lactose")
    #
    #     result = nelly.determine_semantic_frame_from_parsed_tree(
    #         parsed_tree=parsed_tree)
    #     expected = "request_for_information"
    #
    #     self.assertEqual(expected, result)

    def test_triggers_request_order_update__would__True(self):
        parsed_tree = nlp("I would like a sandwich with tomato")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_request_order_update(
            root_tuple=root_tuple, parsed_tree=parsed_tree)

        self.assertTrue(result)

    def test_triggers_request_order_update__have__True(self):
        parsed_tree = nlp("Can i have a sandwich")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_request_order_update(
            root_tuple=root_tuple, parsed_tree=parsed_tree)

        self.assertTrue(result)

    def test_triggers_request_order_update__no_verb__True(self):
        parsed_tree = nlp("A sandwich please")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_request_order_update(
            root_tuple=root_tuple, parsed_tree=parsed_tree)

        self.assertTrue(result)

    def test_triggers_request_order_update__no_verb_just_ingredientes__True(self):
        parsed_tree = nlp("Lettuce and cucumber")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_request_order_update(
            root_tuple=root_tuple, parsed_tree=parsed_tree)

        self.assertTrue(result)

    def test_triggers_request_order_update__would__False(self):
        parsed_tree = nlp("I would like to know if this is vegan")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_request_order_update(
            root_tuple=root_tuple, parsed_tree=parsed_tree)

        self.assertFalse(result)

    def test_is_there_a_verb__False(self):
        parsed_tree = nlp("A sandwich please")

        result = nelly.is_there_a_verb(parsed_tree=parsed_tree)

        self.assertFalse(result)

    def test_is_there_a_verb__True(self):
        parsed_tree = nlp("Can i order a sandwich please")

        result = nelly.is_there_a_verb(parsed_tree=parsed_tree)

        self.assertTrue(result)

    def test_triggers_a_request_for_information__verb_to_be__True(self):
        parsed_tree = nlp("Is the bread gluten free")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_a_request_for_information(
            root_tuple=root_tuple, parsed_tree=parsed_tree)

        self.assertTrue(result)

    def test_triggers_a_request_for_information__verb_to_be__wrong(self):
        parsed_tree = nlp("I don't know")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_a_request_for_information(
            root_tuple=root_tuple, parsed_tree=parsed_tree)

        self.assertFalse(result)

    def test_triggers_a_request_for_information__verb_to_be__False(self):
        parsed_tree = nlp("We are vegan")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_a_request_for_information(
            root_tuple=root_tuple, parsed_tree=parsed_tree)

        self.assertFalse(result)

    def test_triggers_nelly_gender__True(self):
        parsed_tree = nlp("What is your gender")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_a_request_for_information(
            root_tuple=root_tuple, parsed_tree=parsed_tree)

        self.assertTrue(result)

    def test_triggers_nelly_gender__False(self):
        parsed_tree = nlp("Hey there what's up")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_a_request_for_information(
            root_tuple=root_tuple, parsed_tree=parsed_tree)

        self.assertFalse(result)

    def test_update_customer_with_greeting__True(self):
        new_customer = sf.Customer()
        nelly.update_customer_with_greeting(customer=new_customer)
        expected = 1
        self.assertEqual(expected, new_customer.number_of_greetings)

    def test_triggers_a_request_order_update_all_ingredients(self):
        new_customer = sf.Customer()

        parsed_tree = nlp("I want a sandwich with onions tomato beef ketchup rice bread and regular cheese")
        nelly.update_state(customer=new_customer, parsed_tree=parsed_tree)

        results_list = [new_customer.order.vegetable_list, new_customer.order.protein,
                        new_customer.order.cheese, new_customer.order.bread_type, new_customer.order.sauce_list]

        expected_list =[["onion","tomato"], "beef", "regular_cheese", "rice_bread", ["ketchup"]]
        expected_last_state_change = {
            'semantic_frames': ['request_order_update'],
            'state_changed': {
                'order': {
                    'vegetable_list': ['onion', 'tomato'], 'protein': 'beef',
                    'sauce_list': ['ketchup'], 'bread_type': 'rice_bread',
                    'cheese': 'regular_cheese'}
            }
        }

        print(new_customer.last_state_change)

        self.assertEqual(expected_list, results_list)
        self.assertEqual(expected_last_state_change, new_customer.last_state_change)

    def test_adding_vegetables(self):
        new_customer = sf.Customer()
        new_customer.order.add_vegetable("tomato")
        new_customer.order.add_vegetable("lettuce")
        new_customer.order.add_vegetable("olives")
        new_customer.order.add_vegetable("onions")

        result = new_customer.order.vegetable_list
        expected = ["tomato", "lettuce", "olives","onions"]
        self.assertEqual(expected, result)

    def test_update_order_with_request_ignore_food_type__cheese(self):
        new_customer = sf.Customer()
        question_context = {'type':'cheese'}

        nelly.update_order_with_request_ignore_food_type(
            customer=new_customer, question_context=question_context)
        expected_wants_food_type = {
            'cheese': False, 'protein': True, 'sauce': True, 'vegetable': True}

        self.assertEqual(expected_wants_food_type, new_customer.order.wants_food_type)

    def test_update_order_with_request__cheese(self):
        new_customer = sf.Customer()
        parsed_tree = nlp("pita bread")

        nelly.update_order_with_request(
            customer=new_customer, parsed_tree=parsed_tree)
        expected_bread = "pita_bread"

        self.assertEqual(expected_bread, new_customer.order.bread_type)

    def test_update_order_with_request__pita_bread(self):
        new_customer = sf.Customer()
        parsed_tree = nlp("can I have pita bread")

        nelly.update_order_with_request(
            customer=new_customer, parsed_tree=parsed_tree)
        expected_bread = "pita_bread"

        self.assertEqual(expected_bread, new_customer.order.bread_type)

    def test_update_order_with_request__check_feedback(self):
        new_customer = sf.Customer()
        new_customer.food_restrictions_list = ['vegan']
        parsed_tree = nlp("I want a sandwich with whole wheat bread")

        nelly.update_order_with_request(
            customer=new_customer, parsed_tree=parsed_tree)
        expected_feedback = {'nutritional_violations': ['whole_wheat_bread']}

        self.assertEqual(expected_feedback, new_customer.feedback)

    def test_triggers_a_request_order_update_for_bread(self):
        new_customer = sf.Customer()

        parsed_tree = nlp("I want a sandwich with whole wheat bread")
        nelly.update_state(customer=new_customer, parsed_tree=parsed_tree)

        results = new_customer.order.bread_type
        expected = "whole_wheat_bread"

        self.assertEqual(expected, results)


    def test_get_bread_type_strung__no_bread_mention(self):
        parsed_tree = nlp("hello how are you")

        result = nelly.get_food_type_strung(parsed_tree, "bread")
        expected = ''

        self.assertEqual(expected, result)

    def test_get_bread_type_strung__pita_bread(self):
        parsed_tree = nlp("can i have pita bread")

        result = nelly.get_food_type_strung(parsed_tree, "bread")
        expected = 'pita_bread'

        self.assertEqual(expected, result)

    def test_triggers_a_request_special_need(self):
        new_customer = sf.Customer()

        parsed_tree = nlp("i am vegan and vegetarian")
        nelly.update_state(customer=new_customer, parsed_tree=parsed_tree)

        results_list = new_customer.food_restrictions_list
        expected_list = ["vegan", "vegetarian"]

        self.assertEqual(expected_list, results_list)

    def test_update_customer_with_greeting__updated_info_is_correct(self):
        new_customer = sf.Customer()

        nelly.update_customer_with_greeting(customer=new_customer)
        result = new_customer.last_state_change
        expected = {'semantic_frames': ['greeting'], 'state_changed': {'number_of_greetings': 1}}

        self.assertEqual(expected, result)

    def test_filter_food_type_children__bread_filter(self):
        children = ["ketchup", "rice", "whole", "onions"]
        food_type = "bread"
    
        result_list  = nelly.filter_food_type_children(children=children, food_type= food_type)
        expected_list= ["rice", "whole"]

        self.assertEqual(result_list, expected_list)

    def test_get_bread_type_strung__general_test(self):
        parsed_tree = nlp("Is the whole wheat bread vegan")

        result = nelly.get_food_type_strung(parsed_tree =parsed_tree, food_type="bread")
        expected = 'whole_wheat_bread'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__request_cancel_True(self):
        parsed_tree = nlp("i want to cancel the order")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_request_cancel(root_tuple=root_tuple, parsed_tree= parsed_tree)

        self.assertTrue(result)

    def test_determine_semantic_frame_from_parsed_tree__request_cancel_false(self):
        parsed_tree = nlp("do not cancel the order")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_request_cancel(root_tuple=root_tuple, parsed_tree= parsed_tree)

        self.assertTrue(result)

    def test_determine_Semantic_frame_from_parsed_tree__triggers_removal(self):
        parsed_tree = nlp("remove tomato")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = "request_removal"

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__request_removal_true(self):
        parsed_tree = nlp("Nelly, i want to remove the tomato")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_remove_item_from_the_order(root_tuple=root_tuple, parsed_tree=parsed_tree)

        self.assertTrue(result)


    def test_determine_semantic_frame_from_parsed_tree__request_removal_false(self):
        parsed_tree = nlp("Nelly, i do not want to remove tomato")

        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_remove_item_from_the_order(root_tuple=root_tuple, parsed_tree=parsed_tree)

        self.assertFalse(result)

    def test_determine_semantic_frame_from_parsed_tree__request_cancel_False(self):
        parsed_tree = nlp("Hello Nelly my old friend")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_request_cancel(root_tuple=root_tuple, parsed_tree= parsed_tree)

        self.assertFalse(result)


    def test_determine_Semantic_frame_from_parsed_tree__triggers_cancel(self):
        parsed_tree = nlp("cancel my order")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = 'request_cancel'

        self.assertEqual(expected, result)

    def test_triggers_request_order_update__special_case(self):
        parsed_tree = nlp("i want whole wheat bread")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)
        result = nelly.triggers_request_order_update(
        root_tuple=root_tuple, parsed_tree=parsed_tree)
        self.assertTrue(result)

    def test_triggers_request_goodbye_simple_case(self):
        parsed_tree = nlp("goodbye nelly")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = 'request_goodbye'
        self.assertEqual(result,expected)

    def test_triggers_request_ignore_food_type__simple__True(self):
        parsed_tree = nlp("no")
        question_context = {'type':'vegetable'}

        result = nelly.triggers_request_ignore_food_type(
            parsed_tree=parsed_tree, question_context=question_context)

        self.assertTrue(result)

    def test_triggers_request_ignore_food_type__no_thanks__True(self):
        parsed_tree = nlp("no thanks")
        question_context = {'type':'vegetable'}

        result = nelly.triggers_request_ignore_food_type(
            parsed_tree=parsed_tree, question_context=question_context)

        self.assertTrue(result)

    def test_triggers_request_ignore_food_type__complex_want__True(self):
        parsed_tree = nlp("I don't want vegetables")
        question_context = {'type':'vegetable'}

        result = nelly.triggers_request_ignore_food_type(
            parsed_tree=parsed_tree, question_context=question_context)

        self.assertTrue(result)

    def test_triggers_request_ignore_food_type__complex_like_True(self):
        parsed_tree = nlp("I do not like vegetables")
        question_context = {'type':'vegetable'}

        result = nelly.triggers_request_ignore_food_type(
            parsed_tree=parsed_tree, question_context=question_context)

        self.assertTrue(result)

    def test_check_item_food_restriction__gluten(self):
        food_type = 'bread'
        food_name = 'oregano_bread'
        food_restriction = 'gluten'
        ignored_food_restrictions_items = {'bread':['oregano_bread']}

        result = nelly.check_item_food_restriction(
            food_type=food_type, food_name=food_name,
            food_restriction=food_restriction,
            ignored_food_restrictions_items=ignored_food_restrictions_items
        )

        self.assertFalse(result)

    def test_check_item_food_restriction__gluten__already_ignored(self):
        food_type = 'bread'
        food_name = 'oregano_bread'
        food_restriction = 'gluten'
        ignored_food_restrictions_items = {}

        result = nelly.check_item_food_restriction(
            food_type=food_type, food_name=food_name,
            food_restriction=food_restriction,
            ignored_food_restrictions_items=ignored_food_restrictions_items
        )

        self.assertTrue(result)

    def test_check_item_food_restriction__gluten__empty_list(self):
        food_type = 'bread'
        food_name = 'rice_bread'
        food_restriction = 'gluten'
        ignored_food_restrictions_items = {}

        result = nelly.check_item_food_restriction(
            food_type=food_type, food_name=food_name,
            food_restriction=food_restriction,
            ignored_food_restrictions_items=ignored_food_restrictions_items
        )

        self.assertFalse(result)

    def test_check_nutritional_inconsistencies__empty(self):
        new_customer = sf.Customer()

        result = nelly.check_nutritional_inconsistencies(customer=new_customer)
        expected = {}

        self.assertEqual(expected, result)


    def test_check_nutritional_inconsistencies__vegan_non_empty(self):
        new_customer = sf.Customer()
        new_customer.food_restrictions_list = ['vegan']

        new_customer.order.add_bread_type("oregano_bread")
        new_customer.order.add_vegetable("tomato")
        new_customer.order.add_protein_type("bacon")
        new_customer.order.add_sauce("ranch")

        result = nelly.check_nutritional_inconsistencies(customer=new_customer)
        expected = {
            'vegan': {
                'bread': ['oregano_bread'], 'protein': ['bacon'],
                'sauce': ['ranch']}
        }

        self.assertEqual(expected, result)

    def test_check_nutritional_inconsistencies__vegan_gluten__non_empty(self):
        new_customer = sf.Customer()
        new_customer.food_restrictions_list = ['vegan', 'gluten']

        new_customer.order.add_bread_type("oregano_bread")
        new_customer.order.add_vegetable("tomato")
        new_customer.order.add_protein_type("bacon")
        new_customer.order.add_sauce("ranch")

        result = nelly.check_nutritional_inconsistencies(customer=new_customer)
        expected = {
            'vegan': {'bread': ['oregano_bread'],
                      'protein': ['bacon'],
                      'sauce': ['ranch']},
            'gluten': {'bread': ['oregano_bread']} }

        self.assertEqual(expected, result)

    # def test_update_nutritional_restrictions__update_feedback(self):
    #     new_customer = sf.Customer()
    #     new_customer.order.add_bread_type("oregano_bread")
    #     new_customer.order.add_vegetable("tomato")
    #     new_customer.order.add_protein_type("bacon")
    #     new_customer.order.add_sauce("ranch")
    #     parsed_tree = nlp("I am vegan")
    #
    #     nelly.update_nutritional_restrictions(customer=new_customer, parsed_tree=parsed_tree)
    #     update_feedback_expected = {
    #         'nutritional_violations': {'vegan': {'bread': ['oregano_bread'],
    #                                              'protein': ['bacon'],
    #                                              'sauce': ['ranch']}}}
    #     set_trace()
    #     self.assertEqual(update_feedback_expected, new_customer.feedback)

    def test_check_update_order_with_removal_request_vegetables(self):
        new_customer = sf.Customer()
        new_customer.order.add_vegetable("tomato")
        new_customer.order.add_vegetable("onion")
        new_customer.order.add_vegetable("lettuce")
        parsed_tree = nlp("Nelly, please remove tomato")

        nelly.update_order_with_removal_request(customer=new_customer, parsed_tree=parsed_tree)

        result = new_customer.vegetable_list = ["onion", "lettuce"]
        self.assertTrue(result)

    def test_check_update_order_with_removal_request_sauces(self):
        new_customer = sf.Customer()
        new_customer.order.add_sauce("ketchup")
        new_customer.order.add_sauce("mustard")
        parsed_tree = nlp("Nelly, please remove ketchup")

        nelly.update_order_with_removal_request(customer=new_customer, parsed_tree=parsed_tree)

        result = new_customer.sauce_list = ["mustard"]
        expected_last_state_change = {'semantic_frames': ['request_removal'],
        'state_changed': {'order': {'sauce_list': ['ketchup']}}}
        self.assertEqual(expected_last_state_change, new_customer.last_state_change)
        self.assertTrue(result)

    def test_check_update_order_with_removal_request_sauces_that_does_not_exist(self):
        new_customer = sf.Customer()
        new_customer.order.add_sauce("ketchup")
        parsed_tree = nlp("Nelly, please remove mustard")

        nelly.update_order_with_removal_request(customer=new_customer, parsed_tree=parsed_tree)

        result = new_customer.sauce_list = ["mustard"]

        self.assertTrue(result)

    def test_triggers_request_no_food_restriction__True(self):

        parsed_tree = nlp("No I don't")
        question_context = {'type': 'food_restriction'}

        result = nelly.triggers_request_no_food_restriction(
            parsed_tree=parsed_tree, question_context=question_context)

        self.assertTrue(result)

    def test_check_item_food_restrictions__general_test(self):
        food_type = 'bread'
        food_name = 'oregano_bread'
        food_restrictions = ['gluten', 'vegan']
        ignored_food_restrictions_items = {}

        result = nelly.check_item_food_restrictions(
            food_type=food_type, food_name=food_name,
            food_restrictions = food_restrictions,
            ignored_food_restrictions_items=ignored_food_restrictions_items
        )
        expected = ['gluten', 'vegan']

        self.assertEqual(expected, result)

    def test_update_order_with_removal_acceptance__check_order_and_feedback(self):
        new_customer = sf.Customer()
        new_customer.order.add_bread_type("sourdough_bread")
        new_customer.order.add_sauce("mayonnaise")
        new_customer.order.add_sauce("ranch")

        question_context = {
            'type': 'accept_remove_items',
            'items': ['mayonnaise', 'ranch']
        }

        nelly.update_order_with_removal_acceptance(
            customer=new_customer, question_context=question_context)
        expected = [[],
                    'sourdough_bread']
        expected_feedback = {'items_deleted': ['mayonnaise', 'ranch']}
        result = [new_customer.order.sauce_list,
                  new_customer.order.bread_type]
        result_feedback = new_customer.feedback

        self.assertEqual(expected, result)
        self.assertEqual(expected_feedback, result_feedback)

    # def test_triggers_a_request_for_information__verb_to_be__False(self):
    #
    #     parsed_tree = nlp("Is the whole wheat bread vegan")
    #     root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)
    #
    #     result = nelly.triggers_a_request_for_information(
    #         root_tuple=root_tuple, parsed_tree=parsed_tree)
    #
    #     self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
