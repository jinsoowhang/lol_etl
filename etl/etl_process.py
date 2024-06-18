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
    def __init__(self, game_name, tag_line):
        self.game_name = game_name
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

    def run(self):
        # Step 1: Extract data
        extractor = Extract(self.game_name, self.tag_line)
        puuid, match_details_list = extractor.extract_data()

        if not puuid:
            print("Failed to get PUUID")
            return
        if not match_details_list:
            print("No match details found")
            return

        # Save raw data to Parquet file
        if puuid and match_details_list:
            extracted_file_path = "raw_match_details.parquet"
            self.save_to_parquet(match_details_list, extracted_file_path)
            print(f"Data saved to {extracted_file_path} in 'etl/data' folder")
        else:
            print("Failed to extract data")

        # Step 2: Transform data
        transformer = DataTransformer()
        raw_match_details_df = transformer.load_parquet()

        if raw_match_details_df is not None:
            transformed_file_path = "transformed_match_details.parquet"
            transformed_df = transformer.transform_data(raw_match_details_df)
            self.save_to_parquet(transformed_df, transformed_file_path)
            print(f"Data saved to {transformed_file_path} in 'etl/data' folder\n")
        else:
            print("Failed to load the raw match details.")

        # # Step 3: Load data
        # loader = Load()
        # loader.load_data(transformed_data)
