import streamlit as st

st.set_page_config(page_title="Project Overview - Cricbuzz LiveStats", page_icon="🏠", layout="wide")

st.title("🏠 Project Overview & System Architecture")

st.markdown("""
### 📌 Problem Statement
This platform solves the fragmentation between real-time live cricket score feeds and historical database analytics. By bridging the **Cricbuzz REST API** with a normalized **3NF SQL Database**, sports analysts and broadcasters can query live telemetry and solve advanced historical analytical scenarios.

---

### 🏛️ Relational Database Schema (3NF)
The backend database (`cricket_stats.db`) is structured into 9 normalized tables:
* **`teams`**: Country profiles and short codes.
* **`venues`**: Stadium names, geographical cities, and seating capacities.
* **`series`**: International bilateral tours and multi-team tournaments.
* **`matches`**: Fixtures, formats (Test, ODI, T20I), toss decisions, match winners, and margins.
* **`players`**: Athlete rosters, playing roles (Batsman, Bowler, All-rounder, Wicket-keeper), and styles.
* **`batting_stats`**: Granular innings records (runs, balls faced, boundaries, dismissal status).
* **`bowling_stats`**: Overs bowled, maidens, runs conceded, and wickets.
* **`fielding_stats`**: Catches, stumpings, and run-outs.
* **`partnerships`**: Consecutive partnership runs per innings.

---

### 🛠️ Technology Stack
* **Frontend:** Streamlit Multi-Page Framework
* **Backend:** Python 3.10+, Pandas DataFrames, Plotly Visuals
* **Database:** SQLite (Database-agnostic connector architecture)
* **API Telemetry:** Cricbuzz Cricket REST API via RapidAPI
""")