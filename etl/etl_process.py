# etl/etl_process.py

import sys 
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from etl.extract import Extract
# from etl.transform import Transform
# from etl.load import Load

class ETLProcess:
    def __init__(self, game_name, tag_line):
        self.game_name = game_name
        self.tag_line = tag_line

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
            file_path = "raw_match_details.parquet"
            extractor.save_to_parquet(match_details_list, file_path)
            print(f"Data saved to {file_path} in 'etl/data' folder")
        else:
            print("Failed to extract data")

        # # Step 2: Transform data
        # transformer = Transform()
        # transformed_data = transformer.transform_data(match_details_list)

        # # Step 3: Load data
        # loader = Load()
        # loader.load_data(transformed_data)
