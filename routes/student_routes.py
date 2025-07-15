from flask import Blueprint, request, render_template, redirect, url_for
from database import projects_collection
from bson.objectid import ObjectId
from bson.errors import InvalidId
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER
from emails.send_email import send_email
from flask import send_from_directory
import os
from flask import redirect, url_for, flash
from flask import jsonify
from database import projects_collection
from extensions import mongo
import logging

student_routes = Blueprint("student_routes", __name__)

# ✅ Student project submission form
@student_routes.route("/submit", methods=["GET", "POST"])
def submit_project():
    if request.method == "POST":
        data = request.form.to_dict()
        data["team_members"] = request.form.getlist("team_members[]")

        email = data.get("email")
        project_title = data.get("project_title")

        # Check if project exists
        existing_project = projects_collection.find_one({
            "email": email,
            "project_title": project_title
        })

        file = request.files.get("project_file")
        if file and file.filename != "":
            filename = secure_filename(file.filename)

            # Create uploads folder if not exists
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            data["project_file"] = filename
            data["file_path"] = file_path  # store full path for download

        if existing_project:
            projects_collection.update_one(
                {"_id": existing_project["_id"]},
                {"$set": data}
            )
        else:
            projects_collection.insert_one(data)

        send_email(email, "Project Submission Received", "Your project has been submitted successfully.")
        return redirect(url_for("student_routes.submission_complete"))

    return render_template("student_form.html")


# ✅ Project Submission Complete Page
@student_routes.route("/submission_complete")
def submission_complete():
    return render_template("submission_complete.html")

# Route to render email input page
@student_routes.route('/view', methods=['GET'])
def view_project_form():
    return render_template('view.html')

# Route to fetch and display projects
@student_routes.route('/view/projects', methods=['GET'])
def view_projects():
    email = request.args.get('email')

    if not email:
        return "Email not provided", 400

    try:
        project_cursor = projects_collection.find({"email": email})
        project_list = list(project_cursor)  # Safely convert to list
    except Exception as e:
        return f"Database error: {e}", 500

    return render_template('project_list.html', projects=project_list)

@student_routes.route('/download/<filename>')
def download_file(filename):
    uploads_path = os.path.join(os.getcwd(), 'uploads')  # Absolute path to uploads/
    return send_from_directory(uploads_path, filename, as_attachment=True)

@student_routes.route("/project_form/<project_id>", methods=["GET", "POST"])
def edit_project_form(project_id):
    if request.method == "POST":
        updated_data = request.form.to_dict()

        # ✅ Important: Ensure team_members is correctly handled as a list
        updated_data["team_members"] = request.form.getlist("team_members[]")

        # ✅ Optional: Handle file update
        if 'project_file' in request.files:
            file = request.files['project_file']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                updated_data['project_file'] = filename

        projects_collection.update_one(
            {"_id": ObjectId(project_id)},
            {"$set": updated_data}
        )

        return redirect(url_for("student_routes.view_projects", email=updated_data["email"]))

    # GET request: Load form with existing project data
    project = projects_collection.find_one({"_id": ObjectId(project_id)})
    return render_template("student_form.html", project=project)

@student_routes.route('/student/delete_project/<project_id>', methods=['POST'])
def delete_project(project_id):
    try:
        result = projects_collection.delete_one({"_id": ObjectId(project_id)})
        if result.deleted_count == 1:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Project not found"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

# Enable logging for better debugging
logging.basicConfig(level=logging.DEBUG)
@student_routes.route('/view_review/<project_id>')
def view_review(project_id):
    try:
        # Try converting the project_id into ObjectId
        try:
            obj_id = ObjectId(project_id)
        except InvalidId:
            return render_template('review_display.html', message="Invalid project ID.")

        # Fetching the project from projects collection
        project = mongo.db.projects.find_one({'_id': obj_id})
        print("Project:", project)  # Add this to check project data

        # Fetching the review from reviews collection
        review = mongo.db.reviews.find_one({'project_id': project_id})
        print("Review:", review)  # Add this to check review data

        if project:
            # Add review into project data (optional chaining for review)
            project['review'] = review.get('review', 'No review found') if review else 'No review found'
            return render_template('review_display.html', project=project)
        else:
            return render_template('review_display.html', message="Project not found.")
    
    except Exception as e:
        print("Error occurred:", e)  # For debugging purposes
        return render_template('review_display.html', message="An error occurred while fetching the review.")
