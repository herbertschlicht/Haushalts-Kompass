import streamlit as st
from services.data_service_gesundheit import load_entries_gesundheit, save_entries_gesundheit

def show():
    st.title("🩺 Gesundheit – Belege erfassen")

    st.subheader("Neue Gesundheitskosten hinzufügen")

    # Kategorien für Gesundheit
    gesundheits_kategorien = [
        "Allgemeinmedizin", "Kardiologie", "Pneumologie", "Diabetologie",
        "Dermatologie", "Orthopädie", "Neurologie", "HNO", "Augenarzt",
        "Zahnarzt", "Labor", "Medikamente", "Physiotherapie",
        "Psychotherapie", "Krankenhaus", "Fahrtkosten", "Sonstiges"
    ]

    betrag = st.number_input("Betrag (€)", min_value=0.0, format="%.2f")
    kategorie = st.selectbox("Kategorie", gesundheits_kategorien)
    datum = st.date_input("Datum")
    kommentar = st.text_input("Kommentar")

    # Platzhalter für spätere Scan-Funktion
    st.info("📸 Scan-Funktion für Arztrechnungen wird später integriert.")

    if st.button("Beleg speichern"):
        eintrag = {
            "betrag": betrag,
            "kategorie": kategorie,
            "datum": str(datum),
            "kommentar": kommentar
        }

        eintraege = load_entries_gesundheit()
        eintraege.append(eintrag)
        save_entries_gesundheit(eintraege)

        st.success("Gesundheitsbeleg gespeichert!")

    st.subheader("Gespeicherte Gesundheitsbelege")
    eintraege = load_entries_gesundheit()

    if len(eintraege) == 0:
        st.info("Noch keine Gesundheitsbelege vorhanden.")
    else:
        st.dataframe(eintraege, use_container_width=True)
