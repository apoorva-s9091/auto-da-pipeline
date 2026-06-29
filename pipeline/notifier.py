import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from utils.logger import logger

def send_email(report_path: str) -> None:
    print("\nEmail Notification Setup")
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    receiver = input("Enter recipient email: ").strip()
    
    if not sender or not password:
        logger.error("EMAIL_SENDER or EMAIL_PASSWORD not set in environment variables")
        print("Set these first:")
        print("  set EMAIL_SENDER=your@gmail.com")
        print("  set EMAIL_PASSWORD=your_app_password")
        return

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = "Auto-DA-Pipeline — Analysis Report Ready"

    body = "Your automated data analysis is complete. Report is attached."
    msg.attach(MIMEText(body, "plain"))

    # attach report file
    with open(report_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename=report.html")
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
            logger.info(f"Report emailed to {receiver}")
            print(f"Report sent to {receiver}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        print(f"Email failed: {e}")