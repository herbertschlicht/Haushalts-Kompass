import json
from pathlib import Path
from typing import List, Dict, Any

# Eigene Datenbank für Haushalt
DB_PATH = Path("database_haushalt.json")

def load_entries_haushalt() -> List[Dict[str, Any]]:
    if DB_PATH.exists():
        try:
            with DB_PATH.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    else:
        # Datei anlegen, wenn sie fehlt
        with DB_PATH.open("w", encoding="utf-8") as f:
            json.dump([], f)
        return []

def save_entries_haushalt(entries: List[Dict[str, Any]]) -> None:
    with DB_PATH.open("w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
