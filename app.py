import json
import logging
from flask_cors import CORS
from flask import Flask, request
from googletrans import Translator

# Import custom modules
import tests
import search
import response
import dialog

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"
cors = CORS(app)
global product_found
product_found = None

tr = Translator()


"""
    Process the user's request and return the appropriate response.
    Args:
        data (dict): A dictionary containing the user's request data.
    Returns:

        dict: A dictionary containing the response data to be sent back to the user.
"""


def process_request(data: dict):
    global product_found 
    user_utterance = data.get("utterance")
    file = data.get("file")

    if user_utterance == "Hi!":
        return {"has_response": True, "recommendations": "", "response": "Hello, I'm your virtual shopping chat bot, I can suggest you clothes in every languages", "system_action": ""}
    if user_utterance == "test":
        tests.run_tests()
        return {"has_response": True, "recommendations": "", "response": "Test done", "system_action": ""}
    try:
        # Run help command
        if user_utterance == "!help":
            return {
                "has_response": True,
                "recommendations": "",
                "response": """You can proceed with one of the following ways: \n
                            1) For debug mode send a message using this template.
                            !debug color:<a color> gender:<a gender> category:<a category> brand:<a brand> \n
                            2) For natural language search just type what you want to search""",
                "system_action": "",
            }

        # Run debug command
        if user_utterance[:6] == "!debug":
            user_utterance = user_utterance[6:]
            search_response = search.search_raw_info(user_utterance)
        else:


            language = tr.detect(user_utterance).lang
            if language != "en":
                user_utterance = tr.translate(user_utterance).text
            
            if(dialog.get_utterance_intent(user_utterance) == "user_qa_product_description" ):
              response_prompt = dialog.get_bot_response(user_utterance, product_found, None)
              
              return {
                "has_response": True,
                "recommendations": [],
                "response": response_prompt,
                "system_action": "",
              }
            
            elif(dialog.get_utterance_intent(user_utterance) != "user_request_get_products" ):
              response_prompt = dialog.get_bot_response(user_utterance, None, file)
              return {
                "has_response": True,
                "recommendations": [],
                "response": response_prompt,
                "system_action": "",
              }
              
            else:
              search_response = dialog.get_bot_response(user_utterance, None, None)
               
            

        if search_response["hits"]["total"]["value"] > 0:
            product_found = search_response
            response_recommendations = response.response_to_recommendations(search_response)
            response_prompt = "Here's what I found for you"
        else:
            response_recommendations = []
            response_prompt = "Sorry no item were found with what you asked, try something else.\n"

    except ValueError as e:
        logging.error(f"Error processing request: {e}")
        response_recommendations = []
        response_prompt = str(e)

    return {
        "has_response": True,
        "recommendations": response_recommendations,
        "response": response_prompt,
        "system_action": "",
    }


"""
    Handle the dialog turn by processing the user's request and returning the appropriate response.

    Returns:
        str: A JSON-formatted string containing the response data.
"""


@app.route("/", methods=["POST"])
def dialog_turn():
    if not request.is_json:
        return json.dumps(
            {
                "has_response": True,
                "recommendations": "",
                "response": "An error occurred, please try again later.",
                "system_action": "",
            }
        )

    data = request.json
    logging.info(f"Request data: {data}")

    response_dict = process_request(data)
    return json.dumps(response_dict)


if __name__ == "__main__":
    app.run(port=4000)
