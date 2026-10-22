"""
CRUD Service handling Create, Read, Update, and Delete operations for players.
"""
import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "cricket_stats.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_all_players():
    conn = get_connection()
    df = pd.read_sql("SELECT p.player_id, p.full_name, t.team_name, p.playing_role, p.batting_style, p.bowling_style FROM players p JOIN teams t ON p.team_id = t.team_id ORDER BY p.player_id DESC;", conn)
    conn.close()
    return df

def get_teams():
    conn = get_connection()
    df = pd.read_sql("SELECT team_id, team_name FROM teams;", conn)
    conn.close()
    return dict(zip(df['team_name'], df['team_id']))

def add_player(full_name, team_id, playing_role, batting_style, bowling_style):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO players (full_name, team_id, playing_role, batting_style, bowling_style)
        VALUES (?, ?, ?, ?, ?)
    """, (full_name, team_id, playing_role, batting_style, bowling_style))
    conn.commit()
    conn.close()
    return True

def update_player(player_id, full_name, team_id, playing_role, batting_style, bowling_style):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE players 
        SET full_name = ?, team_id = ?, playing_role = ?, batting_style = ?, bowling_style = ?
        WHERE player_id = ?
    """, (full_name, team_id, playing_role, batting_style, bowling_style, player_id))
    conn.commit()
    conn.close()
    return True

def delete_player(player_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players WHERE player_id = ?", (player_id,))
    conn.commit()
    conn.close()
    return True