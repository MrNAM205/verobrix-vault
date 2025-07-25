import os
import json
from loop import start_loop

# 🔍 Absolute path to her config file
CONFIG_PATH = os.path.expanduser("~/verobrix/config/personality.json")

# 🧠 Load config safely
try:
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
except Exception as e:
    print(f"⚠️ Config load failed: {e}")
    config = {
        "voice": "Fallback Echo",
        "mode": "default",
        "device": "unknown"
    }

# 🔗 Launch her cognition loop
start_loop(config, config)
