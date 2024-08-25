# import os
from constants import GEMINI_API,clientID,clientSecret,context
from llama_index.llms.gemini import Gemini
from llama_index.core import Settings

from llama_index.core.agent import ReActAgent
from llama_index.core.agent import FnAgentWorker
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core.memory import ChatMemoryBuffer
from typing import Optional
from llama_index.core.tools import BaseTool, FunctionTool
import webbrowser
import os
import datetime
import requests
from bs4 import BeautifulSoup
import json
import spotipy

def today_weather(city: str = "jaipur"):
    """Return weather update of the city; default is Jaipur."""
    url = "https://www.google.com/search?q=" + "weather+" + city
    try:
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')

        # Temperature extraction
        temp_fahrenheit = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'})
        if temp_fahrenheit:
            temp_fahrenheit = float(temp_fahrenheit.text.split('°')[0].replace(',', ''))
            temp_celsius = (temp_fahrenheit - 32) * 5 / 9
        else:
            return "Temperature data not found."

        # Weather description extraction
        str_weather = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'})
        if str_weather:
            data = str_weather.text.split('\n')
            time = data[0]
            sky = data[1]
        else:
            return "Weather description not found."

        # Other information extraction
        listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
        if len(listdiv) > 5:
            strd = listdiv[5].text
            pos = strd.find('Wind')
            other_data = strd[pos:]
        else:
            return "Additional weather data not found."

        return (f"Temperature in Celsius is: {round(temp_fahrenheit, 2)}. At time: {time}. "
                f"Sky Description: {sky}. Other information: {other_data}")

    except Exception as e:
        return f"An error occurred: {e}"
def open_spotify(clientID=clientID,clientSeceret=clientSecret,song_name:str=None):
    """It seraches the song on the database and play the songs."""
    username = 'ashish'
    # clientID = clientID
    # clientSecret = clientSeceret
    # redirect_uri = 'https://open.spotify.com'
    # oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri) 
    # token_dict = oauth_object.get_access_token() 
    # token = token_dict['access_token'] 
    # spotifyObject = spotipy.Spotify(auth=token) 
    # user_name = spotifyObject.current_user() 
    # # To print the response in readable format. 
    # print(json.dumps(user_name, sort_keys=True, indent=4))
    # results = spotifyObject.search(song_name, 1, 0, "track") 
    # songs_dict = results['tracks'] 
    # song_items = songs_dict['items'] 
    # song = song_items[0]['external_urls']['spotify'] 
    # print('Song has opened in your browser.') 
    # webbrowser.open(song) 
    print("the song will be played")

def control_lights(room: str, state: str) -> None:
    """
    Controls the lights in a specified room.

    :param room: The room where the lights should be controlled.
    :param state: Desired state of the lights ('on' or 'off').
    """
    if state.lower() not in ['on', 'off']:
        raise ValueError("State must be 'on' or 'off'.")
    # Here, you would integrate with your smart home API to control the lights.
    print(f"Turning {state} lights in {room}.")

def adjust_thermostat(temperature: Optional[int] = None, mode: Optional[str] = None) -> None:
    """
    Adjusts the thermostat settings.

    :param temperature: Desired temperature to set (in Celsius or Fahrenheit).
    :param mode: Desired mode of the thermostat ('heat', 'cool', 'auto').
    """
    if temperature is not None and (temperature < 10 or temperature > 30):
        raise ValueError("Temperature should be between 10 and 30 degrees Celsius.")
    if mode and mode not in ['heat', 'cool', 'auto']:
        raise ValueError("Mode should be 'heat', 'cool', or 'auto'.")
    # Here, you would integrate with your smart home API to adjust the thermostat.
    print(f"Setting thermostat to {temperature}°C and mode to {mode}.")

def activate_security_system(status: str) -> None:
    """
    Activates or deactivates the security system.

    :param status: Desired status of the security system ('activate' or 'deactivate').
    """
    if status.lower() not in ['activate', 'deactivate']:
        raise ValueError("Status must be 'activate' or 'deactivate'.")
    # Here, you would integrate with your smart home API to control the security system.
    print(f"Security system {status}d.")

def lock_doors(status: str) -> None:
    """
    Locks or unlocks the doors.

    :param status: Desired status of the doors ('lock' or 'unlock').
    """
    if status.lower() not in ['lock', 'unlock']:
        raise ValueError("Status must be 'lock' or 'unlock'.")
    # Here, you would integrate with your smart home API to control the doors.
    print(f"Doors {status}ed.")


weather_tool = FunctionTool.from_defaults(fn=today_weather)
open_spotify_tool= FunctionTool.from_defaults(fn=open_spotify)
control_lights_tool=FunctionTool.from_defaults(fn=control_lights)
thermostat_tool=FunctionTool.from_defaults(fn=adjust_thermostat)
security_tool=FunctionTool.from_defaults(fn=activate_security_system)
lock_door_tool=FunctionTool.from_defaults(fn=lock_doors)


llm = Gemini(api_key=GEMINI_API)

class myqueryEngine(CustomQueryEngine):
    """RAG String Query Engine."""
    
    llm: Gemini
    prompt: str = None

    def custom_query(self, query: str):
        """Give query response to my answer"""
        # if self.prompt is None:
        #     raise ValueError("Prompt cannot be None")

        question = (
            "You are an exceptional Python developer who creates outstanding applications according to the user requirements.\n"
            "Always remember to enclose code within triple backticks ```{code}``` for clarity.\n"
            "List dependencies or packages using $$${packages}$$$ to make them easily identifiable.\n"
            "Please be consistent with this format.\n\n"
            "Question : "
        )

        
        response = self.llm.complete(question+query)
        
        return str(response)

# queryEngine=myqueryEngine(llm=llm)
list_of_tools=[
    weather_tool,
    open_spotify_tool,
    control_lights_tool,
    thermostat_tool,
    security_tool,
    lock_door_tool,
]

memory= ChatMemoryBuffer.from_defaults(llm=llm)

reactAgent=ReActAgent.from_tools(tools=list_of_tools,llm=llm,memory=memory,context=context,verbose=True)

if __name__=="__main__":
    # print(queryEngine.query("write me the code for nosql database changes"))
    # print(llm.complete("who is the father of the universe"))
    print(str(reactAgent.chat("please switch of lights of hall")))