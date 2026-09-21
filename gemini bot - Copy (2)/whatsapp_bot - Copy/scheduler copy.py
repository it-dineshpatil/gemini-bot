import schedule
import time
from whatsapp_send_text import whatsapp_send_text
import json
import time
import requests
import array as arr

from datetime import date
from security import (
    erpnext_local,
    erpnext_local_key,
    erpnext_local_secret,
)


def remainder():
    url = f"{erpnext_local}/api/method/fetch_ticket.fetch_ticket"
    headers = {
        "Authorization": f"token {erpnext_local_key}:{erpnext_local_secret}",
        "Content-Type": "application/json",
    }
    params = {}

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()
if __name__ == "__main__":
    print(remainder())
# schedule.every().day.at("18:56").do(remainder)

# while True:
#     schedule.run_pending()
#     time.sleep(1)