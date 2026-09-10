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
        "fields": json.dumps([
            "name",
            "subject",
            "status",
            "custom_remainder_date",
        ]),
    }
    response = requests.get(
        f"{base_url}/api/resource/{target_doctype}",
        headers=get_headers(),
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    response_data = response.json()
    tickets = response_data.get("data", [])
    return tickets if tickets else None


if __name__ == "__main__":
    tickets = ticket_fetch("918140021166")
    if tickets:
        for ticket in tickets:
            print(f"Ticket Name: {ticket['name']}, Subject: {ticket['subject']}, Status: {ticket['status']}, Remainder Date: {ticket['custom_remainder_date']}")