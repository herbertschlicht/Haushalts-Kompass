import streamlit as st
from pages import belegeseite, dashboardseite, analyseseite, einstellungen

# Titel oben
st.set_page_config(page_title="Haushalts-Kompass", layout="wide")

# Sidebar Navigation
st.sidebar.title("📘 Haushalts-Kompass")
auswahl = st.sidebar.radio(
    "Navigation",
    ["Belege", "Dashboard", "Analyse", "Einstellungen"]
)

# Seitenlogik
if auswahl == "Belege":
    belegeseite.show()

elif auswahl == "Dashboard":
    dashboardseite.show()

elif auswahl == "Analyse":
    analyseseite.show()

elif auswahl == "Einstellungen":
    einstellungen.show()
