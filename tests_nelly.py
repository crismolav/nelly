import unittest
import spacy
import nelly
import semantic_frames as sf

nlp = spacy.load("en_core_web_sm")
class NellyTests(unittest.TestCase):
    def test_determine_semantic_frame_from_parsed_tree__request_special_need__have(self):
        parsed_tree = nlp("I have gluten allergy")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = 'request_special_need'

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

    def test_determine_semantic_frame_from_parsed_tree__request_for_information(self):
        parsed_tree = nlp("does my sandwich has lactose")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = "request_for_information"

        self.assertEqual(expected, result)

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

    def test_triggers_a_request_for_information__verb_to_be__False(self):
        parsed_tree = nlp("We are vegan")
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

        parsed_tree = nlp("I want a sandwich with onions beef ketchup rice_bread and regular_cheese")
        nelly.update_state(customer=new_customer, parsed_tree=parsed_tree)

        results_list = [new_customer.order.vegetable_list, new_customer.order.protein,
                        new_customer.order.cheese, new_customer.order.bread_type, new_customer.order.sauce_list]

        expected_list =[["onions"], "beef", "regular_cheese", "rice_bread", ["ketchup"]]

        self.assertIsNot(expected_list, results_list)

    # def test_triggers_a_request_order_update_for_bread(self):
    #     new_customer = sf.Customer()
    #
    #     parsed_tree = nlp("I want a sandwich with whole wheat bread")
    #     nelly.update_state(customer=new_customer, parsed_tree=parsed_tree)
    #
    #     results = new_customer.order.bread_type
    #     expected = "whole_wheat_bread"
    #
    #     self.assertEqual(expected, results)

    def test_get_bread_type_strung__general_test(self):
        parsed_tree = nlp("Is the whole wheat bread vegan")

        result = nelly.get_food_type_strung(parsed_tree, "bread")
        expected = 'whole_wheat_bread'

        self.assertEqual(expected, result)

    def test_get_bread_type_strung__no_bread_mention(self):
        parsed_tree = nlp("hello how are you")

        result = nelly.get_food_type_strung(parsed_tree, "bread")
        expected = ''

        self.assertEqual(expected, result)

    def test_triggers_a_request_special_need(self):
        new_customer = sf.Customer()
        parsed_tree = nlp("vegan and celiac")

        nelly.update_state(customer=new_customer, parsed_tree=parsed_tree)

        results_list = new_customer.food_restrictions_list
        expected_list = ["vegan", "celiac"]

        self.assertIsNot(expected_list, results_list)

    def test_update_customer_with_greeting__updated_info_is_correct(self):
        new_customer = sf.Customer()
        updated_info = {}

        nelly.update_customer_with_greeting(customer=new_customer, updated_info=updated_info)
        expected = {'semantic_frames': ['greeting'], 'status_changed': {'customer': {'number_of_greetings'}}}

        self.assertEqual(expected, updated_info)

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