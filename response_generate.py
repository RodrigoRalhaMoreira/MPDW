
def response_to_recommandations(response: dict) -> [{'brand':str, 'description':str, 'id': int, 'image_path':str}]:
    recommandations = []
    for item in response['hits']['hits']:
        recommandations.append({
            'id': item['_source']['product_id'],
            'brand': item['_source']['product_brand'],
            'description': item['_source']['product_short_description'],
            'image_path': item['_source']['product_image_path'],
        })
    return recommandations
