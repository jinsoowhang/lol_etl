import streamlit as st

# Title page 
st.markdown("# 📙 About")

st.markdown("## 🚀 Goal")
st.markdown("""
The goal of this project is to create a data analytics application with League of Legends data. It extracts, transforms, and loads game data to provide performance metrics and insights. The insights are displayed in an interactive Streamlit dashboard, helping its users track performance and identify trends.
""")

st.markdown("### 🔗 Useful Links")
col1, col2 = st.columns(2)
with col1:
    st.markdown("### [🌐 GitHub](https://github.com/jinsoowhang/lol_etl)")
    st.write("Link to the source code")

with col2:
    st.markdown("### [👾 League of Legends API](https://developer.riotgames.com/apis)")
    st.write("Learn more about the API used for data extraction")
