import requests
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from config.config import GET_MATCH_BY_ID_URL, API_KEY

class Match:
    def __init__(self, match_id):
        self.match_id = match_id

    def get_match_details(self):
        full_url = f"{GET_MATCH_BY_ID_URL}/{self.match_id}?api_key={API_KEY}"
        response = requests.get(full_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} for match_id: {self.match_id}")
            return None