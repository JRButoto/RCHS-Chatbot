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
                    {"role": "system", "content": "Assist parents, mainly mothers, with nutritional advice for themselves and their children under 5 years. Keep responses short, concise and quota-saving. Respond only in Swahili."},
                    {"role": "user", "content": user_message}
                ]
            )


            openai_reply = response.choices[0].message.content

            # Use dispatcher to send the message back to the user
            dispatcher.utter_message(text=openai_reply)

        except Exception as e:
            print(f"Error: {e}")
            dispatcher.utter_message(text="Samahani, kuna tatizo na mfumo wetu. Tafadhali jaribu tena baadaye.")

        return []



