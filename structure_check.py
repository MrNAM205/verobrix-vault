# structure_check.py

import os

base_path = "verobrix"

# Define expected structure
structure = {
    "verobrix": [
        "loop.py"
    ],
    "verobrix_ingest": [
        "ingest.py",
        "memory_load.py"
    ],
    "verobrix_utils": [
        "log_query.py",
        "timestamp.py"
    ],
    "verobrix_ethos": [
        "synthesize_response.py"
    ],
    "verobrix_dialogue": [
        "reflect.py",
        "journal.py"
    ]
}

def ensure_structure(base):
    for folder, files in structure.items():
        path = os.path.join(base, folder) if folder != "verobrix" else base
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"📁 Created missing folder: {path}")

        for file in files:
            file_path = os.path.join(path, file)
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    f.write(f"# 🧠 Stub for {file}\n")
                print(f"📝 Created missing file: {file_path}")

if __name__ == "__main__":
    ensure_structure(base_path)
