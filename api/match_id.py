import requests
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from config.config import GET_MATCH_IDS_BY_PUUID_URL, API_KEY

class MatchID:
    def __init__(self, puuid):
        self.puuid = puuid 

    def get_match_ids(self):
        full_url = f"{GET_MATCH_IDS_BY_PUUID_URL}/{self.puuid}/ids?api_key={API_KEY}"
        response = requests.get(full_url)
        if response.status_code == 200:
            # remove [:2] once we want to get all the matches
            match_ids = response.json()
            return match_ids[:2]
        else:
            print(f"Error: {response.status_code}")
            return None