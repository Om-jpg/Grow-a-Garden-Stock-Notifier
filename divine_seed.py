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

# 🔔 Webhook URLs
WEBHOOKS = {
    # Seeds
    "sugar apple": "https://maker.ifttt.com/trigger/sugar_apple/with/key/d-fwXYxGn_at_dAHN8A_KuBvikAagdCJn_roBV9HRQq",
    "beanstalk": "https://maker.ifttt.com/trigger/beanstalk/with/key/d-fwXYxGn_at_dAHN8A_KuBvikAagdCJn_roBV9HRQq",
    "burning bud": "https://maker.ifttt.com/trigger/burning_bud/with/key/d-fwXYxGn_at_dAHN8A_KuBvikAagdCJn_roBV9HRQq",
    "ember lily": "https://maker.ifttt.com/trigger/ember_lily/with/key/d-fwXYxGn_at_dAHN8A_KuBvikAagdCJn_roBV9HRQq",
    "mushroom": "https://maker.ifttt.com/trigger/mushroom/with/key/d-fwXYxGn_at_dAHN8A_KuBvikAagdCJn_roBV9HRQq",

    # Eggs
    "bug egg": "https://maker.ifttt.com/trigger/bug_egg/with/key/d-fwXYxGn_at_dAHN8A_KuBvikAagdCJn_roBV9HRQq",
    "mythical egg": "https://maker.ifttt.com/trigger/mythic_egg/with/key/d-fwXYxGn_at_dAHN8A_KuBvikAagdCJn_roBV9HRQq",
    "paradise egg": "https://maker.ifttt.com/trigger/paradise_egg/with/key/d-fwXYxGn_at_dAHN8A_KuBvikAagdCJn_roBV9HRQq",
    "bee egg": "https://maker.ifttt.com/trigger/bee_egg/with/key/d-fwXYxGn_at_dAHN8A_KuBvikAagdCJn_roBV9HRQq",

    # Gear
    "master sprinkler": "https://maker.ifttt.com/trigger/master_sprinkler/with/key/d-fwXYxGn_at_dAHN8A_KuBvikAagdCJn_roBV9HRQq",
    "tanning mirror": "https://maker.ifttt.com/trigger/tanning_mirror/with/key/d-fwXYxGn_at_dAHN8A_KuBvikAagdCJn_roBV9HRQq",

    # Heartbeat
    "heartbeat": "https://maker.ifttt.com/trigger/script_heartbeat/with/key/d-fwXYxGn_at_dAHN8A_KuBvikAagdCJn_roBV9HRQq"
}

# 🧠 Memory
notified_seeds = set()
notified_eggs = set()
notified_gear = set()
last_heartbeat = time.time()


# 🌱 Top seeds to track
RARE_SEEDS = ["Sugar Apple", "Beanstalk", "Burning Bud", "Ember Lily", "Mushroom"]

# 🥚 Rare eggs
RARE_EGGS = ["Bug Egg", "Mythical Egg", "Paradise Egg", "Bee Egg"]

# ⚙️ Rare gear
RARE_GEAR = ["Master Sprinkler", "Tanning Mirror"]

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
                log(f"[🌱] Rare seed found: {seed}")
                try:
                    requests.post(WEBHOOKS[s], json={"value1": f"🌱 {seed} is in stock!"}, timeout=5)
                except Exception as e:
                    log(f"[!] Failed to send seed webhook: {e}")
                notified_seeds.add(s)

        for egg in RARE_EGGS:
            e = egg.lower()
            if e in all_text and e not in notified_eggs:
                log(f"[🥚] Rare egg found: {egg}")
                try:
                    requests.post(WEBHOOKS[e], json={"value1": f"🥚 {egg} is in stock!"}, timeout=5)
                except Exception as e:
                    log(f"[!] Failed to send egg webhook: {e}")
                notified_eggs.add(e)

        for gear in RARE_GEAR:
            g = gear.lower()
            if g in all_text and g not in notified_gear:
                log(f"[⚙️] Rare gear found: {gear}")
                try:
                    requests.post(WEBHOOKS[g], json={"value1": f"⚙️ {gear} is in stock!"}, timeout=5)
                except Exception as e:
                    log(f"[!] Failed to send gear webhook: {e}")
                notified_gear.add(g)

    except Exception as e:
        log(f"[!] Error while checking stock: {e}")

def send_heartbeat():
    log("[♥] Sending heartbeat...")
    try:
        requests.post(WEBHOOKS["heartbeat"], json={"value1": f"✅ Script running - {datetime.now()}"}, timeout=5)
    except Exception as e:
        log(f"[!] Heartbeat failed: {e}")

# 🕐 Main loop
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

