from flask import Flask, request
from flask_cors import CORS
import json 

import response_generate as r
import opensearchData
import test

app = Flask(__name__)  # create the Flask app
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)


@app.route('/', methods=['POST'])
def dialog_turn():
    if not request.is_json:  # if the request isn't json display an error message
        jsonString = json.dumps({
                "has_response": True,
                "recommendations": '',
                "response": "An error occurred, please try again later.",
                "system_action": ""})
        return jsonString

    data = request.json
    print(f'Request data: {data}')  
    """ print(data)
    print(request.headers)
    print(data.get('utterance'))
    print(data.get('session_id'))
    print(data.get('user_action'))
    print(data.get('interface_selected_product_id'))
    print(data.get('image')) """

    userUtterance = data.get('utterance')

    if userUtterance == "test":
        test.test_color_cloth(10)
        print("Combined test done")
        test.test_one_category('clothes', 5)
        print("Clothes test done")
        test.test_one_category('colors', 5)
        print("Colors test done")
        jsonString = json.dumps({
            "has_response": True,
            "recommendations": '',
            "response": "Test done",
            "system_action": ""})
        return jsonString
    try:
        response = opensearchData.search_raw_info(userUtterance)
        print(f'Search response: {response}')
        if response['hits']['total']['value'] > 0:  
            response_recommendations = r.response_to_recommendations(response)
            response_prompt = "Here's what I found for you"
        else:
            response_recommendations = []
            response_prompt = "Sorry no item were found with what you asked, try something else.\n"
    except ValueError as e:
        response_recommendations = []
        response_prompt = str(e)

    responseDict = {
        "has_response": True,
        "recommendations": response_recommendations,
        "response": response_prompt,
        "system_action": ""}
    jsonString = json.dumps(responseDict)

    return jsonString


app.run(port=4000)  # run app in debug mode on port 5000