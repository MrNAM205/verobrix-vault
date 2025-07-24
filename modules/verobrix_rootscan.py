#!/usr/bin/env python3
import os, json, platform
from pathlib import Path

CONFIG = Path.home() / "verobrix/config/verobrix_config.json"
OUTPUT = Path.home() / "verobrix/output/vault_scan.json"

def load_config():
    with open(CONFIG) as f:
        return json.load(f)


def get_env():
    return "mobile"


def get_env():
    name = platform.node().lower()
    if "oneplus" in name or "android" in name:
        return "mobile"
    else:
        return "desktop"

def classify(file, rules):
    ext = os.path.splitext(file)[1].lower()
    for tag, exts in rules.items():
        if ext in exts:
            return tag
    return "unknown"

def scan_paths(paths, rules):
    result = {key: [] for key in rules}
    result["unknown"] = []
    for path in paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                try:
                    full = os.path.join(root, file)
                    tag = classify(file, rules)
                    result[tag].append(full)
                except:
                    continue
    return result

def main():
    config = load_config()
    env = get_env()
    paths = config["scan_paths"].get(env, [])
    file_types = config["file_types"]
    print(f"[verobrix] scanning for {env} in {paths}")
    result = scan_paths(paths, file_types)
    with open(OUTPUT, "w") as f:
        json.dump(result, f, indent=2)
    print(f"[verobrix] scan complete → {OUTPUT}")

if __name__ == "__main__":
    main()
