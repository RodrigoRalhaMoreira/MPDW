import json
import logging
from flask_cors import CORS
from flask import Flask, request

# Import custom modules
import tests
import search
import response

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"
cors = CORS(app)

"""
    Process the user's request and return the appropriate response.
    Args:
        data (dict): A dictionary containing the user's request data.
    Returns:

        dict: A dictionary containing the response data to be sent back to the user.
"""


def process_request(data: dict):
    user_utterance = data.get("utterance")

    if user_utterance == "test":
        tests.run_tests()
        return {"has_response": True, "recommendations": "", "response": "Test done", "system_action": ""}
    try:
        if user_utterance == "!help":
            return {
                "has_response": True,
                "recommendations": "",
                "response": """Enter your search in the following order: color, gender, category, brand: \n
                            For debug mode send a message using this template.
                            !search color:<a color> gender:<a gender> category:<a category> band:<a brand>""",
                "system_action": "",
            }

        if user_utterance[:7] == "!search":
            user_utterance = user_utterance[7:]

        search_response = search.search_natural_text(user_utterance)
        # search_response = search.search_raw_info(user_utterance)
        logging.info(f"Search response: {search_response}")

        if search_response["hits"]["total"]["value"] > 0:
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
