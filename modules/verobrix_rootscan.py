#!/usr/bin/env python3
import os, json, time
from pathlib import Path
from verobrix_envdetect import load_config, infer_identity_from_env, get_scan_paths

# 🔍 Load session focus
FOCUS_FILE = Path.home() / "verobrix/journal/session_focus.json"
try:
    with open(FOCUS_FILE) as f:
        FOCUS = json.load(f)
        FOCUS_TAG = FOCUS.get("tag", "multi").lower()
except:
    FOCUS_TAG = "multi"

# 🔧 Paths and settings
BASE = Path.home() / "verobrix"
CONFIG = load_config()
IDENTITY = infer_identity_from_env()
SCAN_PATHS = get_scan_paths(CONFIG, IDENTITY)
FILE_TYPES = CONFIG.get("file_types", {})
EXCLUDE_PATHS = CONFIG.get("exclude_paths", {}).get(IDENTITY, [])
SETTINGS = CONFIG.get("scan_settings", {})

MAX_SIZE_MB = SETTINGS.get("max_file_size_mb", 100)
SKIP_HIDDEN = SETTINGS.get("skip_hidden", True)
LOG_SKIPPED = SETTINGS.get("log_skipped", True)

OUTPUT_FILE = BASE / "output/rootscan_results.json"
SKIP_LOG = BASE / "output/rootscan_skipped.txt"

def load_domain_keywords():
    keywords_file = BASE / "config/domain_keywords.json"
    try:
        with open(keywords_file) as f:
            return json.load(f).get(FOCUS_TAG, [])
    except:
        return []

DOMAIN_KEYWORDS = load_domain_keywords()

def is_hidden(path):
    return any(part.startswith('.') for part in Path(path).parts)

def is_excluded(path):
    return any(str(path).startswith(str(ex)) for ex in EXCLUDE_PATHS)

def scan_files():
    results = {ftype: [] for ftype in FILE_TYPES}
    results["unclassified"] = []
    skipped = []

    for root_path in SCAN_PATHS:
        root = Path(root_path)
        try:
            if not root.exists():
                skipped.append(f"❌ {root} does not exist")
                continue
        except PermissionError:
            skipped.append(f"🚫 {root} — Permission Denied")
            continue

        for dirpath, dirs, files in os.walk(root):
            dirpath_obj = Path(dirpath)

            # Skip excluded or hidden folders
            if is_excluded(dirpath_obj):
                skipped.append(f"🔒 Skipped folder {dirpath}")
                dirs[:] = []
                continue
            if SKIP_HIDDEN and is_hidden(dirpath_obj):
                skipped.append(f"⚫️ Hidden folder {dirpath}")
                dirs[:] = []
                continue

            for file in files:
                filepath = dirpath_obj / file
                if SKIP_HIDDEN and is_hidden(filepath):
                    skipped.append(f"⚫️ Hidden file {filepath}")
                    continue
                if is_excluded(filepath):
                    skipped.append(f"🔒 Excluded file {filepath}")
                    continue

                try:
                    if filepath.stat().st_size > MAX_SIZE_MB * 1024 * 1024:
                        skipped.append(f"💾 Oversized file {filepath}")
                        continue
                except:
                    skipped.append(f"⚠️ Stat fail: {filepath}")
                    continue

                ext = filepath.suffix.lower()
                path_str = str(filepath).lower()
                classified = False

                # 🧠 Domain-aware filtering
                if DOMAIN_KEYWORDS:
                    if not any(kw in path_str for kw in DOMAIN_KEYWORDS):
                        skipped.append(f"🪐 Irrelevant file {filepath} (outside focus: {FOCUS_TAG})")
                        continue

                for ftype, extensions in FILE_TYPES.items():
                    if ext in extensions:
                        results[ftype].append(str(filepath))
                        classified = True
                        break

                if not classified:
                    results["unclassified"].append(str(filepath))

    return results, skipped

def save_results(data, skipped):
    payload = {
        "identity": IDENTITY,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "focus": FOCUS_TAG,
        "keywords": DOMAIN_KEYWORDS,
        "paths_scanned": SCAN_PATHS,
        "excluded": EXCLUDE_PATHS,
        "file_summary": {k: len(v) for k,v in data.items()},
        "files": data
    }

    try:
        with open(OUTPUT_FILE, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"\n✅ Scan complete. Saved to: {OUTPUT_FILE}")
    except Exception as e:
        print(f"⚠️ Failed to save results: {e}")

    if LOG_SKIPPED and skipped:
        try:
            with open(SKIP_LOG, "w") as f:
                for line in skipped:
                    f.write(line + "\n")
            print(f"📓 Skipped items logged to: {SKIP_LOG}")
        except:
            print("⚠️ Couldn't log skipped items.")

def main():
    print(f"\n📡 Verobrix Rootscan — Identity: {IDENTITY} — Focus: {FOCUS_TAG}")
    print(f"📁 Domain keywords: {', '.join(DOMAIN_KEYWORDS) if DOMAIN_KEYWORDS else 'None'}")
    print(f"📁 Scanning paths:")
    for p in SCAN_PATHS:
        print(f"   - {p}")

    results, skipped = scan_files()
    save_results(results, skipped)

if __name__ == "__main__":
    main()
