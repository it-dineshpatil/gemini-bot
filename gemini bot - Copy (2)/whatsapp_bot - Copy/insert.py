import requests
import json
import os

from whatsapp_send_text import whatsapp_send_text
from security import (
    erpnext_local,
    erpnext_local_key,
    erpnext_local_secret
)
target_doctype = "Issue"
base_url = erpnext_local  # Assuming this is the base URL for your ERPNext instance

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
            "custom_regarding": data.get("custom_issue_regarding","hr"),
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

#Line Code Not Need THis Only  custom_file_attach Audio File  link frappe atual stock in  "File Manager" doctype in first after i am link attach field in "attachment" field in "Issue" doctype in erpnext

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

        # -----------------------------------
        # 6. WhatsApp response
        # -----------------------------------
        
        return whatsapp_send_text(
            from_number,
f"""
✅ Ticket #{docname}

📌Subject: {data.get('subject', 'N/A')}
📝Regarding: {data.get('custom_issue_regarding', 'N/A')}
📅Remainder Date: {data.get('custom_remainder_date', 'N/A')}
⭐Priority: {data.get('priority', 'N/A')}

🔗 Keep this ID for tracking
""")
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