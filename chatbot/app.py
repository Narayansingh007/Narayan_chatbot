import os
import traceback
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
from processing import setup, sale_script_welcome_message, sale_script_reply_message
from scheduling import sale_script_get_message_code, sale_script_get_scheduled_time, get_date_time_condition
from config import JWT_SECRET_KEY
from utils import validate_jwt_token

app = Flask(__name__)
CORS(app)
# Setup retriever and openai client
retriever, openai_client = setup()

@app.route('/')
def home():
    return '<h1>Hello FROM FREEDOM CHATBOT SERVICE</h1>'

@app.route('/sale_script', methods=['POST'])
def sale_script():
    # Check JWT Token
    token = None,
    error = validate_jwt_token()
    print(error)
    if error:
       return error, 401
    if 'x-access-tokens' in request.headers:
        token = request.headers['x-access-tokens']
    request_json = request.json
    if not request_json:
        return "No request json", 400

    # Get chat history
    if 'history' in request_json:
        history = request_json["history"]
    else:
        print(f"Receiving request: {request_json}")
        print(f"`history` is missing!")
        return "`history` is missing", 400

    print("==== Request ====")
    print(history)

    try:
        scheduled_time = None
        message_code = None

        # First welcome message
        if history is None or len(history) == 0:
            answer = sale_script_welcome_message()
        # Answer question
        else:
            message_code = sale_script_get_message_code(openai_client, history)
            print("===>", message_code)
            if message_code.lower() == "opt-out":
                # answer = ""
                answer = "Opt-out"
            elif message_code.lower() == "cancel":
                answer = "Cancel"
            else:
                date_time_condition = ""
                if message_code == "Scheduled":
                    scheduled_time = sale_script_get_scheduled_time(openai_client, history)
                    if scheduled_time is not None:
                        date_time_condition = get_date_time_condition(history[-1]["timestamp"], scheduled_time)
                        if date_time_condition != "":
                            scheduled_time = None
                answer = sale_script_reply_message(retriever, openai_client, history, date_time_condition)

                if scheduled_time is not None:
                    answer = scheduled_time

        # return {
        #     "answer": answer,
        #     "message_code": message_code,
        #     "scheduled_time": scheduled_time
        # }
        return answer
    except Exception as err:
        print(traceback.format_exc())
        return f"Error happens while generating response: {err}", 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)