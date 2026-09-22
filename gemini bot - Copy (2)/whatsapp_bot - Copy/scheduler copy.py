import schedule
import time
from whatsapp_send_text import whatsapp_send_text
import json
import time
import requests
import array as arr
from Template_send import close_ticket_noti_temp
from datetime import date
from security import (
    erpnext_local,
    erpnext_local_key,
    erpnext_local_secret,
)


def remainder_fetch():
    url = f"{erpnext_local}/api/method/fetch_ticket"
    headers = {
        "Authorization": f"token {erpnext_local_key}:{erpnext_local_secret}",
        "Content-Type": "application/json",
    }
    # params = {}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("message")

def call():
    for i in remainder_fetch():
        message = (
            f"🔔 *Reminder*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🆔 *Ticket ID:* {i.get('name')}\n\n"
            f"📝 *Subject:*\n"
            f"*{i.get('subject')}*\n\n"
            f"👤 *Regarding:* {i.get('issue_type')}\n\n"
            f"⏰ *Reminder Date:* {i.get('custom_remainder_date')}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📌 Please take the necessary action.")
        whatsapp_status = whatsapp_send_text("918140021166",message=message)
        if whatsapp_status != 200:
            close_ticket_noti_temp("918140021166",message=message
        )
            
schedule.every().day.at("14:55").do(call)
    
while True:
    schedule.run_pending()
    time.sleep(1)   