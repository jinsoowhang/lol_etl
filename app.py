import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

parquet_file_path = 'etl/data/transformed_match_details.parquet'
df = pd.read_parquet(parquet_file_path)

st.title("""This is Unchained Visualization""")

st.divider()

st.markdown(f"## Who's the real carry?")
select_name = st.multiselect("Select names", df['summoner_name'].unique().tolist(), key='names')

if select_name:
    filtered_df = df[df['summoner_name'].isin(select_name)]
    st.bar_chart(filtered_df, x='game_date', y='total_damage_dealt', color='summoner_name')


st.divider()

st.markdown(f"### Raw data table")

st.dataframe(df)