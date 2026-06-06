import sqlite3
import pandas as pd
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, '..', 'data', 'raw', 'chess_games.csv')
db_path = os.path.join(base_dir, '..', 'data', 'chess.db')

conn = sqlite3.connect(db_path)
df = pd.read_csv(csv_path)
df.to_sql('games', conn, if_exists='replace', index=False)
conn.commit()
print("Database built successfully!")

# ── Stage 1: SELECT ────────────────────────────────────────────────────────────

# Q1: How many total games are in the database? How many are rated?
q1 = conn.execute("""
    SELECT
        COUNT(*)                          AS total_games,
        SUM(CASE WHEN rated = 'TRUE' THEN 1 ELSE 0 END) AS rated_games
    FROM games;
""").fetchall()
print("\nQ1 - Total & Rated Games:", q1)

# Q2: List all distinct victory_status values and their counts
q2 = conn.execute("""
    SELECT victory_status, COUNT(*) AS count
    FROM games
    GROUP BY victory_status;
""").fetchall()
print("\nQ2 - Victory Status Counts:")
for row in q2:
    print(" ", row)

# Q3: Top 10 games with the most turns — show game_id, winner, turns
q3 = conn.execute("""
    SELECT game_id, winner, turns
    FROM games
    ORDER BY turns DESC
    LIMIT 10;
""").fetchall()
print("\nQ3 - Top 10 Games by Turns:")
for row in q3:
    print(" ", row)

# ── Stage 2: GROUP BY ──────────────────────────────────────────────────────────

# Q4: Win rate (%) for White, Black, and Draw across all games
q4 = conn.execute("""
    SELECT
        winner,
        COUNT(*) AS wins,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM games), 2) AS win_rate_pct
    FROM games
    GROUP BY winner;
""").fetchall()
print("\nQ4 - Win Rate by Winner:")
for row in q4:
    print(" ", row)

# Q5: For each victory_status — avg and max turns, sorted by highest avg first
q5 = conn.execute("""
    SELECT
        victory_status,
        ROUND(AVG(turns), 2) AS avg_turns,
        MAX(turns)           AS max_turns
    FROM games
    GROUP BY victory_status
    ORDER BY avg_turns DESC;
""").fetchall()
print("\nQ5 - Avg & Max Turns by Victory Status:")
for row in q5:
    print(" ", row)

# Q6: Top 5 opening_codes with more than 500 games
q6 = conn.execute("""
    SELECT opening_code, COUNT(*) AS total
    FROM games
    GROUP BY opening_code
    HAVING total > 500
    ORDER BY total DESC
    LIMIT 5;
""").fetchall()
print("\nQ6 - Top 5 Opening Codes (>500 games):")
for row in q6:
    print(" ", row)

conn.close()
