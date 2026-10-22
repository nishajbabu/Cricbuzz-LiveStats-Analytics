"""
Top Player Statistics Page
"""
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Top Player Stats - Cricbuzz LiveStats", layout="wide")

st.title("📊 Top Player Leaderboards & Statistics")
st.write("Aggregated leaderboards across Test, ODI, and T20I formats.")

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "cricket_stats.db")

def run_query(sql):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

tab1, tab2, tab3 = st.tabs(["🏏 Top Run Scorers", "🎯 Top Wicket Takers", "⭐ Highest Individual Scores"])

with tab1:
    st.subheader("Top Batting Performers by Total Runs")
    sql_bat = """
    SELECT 
        p.full_name AS Player,
        t.short_name AS Team,
        SUM(b.runs_scored) AS Total_Runs,
        SUM(CASE WHEN b.runs_scored >= 100 THEN 1 ELSE 0 END) AS Centuries,
        SUM(CASE WHEN b.runs_scored >= 50 AND b.runs_scored < 100 THEN 1 ELSE 0 END) AS Fifties
    FROM batting_stats b
    JOIN players p ON b.player_id = p.player_id
    JOIN teams t ON p.team_id = t.team_id
    GROUP BY p.player_id, p.full_name, t.short_name
    ORDER BY Total_Runs DESC;
    """
    df_bat = run_query(sql_bat)
    st.dataframe(df_bat, use_container_width=True)

    if not df_bat.empty:
        fig_bat = px.bar(df_bat, x="Player", y="Total_Runs", color="Team", 
                         title="Total Runs by Player", text_auto=True)
        st.plotly_chart(fig_bat, use_container_width=True)

with tab2:
    st.subheader("Top Bowling Performers by Total Wickets")
    sql_bowl = """
    SELECT 
        p.full_name AS Bowler,
        t.short_name AS Team,
        SUM(bw.wickets_taken) AS Wickets,
        SUM(bw.runs_conceded) AS Runs_Conceded,
        ROUND(CAST(SUM(bw.runs_conceded) AS FLOAT) / MAX(1, SUM(bw.overs_bowled)), 2) AS Economy_Rate
    FROM bowling_stats bw
    JOIN players p ON bw.player_id = p.player_id
    JOIN teams t ON p.team_id = t.team_id
    GROUP BY p.player_id, p.full_name, t.short_name
    ORDER BY Wickets DESC, Economy_Rate ASC;
    """
    df_bowl = run_query(sql_bowl)
    st.dataframe(df_bowl, use_container_width=True)

    if not df_bowl.empty:
        fig_bowl = px.bar(df_bowl, x="Bowler", y="Wickets", color="Team", 
                          title="Total Wickets Taken", text_auto=True)
        st.plotly_chart(fig_bowl, use_container_width=True)

with tab3:
    st.subheader("Highest Individual Scores per Cricket Format")
    sql_high = """
    SELECT 
        b.match_format AS Format,
        p.full_name AS Player,
        b.runs_scored AS Highest_Score,
        b.balls_faced AS Balls_Faced,
        b.match_date AS Date
    FROM batting_stats b
    JOIN players p ON b.player_id = p.player_id
    INNER JOIN (
        SELECT match_format, MAX(runs_scored) AS max_runs
        FROM batting_stats
        GROUP BY match_format
    ) max_b ON b.match_format = max_b.match_format AND b.runs_scored = max_b.max_runs;
    """
    df_high = run_query(sql_high)
    st.dataframe(df_high, use_container_width=True)	