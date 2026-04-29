import sqlite3
import json
import os

# Connect directly to the SQLite database
db_path = os.path.join(os.path.dirname(__file__), 'app_data.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Your precise, corrected schedule
my_schedule = {
    "0": [ # MONDAY
        {"name": "Cross Climber (Abs)", "sets": 1, "reps": "60s max", "rest": 0, "rest_after": 15, "video": ""},
        {"name": "Leg Raise (Abs)", "sets": 1, "reps": "60s max", "rest": 0, "rest_after": 15, "video": ""},
        {"name": "Crusifix Crunches (Abs)", "sets": 1, "reps": "60s max", "rest": 0, "rest_after": 15, "video": ""},
        {"name": "Russian Twist (Abs)", "sets": 1, "reps": "60s max", "rest": 0, "rest_after": 15, "video": ""},
        {"name": "Ablique Crunches Type 1 (Abs)", "sets": 1, "reps": "60s max", "rest": 0, "rest_after": 240, "video": ""},
        {"name": "Two Arm Dumbbell Rows", "sets": 3, "reps": "6-10", "rest": 90, "rest_after": 240, "video": ""},
        {"name": "Floor Dumbbell Pullover", "sets": 2, "reps": "8-12", "rest": 60, "rest_after": 240, "video": ""},
        {"name": "Biceps Curl (Both arms)", "sets": 2, "reps": "8-12", "rest": 60, "rest_after": 240, "video": ""},
        {"name": "Hammer Curl", "sets": 2, "reps": "8-12", "rest": 60, "rest_after": 240, "video": ""}
    ],
    "1": [ # TUESDAY
        {"name": "Standing Behind Back Curl (Forearms)", "sets": 1, "reps": "15-20", "rest": 0, "rest_after": 15, "video": ""},
        {"name": "Waiter Curl (Forearms)", "sets": 1, "reps": "15-20", "rest": 0, "rest_after": 15, "video": ""},
        {"name": "Reverse Curl (Forearms)", "sets": 1, "reps": "15-20", "rest": 0, "rest_after": 240, "video": ""},
        {"name": "Floor Dumbbell Press", "sets": 3, "reps": "6-10", "rest": 90, "rest_after": 240, "video": ""},
        {"name": "Floor Dumbbell Fly", "sets": 2, "reps": "8-12", "rest": 60, "rest_after": 240, "video": ""},
        {"name": "Floor Skull Crushers", "sets": 2, "reps": "8-12", "rest": 60, "rest_after": 240, "video": ""},
        {"name": "Dumbbell Overhead Extension", "sets": 2, "reps": "8-12", "rest": 60, "rest_after": 240, "video": ""}
    ],
    "2": [ # WEDNESDAY
        {"name": "Goblet Squat", "sets": 3, "reps": "6-10", "rest": 90, "rest_after": 240, "video": ""},
        {"name": "Dumbbell Romanian Deadlift (RDL)", "sets": 3, "reps": "8-12", "rest": 120, "rest_after": 240, "video": ""},
        {"name": "Seated Dumbbell Shoulder Press", "sets": 3, "reps": "6-10", "rest": 90, "rest_after": 240, "video": ""},
        {"name": "Lateral Raise", "sets": 3, "reps": "8-12", "rest": 60, "rest_after": 240, "video": ""},
        {"name": "Reverse Fly (Rear Delt)", "sets": 2, "reps": "8-12", "rest": 60, "rest_after": 240, "video": ""}
    ],
    "3": [ # THURSDAY
        {"name": "V In and Out (Abs)", "sets": 1, "reps": "60s max", "rest": 0, "rest_after": 15, "video": ""},
        {"name": "Flutter Kick (Abs)", "sets": 1, "reps": "60s max", "rest": 0, "rest_after": 15, "video": ""},
        {"name": "Star Crunches (Abs)", "sets": 1, "reps": "60s max", "rest": 0, "rest_after": 15, "video": ""},
        {"name": "Bicycle Crunches (Abs)", "sets": 1, "reps": "60s max", "rest": 0, "rest_after": 15, "video": ""},
        {"name": "Oblique Crunches (Abs)", "sets": 1, "reps": "60s max", "rest": 0, "rest_after": 240, "video": ""},
        {"name": "Two Arm Dumbbell Rows", "sets": 3, "reps": "6-10", "rest": 90, "rest_after": 240, "video": ""},
        {"name": "Floor Dumbbell Pullover", "sets": 2, "reps": "8-12", "rest": 60, "rest_after": 240, "video": ""},
        {"name": "Biceps Curl (Both arms)", "sets": 2, "reps": "8-12", "rest": 60, "rest_after": 240, "video": ""},
        {"name": "Hammer Curl", "sets": 2, "reps": "8-12", "rest": 60, "rest_after": 240, "video": ""}
    ],
    "4": [ # FRIDAY
        {"name": "Standing Behind Back Curl (Forearms)", "sets": 1, "reps": "15-20", "rest": 0, "rest_after": 15, "video": ""},
        {"name": "Waiter Curl (Forearms)", "sets": 1, "reps": "15-20", "rest": 0, "rest_after": 15, "video": ""},
        {"name": "Reverse Curl (Forearms)", "sets": 1, "reps": "15-20", "rest": 0, "rest_after": 240, "video": ""},
        {"name": "Floor Dumbbell Press", "sets": 3, "reps": "6-10", "rest": 90, "rest_after": 240, "video": ""},
        {"name": "Floor Dumbbell Fly", "sets": 2, "reps": "8-12", "rest": 60, "rest_after": 240, "video": ""},
        {"name": "Floor Skull Crushers", "sets": 2, "reps": "8-12", "rest": 60, "rest_after": 240, "video": ""},
        {"name": "Dumbbell Overhead Extension", "sets": 2, "reps": "8-12", "rest": 60, "rest_after": 240, "video": ""}
    ],
    "5": [ # SATURDAY
        {"name": "Goblet Squat", "sets": 3, "reps": "6-10", "rest": 90, "rest_after": 240, "video": ""},
        {"name": "Dumbbell Romanian Deadlift (RDL)", "sets": 3, "reps": "8-12", "rest": 120, "rest_after": 240, "video": ""},
        {"name": "Seated Dumbbell Shoulder Press", "sets": 3, "reps": "6-10", "rest": 90, "rest_after": 240, "video": ""},
        {"name": "Lateral Raise", "sets": 3, "reps": "8-12", "rest": 60, "rest_after": 240, "video": ""},
        {"name": "Reverse Fly (Rear Delt)", "sets": 2, "reps": "8-12", "rest": 60, "rest_after": 240, "video": ""}
    ],
    "6": [ # SUNDAY
        {"name": "Rest Day - Stretch Only", "sets": 1, "reps": "-", "rest": 0, "rest_after": 0, "video": ""}
    ]
}

# Ensure the table exists and insert the data
c.execute('''CREATE TABLE IF NOT EXISTS full_schedule (id INTEGER PRIMARY KEY, schedule_data TEXT)''')
c.execute("INSERT OR REPLACE INTO full_schedule (id, schedule_data) VALUES (1, ?)", (json.dumps(my_schedule),))
conn.commit()
print("Success: Your completely corrected, full personal schedule has been securely injected into the database.")