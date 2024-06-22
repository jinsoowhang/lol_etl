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
test_df['cumsum_wins'] = df.sort_values(by=['game_date']).groupby('summoner_name')['win'].cumsum()

st.markdown('## Wins over the past 20 games')

# test_df[test_df['summoner_name'] == 'TanktopMastr'].plot(kind='line', grid=True, color='blue')

# plt.show()