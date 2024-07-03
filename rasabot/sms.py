
# from flask import Flask, request, jsonify, Response
# import africastalking
# import requests  # <-- Ensure this import is included
# import threading
# import os
# from dotenv import load_dotenv

# app = Flask(__name__)

# load_dotenv()

# AFRICAS_TALKING_USERNAME = os.getenv("AFRICAS_TALKING_USERNAME", default="")
# AFRICAS_TALKING_API_KEY = os.getenv("AFRICAS_TALKING_API_KEY", default="")

# # africastalking.initialize(AFRICAS_TALKING_USERNAME, AFRICAS_TALKING_API_KEY)
# # sms = africastalking.SMS

# RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'

# def response_to_sms(phone_number, message):
#     # Corrected to use requests.post instead of request.post
#     response = requests.post(
#         "https://api.sandbox.africastalking.com/version1/messaging",
#         data={
#             "username": AFRICAS_TALKING_USERNAME,
#             "to": phone_number,
#             "message": message,
#             "username": "25665"
#         },
#         headers={
#             "apiKey": AFRICAS_TALKING_API_KEY,
#             "Accept": "application/json",
#             "Content-Type": "application/x-www-form-urlencoded",  # Corrected from "application/x-www-from-urlencoded"
#         }
#     )
#     return response  # Ensure to return the response for error checking

# def handle_message(data):
#     # Extract message and sender information
#     user_message = data.get('text')
#     phone_number = data.get('from')

#     # Send the message to the RASA bot
#     response = requests.post(RASA_API_URL, json={'sender': phone_number, 'message': user_message})
#     response_json = response.json()
#     print("Rasa Response:", response_json)

#     # Get the bot response
#     bot_response = response_json[0]['text'] if response_json else 'Sorry, I didn\'t understand that.'

#     if not isinstance(phone_number, str):
#         phone_number = str(phone_number)
#     if not isinstance(bot_response, str):
#         bot_response = str(bot_response)

#     # Send the response back to the user via Africa's Talking
#     response = response_to_sms(phone_number, bot_response)
    
#     if response.ok:  # Check if the response was successful
#         print(f"API Response: {response.json()}")
#     else:
#         print("Failed to send SMS")

# @app.route('/incoming-messages', methods=['POST'])
# def incoming_messages():
#     data = request.form.to_dict()
#     print(f'Incoming message...\n {data}')

#     # Start a new thread to handle the message
#     threading.Thread(target=handle_message, args=(data,)).start()

#     # Return a response immediately
#     return Response(status=200)

# if __name__ == "__main__":
#     app.run(port=3200, debug=True, host="0.0.0.0")


from flask import Flask, request, Response
import africastalking
import requests
import threading
import os
from dotenv import load_dotenv

# Load environmental variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load Africa's Talking credentials from environment variables
AFRICAS_TALKING_USERNAME = os.environ.get("AFRICAS_TALKING_USERNAME")
AFRICAS_TALKING_API_KEY = os.environ.get("AFRICAS_TALKING_API_KEY")
AFRICAS_TALKING_SENDER_ID = os.environ.get("AFRICAS_TALKING_SENDER_ID")


# Initialize Africa's Talking
africastalking.initialize(AFRICAS_TALKING_USERNAME, AFRICAS_TALKING_API_KEY)
# africastalking.initialize('sandbox', 'atsk_b4f4bd7fc9415eaf767fc0179dc9585ba3a183b5e87825e83e2753fea7217ebd1adb66c5')

sms = africastalking.SMS

RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'

def send_sms(phone_number, message):
    try:
        response = sms.send(message, [phone_number],sender_id=AFRICAS_TALKING_SENDER_ID)
        print("SMS Response:", response)
        return response
    except Exception as e:
        print("Error sending SMS:", e)
        return None

def handle_message(data):
    # Extract message and sender information
    user_message = data.get('text')
    phone_number = data.get('from')

    # # Send the message to the RASA bot
    # response = requests.post(RASA_API_URL, json={'sender': phone_number, 'message': user_message})
    # response_json = response.json()
    # print("Rasa Response:", response_json)

    # # Get the bot response
    # bot_response = response_json[0]['text'] if response_json else 'Sorry, I didn\'t understand that.'

    # # Send the response back to the user via Africa's Talking
    # send_sms(phone_number, bot_response)

    response = requests.post(RASA_API_URL, json={'sender': phone_number, 'message': user_message})
    response_json = response.json()
    print("Rasa Response:", response_json)

    # Get the bot response
    if response_json and isinstance(response_json, list) and len(response_json) > 0:
        main_text = response_json[0].get('text', '')
        buttons = response_json[0].get('buttons', [])
        
        # Combine main text with button titles
        button_texts = [button['title'] for button in buttons]
        combined_text = main_text + '\n' + ' or\n'.join(button_texts)
        
        bot_response = combined_text
    else:
        bot_response = 'Sorry, I didn\'t understand that.'

# Send the response back to the user via Africa's Talking
    send_sms(phone_number, bot_response)

@app.route('/incoming-messages', methods=['POST'])
def incoming_messages():
    data = request.form.to_dict()
    # data = request.get_json()
    print(AFRICAS_TALKING_USERNAME)
    
    print(f'Incoming message...\n {data}')

    # Start a new thread to handle the message
    threading.Thread(target=handle_message, args=(data,)).start()

    # Return a response immediately
    return Response(status=200)

if __name__ == "__main__":
    app.run(port=3200, debug=True, host="0.0.0.0")
