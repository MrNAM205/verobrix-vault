#!/usr/bin/env python3
import os, json
from pathlib import Path

# 🧠 Define key paths
base = Path.home() / "verobrix"
modules = base / "modules"
state_file = base / "output/verobrix_state.json"
scan_file = base / "output/vault_scan.json"

# 🧠 Define available modules and descriptions
commands = {
    "rootscan": "Scan filesystem and classify files",
    "report":   "Summarize scan results and reflect",
    "sorter":   "Organize files by use-case or theme",
    "cleaner":  "Archive or isolate unknown/duplicate files"
}

def check_module(name):
    return modules.joinpath(f"verobrix_{name}.py").exists()

def load_state():
    try:
        with open(state_file) as f:
            return json.load(f)
    except:
        return {"last_scan": None, "setup_complete": False}

def suggest_action():
    if not scan_file.exists():
        return "→ Vault not yet scanned. Run 'rootscan' to begin."
    if check_module("report"):
        return "→ Scan complete. Run 'report' to reflect."
    return "→ Modules ready. Choose any to proceed."

def run_module(name):
    mod_path = modules / f"verobrix_{name}.py"
    if mod_path.exists():
        os.system(f"python {mod_path}")
    else:
        print(f"⚠️ Module '{name}' not found in {modules}.")

def launcher():
    print("\n🧠 Verobrix Launcher\n")
    state = load_state()
    for name, desc in commands.items():
        status = "✅" if check_module(name) else "❌"
        print(f" {status} {name:<8} — {desc}")
    print("\n" + suggest_action())
    choice = input("\nRun which module? ").strip().lower()
    if choice in commands:
        run_module(choice)
    else:
        print("⛔ Unrecognized command.")

if __name__ == "__main__":
    launcher()
