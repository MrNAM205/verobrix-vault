#!/usr/bin/env python3
import json
from pathlib import Path

BASE = Path.home() / "verobrix"
SCAN_FILE = BASE / "output/rootscan_results.json"
KEYWORDS_FILE = BASE / "config/domain_keywords.json"
OUTPUT = BASE / "output/semantic_reflection.json"

def load_scan():
    try:
        with open(SCAN_FILE) as f:
            return json.load(f)
    except:
        print("⚠️ Scan results not found.")
        return {}

def load_keywords(tag):
    try:
        with open(KEYWORDS_FILE) as f:
            all_keys = json.load(f)
            return all_keys.get(tag, [])
    except:
        return []

def semantic_filter(files, keywords):
    reflections = []

    for ftype, paths in files.items():
        for path in paths:
            path_lower = path.lower()
            matched = [kw for kw in keywords if kw in path_lower]
            if matched:
                reflections.append({
                    "file": path,
                    "type": ftype,
                    "matched_keywords": matched
                })

    return reflections

def main():
    scan = load_scan()
    tag = scan.get("focus", "multi")
    files = scan.get("files", {})
    keywords = load_keywords(tag)

    print(f"\n🧠 Verobrix Semantic — Focus: {tag}")
    print(f"🔍 Keywords: {', '.join(keywords) if keywords else 'None'}")

    reflections = semantic_filter(files, keywords)

    payload = {
        "tag": tag,
        "timestamp": scan.get("timestamp", ""),
        "keywords_used": keywords,
        "files_matched": len(reflections),
        "reflections": reflections
    }

    try:
        with open(OUTPUT, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"\n✅ Semantic reflection saved: {OUTPUT}")
    except Exception as e:
        print(f"⚠️ Failed to save reflection: {e}")

if __name__ == "__main__":
    main()
