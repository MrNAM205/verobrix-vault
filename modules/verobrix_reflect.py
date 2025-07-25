#!/usr/bin/env python3
import json, time
from pathlib import Path
from collections import defaultdict, Counter

# === Paths ===
BASE         = Path.home() / "verobrix"
DBFILE       = BASE / "verobrix_db.json"
REFLECTION   = BASE / "output/semantic_reflection.json"
LOGFILE      = BASE / "journal/reflection_log.txt"

# === Helpers ===
def load_db():
    try:
        with open(DBFILE) as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load DB: {e}")
        return []

def cluster_by_domain(entries):
    clusters = defaultdict(list)
    for e in entries:
        tag = e.get("domain", "unknown")
        clusters[tag].append(e)
    return clusters

def summarize_cluster(cluster):
    keywords = Counter()
    for entry in cluster:
        keywords.update(entry.get("keywords", []))
    common = [kw for kw, _ in keywords.most_common(6)]
    files = [e["file"] for e in cluster]
    return {
        "count": len(cluster),
        "keywords": common,
        "files": files,
        "summary": f"This cluster contains {len(cluster)} entries focused on {', '.join(common)}."
    }

def detect_contradictions(cluster):
    contradictions = []
    seen = defaultdict(list)
    for e in cluster:
        for kw in e.get("keywords", []):
            seen[kw].append(e["file"])
    for kw, files in seen.items():
        if len(files) > 1 and kw in ["voltage", "config", "setting"]:
            contradictions.append({
                "keyword": kw,
                "files": files[:5]
            })
    return contradictions

def log_reflection(domain, summary, contradictions):
    with open(LOGFILE, "a") as f:
        f.write(f"\n=== Reflection: {domain} @ {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        f.write(summary["summary"] + "\n")
        if contradictions:
            f.write("⚡ Contradictions detected:\n")
            for c in contradictions:
                f.write(f" - '{c['keyword']}' in: {', '.join(c['files'])}\n")

def save_reflection(reflections):
    with open(REFLECTION, "w") as f:
        json.dump(reflections, f, indent=2)
    print(f"🧠 Reflection saved: {REFLECTION}")

def main():
    print("\n🔁 Verobrix Reflection — Semantic Awareness Begins")
    db = load_db()
    if not db:
        print("⚠️ Empty knowledge base.")
        return

    clusters = cluster_by_domain(db)
    reflections = {"reflections": []}

    for domain, cluster in clusters.items():
        summary = summarize_cluster(cluster)
        contradictions = detect_contradictions(cluster)
        log_reflection(domain, summary, contradictions)

        reflections["reflections"].append({
            "tag": domain,
            "summary": summary,
            "contradictions": contradictions
        })

    save_reflection(reflections)
    print(f"\n✅ Reflected on {len(clusters)} domains. Insights logged & contradictions mapped.")

if __name__ == "__main__":
    main()
