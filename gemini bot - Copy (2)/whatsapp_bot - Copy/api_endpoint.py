from urllib import response
from flask import Flask, request, jsonify
from repy_analy import reply_analysis
from log import log
import pandas as pd
import time
from datetime import datetime
from  Audio_repy_analy import audio_reply
# from ai import confirm_ticket
from regarding_per import number_check
from ai_chat_ana import ask_chat_ana
from insert import create_supplier_challan
from  repy_analy import jobwork_report
from ticket_fetch import ticket_fetch
app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Webhook server running"

@app.route("/number_check", methods=["POST"])
def number_check_endpoint():
    data = request.get_json(silent=True) or {}
    
    response = number_check(data.get("from_number"))
    print(f"Number check result: {response},{data.get('from_number')}")
    
    log(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), data.get("from_number"), data.get("userResponse"), response)
    return jsonify({
        "status": "received",
        "result": response
    }), 200


@app.route("/ticket_text", methods=["POST"])
def ticket_text_endpoint():
    data = request.get_json(silent=True) or {}
    print(data.get("subject"))
    response = ask_chat_ana(user_text=data.get("subject"), from_number=data.get("from_number"))
    # print(f"Ticket text analysis result: {response}")
    #exell in log save
    log(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), data.get("from_number"), data.get("userResponse"), response)
    return jsonify({
        "status": "received",
        "result": response
    }),200
    
@app.route("/voice_ticket", methods=["POST"])
def voice_ticket_endpoint():
    data = request.get_json(silent=True) or {}
    # time.sleep(1)  # Add a 1-second delay before processing
    print(f"Received voice ticket data: {data}")
    #audio_path file  audio download and save and call ai.py file in ask funcation
    
    response = audio_reply(url=data.get("url"), from_number=data.get("from_number"))
    log(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), data.get("from_number"), response, f"Audio URL: {data.get('url')}")
    print(f"Voice ticket analysis result: {response}")
    return jsonify({
        "status": "received",
        "result": response
    }), 200
    
@app.route("/insert_ticket", methods=["POST"])
def insert_ticket_endpoint():
    data = request.get_json(silent=True) or {}
    print(f"Received insert ticket data: {data}")
    create_supplier_challan(
        data=data,
        from_number=data.get("from_number"),
        audio_path=data.get("audio_path"),
    )
    log(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), data.get("from_number"), data.get("userResponse"), f"Ticket inserted: {data.get('subject')}")

    print(f"Ticket inserted: {data.get('subject')}")
    return jsonify({
        "status": "received",
        "result": "Ticket inserted successfully"
    }), 200   
    
@app.route("/job_report", methods=["POST"])
def job_report_endpoint():
    data = request.get_json(silent=True) or {}
    print(f"job_report Endpoint respone{data}")
    repy = jobwork_report(data.get("from_number"),None)
    print(repy)
    
    log(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), data.get("from_number"), data.get("userResponse"), f"Ticket inserted: {data.get('subject')}")
    return jsonify({
        "status": "received",
        "result": repy
    }), 200   
    
@app.route("/ticket_fetch_endpoint", methods=["POST"])
def ticket_fetch_endpoint():
    data = request.get_json(silent=True) or {}
    print(f"job_report Endpoint respone{data}")
    repy = ticket_fetch(data.get("from_number"))
    # print(repy)
    return jsonify({
        "status": "received",
        "result": repy
    }), 200
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    # app.run(host="0.0.0.0", port=5000, debug=True)



