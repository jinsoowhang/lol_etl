import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

###########################
####### Title Page ########
###########################

st.markdown("# 🏟️ Metric Arena")
st.markdown("""
Dive into the Metric Arena to see who reigns supreme based on user-selected metrics, offering a view of each contender's strengths and achievements.
""")

########################
####### Backend ########
########################

# Parquet File Path
parquet_file_path = 'etl/data/transformed_match_details.parquet'
df = pd.read_parquet(parquet_file_path)

# Image Folder Path
image_folder_path = 'assets/images'

########################
####### Filters ########
########################

# Game mode filter columns
list_of_game_modes = [col for col in df.game_mode.unique().tolist()]

# Metric filter columns
non_metric_cols = ['summoner_name', 'player_index', 'match_id', 'game_mode', 'game_date', 'ability_uses', 'champion_name']
list_of_metric_cols = [col for col in df.columns if col not in non_metric_cols]

# Change Column Name to be clean to users
list_of_metrics_clean_col_name = [col.replace('_', ' ').title() for col in list_of_metric_cols]

with st.sidebar:

    st.markdown("# 🛠️ Filters")
    chosen_game_mode = st.radio("Game Mode", options=list_of_game_modes, index=1)
    chosen_metric = st.radio("Metrics", options=list_of_metrics_clean_col_name, index=1)

# Change Column Name back to data compatible
chosen_metric = chosen_metric.replace(' ', '_').lower()

########################
####### Metrics ########
########################

# Filter dataframe by the chosen game mode
df = df[df['game_mode'] == chosen_game_mode]

# Rank for each Summoner
rank_by_metric = df.groupby(['summoner_name'], as_index=False)[chosen_metric].mean().sort_values(by=chosen_metric, ascending=False)

# Changing order for descending ordered columns
descending_order_cols = ['game_length', 'deaths', 'time_played']
print(chosen_metric)
if chosen_metric in descending_order_cols:
    rank_by_metric = df.groupby(['summoner_name'], as_index=False)[chosen_metric].mean().sort_values(by=chosen_metric, ascending=True)

# Title
column_name = rank_by_metric.columns[1] 
column_name = column_name.replace('_', ' ').lower()

st.markdown(f"# Who is the BEST in {column_name}?")

# Rank
col1, col2, col3, col4 = st.columns(4)

# Column Name
cols = [col1, col2, col3, col4]
icons = ['👑', '😒', '👎', '💩']
summoner_ranks = len(rank_by_metric)

for i, col in enumerate(cols):
    with col:
        if i < summoner_ranks:
            summoner = rank_by_metric.iloc[i, 0]
            st.write(f'{icons[i]}{summoner} is #{i + 1}')
            st.write(f'Average of {round(rank_by_metric.iloc[i, 1], 1)} {column_name}')
            st.image(f'{image_folder_path}/{summoner}.jpg')