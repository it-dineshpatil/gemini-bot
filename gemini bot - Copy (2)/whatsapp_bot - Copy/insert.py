import requests
import json
import os
from notication import regarding_pers
from notication import ticket_details_noti ,regarding_pers_audio_with
from whatsapp_send_text import whatsapp_send_text
from attachments import attach_files

from security import (
    erpnext_local,
    erpnext_local_key,
    erpnext_local_secret
)

target_doctype = "Issue"
base_url = erpnext_local  # Assuming this is the base URL for your ERPNext instance

def audio_reply(from_number, url):
    sender_name = create_by(from_number)
    if sender_name == "Unknown":
        print(f"Number {from_number} Not Registered ,  Please Contact IT Team.")
        return None
    
def meation_person_whatsapp(name):
    json_path = os.path.join(os.path.dirname(__file__), "number.json")
    with open(json_path,"r") as f:
        data = json.load(f)
    for number, username in data.items():
        if username == name:
            return number
        
def create_by(from_number):
        json_path = os.path.join(os.path.dirname(__file__), "number.json")
        with open(json_path, "r") as f:
            data = json.load(f)  
            return data.get(from_number)

def get_headers():
    return {
        "Authorization": f"token {erpnext_local_key}:{erpnext_local_secret}",
        "Content-Type": "application/json",
    }

def create_supplier_challan(data=None,from_number=None,audio_path=None):
    file_path = audio_path
    print(f"Creating ticket with data: {data} ,from_number={from_number}, audio_path={audio_path}")
  
    
    print(f"Creating ticket for number: {from_number} with data: {data} ,create_by(from_number)={create_by(from_number)}")
    try:
        # data = data or {}
        payload = {
            # "doctype": target_doctype,
            "subject": data.get("subject", ""),
            "issue_type": data.get("custom_issue_regarding",""),
            "custom_remainder_date": data.get("remainder_date", ""),
            "custom_regarding_whatsapp_number":meation_person_whatsapp(data.get("custom_issue_regarding","")),
            "priority": data.get("priority", ""),
            "custom_raised": create_by(from_number),
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
        # print(f"Created ticket with name: {docname},file_path")
    
    
        # doc_remainder_date = doc.get("remainder_date")
        
        if not docname:
            print("Document name not found")
            return whatsapp_send_text(
                from_number,
                "Ticket creation failed. Please try again later."
            )
        if not audio_path:
            regarding_pers(meation_person_whatsapp(data.get("custom_issue_regarding", "")),create_by(from_number),docname,data,)
            
            return ticket_details_noti(from_number, docname, data)
            
        url = attach_files(docname=docname, audio_path=file_path)
        regarding_pers_audio_with(meation_person_whatsapp(data.get("custom_issue_regarding", "")),create_by(from_number),docname,data,url)
        
        print(f"Attached audio file to ticket .............{docname}, file_path={file_path}, url={url}")
        return ticket_details_noti(from_number, docname, data)
    except Exception as e:

        print(f"ERPNext API Insertion error: {e}")

        return whatsapp_send_text(
            from_number,
            "Error while creating ticket. Please try again later."
        )

# create_supplier_challan(
#     data={
#         "subject": "Test Audio Ticket",
#         "custom_issue_regarding": "Dinesh It",
#         "remainder_date": "",
#         "priority": "Medium"
#     },)
#     sender_name=name("919327228987"),
#     from_number="919327228987",
#     audio_path=r"C:\gemini bot\Chatbot-audio-receive - Copy\whatsapp_bot - Copy\audio_file\919327228987.mp3"
# )


