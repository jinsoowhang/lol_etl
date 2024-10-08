# etl/etl_process.py

import sys 
import os
import pandas as pd

# Directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Add the project root directory to the Python path
project_root = os.path.join(SCRIPT_DIR, '..')
sys.path.append(project_root)

from api.custom_logging.custom_logger import CustomLogger as logger
from etl.extract import Extract
from etl.transform import DataTransformer
# from etl.load import Load

class ETLProcess:
    def __init__(self, game_names, tag_line):
        self.log = logger("ETLProcessLogger").get_logger()
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
        print(f"Saved data to {parquet_file_path}")

    def process_game(self, game_name):
        # Step 1: Extract data
        if game_name == 'dexter mexter':
            extractor = Extract(game_name, tag_line='love')
            puuid, match_details_list = extractor.extract_data()
        else: 
            extractor = Extract(game_name, self.tag_line)
            puuid, match_details_list = extractor.extract_data()

        if not puuid:
            self.log.error(f"Failed to get PUUID for {game_name}")
            return
        if not match_details_list:
            self.log.error(f"No match details found for {game_name}")
            return

        # Save raw data to Parquet file
        if puuid and match_details_list:
            extracted_file_path = f"raw_match_details_{game_name}.parquet"
            self.save_to_parquet(match_details_list, extracted_file_path)
            print(f"Raw data saved to {extracted_file_path} in 'etl/data' folder")
        else:
            self.log.error(f"Failed to extract data for {game_name}")

        # Step 2: Transform data
        transformer = DataTransformer(game_name)
        raw_match_details_df = transformer.load_parquet()

        if raw_match_details_df is not None:
            transformed_file_path = f"transformed_match_details_{game_name}.parquet"
            transformed_df = transformer.transform_data(raw_match_details_df)
            print(f"Transformed data saved to {transformed_file_path} in 'etl/data' folder")
        else: 
            self.log.error(f"Failed to load raw data for transformation in {game_name}")
    def run(self):
        for game_name in self.game_names:
            self.process_game(game_name)