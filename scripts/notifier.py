"""
notifier.py
Send a confirmation email via Gmail SMTP after a reel is published.
Usage: python notifier.py "<subject>" "<body>"
"""
import sys, os, smtplib
from email.mime.text import MIMEText

GMAIL_USER     = os.environ["GMAIL_USER"]
GMAIL_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
NOTIFY_EMAIL   = os.environ["NOTIFY_EMAIL"]

def send_email(subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"]    = GMAIL_USER
    msg["To"]      = NOTIFY_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_PASSWORD)
        smtp.sendmail(GMAIL_USER, NOTIFY_EMAIL, msg.as_string())
    print("Email sent.")

if __name__ == "__main__":
    subject = sys.argv[1] if len(sys.argv) > 1 else "Reel Published"
    body    = sys.argv[2] if len(sys.argv) > 2 else "Your Instagram Reel has been posted."
    send_email(subject, body)
