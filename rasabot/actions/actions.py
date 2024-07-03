# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
import requests
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
    
        # Get user message from Rasa tracker
        user_message = tracker.latest_message.get('text')
        print(user_message)

        openai.api_key = os.environ.get("OPENAI_API_KEY")

        try:
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Assist parents, mainly mothers, with nutritional advice for themselves and their children under 5 years. Keep responses short, concise and quota-saving. Respond only in simple english."},
                    {"role": "user", "content": user_message}
                ]
            )


            openai_reply = response.choices[0].message.content

            # Use dispatcher to send the message back to the user
            dispatcher.utter_message(text=openai_reply)

        except Exception as e:
            print(f"Error: {e}")
            dispatcher.utter_message(text="Sorry there is an issue with the system. Please try again later.")
# Samahani, kuna tatizo na mfumo wetu. Tafadhali jaribu tena baadaye.
        return []



class ActionHandleRegistrationNumber(Action):

    def name(self) -> Text:
        return "action_handle_registration_number"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        registration_number = tracker.get_slot('registration_number')
        if not registration_number:
            dispatcher.utter_message(text="I couldn't find the registration number in your message.")
            return []

        response = requests.post("http://100.42.178.17:8800/api/get_child_nutrition_recomendations/", json={"registration_number": registration_number})

        if response.status_code == 200:
            message = response.json().get('message', 'No message received.')
            dispatcher.utter_message(text=message)
        else:
            error_message = response.json().get('error', 'Something went wrong while fetching the health status.')
            dispatcher.utter_message(text=error_message)

        return []
    


# actions.py

class ActionHandleRegistrationNumberForVisit(Action):

    def name(self) -> Text:
        return "action_handle_registration_number_for_visit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        registration_number = tracker.get_slot('registration_number')

        if registration_number:
            response = requests.post('http://100.42.178.17:8800/api/get_next_visit/', json={'registration_number': registration_number})

            if response.status_code == 200:
                message = response.json().get('message', 'No message received.')
                dispatcher.utter_message(text=message)
            else:
                error_message = response.json().get('error', 'Something went wrong while fetching the next visit date.')
                dispatcher.utter_message(text=error_message)

        else:
            dispatcher.utter_message(text="I couldn't find the registration number.")

        return []




