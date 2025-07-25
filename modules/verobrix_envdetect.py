#!/usr/bin/env python3
import os, json, socket, platform
from pathlib import Path

BASE = Path.home() / "verobrix"
CONFIG_FILE = BASE / "config/verobrix_config.json"

def load_config():
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except:
        print("⚠️ Cannot load config.")
        return {}

def infer_identity_from_env():
    hostname = socket.gethostname().lower()
    shell = os.environ.get("SHELL", "").lower()
    user = os.environ.get("USER", "").lower()
    home_path = str(Path.home())
    system = platform.system().lower()

    mobile_signals = [
        "termux" in shell,
        "android" in hostname,
        "oneplus" in hostname,
        "mobile" in user,
        "/data/data" in home_path,
        "/storage/emulated" in home_path,
        Path("/data/data/com.termux/files/home").exists(),
        Path("/storage/emulated/0").exists()
    ]

    if any(mobile_signals):
        return "mobile"
    return "desktop"

def get_fallback_identity(config):
    return config.get("device_identity", "unknown")

def get_scan_paths(config, identity):
    return config.get("scan_paths", {}).get(identity, [])

def log_env(identity, config, paths):
    envlog = BASE / "output/envlog.txt"
    try:
        with open(envlog, "a") as f:
            f.write(f"[{identity.upper()}] Host: {socket.gethostname()} | Shell: {os.environ.get('SHELL', 'unknown')}\n")
            f.write(f"Paths: {paths}\n---\n")
    except:
        pass

def main():
    config = load_config()
    auto_identity = infer_identity_from_env()
    fallback_identity = get_fallback_identity(config)
    identity = auto_identity or fallback_identity
    paths = get_scan_paths(config, identity)

    print("\n🧠 Verobrix Environment Detector")
    print(f"🔍 Hostname → {socket.gethostname()}")
    print(f"🐚 Shell → {os.environ.get('SHELL', 'Unknown')}")
    print(f"🏠 Home Path → {str(Path.home())}")
    print(f"💡 Detected Identity → {identity}")
    print(f"📁 Scan Paths:")
    for path in paths:
        print(f"   - {path}")

    if config.get("cognition", {}).get("log_environment", False):
        log_env(identity, config, paths)

if __name__ == "__main__":
    main()
