#!/usr/bin/env python3
import json, sys
from pathlib import Path
from difflib import SequenceMatcher
from datetime import datetime

# === Paths ===
BASE         = Path.home() / "verobrix"
DBFILE       = BASE / "verobrix_db.json"
REFLECTION   = BASE / "output/semantic_reflection.json"
LOGFILE      = BASE / "journal/dialogue_log.txt"

# === Helpers ===
def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return []

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def extract_relevant(query, reflections, db):
    tokens = query.lower().split()
    summary_blurbs = []
    contradictions = []
    files = []

    for cluster in reflections.get("reflections", []):
        score = sum(similar(q, kw) for q in tokens for kw in cluster["summary"].get("keywords", []))
        if score > 1.0:
            summary_blurbs.append(f"🪶 {cluster['tag']}: {cluster['summary']['summary']}")
            for con in cluster.get("contradictions", []):
                contradictions.append(f"⚠️ '{con['keyword']}' appears in: {', '.join(con['files'])}")

    for e in db:
        score = sum(similar(q, kw) for q in tokens for kw in e.get("keywords", []))
        if score > 1.0:
            files.append(f"• {e['file']} ({e['domain']}) — {e['summary'][:60]}...")

    return summary_blurbs, contradictions, files

def narrate(query, blurbs, contradictions, files):
    lines = [f"🧠 Verobrix reflects on: \"{query}\""]
    if blurbs:
        lines += ["", "📚 Insights:"] + blurbs
    if contradictions:
        lines += ["", "⚔️ Contradictions:"] + contradictions
    if files:
        lines += ["", f"📁 Related Files ({len(files)}):"] + files
    if not (blurbs or files):
        lines += ["🤷 No strong matches found in memory."]
    return "\n".join(lines)

def log_dialogue(query, output):
    with open(LOGFILE, "a") as f:
        f.write(f"\n=== Dialogue {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        f.write(f"> {query}\n")
        f.write(output + "\n")

def main():
    if len(sys.argv) < 2:
        print("🗣️ Usage: python3 verobrix_dialogue.py \"your statement or question\"")
        return

    query = sys.argv[1]
    reflection = load_json(REFLECTION)
    db         = load_json(DBFILE)
    blurbs, contradictions, files = extract_relevant(query, reflection, db)
    output = narrate(query, blurbs, contradictions, files)
    print(f"\n{output}")
    log_dialogue(query, output)

if __name__ == "__main__":
    main()
