import json

def load_config(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ Config not found. Using fallback.")
        return {
            "device": "7T-Termux",
            "mode": "reflection"
        }
