#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

base = Path.home() / "verobrix"
scan_file = base / "output/vault_scan.json"
journal_dir = base / "journal"
journal_dir.mkdir(parents=True, exist_ok=True)

def load_scan():
    if not scan_file.exists():
        print("🚫 No scan data found. Run rootscan first.")
        return None
    with open(scan_file) as f:
        return json.load(f)

def summarize(data):
    summary = {}
    total = 0
    for key, files in data.items():
        count = len(files)
        summary[key] = count
        total += count
    return summary, total

def reflect(summary, total):
    highlights = []
    if total == 0:
        return "I scanned, but found nothing in the archive today."

    most = max(summary, key=summary.get)
    if summary[most] > 0:
        highlights.append(f"Most abundant: {most} ({summary[most]} files)")

    empty = [k for k, v in summary.items() if v == 0]
    if empty:
        highlights.append(f"Empty types: {', '.join(empty)}")

    return f"""📜 Verobrix Vault Report:
Today I scanned {total} files.
{', '.join(highlights)}.
My archive grows clearer with each pass."""

def write_journal(content):
    ts = datetime.now().isoformat()
    filename = f"report_{ts[:10]}.txt"
    with open(journal_dir / filename, "w") as f:
        f.write(content)
    print(f"📝 Reflection written → {filename}")

def main():
    scan = load_scan()
    if not scan:
        return
    summary, total = summarize(scan)
    note = reflect(summary, total)
    print("\n🔍 Vault Summary:")
    for k, v in summary.items():
        print(f" • {k}: {v}")
    print("\n🧠 Reflection:")
    print(note)
    write_journal(note)

if __name__ == "__main__":
    main()
