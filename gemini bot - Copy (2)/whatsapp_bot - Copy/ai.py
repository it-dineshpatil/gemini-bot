import json
import os
import sys
import time
from google import genai
from numpy import number
from google.genai import types
from insert import create_supplier_challan
from security import gemini
from datetime import date
from whatsapp_send_text import whatsapp_send_text   
from Template_send import chatbot
today= date.today().strftime("%d-%m-%y")

client = genai.Client(api_key=gemini)
pending_tickets = {}


def name(from_number):
    json_path = os.path.join(os.path.dirname(__file__), "number.json")
    with open(json_path, "r") as f:
        data = json.load(f)
        try:
            return(data[from_number])
        except KeyError:
            return "Unknown"

def meation():
        json_path = os.path.join(os.path.dirname(__file__), "number.json")
        with open(json_path, "r") as f:
            data = json.load(f)  
            regading_person = []
            for i in data:
                regading_person.append(data[i])
        return regading_person
# System Instruction

SYSTEM_INSTRUCTION = f"""
ERPNext ticket extractor.
Today: {today}

Return ONLY JSON:
{{
"subject":"",
"custom_issue_regarding":"",
"remainder_date":"",
"priority":""
}}

Rules:
- Extract only what user says. Never guess. Missing = "".
- subject = short issue/request.
- regarding allowed: {meation()}.
- HR = employee/salary/leave/attendance.general/leave IT = ERPNext/computer/network/server/software.
- Person only if clearly related.
- remainder_date = YYYY-MM-DD only if reminder is requested.
  today={today}, tomorrow=+1 day, day after tomorrow=+2 days, after N days=+N days.
- priority: High=critical/business stopped/server/security/payment/production blocked;
  Medium=normal issue; Low=minor/non-urgent request.
- Audio may be Hindi/English/Gujarati/Marathi/Hinglish.
- No extra keys, Markdown, explanation, null, or N/A.
"""


def ask(audio_path: str, from_number: str ,sender_name: str) -> str:
#Upload an audio file and ask Gemini to analyze it and create a ticket.
  
    # Validate audio file
    if name(from_number) == "Unknown":
        return f"This number is not registered in the database: {from_number}"

    try:
    
        audio_file = client.files.upload(
            file=audio_path
        )

        # Wait for audio file to finish processing
        whatsapp_send_text(from_number, "Please wait while we process your audio message and extract ticket details...")
        while audio_file.state.name == "PROCESSING":
            time.sleep(1)
            audio_file = client.files.get(name=audio_file.name)

        if audio_file.state.name == "FAILED":
            return f"Audio file processing failed: {getattr(audio_file, 'error', 'Unknown error')}"

        # -------------------------------------------------
        # Generate response
        # -------------------------------------------------
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                audio_file
            ],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
            ),
        )

        raw_text = (response.text or "").strip()
        # Strip markdown code blocks if present
        if raw_text.startswith("```"):
            lines = raw_text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            raw_text = "\n".join(lines).strip()

        ticket_data = json.loads(raw_text)
        print(f"Extracted ticket data: {ticket_data}")
        # if ticket_data.get("subject") ==none and ticket_data.get("custom_issue_regarding") == None:
        #     whatsapp_send_text(from_number, "We could not extract any ticket details from your audio message. Please try again or contact support.")
        #     return None
        return ticket_data

    except Exception as e:
        return f"Gemini API Error: {e}"
