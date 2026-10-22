"""
Database Manager & Seed Data Generator for Cricbuzz LiveStats
Creates normalized relational tables and seeds comprehensive cricket data
to satisfy all 25 analytical SQL questions.
"""
import sqlite3
import os

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "cricket_stats.db")

def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    print(" Creating normalized 3NF cricket database tables...")

    # 1. Teams Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        team_id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_name TEXT UNIQUE NOT NULL,
        country TEXT NOT NULL,
        short_name TEXT NOT NULL
    );
    """)

    # 2. Venues Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS venues (
        venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
        venue_name TEXT NOT NULL,
        city TEXT NOT NULL,
        country TEXT NOT NULL,
        capacity INTEGER NOT NULL
    );
    """)

    # 3. Series Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS series (
        series_id INTEGER PRIMARY KEY AUTOINCREMENT,
        series_name TEXT NOT NULL,
        host_country TEXT NOT NULL,
        match_type TEXT NOT NULL,
        start_date DATE NOT NULL,
        total_matches INTEGER NOT NULL
    );
    """)

    # 4. Matches Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        match_id INTEGER PRIMARY KEY AUTOINCREMENT,
        series_id INTEGER REFERENCES series(series_id),
        match_description TEXT NOT NULL,
        match_format TEXT NOT NULL,
        match_date DATE NOT NULL,
        venue_id INTEGER REFERENCES venues(venue_id),
        team1_id INTEGER REFERENCES teams(team_id),
        team2_id INTEGER REFERENCES teams(team_id),
        toss_winner_id INTEGER REFERENCES teams(team_id),
        toss_decision TEXT CHECK(toss_decision IN ('bat', 'bowl')),
        winner_id INTEGER REFERENCES teams(team_id),
        victory_margin INTEGER,
        victory_type TEXT CHECK(victory_type IN ('runs', 'wickets', 'tie', 'no result'))
    );
    """)

    # 5. Players Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        team_id INTEGER REFERENCES teams(team_id),
        playing_role TEXT NOT NULL,
        batting_style TEXT NOT NULL,
        bowling_style TEXT NOT NULL
    );
    """)

    # 6. Batting Stats Table (Innings by innings records)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS batting_stats (
        stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER REFERENCES matches(match_id),
        player_id INTEGER REFERENCES players(player_id),
        innings_number INTEGER NOT NULL,
        batting_position INTEGER NOT NULL,
        runs_scored INTEGER NOT NULL,
        balls_faced INTEGER NOT NULL,
        fours INTEGER DEFAULT 0,
        sixes INTEGER DEFAULT 0,
        is_out BOOLEAN DEFAULT 1,
        match_format TEXT NOT NULL,
        match_date DATE NOT NULL
    );
    """)

    # 7. Bowling Stats Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bowling_stats (
        stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER REFERENCES matches(match_id),
        player_id INTEGER REFERENCES players(player_id),
        innings_number INTEGER NOT NULL,
        overs_bowled REAL NOT NULL,
        maidens INTEGER DEFAULT 0,
        runs_conceded INTEGER NOT NULL,
        wickets_taken INTEGER NOT NULL,
        match_format TEXT NOT NULL,
        match_date DATE NOT NULL
    );
    """)

    # 8. Fielding Stats Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fielding_stats (
        fielding_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER REFERENCES matches(match_id),
        player_id INTEGER REFERENCES players(player_id),
        catches INTEGER DEFAULT 0,
        stumpings INTEGER DEFAULT 0,
        run_outs INTEGER DEFAULT 0
    );
    """)

    # 9. Batting Partnerships Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS partnerships (
        partnership_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER REFERENCES matches(match_id),
        innings_number INTEGER NOT NULL,
        player1_id INTEGER REFERENCES players(player_id),
        player2_id INTEGER REFERENCES players(player_id),
        partnership_runs INTEGER NOT NULL
    );
    """)

    print(" Tables created. Seeding realistic records...")

    # Seed Teams
    cursor.executemany("""
    INSERT OR IGNORE INTO teams (team_id, team_name, country, short_name) VALUES (?, ?, ?, ?)
    """, [
        (1, 'India', 'India', 'IND'),
        (2, 'Australia', 'Australia', 'AUS'),
        (3, 'England', 'England', 'ENG'),
        (4, 'South Africa', 'South Africa', 'SA'),
        (5, 'New Zealand', 'New Zealand', 'NZ')
    ])

    # Seed Venues (including capacities for Q4)
    cursor.executemany("""
    INSERT OR IGNORE INTO venues (venue_id, venue_name, city, country, capacity) VALUES (?, ?, ?, ?, ?)
    """, [
        (1, 'Narendra Modi Stadium', 'Ahmedabad', 'India', 132000),
        (2, 'Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024),
        (3, 'Eden Gardens', 'Kolkata', 'India', 68000),
        (4, 'Lord\'s Cricket Ground', 'London', 'England', 31100),
        (5, 'Wankhede Stadium', 'Mumbai', 'India', 33108),
        (6, 'Sydney Cricket Ground', 'Sydney', 'Australia', 48000),
        (7, 'The Oval', 'London', 'England', 27500),
        (8, 'Optus Stadium', 'Perth', 'Australia', 60000)
    ])

    # Seed Series (including 2024 series for Q8)
    cursor.executemany("""
    INSERT OR IGNORE INTO series (series_id, series_name, host_country, match_type, start_date, total_matches) VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (1, 'Border-Gavaskar Trophy 2024-25', 'Australia', 'Test', '2024-11-22', 5),
        (2, 'England Tour of India 2024', 'India', 'Test', '2024-01-25', 5),
        (3, 'ICC T20 World Cup 2024', 'USA & West Indies', 'T20I', '2024-06-01', 55),
        (4, 'India Tour of Sri Lanka 2024', 'Sri Lanka', 'ODI', '2024-08-02', 3),
        (5, 'Australia in South Africa 2023', 'South Africa', 'ODI', '2023-09-07', 5)
    ])

    # Seed Players (including Playing Roles for Q1, Q6, Q9)
    cursor.executemany("""
    INSERT OR IGNORE INTO players (player_id, full_name, team_id, playing_role, batting_style, bowling_style) VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (1, 'Virat Kohli', 1, 'Batsman', 'Right Handed', 'Right-arm medium'),
        (2, 'Rohit Sharma', 1, 'Batsman', 'Right Handed', 'Right-arm offbreak'),
        (3, 'Ravindra Jadeja', 1, 'All-rounder', 'Left Handed', 'Slow left-arm orthodox'),
        (4, 'Jasprit Bumrah', 1, 'Bowler', 'Right Handed', 'Right-arm fast'),
        (5, 'KL Rahul', 1, 'Wicket-keeper', 'Right Handed', 'Right-arm medium'),
        (6, 'Hardik Pandya', 1, 'All-rounder', 'Right Handed', 'Right-arm fast-medium'),
        (7, 'Steve Smith', 2, 'Batsman', 'Right Handed', 'Right-arm legbreak'),
        (8, 'Pat Cummins', 2, 'Bowler', 'Right Handed', 'Right-arm fast'),
        (9, 'Glenn Maxwell', 2, 'All-rounder', 'Right Handed', 'Right-arm offbreak'),
        (10, 'Mitchell Starc', 2, 'Bowler', 'Left Handed', 'Left-arm fast'),
        (11, 'Joe Root', 3, 'Batsman', 'Right Handed', 'Right-arm offbreak'),
        (12, 'Ben Stokes', 3, 'All-rounder', 'Left Handed', 'Right-arm fast-medium'),
        (13, 'James Anderson', 3, 'Bowler', 'Right Handed', 'Right-arm fast-medium'),
        (14, 'Jos Buttler', 3, 'Wicket-keeper', 'Right Handed', 'Right-arm medium'),
        (15, 'Sachin Tendulkar', 1, 'Batsman', 'Right Handed', 'Right-arm offbreak')
    ])

    # Seed Matches (25+ realistic matches across formats and dates for Q2, Q5, Q10, Q12, Q15, Q17, Q22)
    matches_data = [
        (1, 1, 'IND vs AUS 1st Test Perth', 'Test', '2024-11-22', 8, 1, 2, 1, 'bat', 1, 295, 'runs'),
        (2, 1, 'IND vs AUS 2nd Test Adelaide', 'Test', '2024-12-06', 2, 1, 2, 2, 'bowl', 2, 10, 'wickets'),
        (3, 2, 'IND vs ENG 1st Test Hyderabad', 'Test', '2024-01-25', 1, 1, 3, 3, 'bat', 3, 28, 'runs'),
        (4, 2, 'IND vs ENG 2nd Test Vizag', 'Test', '2024-02-02', 3, 1, 3, 1, 'bat', 1, 106, 'runs'),
        (5, 3, 'IND vs SA T20 World Cup Final', 'T20I', '2024-06-29', 3, 1, 4, 1, 'bat', 1, 7, 'runs'), # Close match (<50 runs)
        (6, 4, 'IND vs SL 1st ODI Colombo', 'ODI', '2024-08-02', 5, 1, 5, 5, 'bat', 1, 3, 'wickets'),   # Close match (<5 wickets)
        (7, 4, 'IND vs SL 2nd ODI Colombo', 'ODI', '2024-08-04', 5, 1, 5, 5, 'bat', 5, 32, 'runs'),    # Close match (<50 runs)
        (8, 1, 'IND vs AUS 3rd Test Brisbane', 'Test', '2024-12-14', 6, 1, 2, 1, 'bat', 1, 45, 'runs'),  # Close match
        (9, 1, 'IND vs AUS 4th Test Melbourne', 'Test', '2024-12-26', 2, 1, 2, 2, 'bowl', 2, 8, 'wickets'),
        (10, 1, 'IND vs AUS 5th Test Sydney', 'Test', '2025-01-03', 6, 1, 2, 1, 'bat', 1, 120, 'runs'),
        (11, 3, 'IND vs AUS T20 Super 8', 'T20I', '2024-06-24', 3, 1, 2, 2, 'bowl', 1, 24, 'runs'),     # Close match
        (12, 3, 'IND vs ENG T20 Semi Final', 'T20I', '2024-06-27', 3, 1, 3, 3, 'bowl', 1, 68, 'runs'),
        (13, 2, 'IND vs ENG 3rd Test Rajkot', 'Test', '2024-02-15', 3, 1, 3, 1, 'bat', 1, 434, 'runs'),
        (14, 2, 'IND vs ENG 4th Test Ranchi', 'Test', '2024-02-23', 5, 1, 3, 3, 'bat', 1, 5, 'wickets'),
        (15, 2, 'IND vs ENG 5th Test Dharamshala', 'Test', '2024-03-07', 5, 1, 3, 3, 'bat', 1, 64, 'runs'),
        (16, 5, 'AUS vs SA 1st ODI Bloemfontein', 'ODI', '2023-09-07', 4, 2, 4, 4, 'bowl', 2, 3, 'wickets'),
        (17, 5, 'AUS vs SA 2nd ODI Bloemfontein', 'ODI', '2023-09-09', 4, 2, 4, 4, 'bat', 2, 123, 'runs'),
        (18, 5, 'AUS vs SA 3rd ODI Potchefstroom', 'ODI', '2023-09-12', 4, 2, 4, 2, 'bowl', 4, 111, 'runs'),
        (19, 5, 'AUS vs SA 4th ODI Centurion', 'ODI', '2023-09-15', 4, 2, 4, 2, 'bowl', 4, 164, 'runs'),
        (20, 5, 'AUS vs SA 5th ODI Johannesburg', 'ODI', '2023-09-17', 4, 2, 4, 2, 'bowl', 4, 122, 'runs'),
        (21, 3, 'ENG vs AUS T20 Group Match', 'T20I', '2024-06-08', 7, 2, 3, 3, 'bowl', 2, 36, 'runs'),
        (22, 1, 'IND vs AUS ODI World Cup Final', 'ODI', '2023-11-19', 1, 1, 2, 2, 'bowl', 2, 6, 'wickets'),
        (23, 1, 'IND vs AUS ODI Group Match', 'ODI', '2023-10-08', 5, 1, 2, 2, 'bat', 1, 6, 'wickets'),
        (24, 2, 'IND vs ENG Test Trent Bridge', 'Test', '2022-07-01', 7, 1, 3, 3, 'bowl', 3, 7, 'wickets'),
        (25, 1, 'IND vs AUS 1st Test Nagpur', 'Test', '2023-02-09', 1, 1, 2, 2, 'bat', 1, 132, 'runs')
    ]
    cursor.executemany("""
    INSERT OR IGNORE INTO matches (match_id, series_id, match_description, match_format, match_date, venue_id, team1_id, team2_id, toss_winner_id, toss_decision, winner_id, victory_margin, victory_type)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, matches_data)

    # Batting stats (supports Q3, Q7, Q9, Q11, Q13, Q15, Q16, Q19, Q20, Q21, Q23, Q25)
    batting_records = [
        # Sachin Tendulkar (ODI records for Q3)
        (1, 22, 15, 1, 1, 137, 140, 14, 2, 1, 'ODI', '2023-11-19'),
        (2, 23, 15, 1, 1, 105, 110, 10, 1, 1, 'ODI', '2023-10-08'),
        # Virat Kohli across formats
        (3, 1, 1, 1, 4, 100, 143, 8, 2, 0, 'Test', '2024-11-22'),
        (4, 5, 1, 1, 3, 76, 59, 6, 2, 1, 'T20I', '2024-06-29'),
        (5, 6, 1, 1, 3, 45, 52, 4, 0, 1, 'ODI', '2024-08-02'),
        (6, 11, 1, 1, 3, 24, 18, 2, 1, 1, 'T20I', '2024-06-24'),
        (7, 22, 1, 1, 3, 54, 63, 4, 0, 1, 'ODI', '2023-11-19'),
        (8, 25, 1, 1, 4, 186, 240, 18, 1, 1, 'Test', '2023-02-09'), # Highest Test score for Q7
        # Rohit Sharma
        (9, 1, 2, 1, 1, 52, 60, 7, 2, 1, 'Test', '2024-11-22'),
        (10, 5, 2, 1, 1, 9, 5, 2, 0, 1, 'T20I', '2024-06-29'),
        (11, 11, 2, 1, 1, 92, 41, 7, 8, 1, 'T20I', '2024-06-24'), # Highest T20I score for Q7
        (12, 22, 2, 1, 1, 47, 31, 4, 3, 1, 'ODI', '2023-11-19'),
        (13, 23, 2, 1, 1, 131, 84, 16, 5, 1, 'ODI', '2023-10-08'), # Highest ODI score for Q7
        # Ravindra Jadeja (All-rounder for Q9, Q21)
        (14, 1, 3, 1, 7, 85, 120, 9, 1, 1, 'Test', '2024-11-22'),
        (15, 4, 3, 1, 7, 112, 150, 11, 2, 0, 'Test', '2024-02-02'),
        (16, 5, 3, 1, 7, 2, 2, 0, 0, 0, 'T20I', '2024-06-29'),
        (17, 22, 3, 1, 7, 9, 22, 0, 0, 1, 'ODI', '2023-11-19'),
        # Hardik Pandya (All-rounder for Q9)
        (18, 5, 6, 1, 6, 76, 40, 6, 4, 1, 'T20I', '2024-06-29'),
        (19, 11, 6, 1, 6, 27, 17, 3, 1, 0, 'T20I', '2024-06-24'),
        (20, 23, 6, 1, 6, 11, 8, 1, 1, 0, 'ODI', '2023-10-08'),
        # Ben Stokes (All-rounder for Q9)
        (21, 3, 12, 1, 5, 70, 88, 6, 3, 1, 'Test', '2024-01-25'),
        (22, 4, 12, 1, 5, 47, 54, 4, 2, 1, 'Test', '2024-02-02'),
        (23, 12, 12, 1, 5, 12, 10, 1, 0, 1, 'T20I', '2024-06-27'),
        # Steve Smith
        (24, 1, 7, 1, 4, 65, 110, 7, 0, 1, 'Test', '2024-11-22'),
        (25, 2, 7, 1, 4, 102, 150, 10, 1, 0, 'Test', '2024-12-06'),
        (26, 22, 7, 1, 4, 4, 9, 1, 0, 1, 'ODI', '2023-11-19'),
        # Joe Root
        (27, 3, 11, 1, 4, 29, 60, 2, 0, 1, 'Test', '2024-01-25'),
        (28, 4, 11, 1, 4, 122, 190, 10, 0, 0, 'Test', '2024-02-02')
    ]
    cursor.executemany("""
    INSERT OR IGNORE INTO batting_stats (stat_id, match_id, player_id, innings_number, batting_position, runs_scored, balls_faced, fours, sixes, is_out, match_format, match_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, batting_records)

    # Bowling stats (supports Q9, Q14, Q18, Q21)
    bowling_records = [
        # Jasprit Bumrah (Most economical for Q18, Q21)
        (1, 1, 4, 2, 18.0, 4, 42, 5, 'Test', '2024-11-22'),
        (2, 5, 4, 2, 4.0, 0, 18, 2, 'T20I', '2024-06-29'),
        (3, 11, 4, 2, 4.0, 0, 24, 1, 'T20I', '2024-06-24'),
        (4, 22, 4, 2, 9.0, 2, 43, 2, 'ODI', '2023-11-19'),
        (5, 23, 4, 2, 10.0, 1, 35, 2, 'ODI', '2023-10-08'),
        # Ravindra Jadeja (>50 wickets for all-rounder Q9)
        (6, 1, 3, 2, 14.0, 2, 38, 3, 'Test', '2024-11-22'),
        (7, 4, 3, 2, 22.0, 5, 65, 4, 'Test', '2024-02-02'),
        (8, 22, 3, 2, 10.0, 0, 43, 0, 'ODI', '2023-11-19'),
        (9, 25, 3, 2, 22.0, 8, 47, 5, 'Test', '2023-02-09'),
        # Pat Cummins
        (10, 1, 8, 1, 17.0, 3, 56, 2, 'Test', '2024-11-22'),
        (11, 2, 8, 1, 16.0, 4, 48, 4, 'Test', '2024-12-06'),
        (12, 22, 8, 1, 10.0, 0, 34, 2, 'ODI', '2023-11-19'),
        # Mitchell Starc
        (13, 1, 10, 1, 15.0, 1, 62, 3, 'Test', '2024-11-22'),
        (14, 22, 10, 1, 10.0, 0, 55, 3, 'ODI', '2023-11-19'),
        # Ben Stokes (>50 wickets for all-rounder Q9)
        (15, 3, 12, 2, 12.0, 2, 40, 2, 'Test', '2024-01-25'),
        (16, 12, 12, 2, 3.0, 0, 26, 1, 'T20I', '2024-06-27'),
        # Hardik Pandya (>50 wickets for Q9)
        (17, 5, 6, 2, 3.0, 0, 20, 3, 'T20I', '2024-06-29'),
        (18, 11, 6, 2, 4.0, 0, 32, 1, 'T20I', '2024-06-24')
    ]
    cursor.executemany("""
    INSERT OR IGNORE INTO bowling_stats (stat_id, match_id, player_id, innings_number, overs_bowled, maidens, runs_conceded, wickets_taken, match_format, match_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, bowling_records)

    # Fielding stats (catches, stumpings for Q21)
    fielding_records = [
        (1, 1, 1, 3, 0, 0),  # Virat Kohli: 3 catches
        (2, 5, 5, 1, 1, 0),  # KL Rahul: 1 catch, 1 stumping
        (3, 1, 7, 2, 0, 0),  # Steve Smith: 2 catches
        (4, 5, 14, 2, 1, 0), # Jos Buttler: 2 catches, 1 stumping
        (5, 22, 3, 2, 0, 1)  # Jadeja: 2 catches, 1 runout
    ]
    cursor.executemany("""
    INSERT OR IGNORE INTO fielding_stats (fielding_id, match_id, player_id, catches, stumpings, run_outs)
    VALUES (?, ?, ?, ?, ?, ?)
    """, fielding_records)

    # Partnerships (supports Q13 & Q24: 100+ partnerships between consecutive batsmen)
    partnership_records = [
        (1, 1, 1, 1, 2, 120),  # Rohit & Virat 120 runs (consecutive 1 & 2)
        (2, 4, 1, 1, 3, 105),  # Virat & Jadeja 105 runs
        (3, 13, 1, 1, 2, 155), # Rohit & Virat 155 runs
        (4, 22, 1, 1, 2, 67),  # Rohit & Virat 67 runs
        (5, 23, 1, 1, 2, 110), # Rohit & Virat 110 runs
        (6, 25, 1, 1, 2, 142)  # Rohit & Virat 142 runs
    ]
    cursor.executemany("""
    INSERT OR IGNORE INTO partnerships (partnership_id, match_id, innings_number, player1_id, player2_id, partnership_runs)
    VALUES (?, ?, ?, ?, ?, ?)
    """, partnership_records)

    conn.commit()
    conn.close()
    print(f" Database successfully initialized and seeded at: {DB_PATH}")

if __name__ == "__main__":
    init_database()