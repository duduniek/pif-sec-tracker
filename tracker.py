import feedparser
import requests
import os

# Load Discord webhook from GitHub Secrets
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# SEC RSS Feed for PIF
RSS_FEED_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001838314&type=&owner=exclude&count=100&output=atom"

def send_discord_alert(entry):
    if not DISCORD_WEBHOOK_URL:
        print("No webhook URL found.")
        return
    content = (
        f"📄 **[TEST] SEC Filing by PIF**\n"
        f"**{entry.title}**\n"
        f"🕒 {entry.published}\n"
        f"🔗 <{entry.link}>"
    )
    payload = {"content": content}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code != 204:
        print("Failed to send message:", response.text)
    else:
        print(f"✅ Sent: {entry.title}")

def run_tracker():
    print("🔍 Fetching feed...")
    feed = feedparser.parse(RSS_FEED_URL)
    
    for entry in feed.entries:
        send_discord_alert(entry)

run_tracker()
