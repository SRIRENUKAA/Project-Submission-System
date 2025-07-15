from fpdf import FPDF
import os

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def generate_pdf(project):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add Student & Project Details
        pdf.cell(200, 10, txt=f"Project Title: {project.get('project_title', 'N/A')}", ln=True)
        pdf.cell(200, 10, txt=f"Student Name: {project.get('name', 'N/A')}", ln=True)
        pdf.cell(200, 10, txt=f"Student Email: {project.get('email', 'N/A')}", ln=True)
        pdf.multi_cell(0, 10, txt=f"Description: {project.get('description', 'N/A')}")

        # Save PDF File
        pdf_filename = os.path.join(UPLOAD_FOLDER, f"{project.get('name', 'Unknown')}_project.pdf")
        pdf.output(pdf_filename)

        return pdf_filename

    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None
