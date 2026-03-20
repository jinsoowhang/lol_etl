# League of Legends ETL

A data pipeline and analytics dashboard that extracts ranked game data from the Riot Games API, transforms it into performance metrics, and visualizes player stats through an interactive Streamlit app.

**Live:** [unchained.streamlit.app](https://unchained.streamlit.app/)

![dashboard](/assets/images/about.PNG)

## What It Does

Tracks 5 players across their last 20 ranked games, comparing 30+ performance metrics — kills, deaths, KDA, gold efficiency, damage output, win rates, and more.

### Dashboard Pages

| Page | Description |
|------|-------------|
| **Metric Arena** | Head-to-head rankings per metric — who has the best KDA, most damage, etc. |
| **Gaming Schedule** | Scatterplot of when each player plays (date vs. time of day) |
| **Past 20 Games** | Cumulative win and playtime trends over recent matches |

## Architecture

```
Riot Games API
  ├── Account API → player PUUIDs
  ├── Match API   → match IDs → full match details
  │
  └── Extract (raw JSON → Parquet)
        └── Transform (nested → flat, 30+ metrics)
              └── Streamlit reads Parquet directly
```

No database — uses **Apache Parquet** files for efficient columnar storage.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Data Source | [Riot Games API](https://developer.riotgames.com/apis) |
| ETL | Python, pandas, requests |
| Storage | Apache Parquet |
| Visualization | Streamlit, Altair, Matplotlib |
| Deployment | Streamlit Cloud |

## Project Structure

```
lol_etl/
├── api/                    # Riot API client modules
│   ├── summoners.py        # PUUID lookup
│   ├── match_id.py         # Match ID fetching
│   └── match.py            # Match detail extraction
├── etl/
│   ├── etl_process.py      # Pipeline orchestrator
│   ├── extract.py          # Raw data → Parquet
│   └── transform.py        # Flatten & compute metrics
├── pages/                  # Streamlit dashboard
│   ├── metric_arena.py
│   ├── gaming_schedule.py
│   ├── past_20_games.py
│   └── about.py
├── app.py                  # Streamlit entry point
└── main.py                 # ETL entry point
```

## Run Locally

```bash
pip install -r requirements.txt
python main.py              # Run ETL pipeline
streamlit run app.py        # Launch dashboard
```

Requires a `config/config.py` with your Riot Games API key and player names.
