import schedule
import time
import app

schedule.every().day.at("08:00").do(app)
schedule.every().day.at("15:00").do(app)

while True:

    schedule.run_pending()
    time.sleep(60)