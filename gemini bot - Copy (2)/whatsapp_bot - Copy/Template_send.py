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
    
# chatbot("8140021166", "Test Subject", "Test Regarding", "2023-10-10", "High")


# {
#     "authToken": "U2FsdGVkX18YdKcPMX....",
#     "name": "Name of the Customer",
#     "sendto": "910000000000",
#     "originWebsite": "www.11za.com",
#     "templateName": "template_name",
#     "language": "en",
#     "buttonValue": "https://11za.com",//multiple button value => ["https://11za.com","https://11za.in"]
#     "headerdata": "headerdata", //required when header type is text with dynamic variable
#     "myfile": "", // add media URL
#     "myfileName" : "filename", //Specify the filename, visible on customer side
#     "data": [
#         "Test",
#         "test2"
#     ],
#     "tags": "ABC,DEF"
# }

def assigned_a_ticket(meationwhatsapp, sender_name: str, docname: str, data: dict, url: str = None):
    url = "https://api.11za.in/apis/template/sendTemplate"

    payload = {
        "authToken": (env.get("WHATSAPP_TOKEN")),
        "sendto": clean_mobile(meationwhatsapp),
        "originWebsite": "https://gokulprint.com/",
        "templateName": "chatbot",
        "language": "en",
        "data": [
            sender_name,
            docname,
            data.get('subject', 'N/A'),
            url if url else "N/A",
            data.get('custom_issue_regarding', 'N/A'),
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


