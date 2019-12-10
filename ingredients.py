ingredients_dict = {
    'tomato' : {
        "type" : "vegetable",
        "restrictions" : []
    },
    "lettuce" : {
        "type" : "vegetable",
        "restrictions" : []
    },
    'cheese' : {
        "type" : "dairy",
        "restrictions" : ["lactose"],
        "ingredients": ["milk", "coagulant"]
    },
    'beef'  : {
        "type" : "protein",
        "restrictions" : ["vegan"]
    },
    'wheat_bread'  : {
        "type": "bread",
        "restrictions": ["gluten", "vegan"],
        "ingredients": ["wheat_flour", "yeast", "butter", "water", "salt", "sugar"]
    },
    'whole_wheat_bread'  : {
        "type": "bread",
        "restrictions": ["gluten", "vegan"],
        "ingredients": ["whole_wheat_flour", "yeast", "sun_flower_oil", "water", "salt", "sugar"]
    },
    'rice_bread' : {
        "type": "bread",
        "restrictions": ["vegan"],
        "ingredients": ["rice_flour", "yeast", "butter", "water", "salt", "sugar"]

    },
    'sourdough_bread' : {
        "type": "bread",
        "restrictions": [],
        "ingredients": ["wheat_flour", "water", "salt", "olive_oil","sun_flower_seeds"]

    }
    # 'customer' : {
    #     "greeting": true / false,
    #     "name" :,
    #     "nutritional restriction":,
    #     "price":,
    # }
}
