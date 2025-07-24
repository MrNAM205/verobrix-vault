#!/usr/bin/env python3
import json
from pathlib import Path

base = Path.home() / "verobrix"
folders = ["modules", "config", "output", "vault", "journal"]
modules = [
    "verobrix_rootscan.py",
    "verobrix_report.py",
    "verobrix_sorter.py",
    "verobrix_cleaner.py",
    "verobrix_semantic.py",
    "verobrix_launch.py"
]

def check_folders():
    print("\n📁 Verifying folders:")
    for name in folders:
        path = base / name
        status = "✅" if path.exists() else "❌"
        print(f" {status} {name}")

def check_modules():
    print("\n🧠 Checking modules:")
    mod_path = base / "modules"
    for name in modules:
        path = mod_path / name
        status = "✅" if path.exists() else "❌"
        print(f" {status} {name}")

def check_scan():
    scan_file = base / "output/vault_scan.json"
    semantic_file = base / "output/vault_semantics.json"
    print("\n🔍 Scan status:")
    if scan_file.exists():
        print(" ✅ vault_scan.json found")
    else:
        print(" ❌ No rootscan results")

    if semantic_file.exists():
        try:
            with open(semantic_file) as f:
                data = json.load(f)
            count = len(data)
            print(f" ✅ Semantics annotated → {count} files")
        except:
            print(" ⚠️ Error reading vault_semantics.json")
    else:
        print(" ❌ No semantic output yet")

def main():
    print("\n🧼 Verobrix System Checkup")
    check_folders()
    check_modules()
    check_scan()
    print("\n✨ Status reflected. Ready for cognition cycle.\n")

if __name__ == "__main__":
    main()
