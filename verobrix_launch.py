#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path

# === Paths ===
BASE        = Path.home() / "verobrix"
MODULES     = BASE / "modules"
MANIFEST    = BASE / "vault_manifest.json"
FOUNDATION  = MODULES / "verobrix_foundation.py"
ROOTSCAN    = MODULES / "verobrix_rootscan.py"
SEMANTIC    = MODULES / "verobrix_semantic.py"
ENVDETECT   = MODULES / "verobrix_envdetect.py"
FOCUS       = MODULES / "verobrix_focus.py"

# === Extend module path ===
sys.path.append(str(MODULES))

# === Imports ===
from verobrix_envdetect import infer_identity_from_env, load_config
from verobrix_focus import prompt_user, save_focus

# === Utilities ===
def check_tool(name, command):
    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except Exception:
        return False

def run_module(script_path, label):
    if not script_path.exists():
        print(f"⚠️ Missing: {label} — {script_path}")
        return
    print(f"\n🚀 Launching: {label}")
    subprocess.run(["python3", str(script_path)])

# === Launch Sequence ===
def main():
    print("\n🧠 Verobrix Launch Sequence")
    print("🔎 Scanning environment...")

    identity = infer_identity_from_env()
    config   = load_config()
    root_ok  = check_tool("root", ["id", "-u"]) and subprocess.getoutput("id -u") == "0"
    python_ok= check_tool("python3", ["python3", "--version"])

    print(f"📍 Identity:  {identity}")
