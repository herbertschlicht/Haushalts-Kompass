import streamlit as st
import pandas as pd
from services.data_service_haushalt import load_entries_haushalt, save_entry_haushalt
from services.steuer_config import get_steuersatz_for_category, berechne_netto_und_mwst

def show():
    st.title("🧾 Haushalt – Belege")

    st.subheader("Neuen Beleg erfassen")

    # Eingabefelder
    col1, col2 = st.columns(2)
    datum = col1.date_input("Datum")
    kategorie = col2.selectbox(
        "Kategorie",
        [
            "Haushalt", "Elektronik", "Dienstleistungen", "Haushaltswaren",
            "Handwerker", "Auto", "Garten",
            "Lebensmittel", "Bücher", "Zeitschriften",
            "Miete", "Versicherung", "Gebühren", "Bank", "Spenden"
        ]
    )

    betrag_brutto = st.number_input("Bruttobetrag (€)", min_value=0.0, step=0.10)

    # Automatischer Steuersatz-Vorschlag
    vorgeschlagen = get_steuersatz_for_category(kategorie)

    # Manuelle Überschreibung (K3)
    steuersatz_key = st.selectbox(
        "Steuersatz",
        ["19", "7", "0"],
        index=["19", "7", "0"].index(vorgeschlagen)
    )

    # Netto + MwSt berechnen
    betrag_netto, mwst_betrag = berechne_netto_und_mwst(betrag_brutto, steuersatz_key)

    st.info(
        f"**Netto:** {betrag_netto:.2f} €\n\n"
        f"**MwSt:** {mwst_betrag:.2f} €\n\n"
        f"**Brutto:** {betrag_brutto:.2f} €"
    )

    kommentar = st.text_input("Kommentar (optional)")

    if st.button("Beleg speichern"):
        eintrag = {
            "datum": str(datum),
            "kategorie": kategorie,
            "betrag_brutto": round(betrag_brutto, 2),
            "betrag_netto": round(betrag_netto, 2),
            "mwst_betrag": round(mwst_betrag, 2),
            "steuersatz": steuersatz_key,
            "kommentar": kommentar
        }

        save_entry_haushalt(eintrag)
        st.success("Beleg gespeichert!")

    st.subheader("Gespeicherte Belege")

    eintraege = load_entries_haushalt()

    if len(eintraege) == 0:
        st.info("Noch keine Belege vorhanden.")
        return

    df = pd.DataFrame(eintraege)
    st.dataframe(df, use_container_width=True)
