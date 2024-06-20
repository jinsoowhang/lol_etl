import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

parquet_file_path = 'etl/data/transformed_match_details.parquet'
df = pd.read_parquet(parquet_file_path)

st.title("""This is Unchained Visualization""")

st.divider()

st.markdown(f"## Who's the real carry?")
st.bar_chart(df, x='puuid', y='total_damage_dealt')

st.divider()

st.markdown(f"### Raw data table")

st.dataframe(df)