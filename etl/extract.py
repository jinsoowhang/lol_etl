import requests
import sys 
import os
import pandas as pd

# Directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Add the project root directory to the Python path
project_root = os.path.join(SCRIPT_DIR, '..')
sys.path.append(project_root)

from api.custom_logging.custom_logger import CustomLogger as logger
from api.summoners import Summoner
from api.match_id import MatchID
from api.match import Match

class Extract:
    def __init__(self, game_name, tag_line):
        self.log = logger('ExtractLogger').get_logger()
        self.game_name = game_name
        self.tag_line = tag_line 
    
    def extract_data(self):
        # Step 1: Get PUUID
        summoner = Summoner(self.game_name, self.tag_line)
        puuid = summoner.get_puuid()
        self.log.info(f"Got PUUID {puuid} for summoner {self.game_name}")
        
        # Step 2: Get match IDs
        match_id_fetcher = MatchID(puuid)
        match_ids = match_id_fetcher.get_match_ids()
        self.log.info(f"Fetched {len(match_ids)} match IDs for summoner {self.game_name}")

        # Step 3: Get match details and include PUUID
        print(f'\nExtracting data for {self.game_name}')
        match_details_list = []
        for match_id in match_ids:
            match_fetcher = Match(match_id)
            match_details = match_fetcher.get_match_details()
            if match_details:
                match_details['puuid'] = puuid  # Add PUUID to match details
                match_details['summoner_name'] = self.game_name

                 # Remove 'missions' from each participant
                for participant in match_details['info']['participants']:
                    participant.pop('missions', None)

                match_details_list.append(match_details)
                self.log.info(f"Fetched details for match_id {match_id} for summoner {self.game_name}")
            else:
                self.log.error(f"Failed to fetch details for match_id {match_id} for summoner {self.game_name}")

        return puuid, match_details_list
    
