import requests
from security import read_env

def whatsapp_send_text(to_number, message):
    env = read_env()

    send_text_url = "https://api.11za.in/apis/sendMessage/sendMessages"

    clean_number = "".join(char for char in str(to_number) if char.isdigit())

    if len(clean_number) == 10:
        clean_number = "91" + clean_number


    payload = {
        "authToken": env.get("WHATSAPP_TOKEN", ""),
        "sendto": clean_number,
        "originWebsite": "https://gokulprint.com/",
        "contentType": "text",
        "text": str(message),
    }
    send = requests.post(
        send_text_url,
        headers={
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )

    print(send.status_code)

    try:
        print(send.json())
        return send.json()
    
    except ValueError as e:
        print(send.text)
        print("Error parsing JSON response:", str(e))
        return send.text

# Explanation How to This Function Call
# whatsapp_send_text(
#     "8140021166",
#     "Hello, this is a test message from the WhatsApp API!"
# )
