import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt

# Parquet File Path
parquet_file_path = 'etl/data/transformed_match_details.parquet'
df = pd.read_parquet(parquet_file_path)

# Image Folder Path
image_folder_path = 'assets/images'

# Variables
test_df = df.copy()
test_df = test_df.sort_values(by=['summoner_name', 'game_date'], ascending=[True, True])

# Row ID
test_df = test_df.groupby('summoner_name').tail(20).sort_values(by=['summoner_name', 'game_date'])
test_df['row_id'] = test_df.groupby('summoner_name').cumcount() + 1
test_df['row_id'] = test_df['row_id'].astype(str)

# Cumulative Wins
test_df['cumsum_wins'] = test_df.groupby('summoner_name')['win'].cumsum()

# Convert Time Played to Minutes and Calculate Cumulative Time Played
test_df['time_played'] = test_df['time_played'] / 3600
test_df['cumsum_time_played'] = test_df.groupby('summoner_name')['time_played'].cumsum()
test_df = test_df.sort_values(by=['summoner_name', 'game_date'], ascending=[True, False])

# Filter by Summoner's games
tanktopmastr_df = test_df[test_df['summoner_name'] == 'TanktopMastr']
velbri_df = test_df[test_df['summoner_name'] == 'Velbri']
camachbro_df = test_df[test_df['summoner_name'] == 'Camachbro']
kingvei_df = test_df[test_df['summoner_name'] == 'Kingvei']

############################################
####### Wins over the past 20 games ########
############################################

st.markdown('## 🏆Wins over the past 20 games')

st.write("") # Spacing
st.write("") # Spacing

# Rank for each Summoner
rank_cumsum_wins = test_df.groupby(['summoner_name'], as_index=False)['cumsum_wins'].max().sort_values(by='cumsum_wins', ascending=False)

# Rank
col1, col2, col3, col4 = st.columns(4)

# Column Name
cols = [col1, col2, col3, col4]
icons = ['👑', '😒', '👎', '💩']
summoner_ranks = len(rank_cumsum_wins)

for i, col in enumerate(cols):
    with col:
        if i < summoner_ranks:
            summoner = rank_cumsum_wins.iloc[i, 0]
            st.write(f'{icons[i]}{summoner} is #{i + 1}')
            st.image(f'{image_folder_path}/{summoner}.jpg')
        
# Accumulative sum line plot

fig, ax = plt.subplots()
ax.plot(tanktopmastr_df['row_id'], tanktopmastr_df['cumsum_wins'], marker='o', label='TanktopMastr')
ax.plot(velbri_df['row_id'], velbri_df['cumsum_wins'], marker='x', label='Velbri')
ax.plot(camachbro_df['row_id'], camachbro_df['cumsum_wins'], marker='s', label='Camachbro')
ax.plot(kingvei_df['row_id'], kingvei_df['cumsum_wins'], marker='s', label='Kingvei')

# Reverse the x-axis
ax.invert_xaxis()

# Set plot labels and title
ax.set_xlabel('Game Number')
ax.set_ylabel('Cumulative Wins')
ax.set_title('Cumulative Wins Over Time')
plt.xticks(rotation=45)
plt.tight_layout()

# Add legend
ax.legend()

# Render the plot with Streamlit
st.pyplot(fig)

st.divider()

##########################################################
########### Most Time Played in Past 20 Games ############
##########################################################

st.markdown('## ⏳Most Time Played over the past 20 games')

st.write("") # Spacing
st.write("") # Spacing

# Rank for each Summoner
rank_cumsum_time_played = test_df.groupby(['summoner_name'], as_index=False)['cumsum_time_played'].max().sort_values(by='cumsum_time_played', ascending=False)

# Rank
col1, col2, col3, col4 = st.columns(4)

# Column Name
cols = [col1, col2, col3, col4]
icons = ['👑', '😒', '👎', '💩']
summoner_ranks = len(rank_cumsum_time_played)

for i, col in enumerate(cols):
    with col:
        if i < summoner_ranks:
            summoner = rank_cumsum_time_played.iloc[i, 0]
            st.write(f'{icons[i]}{summoner} is #{i + 1}')
            st.image(f'{image_folder_path}/{summoner}.jpg')

# Accumulative sum line plot

fig, ax = plt.subplots()
ax.plot(tanktopmastr_df['row_id'], tanktopmastr_df['cumsum_time_played'], marker='o', label='TanktopMastr')
ax.plot(velbri_df['row_id'], velbri_df['cumsum_time_played'], marker='x', label='Velbri')
ax.plot(camachbro_df['row_id'], camachbro_df['cumsum_time_played'], marker='s', label='Camachbro')
ax.plot(kingvei_df['row_id'], kingvei_df['cumsum_time_played'], marker='s', label='Kingvei')

# Reverse the x-axis
ax.invert_xaxis()

# Set plot labels and title
ax.set_xlabel('Game Number')
ax.set_ylabel('Cumulative Time Played (hrs)')
ax.set_title('Cumulative Time Played Over Time')
plt.xticks(rotation=45)
plt.tight_layout()

# Add legend
ax.legend()

# Render the plot with Streamlit
st.pyplot(fig)

st.divider()


##########################################
########### Show full dataset ############
##########################################

with st.expander("See full data table"):
    st.write(df)