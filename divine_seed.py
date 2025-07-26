import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import logging

# 📝 Logging setup
logging.basicConfig(
    filename="garden_notifier.log",
    filemode="a",
    format="[{asctime}] {message}",
    style="{",
    level=logging.INFO
)

def log(msg):
    print(msg)
    logging.info(msg)

# 🌐 Stock page
STOCK_URL = "https://growagardenvalues.com/stock/stocks.php"

# 🔗 Single Webhook (your IFTTT webhook)
WEBHOOK_URL = "https://maker.ifttt.com/trigger/garden_alert/with/key/d-fwXYxGn_at_dAHN8A_KuBvikAagdCJn_roBV9HRQq"

# 🧠 Memory
notified_seeds = set()
notified_eggs = set()
notified_gear = set()
last_heartbeat = time.time()

# 🌱 Rare Seeds
RARE_SEEDS = [
    "Sugar Apple",
    "Beanstalk",
    "Burning Bud",
    "Ember Lily",
    "Mushroom",
    "Giant Pinecone Seed",
    "Elder Strawberry Seed"
]

# 🥚 Rare Eggs
RARE_EGGS = [
    "Bug Egg",
    "Mythical Egg",
    "Paradise Egg",
    "Bee Egg"
]

# ⚙️ Rare Gear
RARE_GEAR = [
    "Master Sprinkler",
    "Tanning Mirror",
    "Levelup Lollipop"
]

# 📤 Webhook Sender
def send_alert(emoji, item):
    try:
        message = f"{emoji} {item} is in stock!"
        log(f"[🔔] Sending alert: {message}")
        requests.post(WEBHOOK_URL, json={"value1": message}, timeout=5)
    except Exception as e:
        log(f"[!] Failed to send alert for {item}: {e}")

# 💓 Heartbeat
def send_heartbeat():
    log("[♥] Sending heartbeat...")
    try:
        requests.post(WEBHOOK_URL, json={"value1": f"✅ Script running - {datetime.now()}"} , timeout=5)
    except Exception as e:
        log(f"[!] Heartbeat failed: {e}")

# 🔍 Check Stock
def check_stock():
    global notified_seeds, notified_eggs, notified_gear
    try:
        res = requests.get(STOCK_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        all_text = soup.get_text().lower()

        for seed in RARE_SEEDS:
            s = seed.lower()
            if s in all_text and s not in notified_seeds:
                log(f"[🌱] Found rare seed: {seed}")
                send_alert("🌱", seed)
                notified_seeds.add(s)

        for egg in RARE_EGGS:
            e = egg.lower()
            if e in all_text and e not in notified_eggs:
                log(f"[🥚] Found rare egg: {egg}")
                send_alert("🥚", egg)
                notified_eggs.add(e)

        for gear in RARE_GEAR:
            g = gear.lower()
            if g in all_text and g not in notified_gear:
                log(f"[⚙️] Found rare gear: {gear}")
                send_alert("⚙️", gear)
                notified_gear.add(g)

    except Exception as e:
        log(f"[!] Error during stock check: {e}")

# ▶️ Main loop
log("🌿 Garden Watcher started...")
last_seed_reset = time.time()
last_egg_reset = time.time()
last_gear_reset = time.time()

LOOP_INTERVAL = 60  # seconds

try:
    while True:
        loop_start = time.monotonic()

        check_stock()
        now = time.time()

        if now - last_seed_reset >= 300:
            log("[🔁] Resetting seed alerts")
            notified_seeds.clear()
            last_seed_reset = now

        if now - last_gear_reset >= 300:
            log("[🔁] Resetting gear alerts")
            notified_gear.clear()
            last_gear_reset = now

        if now - last_egg_reset >= 1800:
            log("[🔁] Resetting egg alerts")
            notified_eggs.clear()
            last_egg_reset = now

        if now - last_heartbeat >= 3600:
            send_heartbeat()
            last_heartbeat = now

        loop_duration = time.monotonic() - loop_start
        sleep_time = max(0, LOOP_INTERVAL - loop_duration)
        time.sleep(sleep_time)

except KeyboardInterrupt:
    log("[✋] Script stopped manually.")

