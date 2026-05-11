import streamlit as st
from services.data_service_haushalt import load_entries_haushalt, save_entries_haushalt

def show():
    st.title("🏠 Haushalt – Belege erfassen")

    st.subheader("Neuen Haushaltsbeleg hinzufügen")

    # Kategorien für Haushalt
    haushalt_kategorien = [
        "Lebensmittel", "Drogerie", "Haushalt", "Auto", "Benzin",
        "Strom", "Gas", "Wasser", "Internet", "Telefon",
        "Versicherungen", "Kleidung", "Freizeit", "Restaurant",
        "Geschenke", "Garten", "Haustiere", "Reparaturen",
        "Möbel", "Elektronik", "Transport", "Sonstiges"
    ]

    betrag = st.number_input("Betrag (€)", min_value=0.0, format="%.2f")
    kategorie = st.selectbox("Kategorie", haushalt_kategorien)
    datum = st.date_input("Datum")
    kommentar = st.text_input("Kommentar")

    # Platzhalter für spätere Scan-Funktion
    st.info("📸 Scan-Funktion für Kassenbons wird später integriert.")

    if st.button("Beleg speichern"):
        eintrag = {
            "betrag": betrag,
            "kategorie": kategorie,
            "datum": str(datum),
            "kommentar": kommentar
        }

        eintraege = load_entries_haushalt()
        eintraege.append(eintrag)
        save_entries_haushalt(eintraege)

        st.success("Haushaltsbeleg gespeichert!")

    st.subheader("Gespeicherte Haushaltsbelege")
    eintraege = load_entries_haushalt()

    if len(eintraege) == 0:
        st.info("Noch keine Haushaltsbelege vorhanden.")
    else:
        st.dataframe(eintraege, use_container_width=True)
