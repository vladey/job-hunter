from scraper import search_jobs
from email_sender import send_email
import schedule
import time

def run():

    jobs=search_jobs()

    if jobs:
        send_email(jobs)

    print("Done")

schedule.every().day.at("08:00").do(run)
schedule.every().day.at("15:00").do(run)

run()

while True:
    schedule.run_pending()
    time.sleep(60)