import os
import requests
from datetime import datetime, timezone

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_alert(
    report,
    threat,
    latitude,
    longitude,
    image=None
):

    if not BOT_TOKEN or not CHAT_ID:
        raise RuntimeError("Telegram credentials missing")

    location = "Location unavailable"

    if latitude not in (None, "") and longitude not in (None, ""):
        location = (
            f"https://www.google.com/maps?q="
            f"{latitude},{longitude}"
        )

    timestamp = datetime.now(timezone.utc).strftime(
        "%d-%m-%Y %H:%M:%S UTC"
    )

    message = f"""
🚨 SENTINEL SHIELD AI ALERT

⚠️ Threat Level: {threat}

📌 Situation:
{report[:650]}

📍 Location:
{location}

🕒 Time:
{timestamp}

AI assessment — human verification required.
"""

    base_url = (
        f"https://api.telegram.org/bot{BOT_TOKEN}"
    )

    if image:

        response = requests.post(
            f"{base_url}/sendPhoto",
            data={
                "chat_id": CHAT_ID,
                "caption": message
            },
            files={
                "photo": (
                    "incident.jpg",
                    image,
                    "image/jpeg"
                )
            },
            timeout=10
        )

    else:

        response = requests.post(
            f"{base_url}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=10
        )

    if not response.ok or not response.json().get("ok"):
        raise RuntimeError("Telegram delivery failed")

    return True
