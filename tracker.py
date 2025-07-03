import feedparser
import requests
import time
import json
import os

# Load Discord webhook securely from GitHub secret
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

RSS_FEED_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001838314&type=&owner=exclude&count=100&output=atom"
SEEN_FILE = "seen.json"

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_seen(seen_entries):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen_entries), f)

def send_discord_alert(entry):
    if not DISCORD_WEBHOOK_URL:
        print("No webhook URL found.")
        return
    content = (
        f"📄 **New SEC Filing by PIF**\n"
        f"**{entry.title}**\n"
        f"🕒 {entry.published}\n"
        f"🔗 <{entry.link}>"
    )
    payload = {"content": content}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code != 204:
        print("Discord post failed:", response.text)

def run_tracker():
    seen_entries = load_seen()
    feed = feedparser.parse(RSS_FEED_URL)
    new_seen = set(seen_entries)
    for entry in feed.entries:
        if entry.id not in seen_entries:
            send_discord_alert(entry)
            new_seen.add(entry.id)
    save_seen(new_seen)

run_tracker()
