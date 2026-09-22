import os
import json
import requests
from security import (
    erpnext_local,
    erpnext_local_key,
    erpnext_local_secret,
)
params ={
    "custom_raised":"Dinesh Software"
}
headers={
    "Authorization": f"token {erpnext_local_key}:{erpnext_local_secret}",
    "Content-Type": "application/json",
    }
def fetch_remainder_tickets():
    response = requests.get(
        f"{erpnext_local}/api/method/fetch_ticket",
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("message", data)


if __name__ == "__main__":
    for i in fetch_remainder_tickets():
        print(i.get("name"))