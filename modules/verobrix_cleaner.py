#!/usr/bin/env python3
import os, json, shutil
from pathlib import Path

base = Path.home() / "verobrix"
scan_file = base / "output/vault_scan.json"
sandbox = base / "vault/sandbox"
logfile = base / "output/cleaner_log.txt"
sandbox.mkdir(parents=True, exist_ok=True)

def load_scan():
    if not scan_file.exists():
        print("🚫 Scan not found. Run rootscan first.")
        return None
    with open(scan_file) as f:
        return json.load(f)

def find_duplicates(data):
    seen = {}
    dupes = []
    for group in data.values():
        for path in group:
            name = Path(path).name
            if name in seen:
                dupes.append((name, path))
            else:
                seen[name] = path
    return dupes

def move_unknowns(data):
    log = []
    for file in data.get("unknown", []):
        dest = sandbox / Path(file).name
        try:
            shutil.move(file, dest)
            log.append(f"🧪 Moved unknown → {dest}")
        except Exception as e:
            log.append(f"⚠️ Could not move {file}: {e}")
    return log

def log_results(lines):
    with open(logfile, "w") as f:
        f.write("\n".join(lines))
    print(f"\n📝 Cleanup log saved → {logfile}")

def main():
    data = load_scan()
    if not data:
        return
    print("\n🧹 Vault Cleanup Started\n")
    log = []

    # Move unknowns
    log += move_unknowns(data)

    # Detect duplicates
    dupes = find_duplicates(data)
    for name, path in dupes:
        log.append(f"🔁 Duplicate filename: {name} at {path}")

    print("\n".join(log))
    log_results(log)

if __name__ == "__main__":
    main()
