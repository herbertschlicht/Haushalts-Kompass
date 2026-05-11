import streamlit as st
import pandas as pd
from services.data_service_haushalt import load_entries_haushalt
from services.data_service_gesundheit import load_entries_gesundheit

def show():
    st.title("📊 Steuer-Auswertung")

    st.write("Diese Seite kombiniert Haushalt + Gesundheit für steuerliche Zwecke:")

    st.markdown("""
    - **MwSt / Vorsteuer** (monatlich & jährlich)  
    - **Außergewöhnliche Belastungen**  
    - **Eigenanteile**  
    - **Nicht erstattete Kosten**  
    - **Heilbehandlungen / Medikamente / Arztkosten**  
    - **Jahresübersicht**  
    """)

    # ---------------------------------------------------------
    # HAUSHALT – MwSt / Vorsteuer
    # ---------------------------------------------------------
    st.header("🧾 Haushalt – MwSt / Vorsteuer")

    haushalt = pd.DataFrame(load_entries_haushalt())

    if len(haushalt) == 0:
        st.info("Keine Haushaltsdaten vorhanden.")
    else:
        haushalt["datum"] = pd.to_datetime(haushalt["datum"])
        haushalt["monat"] = haushalt["datum"].dt.to_period("M")
        haushalt["jahr"] = haushalt["datum"].dt.year

        # Monatliche MwSt
        monat_mwst = haushalt.groupby("monat")["mwst_betrag"].sum().reset_index()
        monat_mwst.columns = ["Monat", "MwSt (€)"]

        # Jährliche MwSt
        jahr_mwst = haushalt.groupby("jahr")["mwst_betrag"].sum().reset_index()
        jahr_mwst.columns = ["Jahr", "MwSt (€)"]

        st.subheader("📅 Monatliche MwSt / Vorsteuer")
        st.dataframe(monat_mwst, use_container_width=True)

        st.subheader("📆 Jährliche MwSt / Vorsteuer")
        st.dataframe(jahr_mwst, use_container_width=True)

    # ---------------------------------------------------------
    # GESUNDHEIT – außergewöhnliche Belastungen
    # ---------------------------------------------------------
    st.header("🩺 Gesundheit – Außergewöhnliche Belastungen")

    gesundheit = pd.DataFrame(load_entries_gesundheit())

    if len(gesundheit) == 0:
        st.info("Keine Gesundheitsdaten vorhanden.")
        return

    gesundheit["datum"] = pd.to_datetime(gesundheit["datum"])
    gesundheit["jahr"] = gesundheit["datum"].dt.year

    # Summen
    summe_eigenanteile = gesundheit["eigenanteil"].sum()
    summe_nicht_erstattet = gesundheit[gesundheit["erstattet"] == "Nein"]["betrag"].sum()

    # Kategorien
    heilbehandlungen = gesundheit[
        gesundheit["kategorie"].isin(["Physiotherapie", "Ergotherapie", "Logopädie", "Akupunktur", "Osteopathie"])
    ]["betrag"].sum()

    arztkosten = gesundheit[
        gesundheit["kategorie"].isin([
            "Allgemeinmedizin", "Orthopädie", "Kardiologie", "Dermatologie", "Neurologie",
            "HNO", "Augenarzt", "Diabetologie", "Pneumologie", "Psychotherapie", "Krankenhaus", "Labor"
        ])
    ]["betrag"].sum()

    medikamente = gesundheit[
        gesundheit["kategorie"].isin(["Medikamente", "Hilfsmittel"])
    ]["betrag"].sum()

    # Jahresübersicht Gesundheit
    jahreswerte = gesundheit.groupby("jahr")[["betrag", "eigenanteil"]].sum().reset_index()
    jahreswerte.columns = ["Jahr", "Gesamtkosten (€)", "Eigenanteile (€)"]

    st.subheader("💶 Summen für außergewöhnliche Belastungen")
    st.write(f"**Eigenanteile gesamt:** {summe_eigenanteile:.2f} €")
    st.write(f"**Nicht erstattete Kosten:** {summe_nicht_erstattet:.2f} €")

    st.subheader("🧩 Aufschlüsselung nach Kategorien")
    st.write(f"**Heilbehandlungen:** {heilbehandlungen:.2f} €")
    st.write(f"**Arztkosten:** {arztkosten:.2f} €")
    st.write(f"**Medikamente & Hilfsmittel:** {medikamente:.2f} €")

    st.subheader("📆 Jahresübersicht Gesundheit")
    st.dataframe(jahreswerte, use_container_width=True)

    st.subheader("📋 Alle Gesundheitsbelege")
    st.dataframe(gesundheit, use_container_width=True)

    # ---------------------------------------------------------
    # KOMBINIERTE JAHRESÜBERSICHT – Haushalt + Gesundheit
    # ---------------------------------------------------------
    st.header("📘 Kombinierte Jahres-Steuerübersicht")

    # Haushalt Jahreswerte
    if len(haushalt) > 0:
        haushalt_jahr = haushalt.groupby("jahr")[["mwst_betrag", "betrag_netto", "betrag_brutto"]].sum()
        haushalt_jahr.columns = ["MwSt Haushalt (€)", "Netto Haushalt (€)", "Brutto Haushalt (€)"]
    else:
        haushalt_jahr = pd.DataFrame()

    # Gesundheit Jahreswerte
    if len(gesundheit) > 0:
        gesundheit_jahr = gesundheit.groupby("jahr")[["betrag", "eigenanteil"]].sum()
        gesundheit_jahr.columns = ["Gesundheitskosten (€)", "Eigenanteile (€)"]
    else:
        gesundheit_jahr = pd.DataFrame()

    # Zusammenführen
    if len(haushalt_jahr) > 0 or len(gesundheit_jahr) > 0:
        combined = pd.concat([haushalt_jahr, gesundheit_jahr], axis=1).fillna(0)

        # Steuerlich relevante Summe
        combined["Steuerlich absetzbar (€)"] = (
            combined["Eigenanteile (€)"] +
            (combined["Gesundheitskosten (€)"] - combined["Eigenanteile (€)"])
        )

        st.subheader("📊 Jahresübersicht – Gesamt")
        st.dataframe(combined, use_container_width=True)

        st.info(
            "Die Spalte **„Steuerlich absetzbar“** enthält:\n"
            "- Eigenanteile\n"
            "- nicht erstattete Gesundheitskosten\n"
            "- medizinisch notwendige Leistungen"
        )
    else:
        st.info("Noch keine Daten für eine kombinierte Übersicht vorhanden.")
