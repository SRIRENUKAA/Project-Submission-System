import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your Email Credentials (Use App Password instead of your regular password)
EMAIL_SENDER = "your-email@gmail.com"  # Replace with your Gmail
EMAIL_PASSWORD = "your-app-password"  # Replace with the 16-character App Password

# Function to send an email
def send_email(to_email, subject, message):
    try:
        # Setup Email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        # Connect to Gmail SMTP Server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Secure the connection
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)  # Use the App Password here
        server.sendmail(EMAIL_SENDER, to_email, msg.as_string())  # Send Email
        server.quit()
        
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")
