import requests

BOT_TOKEN = "8759965398:AAEm4ucj97tfkrEYAwEJmKSns2AkREd_JOk"

CHAT_ID = "6385404992"


def send_telegram_alert(
    report,
    threat,
    latitude,
    longitude
):

    maps_link = (
        f"https://www.google.com/maps?q={latitude},{longitude}"
    )

    message = f"""
🚨 Sentinel Shield Alert

📌 Report:
{report}

⚠ Threat Level:
{threat}

📍 Location:
Latitude: {latitude}

Longitude: {longitude}

🌍 Open Map:
{maps_link}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)