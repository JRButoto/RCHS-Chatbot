
# from flask import Flask, render_template, request, jsonify
# import requests

# app = Flask(__name__)

# RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     user_message = request.json['message']
#     print("User Message:", user_message)
    
#     # Send user message to Rasa and get bot's response
#     response = requests.post(RASA_API_URL, json={'message': user_message, 'sender': 'user'})
#     response_json = response.json()
#     print("Rasa Response:", response_json)
    
#     bot_response = response_json[0]['text'] if response_json else 'Sorry, I didn\'t understand that.'
#     return jsonify({'response': bot_response})

# if __name__ == "__main__":
#     app.run(debug=True, port=3000)




from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    user_message = request.json['message']
    print("User Message:", user_message)
    
    # Send user message to Rasa and get bot's response
    response = requests.post(RASA_API_URL, json={'message': user_message, 'sender': 'user'})
    response_json = response.json()
    print("Rasa Response:", response_json)
    
    # Parse the bot response
    bot_response = response_json[0] if response_json else {'text': 'Sorry, I didn\'t understand that.'}
    return jsonify(bot_response)

if __name__ == "__main__":
    app.run(debug=True, port=3100, host='0.0.0.0')

