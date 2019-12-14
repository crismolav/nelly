class Greetings:
    def __init__(self):
        self.speaker = None
        self.addressee = None
        self.message = None

class Request:
    def __init__(self):
        self.speaker = None
        self.addressee = None
        self.message = None

class request_for_information(Request):
    pass

class request_special_need(Request):
    pass


class request_order_update(Request):
    pass

# class Inform:
#     def __init__(self):
#         self.speaker = None
#         self.addressee = None
#         self.message = None

# class ask_information(Ask):
#     pass

class Customer():
    def __init__(self):
        self.name = None
        self.order = Order()
        self.food_restrictions_list = []
        self.number_of_greetings = 0
        self.last_state_change = {}
        self.ignored_food_restrictions_items = {}

    def add_one_greeting(self):
        self.number_of_greetings += 1
    def add_food_restriction(self, food_restriction):
        self.food_restrictions_list.append(food_restriction)
    # def recognized_food_restrictions(self):
    #     return ['vegan', 'celiac', 'lactose_intolerant', 'peanut']

class Order():
    def __init__(self):
        self.bread_type = None
        self.protein = None
        self.cheese = None
        self.sauce_list = []
        self.vegetable_list = []

        self.wants_food_type = {'cheese':True , 'protein':True, 'sauce':True, 'vegetable':True}

    def add_bread_type(self, bread_type):
        self.bread_type = bread_type
    def add_protein_type(self, protein_type):
        self.protein = protein_type
    def add_vegetable(self, vegetable):
        self.vegetable_list.append(vegetable)
    def add_sauce(self, sauce):
        self.sauce_list.append(sauce)
    def add_cheese(self, cheese):
        self.cheese =cheese


