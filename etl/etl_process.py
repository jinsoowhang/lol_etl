# etl/etl_process.py

import sys 
import os
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from etl.extract import Extract
from etl.transform import DataTransformer
# from etl.load import Load

class ETLProcess:
    def __init__(self, game_names, tag_line):
        self.game_names = game_names
        self.tag_line = tag_line

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

    def process_game(self, game_name):
        # Step 1: Extract data
        extractor = Extract(game_name, self.tag_line)
        puuid, match_details_list = extractor.extract_data()

        if not puuid:
            print(f"Failed to get PUUID for {game_name}")
            return
        if not match_details_list:
            print(f"No match details found for {game_name}")
            return

        # Save raw data to Parquet file
        if puuid and match_details_list:
            extracted_file_path = f"raw_match_details_{game_name}.parquet"
            self.save_to_parquet(match_details_list, extracted_file_path)
            print(f"Raw data saved to {extracted_file_path} in 'etl/data' folder")
        else:
            print(f"Failed to extract data for {game_name}")

        # Step 2: Transform data
        transformer = DataTransformer(game_name)
        raw_match_details_df = transformer.load_parquet()

        if raw_match_details_df is not None:
            transformed_file_path = f"transformed_match_details_{game_name}.parquet"
            transformed_df = transformer.transform_data(raw_match_details_df)

        # # Step 3: Load data
        # loader = Load()
        # loader.load_data(transformed_data)

    def run(self):
        for game_name in self.game_names:
            self.process_game(game_name)