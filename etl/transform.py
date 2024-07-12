import pandas as pd
import os 
import sys
from datetime import datetime

# Directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Add the project root directory to the Python path
project_root = os.path.join(SCRIPT_DIR, '..')
sys.path.append(project_root)

from api.custom_logging.custom_logger import CustomLogger

class DataTransformer():
    def __init__(self, game_name, data_folder_name='data'):
        self.log = CustomLogger('DataTransformLogger').get_logger()
        self.game_name = game_name
        # Path to the data folder
        self.data_folder_path = os.path.join(SCRIPT_DIR, data_folder_name)
        self.transformed_parquet_file_name = 'transformed_match_details.parquet'
        self.transformed_parquet_file_path = os.path.join(self.data_folder_path, self.transformed_parquet_file_name)
        self.parquet_file_name = f'raw_match_details_{self.game_name}.parquet'
        self.parquet_file_path = os.path.join(self.data_folder_path, self.parquet_file_name)

    def load_parquet(self):
        try:
            raw_match_details_df = pd.read_parquet(self.parquet_file_path)
            self.log.info(f"\nRaw data loaded from {self.parquet_file_name} in 'etl/data' folder\n")
            return raw_match_details_df
        except Exception as e:
            self.log.error(f"Error loading Parquet file: {e}")
            return None
        
    def transform_data(self, df):
        if df['info'].apply(lambda x: x['gameMode'] in ["URF", "NEXUSBLITZ"]).any():
            self.log.info("Skipping transformation for game modes 'URF' and 'NEXUSBLITZ'")
            return df  # 

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

        # Choose column names in "Info" and identify player's data using "player_index"
        transformed_df = df.copy()

        # Extract player_data for each row
        transformed_df['player_data'] = transformed_df.apply(lambda x: x['info']['participants'][x['player_index']], axis=1)
        
        # Add existing columns from League of Legends API
        transformed_df['match_id'] = transformed_df.apply(lambda x: x['metadata']['matchId'], axis=1)
        transformed_df['game_mode'] = transformed_df.apply(lambda x: x['info']['gameMode'], axis=1)
        transformed_df['game_date'] = transformed_df.apply(lambda x: datetime.fromtimestamp(x['info']['gameCreation']/1000), axis=1)
        transformed_df['assists'] = transformed_df['player_data'].apply(lambda x: x['assists'])
        transformed_df['ability_uses'] = transformed_df['player_data'].apply(lambda x: x['challenges']['abilityUses'])
        transformed_df['damage_per_minute'] = transformed_df['player_data'].apply(lambda x: x['challenges']['damagePerMinute'])
        transformed_df['damage_taken_on_team_percentage'] = transformed_df['player_data'].apply(lambda x: x['challenges']['damageTakenOnTeamPercentage'])
        transformed_df['effective_healing_and_shielding'] = transformed_df['player_data'].apply(lambda x: x['challenges']['effectiveHealAndShielding'])
        transformed_df['game_length'] = transformed_df['player_data'].apply(lambda x: x['challenges']['gameLength'])
        transformed_df['gold_per_minute'] = transformed_df['player_data'].apply(lambda x: x['challenges']['goldPerMinute'])
        transformed_df['kda'] = transformed_df['player_data'].apply(lambda x: x['challenges']['kda'])
        transformed_df['kill_participation'] = transformed_df['player_data'].apply(lambda x: x['challenges']['killParticipation'])
        transformed_df['killing_spree'] = transformed_df['player_data'].apply(lambda x: x['challenges']['killingSprees'])
        transformed_df['team_damage_percentage'] = transformed_df['player_data'].apply(lambda x: x['challenges']['teamDamagePercentage'])
        transformed_df['champion_name'] = transformed_df['player_data'].apply(lambda x: x['championName'])
        transformed_df['deaths'] = transformed_df['player_data'].apply(lambda x: x['deaths'])
        transformed_df['gold_earned'] = transformed_df['player_data'].apply(lambda x: x['goldEarned'])
        transformed_df['gold_spent'] = transformed_df['player_data'].apply(lambda x: x['goldSpent'])
        transformed_df['kills'] = transformed_df['player_data'].apply(lambda x: x['kills'])
        transformed_df['time_played'] = transformed_df['player_data'].apply(lambda x: x['timePlayed'])
        transformed_df['total_damage_dealt'] = transformed_df['player_data'].apply(lambda x: x['totalDamageDealt'])
        transformed_df['total_damage_taken'] = transformed_df['player_data'].apply(lambda x: x['totalDamageTaken'])
        transformed_df['win'] = transformed_df['player_data'].apply(lambda x: x['win'])

        # Save the transformed DataFrame to a Parquet file
        save_transformed_df = transformed_df.copy()
        save_transformed_df = save_transformed_df.drop(columns=['puuid', 'metadata', 'info', 'player_data'])

        try:
            # Load existing transformed data
            if os.path.exists(self.transformed_parquet_file_path):
                existing_df = pd.read_parquet(self.transformed_parquet_file_path)
                save_transformed_df = pd.concat([existing_df, save_transformed_df]).drop_duplicates().reset_index(drop=True)
            
            save_transformed_df.to_parquet(self.transformed_parquet_file_path, index=False)
            self.log.info(f"\nTransformed data saved to {self.transformed_parquet_file_name} in 'etl/data' folder\n")
        except Exception as e:
            self.log.error(f"\nError saving transformed data: {e}")

        return save_transformed_df