import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


def send_email(jobs):
    body = "<h2>Нови executive позиции</h2>"

    for job in jobs:
        body += f"""
        <p>
            <b>{job.get('title', 'Без заглавие')}</b><br>
            {job.get('city', '')}<br>
            Source: {job.get('source', '')}<br>
            <a href="{job.get('link', '#')}">Отвори обявата</a><br>
            <small>{job.get('snippet', '')}</small>
        </p>
        <hr>
        """

    resend.Emails.send({
        "from": os.getenv("EMAIL_FROM"),
        "to": os.getenv("EMAIL_TO"),
        "subject": "Нови executive job alert линкове",
        "html": body
    })
