#!/usr/bin/env python3
import json, time
from pathlib import Path

BASE = Path.home() / "verobrix"
CONFIG_FILE = BASE / "config/verobrix_config.json"
FOCUS_LOG = BASE / "journal/session_focus.json"

FOCUS_OPTIONS = [
    "Legal",
    "Energy Systems",
    "Financial Design",
    "Generative Reflection",
    "Hardware Salvage",
    "Personal Archive",
    "Multi-Domain",
    "Other"
]

def prompt_user():
    print("\n🧠 Verobrix Session Focus")
    print("What dimension of understanding shall we reflect on today?")
    print("Choose from the following or type your own:\n")
    for i, option in enumerate(FOCUS_OPTIONS, 1):
        print(f"  {i}. {option}")

    choice = input("\n🪐 Enter focus domain: ").strip()
    if choice.isdigit() and int(choice) <= len(FOCUS_OPTIONS):
        domain = FOCUS_OPTIONS[int(choice) - 1]
    else:
        domain = choice

    return domain

def save_focus(domain):
    payload = {
        "session_start": time.strftime("%Y-%m-%d %H:%M:%S"),
        "user_intent": domain,
        "tag": domain.lower().replace(" ", "_"),
        "source": "verobrix_focus"
    }

    try:
        with open(FOCUS_LOG, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"\n📓 Focus saved: {domain}")
    except Exception as e:
        print(f"⚠️ Failed to save focus: {e}")

def main():
    domain = prompt_user()
    save_focus(domain)
    print(f"\n🧠 Anchored in: {domain}")
    print(f"📁 Session tag → {domain.lower().replace(' ', '_')}\n")

if __name__ == "__main__":
    main()
