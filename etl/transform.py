import pandas as pd
import os 
import sys

# Directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(script_dir))

from config.config import GAME_NAME_TANKTOP

class DataTransformer():
    def __init__(self, parquet_file_name='raw_match_details.parquet', data_folder_name='data'):
        # Path to the data folder
        self.data_folder_path = os.path.join(script_dir, data_folder_name)
        self.parquet_file_path = os.path.join(self.data_folder_path, parquet_file_name)

    def load_parquet(self):
        try:
            raw_match_details_df = pd.read_parquet(self.parquet_file_path)
            print(f"Data loaded from {self.parquet_file_path}")
            return raw_match_details_df
        except Exception as e:
            print(f"Error loading Parquet file: {e}")
            return None
        
    def transform_data(self, df):
        # Initialize a list to store the indices
        indices = []

        # Loop through each row in the DataFrame
        for i, row in df.iterrows():
            participants = row['metadata']['participants']
            puuid = row['puuid']
            
            # Find the index of the matching participant
            index = next((index for index, participant in enumerate(participants) if participant == puuid), None)
            
            # Append the index to the list
            indices.append(index)

        # Add the indices as a new column in the DataFrame
        df['player_index'] = indices

        # Print the DataFrame to check the result
        print("Data transformation complete.")
        return df
        
if __name__ == "__main__":
    transformer = DataTransformer()
    raw_match_details_df = transformer.load_parquet()

    if raw_match_details_df is not None:
        transformed_df = transformer.transform_data(raw_match_details_df)
        print(transformed_df)
    else:
        print("Failed to load the raw match details.")