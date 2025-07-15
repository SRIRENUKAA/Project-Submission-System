from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, Response, jsonify
from database import get_projects_collection, get_faculty_collection, get_reviews_collection
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from fpdf import FPDF
import secrets
import unicodedata

faculty_routes = Blueprint("faculty_routes", __name__, url_prefix="/faculty")


# ✅ Get Faculty Names for Dropdown
@faculty_routes.route("/get_faculty_names", methods=["GET"])
def get_faculty_names():
    faculties = get_faculty_collection()
    faculty_list = [faculty["name"] for faculty in faculties.find({}, {"_id": 0, "name": 1})]
    return jsonify(faculty_list)

# ✅ Faculty Signup
@faculty_routes.route("/signup", methods=["GET", "POST"])
def faculty_signup():
    faculties = get_faculty_collection()

    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"].strip()

        existing_faculty = faculties.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
        if existing_faculty:
            flash("❌ Faculty name already exists!", "danger")
            return redirect(url_for("faculty_routes.faculty_signup"))

        hashed_password = generate_password_hash(password)
        faculties.insert_one({"name": name, "email": email, "password": hashed_password})

        flash("✅ Signup successful! Please login.", "success")
        return redirect(url_for("faculty_routes.faculty_login"))

    return render_template("faculty_signup.html")

# ✅ Faculty Login
@faculty_routes.route("/login", methods=["GET", "POST"])
def faculty_login():
    faculties = get_faculty_collection()

    if request.method == "POST":
        name = request.form["name"].strip()
        password = request.form["password"].strip()

        faculty = faculties.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})

        if faculty and check_password_hash(faculty["password"], password):
            session["faculty_name"] = faculty["name"]
            flash("✅ Login successful!", "success")
            return redirect(url_for("faculty_routes.faculty_dashboard"))
        else:
            flash("❌ Invalid name or password!", "danger")

    return render_template("faculty_login.html")

# ✅ Faculty Forgot Password
@faculty_routes.route("/forgot_password", methods=["GET", "POST"])
def faculty_forgot_password():
    faculties = get_faculty_collection()

    if request.method == "POST":
        email = request.form["email"].strip().lower()
        faculty = faculties.find_one({"email": email})

        if not faculty:
            flash("❌ No account found with this email!", "danger")
            return redirect(url_for("faculty_routes.faculty_forgot_password"))

        reset_token = secrets.token_urlsafe(32)
        faculties.update_one({"email": email}, {"$set": {"reset_token": reset_token}})

        reset_url = url_for("faculty_routes.faculty_reset_password", token=reset_token, _external=True)
        msg = Message("🔒 Reset Your Password",
                      sender=current_app.config.get("MAIL_USERNAME"),
                      recipients=[email])
        msg.body = f"Click the link below to reset your password:\n\n{reset_url}\n\nIf you didn't request this, ignore this email."

        try:
            mail.send(msg)
            flash("✅ Password reset link sent! Check your email.", "success")
        except Exception as e:
            flash(f"⚠️ Failed to send email: {str(e)}", "danger")

        return redirect(url_for("faculty_routes.faculty_login"))

    return render_template("faculty_forgot_password.html")

# ✅ Faculty Reset Password
def remove_non_ascii(text):
    if text:
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return ""

@faculty_routes.route("/download_pdf/<project_id>")
def download_pdf(project_id):
    if "faculty_name" not in session:
        flash("❌ Please login first!", "danger")
        return redirect(url_for("faculty_routes.faculty_login"))

    projects = get_projects_collection()
    
    try:
        project = projects.find_one({"_id": ObjectId(project_id)})
        if not project:
            flash("❌ Project not found!", "danger")
            return redirect(url_for("faculty_routes.faculty_dashboard"))
    except:
        flash("❌ Invalid Project ID!", "danger")
        return redirect(url_for("faculty_routes.faculty_dashboard"))

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Writing content to PDF using ASCII-safe text
    pdf.cell(200, 10, txt=remove_non_ascii("Project Report"), ln=True, align="C")
    pdf.ln(10)

    pdf.cell(200, 10, txt=remove_non_ascii(f"Title: {project.get('project_title', '')}"), ln=True)
    pdf.cell(200, 10, txt=remove_non_ascii(f"Student: {project.get('name', '')}"), ln=True)
    pdf.cell(200, 10, txt=remove_non_ascii(f"Email: {project.get('email', '')}"), ln=True)
    pdf.cell(200, 10, txt=remove_non_ascii(f"Faculty: {project.get('faculty', '')}"), ln=True)

    # Create response
    response = Response(pdf.output(dest="S").encode("latin1"))
    response.headers["Content-Disposition"] = f"attachment; filename=project_{str(project_id)}.pdf"
    response.headers["Content-Type"] = "application/pdf"

    return response

@faculty_routes.route("/dashboard")
def faculty_dashboard():
    if "faculty_name" not in session:
        flash("❌ Please login first!", "danger")
        return redirect(url_for("faculty_routes.faculty_login"))

    # Get the faculty's name from session
    faculty_name = session["faculty_name"]

    # Fetch projects submitted to this faculty
    projects = get_projects_collection()
    faculty_projects = projects.find({"faculty": {"$regex": f"^{faculty_name}$", "$options": "i"}})

    return render_template("faculty_dashboard.html", projects=faculty_projects, faculty_name=faculty_name)

@faculty_routes.route('/download_file/<project_id>', methods=['GET'])
def download_uploaded_file(project_id):
    # Your logic for downloading the file here
    pass

@faculty_routes.route('/submit_feedback/<project_id>', methods=['POST'])
def submit_feedback(project_id):
    reviews_collection = get_reviews_collection()

    # Get form data
    feedback_data = {
        'project_id': project_id,
        'usability': request.form['usability'],
        'scalability': request.form['scalability'],
        'security': request.form['security'],
        'documentation': request.form['documentation'],
        'industry_relevance': request.form['industry_relevance'],
        'grade': request.form['grade'],
        'final_comments': request.form['final_comments'],
        'rating': request.form['rating']
    }

    # Insert into MongoDB
    reviews_collection.insert_one(feedback_data)

    # Redirect after submission (to faculty dashboard or wherever needed)
    return redirect(url_for('student_routes.view_review', project_id=project_id))
