ingredients_dict = {
    "vegetable":{
        "tomato":{
            "restriction": [],
            "ingredients": []
        },
        "lettuce":{
            "restriction": [],
            "ingredients": []
        },
        "onion":{
            "restriction": [],
            "ingredients": []
        },
        "olives":{
            "restriction": [],
            "ingredients": []
        },
    },
    "protein":{
        "beef":{
            "restriction": ["vegan", "vegetarian"],
            "ingredients": []
        },
        "chicken":{
            "restriction": ["vegan", "vegetarian"],
            "ingredients": []
        },
        "tuna":{
            "restriction": ["vegan", "vegetarian"],
            "ingredients": []
        }
    },
    "cheese":{
        "regular_cheese":{
            "restriction": ["lactose", "vegan"],
            "ingredients": ["milk", "coagulants"]
        },
        "vegan_cheese":{
            "restriction": [],
            "ingredients": ["soja","coconut oil"]
        }
    },
    "bread":{
        "wheat_bread":{
            "restriction": ["vegan", "gluten"],
            "ingredients": ["wheat_flour", "yeast", "butter", "water", "salt", "sugar"]
        },
        "whole_wheat_bread":{
            "restriction": ["vegan", "gluten"],
            "ingredients": ["whole_wheat_flour", "yeast", "sun_flower_oil", "water", "salt", "sugar"]
        },
        "rice_bread":{
            "restriction": ["vegan"],
            "ingredients": ["rice_flour", "yeast", "butter", "water", "salt", "sugar"]
        },
        "sourdough_bread":{
            "restriction": [],
            "ingredients": ["wheat_flour", "water", "salt", "olive_oil","sun_flower_seeds"]
        }
    },
    "sauce":{
        "ketchup":{
            "restriction":[],
            "ingredients":["tomato", "water", "sugar", "sodium"]
        },
        "mustard":{
            "restriction":[],
            "ingredients":["mustard", "water", "sugar", "sodium"]
        },
        "mayonnaise":{
            "restriction":["vegan"],
            "ingredients":["egg", "oil", "sodium"]
        }
    }
}
