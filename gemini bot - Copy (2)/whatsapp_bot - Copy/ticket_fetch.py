import json
import time
import requests
import array as arr
from whatsapp_send_text  import whatsapp_send_text
from security import (
    erpnext_local,
    erpnext_local_key,
    erpnext_local_secret
)
target_doctype = "Issue"
base_url = erpnext_local


def get_headers():
    return {
        "Authorization": f"token {erpnext_local_key}:{erpnext_local_secret}",
        "Content-Type": "application/json",
    }
global send_message
def close_my_ticket(from_number):
    send_message= []
    ids = send_message if send_message else [""]
    params = {
        "filters": json.dumps([
            ["custom_whatsapp_number", "=", from_number],
            # ["name", "not in", ["ISS-2026-00106","ISS-2026-00088"]],
            ["status", "!=", "Closed"],
        ]),
        "order_by": "creation asc",
        "limit_page_length": 10,
        "fields": json.dumps([
            "name",
            "subject",
            "status",
            "custom_remainder_date",
            "custom_raised"
        ]),
    }
    response = requests.get(
        f"{base_url}/api/resource/{target_doctype}",
        headers=get_headers(),
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    # print(f"Response Status Code: {response}")
    response_data = response.json()
    
    

    # if response_data.get("data"):
    #     for ticket in response_data["data"]:
    #         send_message.append(
    #             # f"from_number {from_number}"
    #             f"ticket_Name: {ticket['name']}",

    #         )
    # tickets = response_data.get("data", [])
    # print(send_message)
#     return response_data
# print(close_my_ticket("918140021166").get("data")[0])
# for i in range(1):
#     data = []
#     data = close_my_ticket("918140021166")
    # print(data.get(data])
    # for ticket in data.get("name"):
    #     message =(
    #             f"🎫 Ticket ID:{ticket['name']}"
    #             # f"Custom Raised By: {ticket.get('custom_raised', 'N/A')}, "
    #             f"\n📌Subject:{ticket['subject']}, "
    #             # f"\n👨‍💼Regarding:{ticket['issue_type']}, "
    #             f"\n⚡ Status: {ticket['status']}, "
    #             f"\n⏰ Reminder: {ticket.get('custom_remainder_date', 'N/A')}"
    #             f"\n"
    #     )
    # print(message)

# if __name__ == "__main__":
# datas = ticket_fetch("918347089999")
# for data in datas:
#     print(data)









def ticket_message(from_number):
    params = {
        "filters": json.dumps([
            ["custom_whatsapp_number", "=", from_number],
            ["status", "!=", "Closed"],
        ]),
        "order_by": "creation asc",
        # "limit_page_length": 5,
        "fields": json.dumps([
            "name",
            "subject",
            "status",
            "custom_remainder_date",
            # "custom_raised",
            "issue_type"
        ]),
    }
    response = requests.get(
        f"{base_url}/api/resource/{target_doctype}",
        headers=get_headers(),
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    # print(f"Response Status Code: {response}")
    response_data = response.json()
    # print(response_data)
    
    message = []
    for ticket in response_data.get("data", []):
        message.append(
                f"🎫 Ticket ID:{ticket['name']}"
                # f"Custom Raised By: {ticket.get('custom_raised', 'N/A')}, "
                f"\n📌Subject:{ticket['subject']}, "
                f"\n👨‍💼Regarding:{ticket['issue_type']}, "
                f"\n⚡ Status: {ticket['status']}, "
                f"\n⏰ Reminder: {ticket.get('custom_remainder_date', 'N/A')}"
                f"\n"
        )
    for start in range(0, len(message), 10):
        batch = message[start:start + 10]
        numbered_batch = "\n".join(
            f"{start + position + 1}:{ticket}"
            for position, ticket in enumerate(batch)
        )

        whatsapp_send_text(from_number, numbered_batch)

        if start + 5 < len(message):
            print("More")
        
    if message:
        time.sleep(2)

    return whatsapp_send_text(
        from_number,
        "⚠️ *Notice:* Please close your old tickets if they are resolved.",
    )
# ticket_message("918140021166")

def assignes_ticket(from_number):
    params = {
        "filters": json.dumps([
            ["custom_regarding_whatsapp_number", "=", from_number],
            ["status", "!=", "Closed"],
        ]),
        "order_by": "creation asc",
        # "limit_page_length": 5,
        "fields": json.dumps([
            "name",
            "subject",
            "status",
            "custom_remainder_date",
            "custom_raised",
            # "issue_type"
        ]),
    }
    response = requests.get(
        f"{base_url}/api/resource/{target_doctype}",
        headers=get_headers(),
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    print(f"Response Status Code: {response}")
    response_data = response.json()
    print(response_data)
    
    message = []
    for ticket in response_data.get("data", []):
        message.append(
                # f"You are Assing Tickets",
                f"\n🎫 Ticket ID: {ticket['name']}"
                f"\n🖍 Raised By: {ticket.get('custom_raised', 'N/A')}, "
                f"\n📌 Subject: {ticket['subject']}, "
                # f"\n👨‍💼Regarding:{ticket['issue_type']}, "
                f"\n⚡ Status: {ticket['status']}, "
                f"\n⏰ Reminder: {ticket.get('custom_remainder_date', 'N/A')}"
                f"\n"
        )
    for start in range(0, len(message), 10):
        batch = message[start:start + 10]
        numbered_batch = "\n".join(
            f"{start + position + 1}:{ticket}"
            for position, ticket in enumerate(batch)
        )
        whatsapp_send_text(from_number, numbered_batch)

        if start + 5 < len(message):
            print("More")

    return message
# print(assignes_ticket("9140021166"))
             