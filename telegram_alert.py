import os
import requests
from datetime import datetime, timezone

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_alert(
    report,
    threat,
    latitude=None,
    longitude=None,
    image=None,
    ai_result=None
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
{report}

🤖 AI Analysis:
{ai_result or "See situation details above."}

📍 Location:
{location}

🕒 Time:
{timestamp}

AI assessment - human verification required.
"""

    base_url = f"https://api.telegram.org/bot{BOT_TOKEN}"

    def check_response(response):
        result = response.json()

        if not response.ok or not result.get("ok"):
            raise RuntimeError(
                f"Telegram error: {result.get('error_code')} - "
                f"{result.get('description')}"
            )

    if image:
        response = requests.post(
            f"{base_url}/sendPhoto",
            data={
                "chat_id": CHAT_ID,
                "caption": f"Sentinel Shield Alert: {threat}"
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

        check_response(response)

    for start in range(0, len(message), 1800):
        response = requests.post(
            f"{base_url}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": message[start:start + 1800]
            },
            timeout=10
        )

        check_response(response)

    print("Telegram alert sent successfully", flush=True)

    return True
