import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


def send_email(jobs):
    body = "<h2>Нови позиции</h2>"

    for job in jobs:
        body += f"""
        <p>
        <b>{job['title']}</b><br>
        {job['city']}<br>
        <a href="{job['link']}">Отвори обявата</a>
        </p>
        """

    resend.Emails.send({
        "from": os.getenv("EMAIL_FROM"),
        "to": [os.getenv("EMAIL_TO")],
        "subject": "Нови обяви",
        "html": body
    })
