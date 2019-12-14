ingredients_dict = {
    "vegetable":{
        "tomato":{
            "restriction": [],
            "ingredients": ["tomato"]
        },
        "lettuce":{
            "restriction": [],
            "ingredients": ["lettuce"]
        },
        "onion":{
            "restriction": [],
            "ingredients": ["onion"]
        },
        "olives":{
            "restriction": [],
            "ingredients": ["olives"]
        },
        "pickles":{
            "restriction": [],
            "ingredients": ["pickles"]
        },
        "chile":{
            "restriction": [],
            "ingredients": ["chile"]
        },
        "mushrooms":{
            "restriction": [],
            "ingredients": ["mushrooms"]
        }
    },

    "protein":{
        "beef":{
            "restriction": ["vegan", "vegetarian"],
            "ingredients": ["beef"]
        },
        "chicken":{
            "restriction": ["vegan", "vegetarian"],
            "ingredients": ["chicken"]
        },
        "tuna":{
            "restriction": ["vegan", "vegetarian"],
            "ingredients": ["tuna fish"]
        },
        "pork":{
            "restriction": ["vegan", "vegetarian"],
            "ingredients": ["pork"]
        },
        "tofu":{
            "restriction": [],
            "ingredients": ["tofu"]
        },
        "salami":{
            "restriction": ["vegan", "vegetarian"],
            "ingredients": ["salami","pork"]
        },
        "salmon":{
            "restriction": ["vegan", "vegetarian"],
            "ingredients": ["salmon fish"]
        },
        "turkey":{
            "restriction": ["vegan", "vegetarian"],
            "ingredients": ["turkey"]
        },
        "bacon":{
            "restriction": ["vegan", "vegetarian"],
            "ingredients": ["pork"]
        }
    },

    "cheese":{
        "cheese":{
            "restriction": ["lactose", "vegan"],
            "ingredients": ["milk", "coagulants"]
        },
        "regular_cheese":{
            "restriction": ["lactose", "vegan"],
            "ingredients": ["milk", "coagulants"]
        },
        "vegan_cheese":{
            "restriction": [],
            "ingredients": ["soja","coconut oil"]
        },
        "cheddar_cheese":{
            "restriction": ["lactose", "vegan"],
            "ingredients": ["milk", "coagulants", "yellow colorant"]
        },
        "cottage_cheese":{
            "restriction": ["lactose", "vegan"],
            "ingredients": ["milk", "coagulants"]
        },
        "cream_cheese":{
            "restriction": ["lactose", "vegan"],
            "ingredients": ["milk", "coagulants"]
        }
    },

    "bread":{
        "bread": {
            "restriction": ["vegan", "gluten"],
            "ingredients": ["wheat_flour", "yeast", "butter", "water", "salt", "sugar"]
        },
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
        },
        "oregano_bread":{
            "restriction": ["vegan", "gluten"],
            "ingredients": ["oregano","wheat_flour", "water", "salt", "olive_oil"]
        },
        "pita_bread":{
            "restriction": [],
            "ingredients": ["wheat_flour", "water", "salt"]
        },
        "white_bread":{
            "restriction": ["vegan", "gluten"],
            "ingredients": ["yeast","wheat_flour", "water", "salt"]
        }
    },

    "sauce":{
        "ketchup":{
            "restriction":[],
            "ingredients":["tomato", "water", "sugar", "sodium"]
        },
        "tomato_sauce":{
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
        },
        "barbecue":{
            "restriction":[""],
            "ingredients":["species", "gum", "sodium", "sugar","mustard","water"]
        },
        "honey_mustard":{
            "restriction":[""],
            "ingredients":["honey","species", "gum", "sodium", "sugar","mustard","water"]
        },
        "spicy":{
            "restriction":[""],
            "ingredients":["chile","pepper","species", "gum", "sodium", "sugar","water"]
        },
        "ranch":{
            "restriction":["vegan", "vegetarian"],
            "ingredients":["milk","pepper","species", "gum", "sodium", "sugar","water"]
        }
    }

}
