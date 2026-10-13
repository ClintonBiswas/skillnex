import requests

from django.conf import settings


def normalize_bd_phone(phone):

    phone = phone.strip()
    phone = phone.replace(" ", "")
    phone = phone.replace("-", "")

    if phone.startswith("+880"):
        phone = phone[1:]

    elif phone.startswith("01"):
        phone = "88" + phone

    return phone


def send_sms(phone, message):

    print("\n========== SMS DEBUG ==========")

    print("Original phone:", phone)

    phone = normalize_bd_phone(phone)

    print("Normalized phone:", phone)
    print("API URL:", settings.BULKSMSBD_API_URL)
    print("Sender ID:", settings.BULKSMSBD_SENDER_ID)

    if not settings.BULKSMSBD_API_KEY:

        print("ERROR: BULKSMSBD_API_KEY is empty")
        print("================================\n")

        return {
            "success": False,
            "message": "BulkSMSBD API key is not configured."
        }

    payload = {
        "api_key": settings.BULKSMSBD_API_KEY,
        "type": "text",
        "number": phone,
        "senderid": settings.BULKSMSBD_SENDER_ID,
        "message": message,
    }

    print("Message:", message)
    print("Sending SMS...")

    try:

        response = requests.post(
            settings.BULKSMSBD_API_URL,
            data=payload,
            timeout=15,
        )

        print("HTTP status:", response.status_code)
        print("API response:", response.text)

        response.raise_for_status()

        print("SMS request completed.")
        print("================================\n")

        return {
            "success": True,
            "response": response.text,
        }

    except requests.RequestException as exc:

        print("SMS REQUEST ERROR:", exc)
        print("================================\n")

        return {
            "success": False,
            "message": str(exc),
        }
