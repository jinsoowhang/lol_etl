import requests
import sys 
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from config.config import GET_RIOT_ID_BASE_URL, API_KEY

class Summoner:
    def __init__(self, name, tag):
        
        self.name = name 
        self.tag = tag

    def get_puuid(self):
        # Construct the full URL
        full_url = f"{GET_RIOT_ID_BASE_URL}/{self.name}/{self.tag}?api_key={API_KEY}"

        # Make the request
        response = requests.get(full_url)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()['puuid']
        else:
            print(f"Error: {response.status_code}")
            return None