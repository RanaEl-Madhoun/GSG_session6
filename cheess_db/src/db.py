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
conn.close()
print("Database built successfully!")

# 1. Connect to the existing database
conn = sqlite3.connect("f:/GSG26_Course/GSG_session6/cheess_db/data/chess.db")
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
# 3. Print the results
print("Tables found in database:", tables)
# 4. Always close the connection
conn.close()