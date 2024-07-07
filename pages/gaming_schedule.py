import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
from datetime import datetime

# Parquet File Path
parquet_file_path = 'etl/data/transformed_match_details.parquet'
df = pd.read_parquet(parquet_file_path)

# Copy new dataframe
gs_df = df.copy()

###########################
####### Title Page ########
###########################

st.title("""⛓️📈Unchained Metrics""")
st.text(f"Updated as of {df['game_date'].max().strftime('%Y-%m-%d')}")

st.divider()

########################
####### Filters ########
########################

with st.sidebar:

    st.markdown("# 🛠️ Filters")
    # chosen_metric = st.radio("Metrics", options=gs_df['summoner_name'].unique(), index=1)
    chosen_metric = st.multiselect(
        "Select the players"
        , gs_df['summoner_name'].unique().tolist()
        , ['TanktopMastr'])

    gs_df['first_month_active'] = pd.to_datetime(gs_df['game_date'])
    start_dt = st.sidebar.date_input('From Date', value=gs_df['first_month_active'].min())

    gs_df['last_month_active'] = pd.to_datetime(gs_df['game_date'])
    end_dt = st.sidebar.date_input('To Date', value=gs_df['last_month_active'].max())

############################
####### Scatterplot ########
############################


gs_df['date'] = gs_df['game_date'].dt.date
gs_df['hour'] = gs_df['game_date'].dt.hour

# Filter data by chosen metric
gs_df = gs_df[gs_df['summoner_name'].isin(chosen_metric)]
gs_df = gs_df[(gs_df['date'] >= start_dt) & (gs_df['date'] <= end_dt)]

# Print Total Games Played
st.markdown(f"#### A total of {len(gs_df)} games were played")

# Convert 'summoner_name' to categorical codes
gs_df['summoner_code'] = pd.Categorical(gs_df['summoner_name']).codes

# Create a colormap
cmap = plt.get_cmap('viridis')
colors = cmap(np.linspace(0, 1, len(gs_df['summoner_code'].unique())))

# Plot
fig, ax = plt.subplots()
scatter = ax.scatter(gs_df['date'], gs_df['hour'], c=gs_df['summoner_code'], cmap='viridis', alpha=0.5)

# Create legend
unique_summoners = gs_df[['summoner_code', 'summoner_name']].drop_duplicates().sort_values('summoner_code')

if gs_df['summoner_code'].nunique() > 1:
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=cmap(code / (len(unique_summoners)-1)), markersize=10, label=name) 
            for code, name in unique_summoners.itertuples(index=False)]
else:
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=cmap(code / 1), markersize=10, label=name) 
            for code, name in unique_summoners.itertuples(index=False)]

ax.legend(handles=handles, title='Summoner Name')

# Set plot labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Hour')
ax.set_title('Gaming Schedule')
plt.xticks(rotation=90)
plt.tight_layout()

# Render the plot with Streamlit
st.pyplot(fig)

st.divider()