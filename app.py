from flask import Flask, render_template, redirect, url_for
import os
from config import UPLOAD_FOLDER
from extensions import mongo, mail  # Import extensions from the new file

app = Flask(__name__)

# MongoDB URI and MongoDB Initialization
app.config["MONGO_URI"] = "mongodb+srv://srirenu2004:oDvtE1cUkcS4FgtW@cluster2.8yt1ddx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster2"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your_app_password'  # App password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'  # Replace with your email

# Initialize extensions
mongo.init_app(app)
mail.init_app(app)

# 🔑 Secret Key for Security
app.secret_key = "your_secret_key_here"

# 📁 Upload folder config
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Import routes only after app initialization
from routes.faculty_routes import faculty_routes
from routes.student_routes import student_routes  # Import after initialization

# Register Blueprints
app.register_blueprint(student_routes, url_prefix="/student")
app.register_blueprint(faculty_routes, url_prefix="/faculty")

# 🏠 Homepage Route
@app.route("/")
def home():
    return render_template("student_form.html")

# 🎓 Faculty Dashboard Route
@app.route("/dashboard")
def dashboard():
    return redirect(url_for("faculty_routes.faculty_dashboard"))

# 🚀 Run App
def create_app():
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
