import imaplib
import email
import os
from email.header import decode_header
from dotenv import load_dotenv

load_dotenv()


def get_job_emails():

    user = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_APP_PASSWORD")

    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    imap.login(user, password)

    imap.select("INBOX")

    status, messages = imap.search(
        None,
        '(OR FROM "jobs.bg" FROM "linkedin.com")'
    )

    email_ids = messages[0].split()

    results = []

    for mail_id in email_ids[-20:]:

        _, msg_data = imap.fetch(mail_id, "(RFC822)")

        for response_part in msg_data:

            if not isinstance(response_part, tuple):
                continue

            msg = email.message_from_bytes(response_part[1])

            subject, encoding = decode_header(msg["Subject"])[0]

            if isinstance(subject, bytes):
                subject = subject.decode(
                    encoding if encoding else "utf-8"
                )

            sender = msg.get("From")

            results.append({
                "subject": subject,
                "from": sender
            })

    imap.logout()

    return results
