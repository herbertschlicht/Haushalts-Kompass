import streamlit as st
import pandas as pd
import altair as alt
from services.data_service_gesundheit import load_entries_gesundheit

def show():
    st.title("🩺 Gesundheit – Dashboard")

    # Daten laden
    eintraege = load_entries_gesundheit()

    if len(eintraege) == 0:
        st.info("Noch keine Gesundheitsbelege vorhanden.")
        return

    # In DataFrame umwandeln
    df = pd.DataFrame(eintraege)
    df["betrag"] = df["betrag"].astype(float)
    df["datum"] = pd.to_datetime(df["datum"])

    st.subheader("Gesamtkosten Gesundheit")
    gesamt = df["betrag"].sum()
    st.metric("Summe aller Gesundheitskosten", f"{gesamt:.2f} €")

    # Kosten pro Fachrichtung / Kategorie
    st.subheader("Kosten pro Fachrichtung")
    kat_sum = df.groupby("kategorie")["betrag"].sum().reset_index()

    chart_kat = (
        alt.Chart(kat_sum)
        .mark_bar()
        .encode(
            x=alt.X("kategorie:N", sort="-y", title="Fachrichtung"),
            y=alt.Y("betrag:Q", title="Betrag (€)"),
            tooltip=["kategorie", "betrag"]
        )
        .properties(height=400)
    )
    st.altair_chart(chart_kat, use_container_width=True)

    # Monatsverlauf
    st.subheader("Monatlicher Kostenverlauf")
    df["monat"] = df["datum"].dt.to_period("M").astype(str)
    monat_sum = df.groupby("monat")["betrag"].sum().reset_index()

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

    # Top 5 Kostenstellen
    st.subheader("Top 5 Gesundheitskosten")
    top5 = kat_sum.sort_values("betrag", ascending=False).head(5)
    st.table(top5)
