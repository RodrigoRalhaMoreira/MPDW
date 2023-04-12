import search
import random

categories = [
  "brands",
  "colors",
  "clothes",
  "genders"
]

brands = [
  "alexander-mcqueen",
  "balenciaga",
  "balmain",
  "burberry",
  "dolce-&-gabbana",
  "dsquared2",
  "gucci",
  "moncler",
  "off-white",
  "palm-angers",
  "prada",
  "versace"
]
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
genders = ["men", "women"]


def generate_search_string(brand=None, color=None, cloth=None, gender=None):
    if not brand:
        brand = random.choice(brands)
    if not color:
        color = random.choice(colors)
    if not cloth:
        cloth = random.choice(clothes)
    if not gender:
        gender = random.choice(genders)

    return f"brand:{brand} color:{color} category:{cloth} gender:{gender}"


def run_test(search_string):
    result = search.search_raw_info(search_string)
    if result["hits"]["total"]["value"] <= 0:
        print(f"Error trying: {search_string}" + "\n")


def check_lists():
    for brand in brands:
        search_string = generate_search_string(brand=brand, color="black", cloth="shirt", gender="men")
        run_test(search_string)

    for color in colors:
        search_string = generate_search_string(brand="versace", color=color, cloth="shirt", gender="men")
        run_test(search_string)

    for cloth in clothes:
        search_string = generate_search_string(brand="versace", color="black", cloth=cloth, gender="men")
        run_test(search_string)

    for gender in genders:
        search_string = generate_search_string(brand="versace", color="black", cloth="shirt", gender=gender)
        run_test(search_string)


def test_color_cloth(nb_mots: int):
    for _ in range(nb_mots):
        search_string = generate_search_string()
        run_test(search_string)


def test_one_category(category: str, nb_mots: int):
    if category == "brands":
        for _ in range(nb_mots):
            search_string = generate_search_string(color="black", cloth="shirt", gender="men")
            run_test(search_string)
    elif category == "clothes":
        for _ in range(nb_mots):
            search_string = generate_search_string(brand="versace", color="black", gender="men")
            run_test(search_string)
    elif category == "colors":
        for _ in range(nb_mots):
            search_string = generate_search_string(brand="versace", cloth="shirt", gender="men")
            run_test(search_string)
    elif category == "genders":
        for _ in range(nb_mots):
            search_string = generate_search_string(brand="versace", color="black", cloth="shirt")
            run_test(search_string)
    else:
        print("Invalid category")


def run_tests():
    check_lists()
    for category in categories:
        test_one_category(category, 1)

    test_color_cloth(1)
