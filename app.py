import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

parquet_file_path = 'etl/data/transformed_match_details.parquet'
df = pd.read_parquet(parquet_file_path)

st.write("""
# This is Unchained Visualization
         """)

st.header(f"This is the total damage taken {df['total_damage_taken'].head(1).values}!")

