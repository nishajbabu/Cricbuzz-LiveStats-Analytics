import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.cricbuzz_client import CricbuzzClient

st.set_page_config(page_title="Live Matches - Cricbuzz LiveStats", page_icon="⚡", layout="wide")

st.title("⚡ Real-Time Live Cricket Matches")
st.write("Live match telemetry, active scorecards, and venue status.")

client = CricbuzzClient()
data = client.get_live_matches()

matches = data.get("matches", [])

if not matches:
    st.info("No active matches found at the moment.")
else:
    for m in matches:
        with st.container():
            st.markdown(f"""
            <div style="background-color: #1F2937; padding: 18px; border-radius: 10px; margin-bottom: 15px; border-left: 6px solid #10B981;">
                <h4 style="margin:0; color:#10B981;">{m.get('match_desc', 'Match')}</h4>
                <p style="color:#D1D5DB; margin-top:5px;"><b>Status:</b> {m.get('status', 'In Progress')}</p>
                <div style="display:flex; justify-content:space-between; margin-top:10px;">
                    <div><b>{m.get('team1', 'Team 1')}:</b> {m.get('score1', 'Yet to bat')}</div>
                    <div><b>{m.get('team2', 'Team 2')}:</b> {m.get('score2', 'Yet to bat')}</div>
                </div>
                <small style="color:#9CA3AF; display:block; margin-top:8px;">📍 {m.get('venue', 'Cricket Ground')}</small>
            </div>
            """, unsafe_allow_html=True)