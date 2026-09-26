import requests
from security import read_env

env= read_env()

def clean_mobile(to_number):
    clean_number = "".join(char for char in str(to_number) if char.isdigit())
    if len(clean_number) == 10:
        clean_number = "91" + clean_number
    return clean_number

def chatbot(to_number, subject, regarding, remainder_date, priority):
    url = "https://api.11za.in/apis/template/sendTemplate"

    payload = {
        "authToken": (env.get("WHATSAPP_TOKEN")),
        "sendto": clean_mobile(to_number),
        "originWebsite": "https://gokulprint.com/",
        "templateName": "chatbot",
        "language": "en",
        "data": [
            subject,
            regarding,
            remainder_date,
            priority
        ],

    }

    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=30
    )

    print(response.status_code)
    try:
        print(response.json())
        return response.json()
    except ValueError:
        print(response.text)
        return response.text
    


def assigned_a_ticket(meationwhatsapp, sender_name: str, docname: str, data: dict, audio_link: str = None):
    url = "https://api.11za.in/apis/template/sendTemplate"

    payload = {
        "authToken": (env.get("WHATSAPP_TOKEN")),
        "sendto": clean_mobile(meationwhatsapp),
        "originWebsite": "https://gokulprint.com/",
        "templateName": "assigned_a_ticket",
        "language": "en",
        "data": [
            sender_name,
            docname,
            data.get('subject', 'N/A'),
            audio_link or "None",
            data.get('custom_remainder_date', 'N/A'),
            data.get('priority', 'N/A')
        ],

    }

    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=30
    )

    print(response.status_code)
    try:
        print(response.json())
        return response.json()
    except ValueError:
        print(response.text)
        return response.text


def close_ticket_noti_temp(from_number, message):
    url = "https://api.11za.in/apis/template/sendTemplate"

    payload = {
        "authToken": (env.get("WHATSAPP_TOKEN")),
        "sendto": clean_mobile(from_number),
        "originWebsite": "https://gokulprint.com/",
        "templateName": "remainder",
        "language": "en",
        "data": [
            message
        ],

    }

    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=30
    )

    print(response.status_code)
    try:
        print(response.json())
        return response.json()
    except ValueError:
        print(response.text)
        return response.text
    
def remainder_message_per(i):
    url = "https://api.11za.in/apis/template/sendTemplate"

    payload = {
        "authToken": (env.get("WHATSAPP_TOKEN")),
        "sendto": clean_mobile(i.get("custom_regarding_whatsapp_number")),
        # "sendto": "918140021166",
        "originWebsite": "https://gokulprint.com/",
        "templateName": "assigned_a_ticket_remainder",
        "language": "en",
        "data": [
            i.get('custom_raised'),
            i.get('name'),
           i.get('subject'),
            i.get('custom_remainder_date'),
            i.get('priority'),
            
        ],

    }

    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=30
    )

    print(response.status_code)
    try:
        print(response.json())
        return response.json()
    except ValueError:
        print(response.text)
        return response.text
    
def remainder_message(i):
    # data = i
    url = "https://api.11za.in/apis/template/sendTemplate"

    payload = {
        "authToken": (env.get("WHATSAPP_TOKEN")),
        # "sendto": clean_mobile(i.get("custom_whatsapp_number")),
        "sendto": "918140021166",
        "originWebsite": "https://gokulprint.com/",
        "templateName": "assigned_a_ticket_remainder_copy",
        "language": "en",
        "data": [
             i.get('name'),
             i.get('subject'),
            i.get('custom_raised'),
            i.get('custom_remainder_date'),
            i.get('priority'),
            
        ],

    }

    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=30
    )

    print(response.status_code)
    try:
        print(response.json())
        return response.json()
    except ValueError:
        print(response.text)
        return response.text
# close_ticket_noti(from_number="918140021166", message="Your ticket has been closed.")