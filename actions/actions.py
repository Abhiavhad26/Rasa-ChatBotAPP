from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import datetime

class ActionGetWeather(Action):

    def name(self):
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):

        # Get the city name from the latest user message
        city = tracker.latest_message.get('text')

        # Your OpenWeatherMap API key
        api_key = "eb31cdc87dd50c8492ac205f9fffad51"

        # Build URL
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            humidity = data['main']['humidity']
            time_now = datetime.datetime.now().strftime("%A, %d %B %Y, %I:%M %p")

            reply = (
                f"📅 {time_now}\n"
                f"🌆 Weather in {city.title()}:\n"
                f"🌡️ Temperature: {temp}°C\n"
                f"☁️ Condition: {desc}\n"
                f"💧 Humidity: {humidity}%"
            )
        else:
            reply = "Sorry, I couldn’t fetch the weather. Please check the city name."

        dispatcher.utter_message(text=reply)
        return []
