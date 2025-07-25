#!/usr/bin/env python3
import subprocess, sys, json
from pathlib import Path
from datetime import datetime

# === Paths ===
BASE         = Path.home() / "verobrix"
MODULES      = BASE / "modules"
LOGFILE      = BASE / "journal/listener_log.txt"
INTENT_SCRIPT= MODULES / "verobrix_intent.py"
DIALOGUE_SCRIPT = MODULES / "verobrix_dialogue.py"

# === Prompt Header ===
def intro():
    print("\n🎧 Verobrix Listener — Awaiting Your Command")
    print("🔁 Type a natural phrase (or 'exit' to quit). She’ll parse intent, reflect, and respond.\n")

# === Log Interaction ===
def log_interaction(query, output):
    with open(LOGFILE, "a") as f:
        f.write(f"\n=== Listener {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        f.write(f"> {query}\n")
        f.write(output + "\n")

# === Run Dialogue Reflection ===
def run_dialogue(prompt):
    result = subprocess.run(
        ["python3", str(DIALOGUE_SCRIPT), prompt],
        capture_output=True, text=True
    )
    return result.stdout.strip()

# === Listener Loop ===
def main():
    intro()
    while True:
        try:
            user_input = input("🗣️  You → ").strip()
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("👋 Exiting Verobrix Listener. Her ears will rest.")
                break
            if not user_input:
                continue

            print("\n🔎 Verobrix is reflecting...\n")
            response = run_dialogue(user_input)
            print(response)
            log_interaction(user_input, response)

        except KeyboardInterrupt:
            print("\n🧠 Listener interrupted. Goodbye.")
            break

if __name__ == "__main__":
    main()
