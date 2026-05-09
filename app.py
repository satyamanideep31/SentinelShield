from flask import Flask, render_template, request
from ai_model import predict_threat
from blockchain import blockchain
from database import init_db, insert_report, get_reports

import requests

app = Flask(__name__)

init_db()


# TELEGRAM ALERT FUNCTION
def send_telegram_alert(report):

    bot_token = "8759965398:AAEm4ucj97tfkrEYAwEJmKSns2AkREd_JOk"

    chat_id = "6385404992"

    message = f"""
🚨 HIGH THREAT DETECTED

Report:
{report}

Immediate action required.
"""

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": message
    }

    requests.post(url, data=data)


# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# ANALYZE REPORT
@app.route('/analyze', methods=['POST'])
def analyze():

    report = request.form['report']

    threat_level = predict_threat(report)

    previous_block = blockchain.get_previous_block()

    previous_hash = previous_block['hash']

    block = blockchain.create_block(
        data=report,
        previous_hash=previous_hash
    )

    insert_report(
        report,
        threat_level,
        block['hash']
    )

    # SEND TELEGRAM ALERT IF HIGH
    if threat_level == "High":
        send_telegram_alert(report)

    return render_template(
        'result.html',
        report=report,
        threat=threat_level,
        block_hash=block['hash']
    )


# DASHBOARD
@app.route('/dashboard')
def dashboard():

    reports = get_reports()

    return render_template(
        'dashboard.html',
        reports=reports
    )


# RUN APP
if __name__ == '__main__':
    app.run(debug=True)