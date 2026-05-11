import streamlit as st
import pandas as pd
from services.data_service_gesundheit import load_entries_gesundheit, save_entry_gesundheit

def show():
    st.title("🩺 Gesundheit – Belege")

    st.subheader("Neuen Gesundheitsbeleg erfassen")

    # Eingabefelder
    col1, col2 = st.columns(2)
    datum = col1.date_input("Datum")

    # Sehr detaillierte medizinische Kategorien (G2)
    kategorie = col2.selectbox(
        "Art der medizinischen Leistung",
        [
            "Allgemeinmedizin",
            "Orthopädie",
            "Kardiologie",
            "Dermatologie",
            "Neurologie",
            "HNO",
            "Augenarzt",
            "Diabetologie",
            "Pneumologie",
            "Psychotherapie",
            "Krankenhaus",
            "Labor",
            "Physiotherapie",
            "Ergotherapie",
            "Logopädie",
            "Akupunktur",
            "Osteopathie",
            "Medikamente",
            "Hilfsmittel",
            "Fahrtkosten",
            "Sonstige medizinische Kosten"
        ]
    )

    betrag = st.number_input("Gesamtbetrag (€)", min_value=0.0, step=0.10)

    # Steuerrelevante Felder
    col3, col4 = st.columns(2)
    eingereicht = col3.selectbox("Eingereicht?", ["Nein", "Ja"])
    erstattet = col4.selectbox("Erstattet?", ["Nein", "Ja"])

    eigenanteil = st.number_input(
        "Eigenanteil (€)", 
        min_value=0.0, 
        step=0.10,
        help="Der Teil, den du selbst zahlen musst (für außergewöhnliche Belastungen)."
    )

    kommentar = st.text_input("Kommentar (optional)")

    if st.button("Beleg speichern"):
        eintrag = {
            "datum": str(datum),
            "kategorie": kategorie,
            "betrag": round(betrag, 2),
            "eingereicht": eingereicht,
            "erstattet": erstattet,
            "eigenanteil": round(eigenanteil, 2),
            "kommentar": kommentar
        }

        save_entry_gesundheit(eintrag)
        st.success("Gesundheitsbeleg gespeichert!")

    st.subheader("Gespeicherte Gesundheitsbelege")

    eintraege = load_entries_gesundheit()

    if len(eintraege) == 0:
        st.info("Noch keine Gesundheitsbelege vorhanden.")
        return

    df = pd.DataFrame(eintraege)
    st.dataframe(df, use_container_width=True)
