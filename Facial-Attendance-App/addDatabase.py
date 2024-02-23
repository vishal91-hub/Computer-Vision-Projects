import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{"databaseURL":"https://faceattendance-192c4-default-rtdb.firebaseio.com/"})

ref=db.reference("Employee")

data={
    "010891":
        {
            "name": "vishal singh",
            "major": "Robotics",
            "starting_year": 2012,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-02-21 00:54:34"
        },
    "160690":
        {
            "name": "Divya Raje Singh",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2024-02-21 00:34:34"
        },
        "101122":
        {
            "name": "Varrya Singh",
            "major": "Pareshan kerna",
            "starting_year": 2022,
            "total_attendance": 1,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2024-02-21 00:34:34"
        }}

for key, value in data.items():
    ref.child(key).set(value)