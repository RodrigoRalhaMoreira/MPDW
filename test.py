from flask import Flask, request
from flask_cors import CORS
import json

import response_generate as r
import opensearchData

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

        userUtterance = data.get('utterance')
        
        response = opensearchData.searchRawInfo(userUtterance)

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