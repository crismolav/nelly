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

    def test_determine_semantic_frame_from_parsed_tree__request_special_need__be(self):
        nlp = spacy.load("en_core_web_sm")
        parsed_tree = nlp("I am celiac")

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



if __name__ == '__main__':
    unittest.main()