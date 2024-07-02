
from flask import Flask, request, jsonify, Response
import africastalking
import requests
import threading
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

AFRICAS_TALKING_USERNAME = os.getenv("AFRICAS_TALKING_USERNAME", default="")
AFRICAS_TALKING_API_KEY = os.getenv("AFRICAS_TALKING_API_KEY", default="")

# africastalking.initialize(AFRICAS_TALKING_USERNAME, AFRICAS_TALKING_API_KEY)
# sms = africastalking.SMS

RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'

def response_to_sms(phone_number, message):
    
    request.post(
        "https://api.sandbox.africastalking.com/version1/messaging",
        data = {
            "username" : AFRICAS_TALKING_USERNAME,
            "to" : phone_number,
            "message" : message,
            "username" : "25665"
        },

        headers = {
            "apiKey" : AFRICAS_TALKING_API_KEY,
            "Accept" : "application/json",
            "Content-Type" :"application/x-www-from-urlencoded" ,
        }
    )

def handle_message(data):
    # Extract message and sender information
    user_message = data.get('text')
    phone_number = data.get('from')

    # Send the message to the RASA bot
    response = requests.post(RASA_API_URL, json={'sender': phone_number, 'message': user_message})
    response_json = response.json()
    print("Rasa Response:", response_json)

    # Get the bot response
    bot_response = response_json[0]['text'] if response_json else 'Sorry, I didn\'t understand that.'

    if not isinstance(phone_number, str):
        phone_number = str(phone_number)
    if not isinstance(bot_response, str):
        bot_response = str(bot_response)

    # Send the response back to the user via Africa's Talking
    response = response_to_sms(phone_number, bot_response)
    
    if response:
        print(f"API Response: {response}")
    else:
        print("Failed to send SMS")

@app.route('/incoming-messages', methods=['POST'])
def incoming_messages():
    data = request.form.to_dict()
    print(f'Incoming message...\n {data}')

    # Start a new thread to handle the message
    threading.Thread(target=handle_message, args=(data,)).start()

    # Return a response immediately
    return Response(status=200)

if __name__ == "__main__":
    app.run(port=3200, debug=True, host="0.0.0.0")

