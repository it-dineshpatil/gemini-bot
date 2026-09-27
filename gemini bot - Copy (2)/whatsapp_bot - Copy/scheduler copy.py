import schedule
import time
from whatsapp_send_text import whatsapp_send_text
import json
import time
import requests
import array as arr
from Template_send import remainder_message_per , remainder_message
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
        f"You are assigned a Task Reminder\n"
        f"👤 Created By: *{i.get('custom_raised')}*\n"
        f"🆔 Ticket ID: *{i.get('name')}*\n"
        f"📌 Subject: *{i.get('subject')}*\n"
        f"📅 Reminder Date: {i.get('custom_remainder_date')}\n"
        f"⭐ Priority: {i.get('priority')}\n\n"
        f"🔗 Keep this ID for tracking.\n"
        f"⚠️ Action Required: Please take necessary action."
)
        whatsapp_status = whatsapp_send_text(i.get("custom_regarding_whatsapp_number"),message=message)
        if whatsapp_status != 200:
            remainder_message_per(i)
        tital = "Pending Task Reminder"
        brand = "Power By Gokul Text Print"
        per_message = (
        f"*{tital}*\n\n"
        f"🆔 Ticket ID: *{i.get('name')}*\n"
        f"📌 Subject: *{i.get('subject')}*\n"
        f"👤 Regarding: *{i.get('issue_type')}*\n"
        f"📅 Reminder Date: {i.get('custom_remainder_date')}\n"
        f"⭐ Priority: {i.get('priority')}\n\n"
        f"🔗 Keep this ID for tracking.\n"
        f"⚠️Action Required: Please take the necessary action.\n\n"
        f"*{brand}*"
        )
        whatsapp_status = whatsapp_send_text(i.get("custom_whatsapp_number"),message=per_message)
        if whatsapp_status != 200:
            remainder_message(i)
            
# print(call())         
schedule.every().day.at("10:30").do(call)
    
while True:
    schedule.run_pending()
    time.sleep(1)   