import json
from pathlib import Path
from typing import List, Dict, Any

# Speicherort für Streamlit Cloud
DB_PATH = Path("/mount/data/database.json")

def load_entries() -> List[Dict[str, Any]]:
    try:
        if DB_PATH.exists():
            with DB_PATH.open("r", encoding="utf-8") as f:
                return json.load(f)
        else:
            # Datei automatisch anlegen, wenn sie fehlt
            with DB_PATH.open("w", encoding="utf-8") as f:
                json.dump([], f)
            return []
    except Exception:
        return []

def save_entries(entries: List[Dict[str, Any]]) -> None:
    # Datei immer überschreiben – Streamlit darf das
    with DB_PATH.open("w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

