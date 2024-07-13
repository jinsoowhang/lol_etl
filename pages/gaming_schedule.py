import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Parquet File Path
parquet_file_path = 'etl/data/transformed_match_details.parquet'
df = pd.read_parquet(parquet_file_path)

# Copy new dataframe
gs_df = df.copy()

####################
####### UDF ########
####################

# Function to transform time played
def transform_time_played(df, column):
    # Convert the column values to minutes
    total_minutes = round((df[column].sum()) / 60)
    
    if total_minutes < 60:
        return f"{total_minutes} minutes"
    elif total_minutes < 1440:
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours} hours, {minutes} minutes"
    else:
        days = total_minutes // 1440
        hours = (total_minutes % 1440) // 60
        minutes = total_minutes % 60
        return f"{days} days, {hours} hours, {minutes} minutes"

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

# Print Total Games Played, Total Time Played
total_time_played = transform_time_played(gs_df, 'time_played')
st.markdown(f"#### A total of {len(gs_df)} games were played, equivalent to \n\
             {total_time_played}")

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
ax.set_ylabel('Time of Day (24hr)')

# Create a full date range from min to max date in gs_df
min_date = gs_df['date'].min()
max_date = gs_df['date'].max()

# Check for NaT and handle it
if pd.isna(min_date) or pd.isna(max_date):
    st.error("No valid date range found in the data.")
else:
    full_date_range = pd.date_range(start=min_date, end=max_date, freq='D')

    # Determine date format based on the range
    if (max_date - min_date).days > 30:
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
    else:
        date_format = '%Y-%m-%d'  # Full date format
        ax.set_xticks(full_date_range)
        ax.set_xticklabels(full_date_range.strftime(date_format), rotation=90)
  
plt.tight_layout()

# Render the plot with Streamlit
st.pyplot(fig)

st.divider()