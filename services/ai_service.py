from typing import Optional, Dict, Any
from google import genai

def get_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)

def analyze_receipt_bytes(client: genai.Client, image_bytes: bytes) -> Dict[str, Any]:
    try:
        result = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[image_bytes, "Extrahiere Betrag, Datum, Kategorie und Beschreibung aus diesem Beleg. Antworte kurz strukturiert."]
        )
        return {"raw": result.text}
    except Exception as e:
        return {"error": str(e)}
