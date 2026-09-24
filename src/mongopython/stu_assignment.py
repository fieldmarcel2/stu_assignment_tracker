from pymongo import MongoClient
from flask import Flask, request
import json

app = Flask(__name__)

MONGO_URI = "mongodb+srv://tripathi20t_db_user:YcvNRnPnxRs1w1Jr@attendanceassign.sbapwws.mongodb.net/"
client= MongoClient(MONGO_URI)
db= client["attendance_tracker"]
collection= db["student"] 
print( "connected")


@app.post("/students")
def add_student():

    data = request.get_json()

    if not data:
        return json.dumps({
            "message": "request body is required"
        }), 400

    student_id = data.get("student_id")
    name = data.get("name")
    email = data.get("email")
    course = data.get("course")

    if not student_id or not name or not email or not course:
        return json.dumps({
            "message": "student_id, name, email and course are required"
        }), 400

    if collection.find_one({"email": email}):
        return json.dumps({
            "message": "your email is not unique"
        }), 409

    if collection.find_one({"student_id": student_id}):
        return json.dumps({
            "message": "student_id already exists"
        }), 409

    collection.insert_one({
        "student_id": student_id,
        "name": name,
        "email": email,
        "course": course,
        "assignments": []
    })

    return json.dumps({
        "message": "student added successfully"
    }), 201


@app.get("/students")
def get_student():

    student_list = list(
        collection.find({}, {"_id": 0})
    )

    return json.dumps(student_list), 200


@app.post("/students/<student_id>/assignments")
def add_assign(student_id):

    data = request.get_json()

    if not data:
        return json.dumps({
            "error": "Request body is required"
        }), 400

    title = data.get("title")
    score = data.get("score")

    #  title
    if not title:
        return json.dumps({
            "error": "title is required"
        }), 400

    if score is None:
        return json.dumps({
            "error": "score is required"
        }), 400

    if score < 0 or score > 100:
        return json.dumps({
            "error": "score must be between 0 and 100"
        }), 400

    student = collection.find_one({
        "student_id": student_id
    })

    if not student:
        return json.dumps({
            "message": "student not found"
        }), 404

    collection.update_one(
        {
            "student_id": student_id
        },
        {
            "$push": {
                "assignments": {
                    "title": title,
                    "score": score
                }
            }
        }
    )

    return json.dumps({
        "message": "assignment added successfully"
    }), 201


@app.get("/students/top-performers/<int:score>")
def top_performers(score):

    if score < 0 or score > 100:
        return json.dumps({
            "error": "score must be between 0 and 100"
        }), 400

    students = collection.find(
        {},
        {"_id": 0}
    )

    top_students = []

    for student in students:

        assignments = student.get("assignments", [])

        for assignment in assignments:

            if assignment["score"] >= score:

                top_students.append(student)

                break

    return json.dumps(top_students), 200


if __name__ == "__main__":
    app.run(debug=True)