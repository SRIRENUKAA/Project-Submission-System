<h1 align="center">📂 Project Submission System</h1>

A complete **Project Submission & Review System** using **Flask** and **MongoDB**, built for students to submit project details and for faculty to review, grade, and generate feedback PDFs.

---

### 🎯 Key Features

#### 🧑‍🎓 Student Side:
- Project submission form with email & faculty selection
- Confirmation page after submission
- View and download feedback/review as PDF

#### 👩‍🏫 Faculty Side:
- Signup/Login/Password reset (secured with case-insensitive name)
- Dashboard to view student submissions
- Provide grades, comments, and structured review
- Auto-generate downloadable PDF reviews
- Send feedback to student's email

---

### 🛠️ Technologies Used

- **Frontend:** HTML5, CSS3, Bootstrap
- **Backend:** Python (Flask)
- **Database:** MongoDB
- **PDF Generator:** ReportLab or WeasyPrint (via `pdf_generator.py`)
- **Authentication:** Basic session management
- **Email:** (If configured)

---

### 📁 Folder Structure

```bash
Project-Submission-System/
├── backend/
│   ├── app.py                # Main Flask application
│   ├── config.py             # App configs
│   ├── database.py           # MongoDB connection
│   ├── extensions.py         # Flask extensions setup
│
├── model/
│   └── project_model.py      # Data schema/models
│
├── routes/
│   ├── student_routes.py     # Student route handlers
│   └── faculty_routes.py     # Faculty route handlers
│
├── pdf generator/
│   └── pdf_generator.py      # Generates review PDFs
│
├── frontend/
│   ├── student_form.html
│   ├── submission_complete.html
│   ├── view.html
│   ├── faculty_login.html
│   ├── faculty_signup.html
│   ├── faculty_dashboard.html
│   ├── faculty_forgot_password.html
│   ├── faculty_reset_password.html
│   ├── project_list.html
│   ├── review_display.html
│   └── styles.css
│
└── README.md
