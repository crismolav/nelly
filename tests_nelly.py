import unittest
import spacy
import nelly

class NellyTests(unittest.TestCase):
    def test_determine_semantic_frame_from_parsed_tree__request_special_need__have(self):
        nlp = spacy.load("en_core_web_sm")
        parsed_tree = nlp("I have gluten allergy")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = 'request_special_need'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__request_special_need__be_celiac(self):
        nlp = spacy.load("en_core_web_sm")
        parsed_tree = nlp("I am celiac")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = 'request_special_need'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__request_special_need__be_vegan(self):
        nlp = spacy.load("en_core_web_sm")
        parsed_tree = nlp("I am vegan")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = 'request_special_need'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__request_special_need__negated_verb__dairy(self):
        nlp = spacy.load("en_core_web_sm")
        parsed_tree = nlp("I can't eat dairy")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = 'request_special_need'

        self.assertEqual(expected, result)

    def test_determine_semantic_frame_from_parsed_tree__request_special_need__negated_verb__animals(self):
        nlp = spacy.load("en_core_web_sm")
        parsed_tree = nlp("I do not eat any animal products")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = 'request_special_need'

        self.assertEqual(expected, result)


    def test_determine_semantic_frame_from_parsed_tree__request_for_information(self):
        nlp = spacy.load("en_core_web_sm")
        parsed_tree = nlp("does my sandwich has lactose")

        result = nelly.determine_semantic_frame_from_parsed_tree(
            parsed_tree=parsed_tree)
        expected = "request_for_information"

        self.assertEqual(expected, result)

    def test_triggers_request_order_update__would__True(self):
        nlp = spacy.load("en_core_web_sm")
        parsed_tree = nlp("I would like a sandwich with tomato")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_request_order_update(
            root_tuple=root_tuple, parsed_tree=parsed_tree)

        self.assertTrue(result)

    def test_triggers_request_order_update__have__True(self):
        nlp = spacy.load("en_core_web_sm")
        parsed_tree = nlp("Can i have a sandwich")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_request_order_update(
            root_tuple=root_tuple, parsed_tree=parsed_tree)

        self.assertTrue(result)

    def test_triggers_request_order_update__no_verb__True(self):
        nlp = spacy.load("en_core_web_sm")
        parsed_tree = nlp("A sandwich please")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_request_order_update(
            root_tuple=root_tuple, parsed_tree=parsed_tree)

        self.assertTrue(result)

    def test_triggers_request_order_update__no_verb_just_ingredientes__True(self):
        nlp = spacy.load("en_core_web_sm")
        parsed_tree = nlp("Lettuce and cucumber")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_request_order_update(
            root_tuple=root_tuple, parsed_tree=parsed_tree)

        self.assertTrue(result)

    def test_triggers_request_order_update__would__False(self):
        nlp = spacy.load("en_core_web_sm")
        parsed_tree = nlp("I would like to know if this is vegan")
        root_tuple = nelly.get_parse_tree_root_tuple(parsed_tree)

        result = nelly.triggers_request_order_update(
            root_tuple=root_tuple, parsed_tree=parsed_tree)

        self.assertFalse(result)

    def test_is_there_a_verb__False(self):
        nlp = spacy.load("en_core_web_sm")
        parsed_tree = nlp("A sandwich please")

        result = nelly.is_there_a_verb(parsed_tree=parsed_tree)

        self.assertFalse(result)

    def test_is_there_a_verb__True(self):
        nlp = spacy.load("en_core_web_sm")
        parsed_tree = nlp("Can i order a sandwich please")

        result = nelly.is_there_a_verb(parsed_tree=parsed_tree)

        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()