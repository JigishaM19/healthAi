import os
import httpx

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")

async def send_sms(to_phone: str, message: str) -> bool:
    if not to_phone:
        print("[SMSService] No phone number provided, skipping SMS.")
        return False

    # 1. Try Twilio REST API if credentials provided
    if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE_NUMBER:
        try:
            url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    url,
                    auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
                    data={
                        "From": TWILIO_PHONE_NUMBER,
                        "To": to_phone,
                        "Body": message
                    }
                )
                if resp.status_code in [200, 201]:
                    return True
                else:
                    print(f"[SMSService] Twilio returned status {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"[SMSService] Twilio exception: {e}")

    # 2. Development Fallback (Logger output)
    print(f"[SMSService LOG] Simulated SMS to {to_phone} | Message: '{message}'")
    return True
