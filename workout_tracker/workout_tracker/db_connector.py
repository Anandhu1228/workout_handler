import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / 'app_data.db'

class DBConnector:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.setup()

    def setup(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS daily_sessions (id INTEGER PRIMARY KEY, date TEXT, time TEXT, completed BOOLEAN)''')
        c.execute('''CREATE TABLE IF NOT EXISTS workout_logs (id INTEGER PRIMARY KEY, date TEXT, exercise TEXT, weight_type TEXT, weight_value REAL, summary TEXT, duration INT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS full_schedule (id INTEGER PRIMARY KEY, schedule_data TEXT)''')
        self.conn.commit()

    def has_worked_out_today(self, date_str):
        c = self.conn.cursor()
        c.execute("SELECT * FROM daily_sessions WHERE date=? AND completed=1", (date_str,))
        return c.fetchone() is not None

    def log_workout(self, date_str, exercise, w_type, w_val, summary, duration):
        c = self.conn.cursor()
        # BUG FIX: Check if entry already exists for this exercise TODAY.
        c.execute("SELECT id FROM workout_logs WHERE date=? AND exercise=?", (date_str, exercise))
        row = c.fetchone()
        
        if row:
            # Overwrite the old one
            c.execute("UPDATE workout_logs SET weight_type=?, weight_value=?, summary=?, duration=? WHERE id=?", 
                      (w_type, w_val, summary, duration, row['id']))
        else:
            # Create a new one
            c.execute("INSERT INTO workout_logs (date, exercise, weight_type, weight_value, summary, duration) VALUES (?, ?, ?, ?, ?, ?)", 
                      (date_str, exercise, w_type, w_val, summary, duration))
        self.conn.commit()

    def edit_log(self, log_id, w_type, w_val, summary):
        c = self.conn.cursor()
        c.execute("UPDATE workout_logs SET weight_type=?, weight_value=?, summary=? WHERE id=?", (w_type, w_val, summary, log_id))
        self.conn.commit()

    def mark_daily_complete(self, date_str, time_str):
        c = self.conn.cursor()
        c.execute("INSERT INTO daily_sessions (date, time, completed) VALUES (?, ?, 1)", (date_str, time_str))
        self.conn.commit()

    def get_history(self, exercise):
        c = self.conn.cursor()
        c.execute("SELECT id, date, weight_type, weight_value, summary FROM workout_logs WHERE exercise=? ORDER BY date DESC", (exercise,))
        return [dict(r) for r in c.fetchall()]

    def get_all_logs(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM workout_logs ORDER BY id DESC LIMIT 100")
        return [dict(r) for r in c.fetchall()]

    def save_full_schedule(self, schedule_dict):
        c = self.conn.cursor()
        c.execute("INSERT OR REPLACE INTO full_schedule (id, schedule_data) VALUES (1, ?)", (json.dumps(schedule_dict),))
        self.conn.commit()

    def get_full_schedule(self):
        c = self.conn.cursor()
        c.execute("SELECT schedule_data FROM full_schedule WHERE id=1")
        row = c.fetchone()
        return json.loads(row['schedule_data']) if row else None

db = DBConnector()