import os, json, sqlite3, logging
id INTEGER PRIMARY KEY,
timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
water_temp_1 REAL, water_temp_2 REAL,
air_temp_1 REAL, air_temp_2 REAL,
tds_ppm REAL
)
""")
conn.execute("""
CREATE TABLE IF NOT EXISTS tenmin_log(
id INTEGER PRIMARY KEY,
timestamp TIMESTAMP UNIQUE,
tds_ppm REAL, water_temp REAL
)
""")
return conn




def within_schedule(now: datetime) -> int:
hhmm = now.strftime('%H:%M')
for rng, waitm in SCHEDULE.items():
start, end = rng.split('-')
if start <= hhmm <= end:
return int(waitm)
# fallback
return min([int(v) for v in SCHEDULE.values()])




def auth_ok(req) -> bool:
if not TOKEN:
return True
return (req.headers.get('X-Api-Token') == TOKEN) or (req.args.get('token') == TOKEN)




# ---------- Routes ----------


@app.get('/')
def home():
return render_template('index.html')


@app.post('/sensor_data')
def sensor_data():
if not auth_ok(request):
return jsonify({'error':'unauthorized'}), 401
data = request.get_json(force=True)
conn = get_db()
conn.execute("""
INSERT INTO sensor_data(water_temp_1,water_temp_2,air_temp_1,air_temp_2,tds_ppm)
VALUES (?,?,?,?,?)
""", (
data.get('water_temp_1'), data.get('water_temp_2'),
data.get('air_temp_1'), data.get('air_temp_2'), data.get('tds')
))
conn.commit(); conn.close()
logging.info('sensor upload ok')
return {'status':'ok'}


@app.get('/api/state')
def api_state():
conn = get_db()
row = conn.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1").fetchone()
conn.close()
since = (datetime.now()-last_correction).total_seconds() if last_correction!=datetime.min else None
return jsonify({
'target_ec': TARGET_EC,
'schedule': SCHEDULE,
'kp': KP, 'ki': KI,
'last_correction_seconds_ago': since,
'corrections_total': correction_count,
'latest': {
'timestamp': row[1] if row else None,
'water_temp_1': row[2] if row else None,
'water_temp_2': row[3] if row else None,
'air_temp_1': row[4] if ro
