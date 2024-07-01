import requests
import os
import sys
from .custom_logging.custom_logger import CustomLogger as logger

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from config.config import GET_MATCH_BY_ID_URL, API_KEY

class Match:
    def __init__(self, match_id):
        self.match_id = match_id
        self.log = logger('MatchLogger').get_logger()

    def get_match_details(self):
        full_url = f"{GET_MATCH_BY_ID_URL}/{self.match_id}?api_key={API_KEY}"
        self.log.info(f"Fetching match details from {full_url}")

        response = requests.get(full_url)
        if response.status_code == 200:
            self.log.info(f"Successfully fetched match details for match_id: {self.match_id}")
            return response.json()
        else:
            self.log.error(f"Error: {response.status_code} for match_id: {self.match_id} - {response.text}")
            return None