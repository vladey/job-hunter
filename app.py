from scraper import search_jobs
from email_sender import send_email
import schedule
import time

print("APP STARTED")


def run():

    print("RUNNING SEARCH")

    jobs = search_jobs()

    print("FOUND JOBS:", len(jobs))

    if jobs:
        send_email(jobs)
        print("EMAIL SENT")

    print("Done")


schedule.every().day.at("08:00").do(run)
schedule.every().day.at("15:00").do(run)

run()

while True:
    schedule.run_pending()
    time.sleep(60)
