# [{'brand':str, 'description':str, 'id': int, 'image_path':str}]
# if we want to be specific we can create a schema for this specific items we are returning
# creating a class an calling list[class_we_created]
def response_to_recommandations(response: dict) -> list[dict]:
    recommandations = []
    for item in response['hits']['hits']:
        recommandations.append({
            'id': item['_source']['product_id'],
            'brand': item['_source']['product_brand'],
            'description': item['_source']['product_short_description'],
            'image_path': item['_source']['product_image_path'],
        })
    return recommandations
