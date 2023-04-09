import search
import random

# list different colors and clothes
colors = [
    "black",
    "blue",
    "brown",
    "green",
    "grey",
    "neutrals",
    "orange",
    "pink",
    "purple",
    "red",
    "silver",
    "white",
    "yellow",
]
clothes = ["coats", "denim", "jackets", "pants", "shirt", "shorts", "skirts", "suits", "tee-shirt", "vests"]


def generate_search_string(color=None, cloth=None):
    if not color:
        color = random.choice(colors)
    if not cloth:
        cloth = random.choice(clothes)

    return f"color:{color} category:{cloth}"


def run_test(search_string):
    result = search.search_raw_info(search_string)
    if result["hits"]["total"]["value"] <= 0:
        print(f"Error trying: {search_string}" + "\n")


def check_lists():
    for color in colors:
        search_string = generate_search_string(color=color, cloth="shirt")
        run_test(search_string)

    for cloth in clothes:
        search_string = generate_search_string(color="black", cloth=cloth)
        run_test(search_string)


def test_color_cloth(nb_mots: int):
    for _ in range(nb_mots):
        search_string = generate_search_string()
        run_test(search_string)


def test_one_category(category: str, nb_mots: int):
    if category == "clothes":
        for _ in range(nb_mots):
            search_string = generate_search_string(color="black")
            run_test(search_string)
    elif category == "colors":
        for _ in range(nb_mots):
            search_string = generate_search_string(cloth="shirt")
            run_test(search_string)
    else:
        print("Invalid category")
