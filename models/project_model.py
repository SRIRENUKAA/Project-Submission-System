from database import mongo
from bson import ObjectId

class ProjectModel:
    @staticmethod
    def submit_project(student_email, title, description):
        project = {
            "student_email": student_email,
            "title": title,
            "description": description,
            "status": "Pending",
            "feedback": None,
            "grade": None
        }
        result = mongo.db.projects.insert_one(project)
        return str(result.inserted_id)

    @staticmethod
    def get_projects_for_faculty():
        return list(mongo.db.projects.find({"status": "Pending"}))

    @staticmethod
    def update_project_feedback(project_id, feedback, grade):
        mongo.db.projects.update_one(
            {"_id": ObjectId(project_id)},
            {"$set": {"feedback": feedback, "grade": grade, "status": "Reviewed"}}
        )

    @staticmethod
    def get_student_project(student_email):
        return list(mongo.db.projects.find({"student_email": student_email}))
