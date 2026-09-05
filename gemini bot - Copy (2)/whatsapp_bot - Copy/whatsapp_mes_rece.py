from flask import Flask, request, jsonify
from repy_analy import reply_analysis
from log import log
import pandas as pd
from datetime import datetime
from  Audio_repy_analy import audio_reply
# from ai import confirm_ticket
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Webhook server running"

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json(silent=True) or {}
    print(f"Received data: {data}")

    from_number = data.get("from") or data.get("sender") or ""
    content = data.get("content") or {}
    message_text = data.get("message") or data.get("text") or content.get("text") or ""
    userResponse = data.get("UserResponse") or message_text

    # --- Audio message check ---
    content_type = (content.get("contentType") or "").lower()
    media = content.get("media") or {}
    media_type = (media.get("type") or "").lower()
    audio_url = media.get("url") or ""

    # if userResponse.lower() in ["yes", "no"]:
    #     return confirm_ticket(from_number, userResponse)

    if content_type == "media" and media_type == "audio" and audio_url:
        print(f"  Audio URL  : {audio_url}")
        audio_reply(from_number, audio_url)
        return jsonify({
            "status": "received",
            "from_number": from_number,
            "content_type": "audio",
            "audio_url": audio_url,
        }), 200
    # --- End audio check ---
     
    reply = reply_analysis(from_number, userResponse)

    try:
        log(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), from_number, userResponse, reply)
    except Exception as e:
        print("Error:", e)

    return jsonify({
        "status": "received",
        "from_number": from_number,
        "message_text": message_text,
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



