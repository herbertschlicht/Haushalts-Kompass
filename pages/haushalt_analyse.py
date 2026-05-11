import streamlit as st
import pandas as pd
import altair as alt
from services.data_service_haushalt import load_entries_haushalt

def show():
    st.title("📈 Haushalt – Analyse")

    # Daten laden
    eintraege = load_entries_haushalt()

    if len(eintraege) == 0:
        st.info("Noch keine Haushaltsbelege vorhanden.")
        return

    # DataFrame
    df = pd.DataFrame(eintraege)
    df["betrag"] = df["betrag"].astype(float)
    df["datum"] = pd.to_datetime(df["datum"])

    st.subheader("Filter")

    # Filter: Zeitraum
    col1, col2 = st.columns(2)
    start_datum = col1.date_input("Startdatum", df["datum"].min())
    end_datum = col2.date_input("Enddatum", df["datum"].max())

    # Filter: Kategorie
    kategorien = ["Alle"] + sorted(df["kategorie"].unique().tolist())
    kategorie_filter = st.selectbox("Kategorie", kategorien)

    # Filter anwenden
    df_filtered = df[(df["datum"] >= pd.to_datetime(start_datum)) &
                     (df["datum"] <= pd.to_datetime(end_datum))]

    if kategorie_filter != "Alle":
        df_filtered = df_filtered[df_filtered["kategorie"] == kategorie_filter]

    st.subheader("Gefilterte Belege")
    st.dataframe(df_filtered, use_container_width=True)

    # Gesamtsumme
    summe = df_filtered["betrag"].sum()
    st.metric("Summe der gefilterten Ausgaben", f"{summe:.2f} €")

    # Kategorienvergleich
    st.subheader("Ausgaben pro Kategorie (gefiltert)")
    kat_sum = df_filtered.groupby("kategorie")["betrag"].sum().reset_index()

    if len(kat_sum) > 0:
        chart_kat = (
            alt.Chart(kat_sum)
            .mark_bar()
            .encode(
                x=alt.X("kategorie:N", sort="-y", title="Kategorie"),
                y=alt.Y("betrag:Q", title="Betrag (€)"),
                tooltip=["kategorie", "betrag"]
            )
            .properties(height=400)
        )
        st.altair_chart(chart_kat, use_container_width=True)
    else:
        st.info("Keine Daten für Kategorienvergleich.")

    # Monatsanalyse
    st.subheader("Monatliche Entwicklung (gefiltert)")
    df_filtered["monat"] = df_filtered["datum"].dt.to_period("M").astype(str)
    monat_sum = df_filtered.groupby("monat")["betrag"].sum().reset_index()

    if len(monat_sum) > 0:
        chart_monat = (
            alt.Chart(monat_sum)
            .mark_line(point=True)
            .encode(
                x=alt.X("monat:N", title="Monat"),
                y=alt.Y("betrag:Q", title="Betrag (€)"),
                tooltip=["monat", "betrag"]
            )
            .properties(height=400)
        )
        st.altair_chart(chart_monat, use_container_width=True)
    else:
        st.info("Keine Monatsdaten verfügbar.")
