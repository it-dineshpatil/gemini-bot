import requests
import json
import os
from notication import regarding_pers
from notication import ticket_details_noti
from whatsapp_send_text import whatsapp_send_text
from security import (
    erpnext_local,
    erpnext_local_key,
    erpnext_local_secret
)
target_doctype = "Issue"
base_url = erpnext_local  # Assuming this is the base URL for your ERPNext instance

def meation_person_whatsapp(name):
    json_path = os.path.join(os.path.dirname(__file__), "number.json")
    with open(json_path,"r") as f:
        data = json.load(f)
    for number, username in data.items():
        if username == name:
            return number
        
def name(form_number):
    json_path = os.path.join(os.path.dirname(__file__), "number.json")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get(form_number, "Unknown")

# print(name("919327228987") or "Unknown")


def get_headers():
    return {
        "Authorization": f"token {erpnext_local_key}:{erpnext_local_secret}",
        "Content-Type": "application/json",
    }

def create_supplier_challan(data=None,sender_name=None,from_number=None, audio_path=None):
    try:
        data = data or {}
        payload = {
            "doctype": target_doctype,
            "subject": data.get("subject", ""),
            "issue_type": data.get("custom_issue_regarding","hr"),
            "custom_remainder_date": data.get("remainder_date", ""),
            "priority": data.get("priority", ""),
            "custom_raised": sender_name,
            "custom_whatsapp_number": from_number,
        }

        response = requests.post(
            f"{base_url}/api/resource/{target_doctype}",
            headers=get_headers(),
            json=payload,
            timeout=30,
        )
        response.raise_for_status()

        response_data = response.json()
        # print("Create Response:", response_data)
        
        doc = response_data.get("data", {})

        docname = doc.get("name")
        # doc_remainder_date = doc.get("remainder_date")
        
        if not docname:
            print("Document name not found")
            return whatsapp_send_text(
                from_number,
                "Ticket creation failed. Please try again later."
            )

        # print(f"Ticket Created: {docname}")
        if audio_path:
            if not os.path.exists(audio_path):
                print(f"File not found: {audio_path}")
            else:
                with open(audio_path, "rb") as audio_file:

                    file_response = requests.post(
                        f"{base_url}/api/method/upload_file",
                        headers={
                            "Authorization":
                                f"token {erpnext_local_key}:{erpnext_local_secret}"
                        },
                        files={
                            "file": audio_file
                        },
                        data={
                            "doctype": target_doctype,
                            "docname": docname,
                            "is_private": 1
                        },
                        timeout=60
                    )

                file_response.raise_for_status()
                file_data = file_response.json()
                # print("File Upload Response:", file_data)

                uploaded_file = file_data.get("message", {})

                file_url = uploaded_file.get("file_url")

                if file_url:
                    update_payload = {
                        "custom_files": file_url
                    }
                    update_response = requests.put(
                        f"{base_url}/api/resource/"
                        f"{target_doctype}/{docname}",
                        headers=get_headers(),
                        json=update_payload,
                        timeout=30
                    )

                    update_response.raise_for_status()

                    # print(
                    #     "Attach field updated:",
                    #     update_response.json()
                    # )

        
        if data.get("custom_issue_regarding"):
            meationwhatsapp = meation_person_whatsapp(data.get('custom_issue_regarding'))
            #whatsapp Message Send This Funcation
            regarding_pers(meationwhatsapp, sender_name, docname, data)
            # remainder_date = data.get("custom_remainder_date", "")
            
            
        return ticket_details_noti(from_number, docname, data, )

    except Exception as e:

        print(f"ERPNext API Insertion error: {e}")

        return whatsapp_send_text(
            from_number,
            "Error while creating ticket. Please try again later."
        )

# create_supplier_challan(
#     data={
#         "subject": "Test Audio Ticket",
#         "custom_issue_regarding": "HR",
#         "remainder_date": "",
#         "priority": "Medium"
#     },
#     sender_name=name("919327228987"),
#     from_number="919327228987",
#     audio_path=r"C:\gemini bot\Chatbot-audio-receive - Copy\whatsapp_bot - Copy\audio_file\919327228987.mp3"
# )


