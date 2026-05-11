import json
from pathlib import Path
from typing import List, Dict, Any

DB_PATH = Path("database.json")

def load_entries() -> List[Dict[str, Any]]:
    if not DB_PATH.exists():
        return []
    try:
        with DB_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_entries(entries: List[Dict[str, Any]]) -> None:
    with DB_PATH.open("w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
