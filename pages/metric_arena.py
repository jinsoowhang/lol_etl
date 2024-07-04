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

non_metric_cols = ['summoner_name', 'player_index', 'match_id', 'game_mode', 'game_date', 'ability_uses', 'champion_name']
list_of_metric_cols = [col for col in df.columns if col not in non_metric_cols]

# Change Column Name to be clean to users
list_of_metrics_clean_col_name = [col.replace('_', ' ').title() for col in list_of_metric_cols]

with st.sidebar:

    st.markdown("# 🛠️ Filters")
    chosen_metric = st.radio("Metrics", options=list_of_metrics_clean_col_name, index=1)

# Change Column Name back to data compatible
chosen_metric = chosen_metric.replace(' ', '_').lower()

########################
####### Metrics ########
########################

# Rank for each Summoner
rank_by_metric = df.groupby(['summoner_name'], as_index=False)[chosen_metric].mean().sort_values(by=chosen_metric, ascending=False)

# Title
column_name = rank_by_metric.columns[1] 
column_name = column_name.replace('_', ' ').lower()

st.markdown(f"# Who is the BEST in {column_name}?")

# Rank
col1, col2, col3 = st.columns(3)

# Column Name

with col1:
    for summoner in df['summoner_name'].unique():
        if rank_by_metric.iloc[0,0] == summoner:
            st.write(f'👑{summoner} is #1')
            st.write(f'Average of {round(rank_by_metric.iloc[0,1], 1)} {column_name}')
            st.image(f'{image_folder_path}/{summoner}.jpg')

with col2:
    for summoner in df['summoner_name'].unique():
        if rank_by_metric.iloc[1,0] == summoner:
            st.write(f'😒{summoner} is #2')
            st.write(f'Average of {round(rank_by_metric.iloc[1,1], 1)} {column_name}')
            st.image(f'{image_folder_path}/{summoner}.jpg')

with col3:
    for summoner in df['summoner_name'].unique():
        if rank_by_metric.iloc[2,0] == summoner:
            st.write(f'💩{summoner} is #3')
            st.write(f'Average of {round(rank_by_metric.iloc[2,1], 1)} {column_name}')
            st.image(f'{image_folder_path}/{summoner}.jpg',)