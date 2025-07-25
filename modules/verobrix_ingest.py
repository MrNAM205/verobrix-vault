#!/usr/bin/env python3
import os, json, time
from pathlib import Path
from collections import defaultdict

# === Paths ===
BASE       = Path.home() / "verobrix"
VAULTS     = BASE / "vaults"
LOGFILE    = BASE / "journal/ingest_log.txt"
DBFILE     = BASE / "verobrix_db.json"
EXTENSIONS = [".txt", ".md", ".log", ".py", ".conf"]

def extract_keywords(text):
    words = text.lower().split()
    keywords = [w.strip('.,:;()[]{}') for w in words if 3 < len(w) < 20]
    return list(set(keywords))

def summarize(text, maxlen=200):
    return text.strip().replace('\n', ' ')[:maxlen] + "..."

def ingest_file(filepath, domain_tag):
    try:
        with open(filepath, "r", errors="ignore") as f:
            content = f.read()
        entry = {
            "file": str(filepath.name),
            "keywords": extract_keywords(content),
            "domain": domain_tag,
            "summary": summarize(content),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "source": str(filepath)
        }
        return entry
    except Exception as e:
        print(f"⚠️ Failed to ingest {filepath}: {e}")
        return None

def log_ingestion(entries):
    with open(LOGFILE, "a") as f:
        f.write(f"\n=== Ingest Log {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        for e in entries:
            f.write(f"{e['file']} ({e['domain']})\n - {', '.join(e['keywords'][:10])}\n")

def load_existing_db():
    try:
        with open(DBFILE) as f:
            return json.load(f)
    except:
        return []

def save_db(entries):
    with open(DBFILE, "w") as f:
        json.dump(entries, f, indent=2)
    print(f"🧠 Knowledge base updated: {DBFILE}")

def main():
    print("\n🧠 Verobrix Ingest — Archive Absorption Begins")
    all_entries = []
    for vault in VAULTS.iterdir():
        if not vault.is_dir(): continue
        domain = vault.name
        for root, _, files in os.walk(vault):
            for fname in files:
                path = Path(root) / fname
                if path.suffix.lower() in EXTENSIONS:
                    entry = ingest_file(path, domain)
                    if entry: all_entries.append(entry)

    if not all_entries:
        print("⚠️ No valid files ingested.")
        return

    prev_db = load_existing_db()
    combined = prev_db + all_entries
    save_db(combined)
    log_ingestion(all_entries)
    print(f"\n✅ Ingested {len(all_entries)} files across {len(set(e['domain'] for e in all_entries))} vaults.")

if __name__ == "__main__":
    main()
