import json
import os
from ai import  ask
import requests
from whatsapp_send_text import whatsapp_send_text


def normalize_number(value):
    cleaned = "".join(ch for ch in str(value) if ch.isdigit())
    if len(cleaned) == 10:
        cleaned = "91" + cleaned
    return cleaned


def name(from_number):
    json_path = os.path.join(os.path.dirname(__file__), "number.json")
    with open(json_path, "r") as f:
        data = json.load(f)
        try:
            return(data[from_number])
        except KeyError:
            return "Unknown"



def audio_reply(url: str, from_number: str) -> str:
    sender_name = name(from_number)
    if sender_name == "Unknown":
        print(f"Number {from_number} Not Registered ,  Please Contact IT Team.")
        return None

    file_path = os.path.join("audio_file", f"{from_number}.mp3")

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if os.path.exists(file_path):
            os.remove(file_path)

        response = requests.get(url, timeout=30)
        if response.status_code != 200:
            print(from_number, "Some Technical issue, Please contact IT  team")
            return None

        with open(file_path, "wb") as f:
            f.write(response.content)

        if not os.path.exists(file_path):
            print(from_number, "Some Technical issue, Please contact IT  team")
            return None

        print(f"Audio file saved to: {file_path}")
       
        print(f"Processing audio for number: {file_path}")
        response_ai = ask(audio_path=file_path, from_number=from_number,sender_name=sender_name)
        return response_ai
        # whatsapp_send_text(from_number, "Audio file received and saved successfully.")

    except Exception as e:
        print(f"Error saving audio: {e}")
        whatsapp_send_text(from_number, "Some Technical issue, Please contact IT  team")
        return None
# audio_reply("https://11zamedia.11za.in/gokultexprintsprivatelimited/Receive/AUD/AUD-36634944555899795.ogg", "918140021166")