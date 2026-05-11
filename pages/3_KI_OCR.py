import streamlit as st
import base64
import json
import requests

st.set_page_config(page_title="KI-OCR", page_icon="🤖")

def extract_text_and_data(file_bytes, file_type):
    try:
        b64 = base64.b64encode(file_bytes).decode()

        prompt = """
        Du bist eine professionelle Beleg-KI.
        Analysiere den hochgeladenen Beleg (Bild oder PDF) und extrahiere:

        - Datum
        - Betrag (Brutto)
        - Netto
        - MwSt-Satz
        - Händler
        - Kategorie (Lebensmittel, Haushalt, Gesundheit, Fahrtkosten, Sonstiges)
        - Beschreibung

        Gib das Ergebnis **ausschließlich als JSON** zurück, z.B.:

        {
            "datum": "2026-05-11",
            "betrag": 12.49,
            "netto": 10.50,
            "mwst": 19,
            "haendler": "REWE",
            "kategorie": "Lebensmittel",
            "beschreibung": "Einkauf"
        }
        """

        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers={"Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}"},
            json={
                "model": "gpt-4o-mini",
                "input": [
                    {"role": "user", "content": prompt},
                    {"role": "user", "image": b64}
                ]
            }
        )

        return response.json()

    except Exception as e:
        return {"error": str(e)}


st.title("🤖 KI-OCR – Automatische Belegerkennung")
st.write("Lade ein Bild oder PDF hoch. Die KI erkennt automatisch Datum, Betrag, MwSt, Händler und Kategorie.")

uploaded = st.file_uploader("Datei auswählen", type=["png", "jpg", "jpeg", "pdf"])

if uploaded:
    file_bytes = uploaded.read()
    file_type = uploaded.type

    st.info("⏳ KI analysiert den Beleg… bitte warten…")

    result = extract_text_and_data(file_bytes, file_type)

    if "error" in result:
        st.error("Fehler bei der KI-Verarbeitung:")
        st.code(result["error"])
    else:
        st.success("Beleg erfolgreich erkannt!")
        st.subheader("📄 KI-Ergebnis (JSON)")
        st.json(result)

        # Felder extrahieren
        datum = result.get("datum", "")
        betrag = result.get("betrag", "")
        netto = result.get("netto", "")
        mwst = result.get("mwst", "")
        haendler = result.get("haendler", "")
        kategorie = result.get("kategorie", "")
        beschreibung = result.get("beschreibung", "")

        st.subheader("📝 Automatisch ausgefülltes Formular")

        col1, col2 = st.columns(2)

        with col1:
            f_datum = st.text_input("Datum", datum)
            f_betrag = st.text_input("Betrag (€)", str(betrag))
            f_netto = st.text_input("Netto (€)", str(netto))

        with col2:
            f_mwst = st.text_input("MwSt (%)", str(mwst))
            f_kategorie = st.text_input("Kategorie", kategorie)
            f_haendler = st.text_input("Händler", haendler)

        f_beschreibung = st.text_area("Beschreibung", beschreibung)

        if st.button("Beleg übernehmen"):
            st.success("Beleg wurde übernommen (hier später in DB speichern).")
