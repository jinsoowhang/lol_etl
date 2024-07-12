import requests
import os
import sys
import time
from .custom_logging.custom_logger import CustomLogger as logger

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from config.config import GET_MATCH_IDS_BY_PUUID_URL, API_KEY

class MatchID:
    def __init__(self, puuid):
        self.puuid = puuid 
        self.match_ids = set()  # Use a set to avoid duplicate match IDs
        self.log = logger('MatchIDLogger').get_logger()

    def get_match_ids(self, start=40, count=20):
        # Adjusted to handle pagination and rate limits
        full_url = f"{GET_MATCH_IDS_BY_PUUID_URL}/{self.puuid}/ids?start={start}&count={count}"
        self.log.info(f"Fetching match IDs from {full_url}")

        headers = {
            "X-Riot-Token": API_KEY
        }

        response = requests.get(full_url, headers=headers)

        if response.status_code == 200:
            match_ids = response.json()
            self.match_ids.update(match_ids)  # Add new match IDs to the set
            self.log.info(f"Fetched {len(match_ids)} match IDs")
            return match_ids
        else:
            self.log.error(f"Error: {response.status_code} - {response.text}")
            return []