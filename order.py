class Order:
    def __init__(self):
        self.bread_type = None
        self.protein = None
        self.sauce_list = []
        self.vegetable_list = []
    def add_bread_type(self, bread_type):
        self.bread_type = bread_type
    def available_bread_types(self):
        return ['vegan', 'whole-wheat', 'regular']
    def add_protein_type(self, protein_type):
        self.protein = protein_type
    def available_protein_types(self):
        return ['tofu', 'chicken', 'beef', 'pork']
    def add_vegetable(self, vegetable):
        self.vegetable_list.append(vegetable)
    def available_vegetables(self):
        return ['lettuce', 'tomato', 'cucumber', 'olive', 'onion']
    def add_sauce(self, sauce):
        self.sauce_list.append(sauce)
    def available_sauces(self):
        return ['barbecue', 'ketchup', 'mustard', 'nelly_sauce']
    def get_all_avaible_ingredients(self):
        return self.available_protein_types()+self.available_vegetables()+self.available_sauces()