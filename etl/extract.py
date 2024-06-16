import requests
import sys 
import os
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from api.summoners import Summoner
from api.match_id import MatchID
from api.match import Match

# Riot ID details
GAME_NAME_TANKTOP = "TanktopMastr"
TAG_LINE_TANKTOP = "NA1"

class Extract:
    def __init__(self, game_name, tag_line):
        self.game_name = game_name
        self.tag_line = tag_line 
    
    def extract_data(self):
        # Step 1: Get PUUID
        summoner = Summoner(self.game_name, self.tag_line)
        puuid = summoner.get_puuid()
        
        # Step 2: Get match IDs
        match_id_fetcher = MatchID(puuid)
        match_ids = match_id_fetcher.get_match_ids()

        # Step 3: Get match details and include PUUID
        match_details_list = []
        for match_id in match_ids:
            match_fetcher = Match(match_id)
            match_details = match_fetcher.get_match_details()
            if match_details:
                match_details['puuid'] = puuid  # Add PUUID to match details
                match_details_list.append(match_details)
            else:
                print(f"Failed to fetch details for match_id: {match_id}")

        return puuid, match_details_list
    
    def save_to_parquet(self, data, file_path):
        # Ensure data folder exists
        data_folder = os.path.join(os.path.dirname(__file__), 'data')
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        # Convert the list of match details to a DataFrame
        df = pd.DataFrame(data)
        # Save the DataFrame to a Parquet file
        parquet_file_path = os.path.join(data_folder, file_path)
        df.to_parquet(parquet_file_path, index=False)