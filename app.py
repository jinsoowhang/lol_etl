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

pg = st.navigation({
    "Metrics": [p1]
})

pg.run()