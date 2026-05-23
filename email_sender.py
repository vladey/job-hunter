import yagmail
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(jobs):

    yag=yagmail.SMTP(
        os.getenv("EMAIL_USER"),
        os.getenv("EMAIL_PASS")
    )

    body="Нови позиции:\n\n"

    for job in jobs:

        body+=f"""
{job['title']}
{job['city']}
{job['link']}

"""

    yag.send(
        to="vladi.rusev@gmail.com",
        subject="Нови обяви",
        contents=body
    )