import feedparser
import requests

# ✅ Hardcoded Discord webhook for testing (your provided URL)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1390135398822318284/Qd5f84Oip3jRauemanwGvbAtPIypz9Pv5aNiPL3gYhR1TntMZPxmZjQ06OdwYVjFZXoi"

# SEC RSS feed for Public Investment Fund
RSS_FEED_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001838314&type=&owner=exclude&count=100&output=atom"

def send_discord_alert(entry):
    content = (
        f"📄 **[TEST] SEC Filing by PIF**\n"
        f"**{entry.title}**\n"
        f"🕒 {entry.published}\n"
        f"🔗 <{entry.link}>"
    )

    print(f"📨 Sending to Discord:\n{content}")

    payload = {"content": content}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

    if response.status_code != 204:
        print(f"❌ Failed to send. Status code: {response.status_code}")
        print(response.text)
    else:
        print("✅ Message sent to Discord.")

def run_tracker():
    print("🔎 Checking PIF SEC feed...")
    feed = feedparser.parse(RSS_FEED_URL)
    for entry in feed.entries:
        send_discord_alert(entry)

run_tracker()
