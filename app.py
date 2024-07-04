import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


# Navigation
p1 = st.Page(
    "pages/gaming_schedule.py",
    title = "Gaming Schedule",
    icon = "📅"
)

p2 = st.Page(
    "pages/metric_arena.py",
    title = "Metric Arena",
    icon = "🏟️"
)

p3 = st.Page(
    "pages/past_20_games.py",
    title = "Trends over past 20 Games",
    icon = "📈"
)

p4 = st.Page(
    "pages/about.py",
    title = "About",
    icon = "📙"
    )

pg = st.navigation({
    "Metrics": [p1, p2, p3],
    "Info": [p4]
})

pg.run()