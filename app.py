import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt

parquet_file_path = 'etl/data/transformed_match_details.parquet'
df = pd.read_parquet(parquet_file_path)
df = df.drop(columns='puuid')

st.title("""Unchained Metrics""")

st.divider()

##########################################
########### Show full dataset ############
##########################################

with st.expander("See full data table"):
    st.write(df)

st.divider()

############################################
####### Wins over the past 20 games ########
############################################
test_df = df.copy()
test_df = test_df.sort_values(by=['summoner_name', 'game_date'])
test_df['row_id'] = test_df.groupby('summoner_name').cumcount() + 1 
test_df['row_id'] = test_df['row_id'].astype(str)
test_df['cumsum_wins'] = df.sort_values(by=['game_date']).groupby('summoner_name')['win'].cumsum()
tanktopmastr_df = test_df[test_df['summoner_name'] == 'TanktopMastr']
velbri_df = test_df[test_df['summoner_name'] == 'Velbri']
camachbro_df = test_df[test_df['summoner_name'] == 'Camachbro']

st.markdown('## Wins over the past 20 games')

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