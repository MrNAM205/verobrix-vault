import os
import shutil

ROOT = os.path.expanduser("~/verobrix/")
MODULES = [
    "verobrix_core",
    "verobrix_ingest",
    "verobrix_dialogue",
    "verobrix_utils",
    "verobrix_ethos"
]
NESTED = os.path.join(ROOT, "verobrix")  # suspect folder

def move_file(file, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    shutil.move(file, os.path.join(target_dir, os.path.basename(file)))
    print(f"📁 Moved {file} → {target_dir}")

def scan_and_relocate():
    if not os.path.isdir(NESTED):
        print("✅ No nested 'verobrix/' folder found.")
        return

    for item in os.listdir(NESTED):
        path = os.path.join(NESTED, item)
        if os.path.isfile(path) and item.endswith(".py"):
            move_file(path, os.path.join(ROOT, "modules", "verobrix_core"))
        elif os.path.isdir(path) and item.startswith("verobrix_"):
            dest = os.path.join(ROOT, "modules", item)
            move_file(path, dest)

def suggest_removals():
    candidates = ["vault", "journal", "output", "verobrix"]
    print("\n🧠 Suggested Clean-Up:")
    for folder in candidates:
        full = os.path.join(ROOT, folder)
        if os.path.exists(full):
            print(f" - '{folder}' exists. Consider reviewing its contents.")

if __name__ == "__main__":
    print("🔄 Beginning Verobrix cleanup...\n")
    scan_and_relocate()
    suggest_removals()
    print("\n🧼 Clean-up complete. Nothing deleted, only guided.")
