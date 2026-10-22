"""
Cricbuzz LiveStats - Main Application Entry Point
"""
import streamlit as st
import sqlite3
import os

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 36px;
        font-weight: 800;
        color: #10B981;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 16px;
        color: #9CA3AF;
        text-align: center;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #1F2937;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #10B981;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🏏 Cricbuzz LiveStats Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Real-Time Cricket Telemetry & SQL-Driven Analytics Platform</div>', unsafe_allow_html=True)

# Fetch Database Metrics
DB_PATH = os.path.join(os.path.dirname(__file__), "database", "cricket_stats.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM matches;")
total_matches = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM players;")
total_players = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM venues;")
total_venues = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM teams;")
total_teams = cursor.fetchone()[0]
conn.close()

# Overview Metric Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-card"><h3>🏆 Matches</h3><h2>{total_matches}</h2><p>Tracked</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><h3>👤 Players</h3><h2>{total_players}</h2><p>In Database</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><h3>🏟️ Venues</h3><h2>{total_venues}</h2><p>Mapped</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><h3>🌍 Teams</h3><h2>{total_teams}</h2><p>Nations</p></div>', unsafe_allow_html=True)

st.write("")
st.write("---")

st.markdown("""
### 🧭 Platform Navigation:
Use the **sidebar on the left** to explore all four functional modules:
1. **🏠 Home:** Architecture breakdown, ER schema details, and project documentation.
2. **⚡ Live Matches:** Real-time match telemetry, live scores, and venues from Cricbuzz API.
3. **📊 Top Stats:** Batting run scorers, bowling wicket-takers, and format comparisons.
4. **🔍 SQL Analytics:** Interactive runner for all **25 SQL Business Intelligence queries** (Beginner, Intermediate, Advanced).
5. **⚙️ CRUD Operations:** Administrative portal to Add, View, Edit, and Delete player records.
""")