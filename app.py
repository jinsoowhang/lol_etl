import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


# Navigation
p1 = st.Page(
    "pages/past_20_games.py",
    title = "Trends over past 20 Games",
    icon="📈"
    )

p2 = st.Page(
    "pages/about.py",
    title = "About",
    icon="📙"
    )

pg = st.navigation({
    "Metrics": [p1],
    "Info": [p2]
})

pg.run()