import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import base64
from PIL import Image

# Parquet File Path
parquet_file_path = 'etl/data/transformed_match_details.parquet'
df = pd.read_parquet(parquet_file_path)

# Image Folder Path
image_folder_path = 'etl/images'

# UDF
def resize_images(image_path, width, height):
    img = Image.open(image_path)
    image = base64.b64encode(img).decode("utf-8")
    resized_image = image.resize((width, height))
    return resized_image

# Variables
test_df = df.copy()
test_df = test_df.sort_values(by=['summoner_name', 'game_date'], ascending=[True, False])

# Row ID
test_df['row_id'] = test_df.groupby('summoner_name').cumcount() + 1 
test_df = test_df[test_df['row_id'] <= 20]
test_df['row_id'] = test_df['row_id'].astype(str)

# Cumulative Wins
test_df['cumsum_wins'] = df.sort_values(by=['game_date'], ascending=False).groupby('summoner_name')['win'].cumsum()

# Convert Time Played to Minutes and Calculate Cumulative Time Played
test_df['time_played'] = test_df['time_played'] / 3600
test_df = test_df.sort_values(by=['summoner_name', 'game_date'], ascending=[True, False])
test_df['cumsum_time_played'] = test_df.groupby('summoner_name')['time_played'].cumsum()

# Filter by Summoner's games
tanktopmastr_df = test_df[test_df['summoner_name'] == 'TanktopMastr']
velbri_df = test_df[test_df['summoner_name'] == 'Velbri']
camachbro_df = test_df[test_df['summoner_name'] == 'Camachbro']

# Title
st.title("""⛓️‍💥Unchained Metrics""")
st.text(f"Updated as of {df['game_date'].max().strftime('%Y-%m-%d')}")

st.divider()


############################################
####### Wins over the past 20 games ########
############################################

st.markdown('## 🏆Wins over the past 20 games')

st.write("") # Spacing
st.write("") # Spacing

# Rank for each Summoner
rank_cumsum_wins = test_df.groupby(['summoner_name'], as_index=False)['cumsum_wins'].max().sort_values(by='cumsum_wins', ascending=False)


# Rank
col1, col2, col3 = st.columns(3)

with col1:
    for summoner in test_df['summoner_name'].unique():
        if rank_cumsum_wins.iloc[0,0] == summoner:
            st.write(f'👑{summoner} is #1')
            st.image(f'{image_folder_path}/{summoner}.jpg')

with col2:
    for summoner in test_df['summoner_name'].unique():
        if rank_cumsum_wins.iloc[1,0] == summoner:
            st.write(f'😒{summoner} is #2')
            st.image(f'{image_folder_path}/{summoner}.jpg')

with col3:
    for summoner in test_df['summoner_name'].unique():
        if rank_cumsum_wins.iloc[2,0] == summoner:
            st.write(f'💩{summoner} is #3')
            st.image(f'{image_folder_path}/{summoner}.jpg',)
        
# Accumulative sum line plot

fig, ax = plt.subplots()
ax.plot(tanktopmastr_df['row_id'], tanktopmastr_df['cumsum_wins'], marker='o', label='TanktopMastr')
ax.plot(velbri_df['row_id'], velbri_df['cumsum_wins'], marker='x', label='Velbri')
ax.plot(camachbro_df['row_id'], camachbro_df['cumsum_wins'], marker='s', label='Camachbro')

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
col1, col2, col3 = st.columns(3)

with col1:
    for summoner in test_df['summoner_name'].unique():
        if rank_cumsum_time_played.iloc[0,0] == summoner:
            st.write(f'😫{summoner} is #1')
            st.image(f'{image_folder_path}/{summoner}.jpg')

with col2:
    for summoner in test_df['summoner_name'].unique():
        if rank_cumsum_time_played.iloc[1,0] == summoner:
            st.write(f'😒{summoner} is #2')
            st.image(f'{image_folder_path}/{summoner}.jpg')

with col3:
    for summoner in test_df['summoner_name'].unique():
        if rank_cumsum_time_played.iloc[2,0] == summoner:
            st.write(f'🥱{summoner} is #3')
            st.image(f'{image_folder_path}/{summoner}.jpg',)

# Accumulative sum line plot

fig, ax = plt.subplots()
ax.plot(tanktopmastr_df['row_id'], tanktopmastr_df['cumsum_time_played'], marker='o', label='TanktopMastr')
ax.plot(velbri_df['row_id'], velbri_df['cumsum_time_played'], marker='x', label='Velbri')
ax.plot(camachbro_df['row_id'], camachbro_df['cumsum_time_played'], marker='s', label='Camachbro')

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
