import sqlite3, pandas as pd, os
from datetime import datetime

DB = 'sensor_data.db'
ARCHIVE_DIR = 'archive'

os.makedirs(ARCHIVE_DIR, exist_ok=True)
conn = sqlite3.connect(DB)
df = pd.read_sql_query("SELECT * FROM sensor_data", conn)
conn.close()
if not df.empty:
    filename = datetime.now().strftime('%Y-%m-%d_%H%M') + '.csv'
    df.to_csv(os.path.join(ARCHIVE_DIR, filename), index=False)
    print("Archiviert:", filename)
else:
    print("Keine Daten gefunden")
