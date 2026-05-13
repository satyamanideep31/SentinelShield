from flask import Flask, render_template, request
from blockchain import blockchain
from database import init_db, insert_report, get_reports
from telegram_alert import send_telegram_alert

app = Flask(__name__)

# =========================
# DATABASE INIT
# =========================

init_db()

# =========================
# HOME PAGE
# =========================

@app.route('/')
def home():

    return render_template('index.html')

# =========================
# ANALYZE
# =========================

@app.route('/analyze', methods=['POST'])
def analyze():

    try:

        report = request.form['report']

        latitude = request.form.get('latitude')

        longitude = request.form.get('longitude')

        text = report.lower()

        # =========================
        # DEFAULT
        # =========================

        threat_level = "Low"

        ai_result = """
Threat Level: Low

Reason:
Normal harmless activity detected.
"""

        # =========================
        # HIGH RISK
        # =========================

        high_keywords = [

            "gun",
            "knife",
            "bomb",
            "attack",
            "fight",
            "weapon",
            "terrorist"

        ]

        # =========================
        # MEDIUM RISK
        # =========================

        medium_keywords = [

            "suspicious",
            "intruder",
            "running",
            "panic"

        ]

        # =========================
        # ANALYSIS
        # =========================

        for word in high_keywords:

            if word in text:

                threat_level = "High"

                ai_result = """
Threat Level: High

Reason:
Dangerous activity detected.

Recommended Action:
Immediate security response required.
"""

                break

        for word in medium_keywords:

            if word in text and threat_level != "High":

                threat_level = "Medium"

                ai_result = """
Threat Level: Medium

Reason:
Suspicious activity detected.

Recommended Action:
Monitor carefully.
"""

                break

        # =========================
        # BLOCKCHAIN
        # =========================

        previous_block = blockchain.get_previous_block()

        previous_hash = previous_block['hash']

        block = blockchain.create_block(

            data=report,
            previous_hash=previous_hash

        )

        # =========================
        # DATABASE
        # =========================

        insert_report(

            report,
            threat_level,
            block['hash']

        )

        # =========================
        # TELEGRAM ALERT
        # =========================

        if threat_level == "High":

            send_telegram_alert(

                report,
                threat_level,
                latitude,
                longitude

            )

        # =========================
        # RESULT PAGE
        # =========================

        return render_template(

            'result.html',

            report=report,
            threat=threat_level,
            ai_result=ai_result,
            block_hash=block['hash'],
            latitude=latitude,
            longitude=longitude

        )

    except Exception as e:

        return f"""
<h1>ERROR OCCURRED</h1>

<pre>{str(e)}</pre>
"""

# =========================
# DASHBOARD
# =========================

@app.route('/dashboard')
def dashboard():

    reports = get_reports()

    return render_template(

        'dashboard.html',
        reports=reports

    )

# =========================
# RUN APP
# =========================

if __name__ == '__main__':

    app.run(debug=True)
    if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)