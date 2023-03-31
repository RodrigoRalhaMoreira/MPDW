import opensearchData as o
import random

# list different colors and clothes
colors = ['black', 'blue', 'brown', 'green', 'grey', 'neutrals', 'orange', 'pink', 'purple', 'red', 'silver', 'white',
          'yellow']
clothes = ['coats', 'denim', 'jackets', 'pants', 'shirt', 'shorts', 'skirts', 'suits', 'tee-shirt', 'vests']


def check_lists():
    for color in colors:
        result = o.searchRawInfo(color + " " + "shirt")
        if not (result['hits']['total']['value'] > 0):
            print("Invalid color: " + color + "\n")
    for cloth in clothes:
        result = o.searchRawInfo("black " + cloth)
        if not (result['hits']['total']['value'] > 0):
            print("Invalid cloth: " + cloth + "\n")


def test_color_cloth(nb_mots: int):
    for i in range(nb_mots):
        random_color = random.choice(colors)
        random_cloth = random.choice(clothes)
        result = o.searchRawInfo(random_color + " " + random_cloth)
        if not (result['hits']['total']['value'] > 0):
            print("Error trying: " + random_color + " " + random_cloth + "\n")
    return


def test_one_category(category: str, nb_mots: int):
    if category == 'clothes':
        for i in range(nb_mots):
            random_cloth = random.choice(clothes)
            result = o.searchRawInfo("black " + random_cloth)
            if not (result['hits']['total']['value'] > 0):
                print("Invalid cloth: " + random_cloth + "\n")
    if category == 'colors':
        for i in range(nb_mots):
            random_color = random.choice(colors)
            result = o.searchRawInfo(random_color + " " + "shirt")
            if not (result['hits']['total']['value'] > 0):
                print("Invalid color: " + random_color + "\n")
    if category != 'clothes' and category != 'colors':
        print("Invalid category")
    return
