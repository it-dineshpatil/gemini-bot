import json
import requests
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

def ticket_fetch(from_number):
    params = {
        "filters": json.dumps([
            ["custom_whatsapp_number", "=", from_number],
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
    # print(response_data)
    
    # message = []
    # if response_data.get("data"):
    #     for ticket in response_data["data"]:
    #         message.append(
    #             f"ticket_Name: {ticket['name']}, "
    #             # f"Custom Raised By: {ticket.get('custom_raised', 'N/A')}, "
    #             f"subject: {ticket['subject']}, "
    #             f"status: {ticket['status']}, "
    #             f"remainder_date: {ticket.get('custom_remainder_date', 'N/A')}"
            # )
    # tickets = response_data.get("data", [])
    return response_data


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
    # print(response_data)
    
    if response_data.get("data"):
        for ticket in response_data["data"]:
            message=(
                f"ticket_Name: {ticket['name']}, "
                # f"Custom Raised By: {ticket.get('custom_raised', 'N/A')}, "
                f"subject: {ticket['subject']}, "
                f"status: {ticket['status']}, "
                f"remainder_date: {ticket.get('custom_remainder_date', 'N/A')}"
            )
    # tickets = response_data.get("data", [])
    return 
print(ticket_message("918140021166"))

              