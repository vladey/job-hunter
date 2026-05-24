from gmail_reader import get_job_emails
from email_sender import send_email

import schedule
import time

print("APP STARTED")


def run():

    print("READING GMAIL")

    jobs = get_job_emails()

    print("EMAILS FOUND:", len(jobs))

    if jobs:
        send_email(jobs)
        print("SUMMARY SENT")

    print("Done")


schedule.every().day.at("08:00").do(run)
schedule.every().day.at("15:00").do(run)

run()

while True:
    schedule.run_pending()
    time.sleep(60)
