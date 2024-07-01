import requests
import sys 
import os
from .custom_logging.custom_logger import CustomLogger as logger

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from config.config import GET_RIOT_ID_BASE_URL, API_KEY

class Summoner:
    def __init__(self, name, tag):
        self.name = name 
        self.tag = tag
        self.log = logger('SummonerLogger').get_logger()

    def get_puuid(self):
        # Construct the full URL
        full_url = f"{GET_RIOT_ID_BASE_URL}/{self.name}/{self.tag}?api_key={API_KEY}"
        self.log.info(f"Fetching PUUID for {self.name}#{self.tag} from {full_url}")

        # Make the request
        response = requests.get(full_url)

        # Check if the request was successful
        if response.status_code == 200:
            puuid = response.json()['puuid']
            self.log.info(f"Successfully fetched PUUID: {puuid} for {self.name}#{self.tag}")
            return puuid
        else:
            self.log.error(f"Error: {response.status_code} for {self.name}#{self.tag} - {response.text}")
            return None