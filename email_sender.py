import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


def send_email(jobs):

    body = "<h2>Executive Job Alerts</h2><br>"

    for job in jobs:

        subject = job.get("subject", "No Subject")
        sender = job.get("from", "Unknown Sender")

        body += f"""
        <div style="margin-bottom:20px;">
            <b>{subject}</b><br>
            From: {sender}<br>
        </div>
        """

    resend.Emails.send({
        "from": os.getenv("EMAIL_FROM"),
        "to": os.getenv("EMAIL_TO"),
        "subject": "Executive Job Alerts Summary",
        "html": body
    })
