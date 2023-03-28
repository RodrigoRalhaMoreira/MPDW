from flask import Flask, request
from flask_cors import CORS
import json

import response_generate as r

app = Flask(__name__) # create the Flask app
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

@app.route('/', methods=['POST'])
def dialog_turn():
    if request.is_json:
        data = request.json
        print(data)
        print(request.headers)
        print(data.get('utterance'))
        print(data.get('session_id'))
        print(data.get('user_action'))
        print(data.get('interface_selected_product_id'))
        print(data.get('image'))

        response = {'_shards': {'failed': 0, 'skipped': 0, 'successful': 4, 'total': 4},
                    'hits': {'hits': [{'_id': '17872033',
                                       '_index': 'farfetch_images',
                                       '_score': 1.3735868,
                                       '_source': {'outfits_ids': [76013],
                                                   'outfits_products': [[14592496,
                                                                         15953626,
                                                                         17872033,
                                                                         17872047]],
                                                   'product_attributes': '[{"attribute_name":"Neckline","attribute_values":["Round '
                                                                         'Neck"]},{"attribute_name":"Sleeve '
                                                                         'Length","attribute_values":["Shortsleeved"]}]',
                                                   'product_brand': 'ROBERTO CAVALLI',
                                                   'product_category': 'T-Shirts & Vests',
                                                   'product_family': 'Clothing',
                                                   'product_gender': 'MEN',
                                                   'product_highlights': '[black, cotton, patch '
                                                                         'detail, logo patch to '
                                                                         'the front, crew neck, '
                                                                         'short sleeves]',
                                                   'product_id': 17872033,
                                                   'product_image_path': 'https://large.novasearch.org/farfetch_products/images/17/87/20/33/17872033.jpg',
                                                   'product_main_colour': 'BLACK',
                                                   'product_materials': ['Cotton'],
                                                   'product_second_color': 'N/D',
                                                   'product_short_description': 'patch-detail '
                                                                                'T-shirt',
                                                   'product_sub_category': 'T-Shirts'},
                                       '_type': '_doc'},
                                      {'_id': '17888647',
                                       '_index': 'farfetch_images',
                                       '_score': 1.3735868,
                                       '_source': {'outfits_ids': [],
                                                   'outfits_products': [],
                                                   'product_attributes': '[{"attribute_name":"Neckline","attribute_values":["Round '
                                                                         'Neck"]},{"attribute_name":"Sleeve '
                                                                         'Length","attribute_values":["Shortsleeved"]}]',
                                                   'product_brand': 'A.P.C.',
                                                   'product_category': 'T-Shirts & Vests',
                                                   'product_family': 'Clothing',
                                                   'product_gender': 'MEN',
                                                   'product_highlights': '[black\xa0, cotton\xa0, '
                                                                         'jersey knit, logo print '
                                                                         'to the front, crew '
                                                                         'neck, short sleeves, '
                                                                         'straight hem]',
                                                   'product_id': 17888647,
                                                   'product_image_path': 'https://large.novasearch.org/farfetch_products/images/17/88/86/47/17888647.jpg',
                                                   'product_main_colour': 'BLACK',
                                                   'product_materials': ['Cotton'],
                                                   'product_second_color': 'N/D',
                                                   'product_short_description': 'logo-print '
                                                                                'cotton T-Shirt',
                                                   'product_sub_category': 'T-Shirts'},
                                       '_type': '_doc'},
                                      {'_id': '17905525',
                                       '_index': 'farfetch_images',
                                       '_score': 1.3735868,
                                       '_source': {'outfits_ids': [74297],
                                                   'outfits_products': [[14812812,
                                                                         17477049,
                                                                         17902341,
                                                                         17905525]],
                                                   'product_attributes': '[{"attribute_name":"Neckline","attribute_values":["Round '
                                                                         'Neck"]},{"attribute_name":"Sleeve '
                                                                         'Length","attribute_values":["Shortsleeved"]}]',
                                                   'product_brand': 'DONDUP',
                                                   'product_category': 'T-Shirts & Vests',
                                                   'product_family': 'Clothing',
                                                   'product_gender': 'MEN',
                                                   'product_highlights': '[black/off white, '
                                                                         'stretch-cotton, logo '
                                                                         'print to the front, '
                                                                         'round neck, short '
                                                                         'sleeves, straight hem]',
                                                   'product_id': 17905525,
                                                   'product_image_path': 'https://large.novasearch.org/farfetch_products/images/17/90/55/25/17905525.jpg',
                                                   'product_main_colour': 'BLACK',
                                                   'product_materials': ['Spandex/Elastane',
                                                                         'Cotton'],
                                                   'product_second_color': 'N/D',
                                                   'product_short_description': 'logo-print '
                                                                                'short-sleeve '
                                                                                'T-shirt',
                                                   'product_sub_category': 'T-Shirts'},
                                       '_type': '_doc'}],
                             'max_score': 1.3735868,
                             'total': {'relation': 'gte', 'value': 10000}},
                    'timed_out': False,
                    'took': 15}
        if response['hits']['total']['value'] > 0:
            response_recommandations = r.response_to_recommandations(response)
            response_prompt = "Here's what I found for you:\n test"
        else:
            response_recommandations = []
            response_prompt = "Sorry no item were found with what you asked, try something else.\n"

        responseDict = { "has_response": True, "recommendations": response_recommandations,
        "response": response_prompt, "system_action":""}
        jsonString = json.dumps(responseDict)

    return jsonString

app.run(port=4000) # run app in debug mode on port 5000