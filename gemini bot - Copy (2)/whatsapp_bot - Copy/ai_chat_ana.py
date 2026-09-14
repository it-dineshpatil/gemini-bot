import json
import os
import re
import sys
import time
from google import genai
from numpy import number
from google.genai import types
from insert import create_ticket
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
- subject =   user report analysis issue/request.
- regarding allowed: {meation()}.
- HR = employee/salary/leave/attendance. IT = ERPNext/computer/network/server/software.
- Person only if clearly related.
- remainder_date = YYYY-MM-DD only if reminder is requested.
  today={today}, tomorrow=+1 day, day after tomorrow=+2 days, after N days=+N days.
- priority: High=critical/business stopped/server/security/payment/production blocked;
  Medium=normal issue; Low=minor/non-urgent request.
- Audio may be Hindi/English/Gujarati/Marathi/Hinglish.
- No extra keys, Markdown, explanation, null, or N/A.
"""

def ask_chat_ana(user_text: str, from_number) -> str:
    if name(from_number) == "Unknown":
        return f"This number is not registered in the database: {from_number}"

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                user_text
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
 # Ensure from_number is passed to the ticket data
        ticket_data['from_number'] = from_number  # Add the from_number to the ticket data

        print(f"Extracted ticket data: {ticket_data}")
        # whatsapp_send_text(from_number, f"Ticket details extracted:\nSubject: {ticket_data.get('subject', '')}\nRegarding: {ticket_data.get('custom_issue_regarding', '')}\nRemainder Date: {ticket_data.get('remainder_date', '')}\nPriority: {ticket_data.get('priority', '')}\n\nPlease confirm if you want to create the ticket. Reply with 'Yes' to create or 'No' to cancel.")
        # chatbot(from_number, ticket_data.get('subject', ''), ticket_data.get('custom_issue_regarding', ''), ticket_data.get('remainder_date', ''), ticket_data.get('priority', ''))
        return ticket_data
    
    except (json.JSONDecodeError, ValueError, TypeError) as error:
        print(f"Failed to process ticket data: {error}")
        return whatsapp_send_text(
            from_number,
            "Unable to process the ticket details. Please send the message again."
        )
# result = ask_chat_ana("Hello, I have an issue with my ERPNext account. i am remainder 2 days meation it DInesh ", "918140021166")
# print(result)