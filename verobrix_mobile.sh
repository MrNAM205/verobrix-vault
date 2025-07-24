#!/data/data/com.termux/files/usr/bin/bash
cd ~/verobrix/modules
echo "🧠 Launching Verobrix Cognition Cycle..."
python verobrix_rootscan.py
python verobrix_cleaner.py
python verobrix_report.py
python verobrix_sorter.py
python verobrix_semantic.py
echo "✅ Cycle complete. Reflection and semantic tagging done."
