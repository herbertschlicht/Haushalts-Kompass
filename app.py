import streamlit as st

st.set_page_config(
    page_title="Haushalts-Kompass",
    page_icon="💶",
    layout="wide",
)

st.title("💶 Haushalts-Kompass")
st.markdown("Willkommen im **Haushalts-Kompass** – dein Kompass für Haushalt, Belege, Arztkosten und Steuer.")

st.markdown(
    """
    ### Bereiche
    - 📊 Dashboard (Überblick)
    - 📄 Belege (Erfassung, Upload, KI-Analyse)
    - 🧾 Steuer (Auswertung)
    - 🩺 Arzt & Fahrten (später eigene Seite)
    - 📘 Journal & Druckansicht (später)
    """
)

st.info("Nutze das Seiten-Menü links (Pages), um zwischen Dashboard und Belegen zu wechseln.")
