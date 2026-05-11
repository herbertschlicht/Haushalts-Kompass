import json
from pathlib import Path
from typing import List, Dict, Any

# Speicherort für Streamlit Cloud (schreibbar!)
DB_PATH = Path("/mount/data/database.json")

def load_entries() -> List[Dict[str, Any]]:
    if not DB_PATH.exists():
        return []
    try:
        with DB_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_entries(entries: List[Dict[str, Any]]) -> None:
    # Stelle sicher, dass der Ordner existiert
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DB_PATH.open("w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
