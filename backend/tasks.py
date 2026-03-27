import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

# Initialize Celery app
celery_app = Celery(
    "tasks",
    broker=os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

@celery_app.task
def send_async_email_otp(to_email, otp):
    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    smtp_user = os.environ.get("SMTP_USERNAME")
    smtp_pass = os.environ.get("SMTP_PASSWORD")

    if not smtp_server or not smtp_user or not smtp_pass:
        print(f"[Celery: send_async_email_otp] Missing SMTP config. Would send OTP {otp} to {to_email}")
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = to_email
        msg["Subject"] = "TrashTreasure Verification OTP"

        body = f"""Hello,
        
Your verification code for TrashTreasure is: {otp}

This code will expire in 10 minutes.

Thank you,
The TrashTreasure Team"""

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()

        print(f"[Celery] Successfully sent OTP to {to_email} via SMTP")
    except Exception as e:
        print(f"[Celery Error] Failed to send email to {to_email}: {str(e)}")
