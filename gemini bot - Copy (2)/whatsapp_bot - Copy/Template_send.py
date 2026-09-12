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
