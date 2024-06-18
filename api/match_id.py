import requests
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from config.config import GET_MATCH_IDS_BY_PUUID_URL, API_KEY

class MatchID:
    def __init__(self, puuid):
        self.puuid = puuid 
        self.match_ids = set()  # Use a set to avoid duplicate match IDs

    def get_match_ids(self, start=0, count=20):
        # Adjusted to handle pagination and rate limits
        params = {
            'start': start,
            'count': count,
            'api_key': API_KEY
        }
        full_url = f"{GET_MATCH_IDS_BY_PUUID_URL}/{self.puuid}/ids"
        response = requests.get(full_url, params=params)

        if response.status_code == 200:
            match_ids = response.json()
            self.match_ids.update(match_ids)  # Add new match IDs to the set
            return match_ids
        else:
            print(f"Error: {response.status_code}")
            return []
        
    def fetch_first_20_match_ids(self):
        # Fetch only the first 100 match IDs
        start = 0
        count = 20
        
        self.get_match_ids(start=start, count=count)
        return list(self.match_ids)[:20]  # Return up to 20 match IDs

