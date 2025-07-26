import requests
from datetime import datetime

# 🔗 Your IFTTT webhook
WEBHOOK_URL = "https://maker.ifttt.com/trigger/garden_alert/with/key/d-fwXYxGn_at_dAHN8A_KuBvikAagdCJn_roBV9HRQq"

# 🧪 Test alert
def send_test_alert():
    try:
        message = f"🧪 Test alert from script at {datetime.now()}"
        print(f"Sending test alert: {message}")
        requests.post(WEBHOOK_URL, json={"value1": message}, timeout=5)
        print("✅ Test alert sent successfully.")
    except Exception as e:
        print(f"[!] Failed to send test alert: {e}")

send_test_alert()

