import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("service key.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://pbl-facerecognition-default-rtdb.firebaseio.com/"
})

ref =db.reference('students')

data={
    "210018":
        {
            "name":"Archita Raj",
            "dept":"CSE,BDA",
            "start_year":2021,
            "total_attendance":6,
            "remarks":"G",
            "year":3,
            "last_attendance_time":"24-04-2024 00:54:34"

        },
    "210019":
        {
            "name":"Vedika Singh",
            "dept":"CSE,BDA",
            "start_year":2021,
            "total_attendance":6,
            "remarks":"G",
            "year":3,
            "last_attendance_time":"24-04-2024 01:54:34"

        },
    "220056":
        {
            "name":"Bill gates",
            "dept":"CSE",
            "start_year":2022,
            "total_attendance":5,
            "remarks":"G",
            "year":2,
            "last_attendance_time":"24-04-2024 02:05:34"

        },
    "200009":
        {
            "name":"Elon musk",
            "dept":"CSE",
            "start_year":2020,
            "total_attendance":4,
            "remarks":"E",
            "year":4,
            "last_attendance_time":"24-04-2024 12:54:34"

        },
    "210023":
        {
            "name":"Navya Singhvi",
            "dept":"CSE,BDA",
            "start_year":2021,
            "total_attendance":8,
            "remarks":"G",
            "year":3,
            "last_attendance_time":"24-04-2024 10:50:14"


        },
    "210096":
        {
            "name":"Ria Singh",
            "dept":"CSE",
            "start_year":2021,
            "total_attendance":5,
            "remarks":"G",
            "year":3,
            "last_attendance_time":"24-04-2024 11:44:08 "
                                   ""

        }
}
for key,value in data.items():
    ref.child(key).set(value)