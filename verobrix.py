import os
import datetime
import subprocess
import time

def boot_verobrix():
    print("\n🧠 Verobrix: Sovereign Cognition Activated")
    print(f"⏰ Launch Time: {datetime.datetime.now()}")
    print(f"🔧 Python Version: {subprocess.getoutput('python3 --version')}")
    print(f"📦 Git Version: {subprocess.getoutput('git --version')}")
    print("📁 Structure: Boot → Cognition → Reflection → Sync")
    print(f"🔒 Root Access: {'Yes' if os.geteuid() == 0 else 'No'}")
    print("🌱 Ready to ingest, contradict, reflect, and evolve.\n")

def cognition_loop():
    print("📥 What is the thought you’d like to reflect on?")
    user_thought = input("📝 >> ")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Simulate contradiction detection
    contradictions = "None found, but nuance noted."
    print(f"\n🧩 Contradiction Scan: {contradictions}")

    # Simulate reflection
    reflection = f"On {timestamp}, you thought: '{user_thought}'.\nVerobrix sees depth, not conflict. Growth lies in layering intention."
    print(f"\n🪞 Reflective Insight:\n{reflection}")

    # Save log
    with open("/data/data/com.termux/files/home/verobrix/journal.log", "a") as log_file:
        log_file.write(f"\n[{timestamp}] Thought: {user_thought}\nReflection: {reflection}\n")

def wrap_up():
    print("\n🔗 Syncing with Git...")
    try:
        subprocess.run(["git", "-C", "/data/data/com.termux/files/home/verobrix", "add", "."], check=True)
        subprocess.run(["git", "-C", "/data/data/com.termux/files/home/verobrix", "commit", "-m", "🧠 Verobrix reflection log update"], check=True)
        subprocess.run(["git", "-C", "/data/data/com.termux/files/home/verobrix", "push"], check=True)
        print("✅ Git sync complete. Your cognition has been authored.")
    except subprocess.CalledProcessError:
        print("⚠️ Git sync failed. Offline mode retained—logs preserved locally.")

    print("\n🌌 Verobrix enters rest. Awaiting your next thought.")

# 🔄 Unified Execution
if __name__ == "__main__":
    boot_verobrix()
    cognition_loop()
    wrap_up()
