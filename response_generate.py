# [{'brand':str, 'description':str, 'id': int, 'image_path':str}]
# if we want to be specific we can create a schema for this specific items we are returning
# creating a class and calling list[class_we_created]
def response_to_recommendations(response: dict) -> list[dict]:
    recommendations = []
    for item in response['hits']['hits']:
        recommendations.append({
            'id': item['_source']['product_id'],
            'brand': item['_source']['product_brand'],
            'description': item['_source']['product_short_description'],
            'image_path': item['_source']['product_image_path'],
        })
    return recommendations
