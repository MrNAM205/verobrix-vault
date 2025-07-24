#!/usr/bin/env python3
import os, json
from pathlib import Path

base = Path.home() / "verobrix"
scan_path = base / "output/vault_scan.json"
themes_path = base / "config/verobrix_themes.json"
output_path = base / "output/vault_semantics.json"

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        print(f"⚠️ Cannot load {path.name}")
        return {}

def match_keywords(text, vocab):
    found = []
    text = text.lower()
    for theme, words in vocab.items():
        if any(w.lower() in text for w in words):
            found.append(theme)
    return found

def match_tags(text, tags):
    return [t for t in tags if t.lower() in text.lower()]

def scan_semantics(scan_data, vocab):
    results = []
    keyword_map = vocab.get("keywords", {})
    priority = vocab.get("priority_tags", [])

    for category, files in scan_data.items():
        for file in files:
            name = Path(file).name
            match = match_keywords(name, keyword_map)
            tags = match_tags(name, priority)
            if match or tags:
                results.append({
                    "file": file,
                    "themes": match,
                    "tags": tags,
                    "original_type": category
                })
    return results

def main():
    scan = load_json(scan_path)
    vocab = load_json(themes_path)
    if not scan or not vocab:
        return

    print("🔍 Semantic scan started...")
    annotated = scan_semantics(scan, vocab)

    with open(output_path, "w") as f:
        json.dump(annotated, f, indent=2)
    print(f"🧠 Semantic output → {output_path}")
    print(f"🗂️ Annotated {len(annotated)} files")

if __name__ == "__main__":
    main()
