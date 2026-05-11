import streamlit as st
from services.data_service import load_entries, save_entries

def show():
    st.title("🧾 Belege erfassen")

    st.subheader("Neuen Beleg hinzufügen")

    # Eingabefelder
    betrag = st.number_input("Betrag (€)", min_value=0.0, format="%.2f")
    kategorie = st.text_input("Kategorie")
    art = st.selectbox("Art", ["Allgemein", "Arzt", "Medikamente", "Fahrtkosten", "Sonstiges"])
    datum = st.date_input("Datum")
    kommentar = st.text_input("Kommentar")

    if st.button("Beleg speichern"):
        eintrag = {
            "betrag": betrag,
            "kategorie": kategorie,
            "art": art,
            "datum": str(datum),
            "kommentar": kommentar
        }

        eintraege = load_entries()
        eintraege.append(eintrag)
        save_entries(eintraege)

        st.success("Beleg gespeichert!")

    st.subheader("Gespeicherte Belege")
    eintraege = load_entries()

    if len(eintraege) == 0:
        st.info("Noch keine Belege vorhanden.")
    else:
        st.dataframe(eintraege, use_container_width=True)
