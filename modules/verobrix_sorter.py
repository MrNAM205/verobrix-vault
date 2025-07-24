#!/usr/bin/env python3
import os, json, shutil
from pathlib import Path

base = Path.home() / "verobrix"
scan_file = base / "output/vault_scan.json"
sorted_dir = base / "vault/sorted"
sorted_dir.mkdir(parents=True, exist_ok=True)

buckets = {
    "journal_inputs": [".txt", ".md", ".log", ".out"],
    "code_modules": [".py", ".sh", ".js", ".bat"],
    "salvage_images": [".jpg", ".jpeg", ".png", ".gif"],
    "archives": [".zip", ".rar", ".tar", ".gz"],
    "docs": [".pdf", ".docx"],
    "unknowns": []
}

def classify_file(path):
    ext = Path(path).suffix.lower()
    for label, types in buckets.items():
        if ext in types:
            return label
    return "unknowns"

def sort_files(data):
    log = []
    for category, files in data.items():
        for file in files:
            tag = classify_file(file)
            dest_dir = sorted_dir / tag
            dest_dir.mkdir(exist_ok=True)
            try:
                dest_path = dest_dir / Path(file).name
                shutil.copy2(file, dest_path)
                log.append(f"✅ {file} → {dest_path}")
            except Exception as e:
                log.append(f"⚠️ Could not move {file}: {e}")
    return log

def main():
    if not scan_file.exists():
        print("🚫 No scan file found. Run rootscan first.")
        return
    with open(scan_file) as f:
        data = json.load(f)
    actions = sort_files(data)
    print("\n🗂️ Vault Sorting Log:")
    for line in actions:
        print(" " + line)

if __name__ == "__main__":
    main()
