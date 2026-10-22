"""
Service layer containing all 25 SQL Business Intelligence Queries
organized by Beginner, Intermediate, and Advanced tiers.
"""
import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "cricket_stats.db")

QUERIES = {
    # ------------------ Beginner Level (Q1 - Q8) ------------------
    1: {
        "title": "Q1: Find all players who represent India",
        "level": "Beginner",
        "sql": """
        SELECT 
            p.full_name,
            p.playing_role,
            p.batting_style,
            p.bowling_style
        FROM players p
        INNER JOIN teams t ON p.team_id = t.team_id
        WHERE t.team_name = 'India'
        ORDER BY p.full_name ASC;
        """
    },
    2: {
        "title": "Q2: Show all matches in the last 30 days",
        "level": "Beginner",
        "sql": """
        SELECT 
            m.match_description,
            t1.team_name AS team_1,
            t2.team_name AS team_2,
            v.venue_name || ', ' || v.city AS venue_location,
            m.match_date
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        JOIN venues v ON m.venue_id = v.venue_id
        ORDER BY m.match_date DESC
        LIMIT 10;
        """
    },
    3: {
        "title": "Q3: Top 10 highest run scorers in ODI cricket",
        "level": "Beginner",
        "sql": """
        SELECT 
            p.full_name AS player_name,
            SUM(b.runs_scored) AS total_runs,
            ROUND(CAST(SUM(b.runs_scored) AS FLOAT) / MAX(1, SUM(CASE WHEN b.is_out = 1 THEN 1 ELSE 0 END)), 2) AS batting_average,
            SUM(CASE WHEN b.runs_scored >= 100 THEN 1 ELSE 0 END) AS centuries
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        WHERE b.match_format = 'ODI'
        GROUP BY p.player_id, p.full_name
        ORDER BY total_runs DESC
        LIMIT 10;
        """
    },
    4: {
        "title": "Q4: Venues with seating capacity > 50,000",
        "level": "Beginner",
        "sql": """
        SELECT 
            venue_name,
            city,
            country,
            capacity
        FROM venues
        WHERE capacity > 50000
        ORDER BY capacity DESC;
        """
    },
    5: {
        "title": "Q5: Total match wins by each team",
        "level": "Beginner",
        "sql": """
        SELECT 
            t.team_name,
            COUNT(m.match_id) AS total_wins
        FROM teams t
        LEFT JOIN matches m ON t.team_id = m.winner_id
        GROUP BY t.team_id, t.team_name
        ORDER BY total_wins DESC;
        """
    },
    6: {
        "title": "Q6: Player count per playing role",
        "level": "Beginner",
        "sql": """
        SELECT 
            playing_role,
            COUNT(player_id) AS player_count
        FROM players
        GROUP BY playing_role
        ORDER BY player_count DESC;
        """
    },
    7: {
        "title": "Q7: Highest individual batting score per cricket format",
        "level": "Beginner",
        "sql": """
        SELECT 
            match_format,
            MAX(runs_scored) AS highest_individual_score
        FROM batting_stats
        GROUP BY match_format;
        """
    },
    8: {
        "title": "Q8: Series starting in 2024",
        "level": "Beginner",
        "sql": """
        SELECT 
            series_name,
            host_country,
            match_type,
            start_date,
            total_matches
        FROM series
        WHERE strftime('%Y', start_date) = '2024'
        ORDER BY start_date ASC;
        """
    },

    # ------------------ Intermediate Level (Q9 - Q16) ------------------
    9: {
        "title": "Q9: All-rounders (>1000 runs OR high runs & >50 career wickets)",
        "level": "Intermediate",
        "sql": """
        SELECT 
            p.full_name AS player_name,
            COALESCE(bat.total_runs, 0) AS total_runs,
            COALESCE(bowl.total_wickets, 0) AS total_wickets,
            p.playing_role
        FROM players p
        LEFT JOIN (
            SELECT player_id, SUM(runs_scored) AS total_runs 
            FROM batting_stats GROUP BY player_id
        ) bat ON p.player_id = bat.player_id
        LEFT JOIN (
            SELECT player_id, SUM(wickets_taken) AS total_wickets 
            FROM bowling_stats GROUP BY player_id
        ) bowl ON p.player_id = bowl.player_id
        WHERE p.playing_role = 'All-rounder'
        ORDER BY total_runs DESC;
        """
    },
    10: {
        "title": "Q10: Details of the last 20 completed matches",
        "level": "Intermediate",
        "sql": """
        SELECT 
            m.match_description,
            t1.short_name || ' vs ' || t2.short_name AS teams,
            tw.team_name AS winning_team,
            m.victory_margin || ' ' || m.victory_type AS victory_margin,
            v.venue_name
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        JOIN teams tw ON m.winner_id = tw.team_id
        JOIN venues v ON m.venue_id = v.venue_id
        ORDER BY m.match_date DESC
        LIMIT 20;
        """
    },
    11: {
        "title": "Q11: Multi-format comparison for players with >=2 formats",
        "level": "Intermediate",
        "sql": """
        SELECT 
            p.full_name,
            SUM(CASE WHEN b.match_format = 'Test' THEN b.runs_scored ELSE 0 END) AS test_runs,
            SUM(CASE WHEN b.match_format = 'ODI' THEN b.runs_scored ELSE 0 END) AS odi_runs,
            SUM(CASE WHEN b.match_format = 'T20I' THEN b.runs_scored ELSE 0 END) AS t20i_runs,
            ROUND(CAST(SUM(b.runs_scored) AS FLOAT) / MAX(1, SUM(CASE WHEN b.is_out = 1 THEN 1 ELSE 0 END)), 2) AS overall_avg
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        GROUP BY p.player_id, p.full_name
        HAVING COUNT(DISTINCT b.match_format) >= 2
        ORDER BY overall_avg DESC;
        """
    },
    12: {
        "title": "Q12: Home vs. Away performance for international teams",
        "level": "Intermediate",
        "sql": """
        SELECT 
            t.team_name,
            SUM(CASE WHEN v.country = t.country AND m.winner_id = t.team_id THEN 1 ELSE 0 END) AS home_wins,
            SUM(CASE WHEN v.country != t.country AND m.winner_id = t.team_id THEN 1 ELSE 0 END) AS away_wins
        FROM teams t
        LEFT JOIN matches m ON t.team_id IN (m.team1_id, m.team2_id)
        LEFT JOIN venues v ON m.venue_id = v.venue_id
        GROUP BY t.team_id, t.team_name
        ORDER BY home_wins DESC;
        """
    },
    13: {
        "title": "Q13: Consecutive batting partnerships with >= 100 runs",
        "level": "Intermediate",
        "sql": """
        SELECT 
            p1.full_name AS batsman_1,
            p2.full_name AS batsman_2,
            pr.partnership_runs,
            pr.innings_number,
            m.match_description
        FROM partnerships pr
        JOIN players p1 ON pr.player1_id = p1.player_id
        JOIN players p2 ON pr.player2_id = p2.player_id
        JOIN matches m ON pr.match_id = m.match_id
        WHERE pr.partnership_runs >= 100
        ORDER BY pr.partnership_runs DESC;
        """
    },
    14: {
        "title": "Q14: Bowling performance across venues",
        "level": "Intermediate",
        "sql": """
        SELECT 
            p.full_name AS bowler_name,
            v.venue_name,
            COUNT(b.stat_id) AS matches_bowled,
            SUM(b.wickets_taken) AS total_wickets,
            ROUND(CAST(SUM(b.runs_conceded) AS FLOAT) / MAX(1, SUM(b.overs_bowled)), 2) AS avg_economy
        FROM bowling_stats b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        JOIN venues v ON m.venue_id = v.venue_id
        GROUP BY p.player_id, p.full_name, v.venue_id, v.venue_name
        ORDER BY total_wickets DESC;
        """
    },
    15: {
        "title": "Q15: Player performance in close matches (<50 runs or <5 wickets)",
        "level": "Intermediate",
        "sql": """
        SELECT 
            p.full_name AS player_name,
            COUNT(b.stat_id) AS close_matches_played,
            ROUND(AVG(b.runs_scored), 2) AS avg_runs_close_matches,
            SUM(CASE WHEN m.winner_id = p.team_id THEN 1 ELSE 0 END) AS team_close_match_wins
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        WHERE (m.victory_type = 'runs' AND m.victory_margin < 50)
           OR (m.victory_type = 'wickets' AND m.victory_margin < 5)
        GROUP BY p.player_id, p.full_name
        ORDER BY avg_runs_close_matches DESC;
        """
    },
    16: {
        "title": "Q16: Annual batting trends since 2020",
        "level": "Intermediate",
        "sql": """
        SELECT 
            p.full_name AS player_name,
            strftime('%Y', b.match_date) AS match_year,
            ROUND(AVG(b.runs_scored), 2) AS avg_runs_per_match,
            ROUND(SUM(b.runs_scored) * 100.0 / MAX(1, SUM(b.balls_faced)), 2) AS avg_strike_rate
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        WHERE b.match_date >= '2020-01-01'
        GROUP BY p.player_id, p.full_name, match_year
        ORDER BY p.full_name, match_year DESC;
        """
    },

    # ------------------ Advanced Level (Q17 - Q25) ------------------
    17: {
        "title": "Q17: Toss decision winning advantage percentage",
        "level": "Advanced",
        "sql": """
        SELECT 
            toss_decision,
            COUNT(*) AS total_matches,
            SUM(CASE WHEN toss_winner_id = winner_id THEN 1 ELSE 0 END) AS toss_winner_match_wins,
            ROUND(AVG(CASE WHEN toss_winner_id = winner_id THEN 100.0 ELSE 0.0 END), 2) AS win_percentage
        FROM matches
        WHERE toss_decision IS NOT NULL
        GROUP BY toss_decision;
        """
    },
    18: {
        "title": "Q18: Economical bowlers in limited overs (ODI & T20I)",
        "level": "Advanced",
        "sql": """
        SELECT 
            p.full_name AS bowler_name,
            SUM(b.wickets_taken) AS total_wickets,
            ROUND(CAST(SUM(b.runs_conceded) AS FLOAT) / MAX(1, SUM(b.overs_bowled)), 2) AS economy_rate
        FROM bowling_stats b
        JOIN players p ON b.player_id = p.player_id
        WHERE b.match_format IN ('ODI', 'T20I')
        GROUP BY p.player_id, p.full_name
        ORDER BY economy_rate ASC, total_wickets DESC;
        """
    },
    19: {
        "title": "Q19: Batsman consistency analysis (Average vs. Standard Deviation)",
        "level": "Advanced",
        "sql": """
        SELECT 
            p.full_name AS player_name,
            ROUND(AVG(b.runs_scored), 2) AS avg_runs,
            COUNT(*) AS innings_played
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        WHERE b.balls_faced >= 10
        GROUP BY p.player_id, p.full_name
        ORDER BY avg_runs DESC;
        """
    },
    20: {
        "title": "Q20: Match distribution & batting average across all formats",
        "level": "Advanced",
        "sql": """
        SELECT 
            p.full_name AS player_name,
            SUM(CASE WHEN b.match_format = 'Test' THEN 1 ELSE 0 END) AS test_innings,
            SUM(CASE WHEN b.match_format = 'ODI' THEN 1 ELSE 0 END) AS odi_innings,
            SUM(CASE WHEN b.match_format = 'T20I' THEN 1 ELSE 0 END) AS t20i_innings,
            ROUND(AVG(b.runs_scored), 2) AS overall_avg
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        GROUP BY p.player_id, p.full_name
        ORDER BY overall_avg DESC;
        """
    },
    21: {
        "title": "Q21: Weighted multi-factor player performance ranking",
        "level": "Advanced",
        "sql": """
        WITH PlayerPoints AS (
            SELECT 
                p.player_id,
                p.full_name,
                COALESCE(SUM(b.runs_scored) * 0.01 + AVG(b.runs_scored) * 0.5, 0) AS bat_pts,
                COALESCE(SUM(bw.wickets_taken) * 2.0, 0) AS bowl_pts,
                COALESCE(SUM(f.catches) * 3.0 + SUM(f.stumpings) * 5.0, 0) AS field_pts
            FROM players p
            LEFT JOIN batting_stats b ON p.player_id = b.player_id
            LEFT JOIN bowling_stats bw ON p.player_id = bw.player_id
            LEFT JOIN fielding_stats f ON p.player_id = f.player_id
            GROUP BY p.player_id, p.full_name
        )
        SELECT 
            full_name,
            ROUND(bat_pts, 2) AS batting_points,
            ROUND(bowl_pts, 2) AS bowling_points,
            ROUND(field_pts, 2) AS fielding_points,
            ROUND(bat_pts + bowl_pts + field_pts, 2) AS composite_rating
        FROM PlayerPoints
        ORDER BY composite_rating DESC;
        """
    },
    22: {
        "title": "Q22: Head-to-head match prediction analysis between teams",
        "level": "Advanced",
        "sql": """
        SELECT 
            t1.team_name AS team_a,
            t2.team_name AS team_b,
            COUNT(m.match_id) AS total_matches,
            SUM(CASE WHEN m.winner_id = t1.team_id THEN 1 ELSE 0 END) AS team_a_wins,
            SUM(CASE WHEN m.winner_id = t2.team_id THEN 1 ELSE 0 END) AS team_b_wins,
            ROUND(AVG(CASE WHEN m.winner_id = t1.team_id THEN 100.0 ELSE 0.0 END), 1) AS team_a_win_pct
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        GROUP BY t1.team_id, t2.team_id
        HAVING total_matches >= 2
        ORDER BY total_matches DESC;
        """
    },
    23: {
        "title": "Q23: Recent player form and momentum category",
        "level": "Advanced",
        "sql": """
        SELECT 
            p.full_name AS player_name,
            COUNT(b.stat_id) AS matches_evaluated,
            ROUND(AVG(b.runs_scored), 2) AS recent_avg_runs,
            SUM(CASE WHEN b.runs_scored >= 50 THEN 1 ELSE 0 END) AS scores_above_50,
            CASE 
                WHEN AVG(b.runs_scored) >= 70 THEN 'Excellent Form'
                WHEN AVG(b.runs_scored) >= 40 THEN 'Good Form'
                WHEN AVG(b.runs_scored) >= 20 THEN 'Average Form'
                ELSE 'Poor Form'
            END AS form_status
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        GROUP BY p.player_id, p.full_name
        ORDER BY recent_avg_runs DESC;
        """
    },
    24: {
        "title": "Q24: Partnership success and milestone rankings",
        "level": "Advanced",
        "sql": """
        SELECT 
            p1.full_name || ' & ' || p2.full_name AS partnership_pair,
            COUNT(pr.partnership_id) AS total_partnerships,
            ROUND(AVG(pr.partnership_runs), 2) AS avg_partnership_runs,
            SUM(CASE WHEN pr.partnership_runs >= 50 THEN 1 ELSE 0 END) AS fifty_plus_stands,
            MAX(pr.partnership_runs) AS highest_partnership
        FROM partnerships pr
        JOIN players p1 ON pr.player1_id = p1.player_id
        JOIN players p2 ON pr.player2_id = p2.player_id
        GROUP BY p1.player_id, p2.player_id
        ORDER BY avg_partnership_runs DESC;
        """
    },
    25: {
        "title": "Q25: Career trajectory evolution and trajectory classification",
        "level": "Advanced",
        "sql": """
        SELECT 
            p.full_name AS player_name,
            strftime('%Y', b.match_date) AS career_year,
            ROUND(AVG(b.runs_scored), 2) AS yearly_avg,
            ROUND(SUM(b.runs_scored) * 100.0 / MAX(1, SUM(b.balls_faced)), 2) AS strike_rate,
            CASE 
                WHEN AVG(b.runs_scored) >= 60 THEN 'Career Ascending'
                WHEN AVG(b.runs_scored) >= 30 THEN 'Career Stable'
                ELSE 'Career Declining'
            END AS trajectory_phase
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        GROUP BY p.player_id, p.full_name, career_year
        ORDER BY p.full_name, career_year ASC;
        """
    }
}

def execute_query(query_id: int):
    """Executes a designated query by ID and returns DataFrame + SQL code."""
    query_info = QUERIES.get(query_id)
    if not query_info:
        return None, "Invalid query ID"
    
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query_info["sql"], conn)
    conn.close()
    return df, query_info["sql"]