import streamlit as st
from pages import belegeseite, dashboardseite, analyseseite, einstellungen

# Titel oben
st.set_page_config(page_title="Haushalts-Kompass", layout="wide")

# Sidebar Navigation
st.sidebar.title("📘 Haushalts-Kompass")
auswahl = st.sidebar.radio(
    "Navigation",
    [
        "Haushalt – Belege",
        "Haushalt – Dashboard",
        "Haushalt – Analyse",
        "Gesundheit – Belege",
        "Gesundheit – Dashboard",
        "Gesundheit – Analyse",
        "Einstellungen"
    ]
)

# Seitenlogik
if auswahl == "Haushalt – Belege":
    from pages.haushalt_belege import show
    show()

elif auswahl == "Haushalt – Dashboard":
    st.write("Dashboard Haushalt kommt gleich...")

elif auswahl == "Haushalt – Analyse":
    st.write("Analyse Haushalt kommt gleich...")

elif auswahl == "Gesundheit – Belege":
    from pages.gesundheit_belege import show
    show()

elif auswahl == "Gesundheit – Dashboard":
    st.write("Dashboard Gesundheit kommt gleich...")

elif auswahl == "Gesundheit – Analyse":
    st.write("Analyse Gesundheit kommt gleich...")

elif auswahl == "Einstellungen":
    st.write("Einstellungen kommen gleich...")
