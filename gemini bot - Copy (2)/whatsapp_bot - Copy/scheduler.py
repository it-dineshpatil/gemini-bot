import schedule
import time

def test():
    print("Backup started")

schedule.every().day.at("19:36").do(test)

while True:
    schedule.run_pending()
    time.sleep(1)