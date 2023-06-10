"""
    Converts the raw response from the OpenSearch query into a list of dictionaries containing product recommendations.

    :param response: A dictionary containing the raw response from the OpenSearch query.
    :return: A list of dictionaries containing products with the following keys: id, brand, description, and image_path.
"""


def response_to_recommendations(response: dict) -> list[dict]:
    return [
        {
            "id": item["_source"]["product_id"],
            "brand": item["_source"]["product_brand"],
            "description": item["_source"]["product_short_description"],
            "image_path": item["_source"]["product_image_path"],
        }
        for item in response["hits"]["hits"]
    ]


def response_to_details(item: dict) -> list[dict]:
    txt = "Product ID: {}\nBrand: {}\nDescription: {}\nProduct Materials: {}\n"
    
    aux = {
            "id": item["_source"]["product_id"],
            "brand": item["_source"]["product_brand"],
            "description": item["_source"]["product_short_description"],
            "image_path": item["_source"]["product_image_path"],
            "materials": item["_source"]["product_materials"],
            
    }
    
    
    
    return txt.format(aux.get("id"),aux.get("brand"), aux.get("description"),aux.get("materials"))



