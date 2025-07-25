#!/usr/bin/env python3
import json, sys
from pathlib import Path
from difflib import SequenceMatcher
from datetime import datetime

# === Paths ===
BASE       = Path.home() / "verobrix"
DBFILE     = BASE / "verobrix_db.json"
REFLECTION = BASE / "output/semantic_reflection.json"
LOGFILE    = BASE / "journal/query_log.txt"

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return []

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def match_keywords(query, entries):
    query_tokens = query.lower().split()
    matches = []
    for e in entries:
        score = sum(similar(q, kw) for q in query_tokens for kw in e.get("keywords", []))
        if score > 1.5:
            matches.append((score, e))
    matches.sort(reverse=True, key=lambda x: x[0])
    return [m[1] for m in matches[:5]]

def search_reflections(query, reflections):
    query_tokens = query.lower().split()
    results = []
    for cluster in reflections.get("reflections", []):
        score = sum(similar(q, kw) for q in query_tokens for kw in cluster["summary"].get("keywords", []))
        if score > 1.0:
            results.append({
                "tag": cluster["tag"],
                "summary": cluster["summary"]["summary"],
                "contradictions": cluster.get("contradictions", [])
            })
    return results[:3]

def log_query(query, results):
    with open(LOGFILE, "a") as f:
        f.write(f"\n=== Query {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        f.write(f"> {query}\n")
        for r in results:
            f.write(f"- {r['file']} ({r['domain']})\n")

def main():
    if len(sys.argv) < 2:
        print("🗣️ Usage: python3 verobrix_query.py \"your question here\"")
        return

    query = sys.argv[1]
    print(f"\n🔍 Verobrix Query: \"{query}\"")

    db         = load_json(DBFILE)
    reflection = load_json(REFLECTION)

    if not db:
        print("⚠️ Knowledge base empty.")
        return

    entries = match_keywords(query, db)
    clusters = search_reflections(query, reflection)

    if not entries and not clusters:
        print("🤷‍♀️ No relevant matches found.")
        return

    print(f"\n📚 Found {len(entries)} relevant entries:")
    for e in entries:
        print(f"• {e['file']} ({e['domain']}) — {e['summary'][:60]}...")

    if clusters:
        print(f"\n🧠 Semantic Reflections:")
        for c in clusters:
            print(f"🪶 Domain: {c['tag']}")
            print(f"  ↳ {c['summary']}")
            if c['contradictions']:
                print("  ⚠️ Contradictions:")
                for con in c['contradictions']:
                    print(f"     - {con['keyword']} in: {', '.join(con['files'])}")

    log_query(query, entries)
    print(f"\n📓 Query logged.")

if __name__ == "__main__":
    main()
