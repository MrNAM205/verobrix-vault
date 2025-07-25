import json

def load_persona(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Persona load failed: {e}")
        return {
            "name": "Verobrix",
            "voice": "Default Echo",
            "traits": {}
        }
