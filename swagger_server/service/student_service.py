import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/school")

client = MongoClient(MONGO_URI)
db = client["school"]
students_collection = db["students"]


def add(student=None):
    try:
        student_id = int(student.student_id)

        if students_collection.find_one({"_id": student_id}):
            return "already exists", 409

        student_dict = student.to_dict()
        student_dict["_id"] = student_id
        del student_dict["student_id"]

        # Insert into MongoDB
        students_collection.insert_one(student_dict)

        return student_id

    except ValueError:
        return "Invalid ID format (must be an integer)", 400
    except Exception as e:
        return str(e), 500


def get_by_id(student_id=None, subject=None):
    try:
        student_id = int(student_id)
        student = students_collection.find_one({"_id": student_id})

        if not student:
            return "not found", 404

        student["student_id"] = student["_id"]
        del student["_id"]
        return student
    except ValueError:
        return "Invalid ID format", 400
    except Exception as e:
        return str(e), 500


def delete(student_id=None):
    try:
        student_id = int(student_id)
        result = students_collection.delete_one({"_id": student_id})

        if result.deleted_count == 0:
            return "not found", 404

        return student_id
    except ValueError:
        return "Invalid ID format", 400
    except Exception as e:
        return str(e), 500