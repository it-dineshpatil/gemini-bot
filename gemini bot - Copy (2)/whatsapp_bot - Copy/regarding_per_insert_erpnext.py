import requests
from security import (
    erpnext_local,
    erpnext_local_key,
    erpnext_local_secret
)

target_doctype = "Issue Type"
base_url = erpnext_local


def get_headers():
    return {
        "Authorization": f"token {erpnext_local_key}:{erpnext_local_secret}",
        "Content-Type": "application/json",
    }


def insert(phone, name):
    try:
        payload = {
            "doctype": target_doctype,
            "__newname": name,
            "description": phone,
        }

        response = requests.post(
            f"{base_url}/api/resource/{target_doctype}",
            headers=get_headers(),
            json=payload,
            timeout=30,
        )

        status =  response.status_code

        return status , response.text

    except requests.RequestException as e:
        return e


# respon = insert("8140021166", "Dinesh")
# print(respon[0])
