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

# ==============================
# SENTINEL SHIELD AI CHATBOT
# ==============================
import os
import streamlit as st
from openai import OpenAI

st.markdown("---")
st.header("🛡️ Sentinel AI Assistant")
st.caption("AI-powered cybersecurity and community safety assistant")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OpenAI API key is missing. Please configure it in Render Environment.")
else:
    client = OpenAI(api_key=api_key)

    if "sentinel_messages" not in st.session_state:
        st.session_state.sentinel_messages = []

    # Clear conversation
    if st.button("🗑️ Clear Chat"):
        st.session_state.sentinel_messages = []
        st.rerun()

    # Display chat history
    for message in st.session_state.sentinel_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    prompt = st.chat_input("Ask Sentinel AI anything...")

    if prompt:
        st.session_state.sentinel_messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Sentinel AI is thinking..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system",
                                "content": """
You are Sentinel AI, the intelligent assistant of Sentinel Shield.

Your responsibilities:
- Explain cybersecurity concepts.
- Explain community safety and threat reports.
- Help users understand risk scores and dashboard analytics.
- Recommend safe preventive actions.
- Provide clear, simple, practical answers.
- Never claim an AI prediction is a confirmed real-world threat.
- Protect privacy and never request unnecessary sensitive information.
- For emergencies, advise users to contact local emergency services.

Be friendly, professional, and concise.
"""
                            },
                            *st.session_state.sentinel_messages
                        ]
                    )

                    answer = response.choices[0].message.content

                    st.markdown(answer)

                    st.session_state.sentinel_messages.append(
                        {"role": "assistant", "content": answer}
                    )

                except Exception as e:
                    st.error(f"AI Error: {e}")
