import schedule
import time

def job():
    print("Running scheduled job...")
    # Add your scheduled job logic here

schedule.every().day.at("01:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
