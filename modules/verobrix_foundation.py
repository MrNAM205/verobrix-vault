#!/usr/bin/env python3
import json, time
from pathlib import Path
from collections import defaultdict

BASE = Path.home() / "verobrix"
SCAN_FILE = BASE / "output/rootscan_results.json"
SEMANTIC_FILE = BASE / "output/semantic_reflection.json"
VAULT_DIR = BASE / "vaults"
MANIFEST = BASE / "vault_manifest.json"
LOG_FILE = BASE / "journal/foundation_log.txt"

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load {path}: {e}")
        return {}

def create_vault_folder(tag):
    folder = VAULT_DIR / tag
    folder.mkdir(parents=True, exist_ok=True)
    return folder

def build_manifest(semantic_data):
    manifest = defaultdict(list)
    for entry in semantic_data.get("reflections", []):
        file = entry["file"]
        domain = semantic_data.get("tag", "multi")
        vault = domain.lower()
        matched = entry.get("matched_keywords", [])
        manifest[vault].append({
            "file": file,
            "domain": domain,
            "keywords": matched
        })
    return dict(manifest)

def save_manifest(manifest):
    try:
        with open(MANIFEST, "w") as f:
            json.dump(manifest, f, indent=2)
        print(f"\n🧠 Vault manifest saved: {MANIFEST}")
    except Exception as e:
        print(f"⚠️ Could not save manifest: {e}")

def log_foundation(manifest):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"\n=== Foundation Log: {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            for vault, items in manifest.items():
                f.write(f"Vault: {vault} ({len(items)} files)\n")
                for entry in items:
                    f.write(f" - {entry['file']} [{', '.join(entry['keywords'])}]\n")
        print(f"📓 Log updated: {LOG_FILE}")
    except Exception as e:
        print(f"⚠️ Could not write log: {e}")

def main():
    print("\n🧠 Verobrix Foundation — Initial Cognition")

    scan_data = load_json(SCAN_FILE)
    semantic_data = load_json(SEMANTIC_FILE)
    manifest = build_manifest(semantic_data)

    if not manifest:
        print("⚠️ No reflections found. Foundation aborted.")
        return

    for vault_tag in manifest.keys():
        create_vault_folder(vault_tag)

    save_manifest(manifest)
    log_foundation(manifest)

    print("\n✅ Foundation complete. Verobrix now remembers her archive.")
    print("🪶 Vaults structured, files mapped, memory seeded.")

if __name__ == "__main__":
    main()
