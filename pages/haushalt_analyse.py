import streamlit as st
import pandas as pd
from datetime import date

from services.data_service_haushalt import load_entries_haushalt


def _safe_df(data):
    df = pd.DataFrame(data)
    if len(df) == 0:
        return df
    if "datum" in df.columns:
        df["datum"] = pd.to_datetime(df["datum"])
        df["jahr"] = df["datum"].dt.year
        df["monat"] = df["datum"].dt.to_period("M")
    return df


def show():
    st.title("🏠 Haushalt – Analyse (Premium)")

    st.write(
        "Detaillierte Auswertung der Haushaltsdaten mit Fokus auf "
        "Netto, MwSt, Kategorien und zeitlichen Verläufen."
    )

    data = load_entries_haushalt()
    df = _safe_df(data)

    if len(df) == 0:
        st.info("Noch keine Haushaltsdaten vorhanden.")
        return

    aktuelles_jahr = date.today().year

    # Filterbereich
    st.sidebar.header("Filter – Haushalt")
    jahre = sorted(df["jahr"].unique())
    jahr_auswahl = st.sidebar.selectbox("Jahr", jahre, index=jahre.index(aktuelles_jahr) if aktuelles_jahr in jahre else 0)

    df_jahr = df[df["jahr"] == jahr_auswahl]

    kategorien = sorted(df_jahr["kategorie"].dropna().unique()) if "kategorie" in df_jahr.columns else []
    kategorie_auswahl = st.sidebar.multiselect("Kategorien", kategorien, default=kategorien)

    if kategorie_auswahl:
        df_jahr = df_jahr[df_jahr["kategorie"].isin(kategorie_auswahl)]

    # KPIs
    st.subheader(f"📌 Kennzahlen {jahr_auswahl}")

    sum_brutto = df_jahr["betrag_brutto"].sum()
    sum_netto = df_jahr["betrag_netto"].sum()
    sum_mwst = df_jahr["mwst_betrag"].sum()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Brutto gesamt", f"{sum_brutto:,.2f} €".replace(",", " "))
    with col2:
        st.metric("Netto gesamt", f"{sum_netto:,.2f} €".replace(",", " "))
    with col3:
        st.metric("MwSt gesamt", f"{sum_mwst:,.2f} €".replace(",", " "))

    # Monatsverlauf
    st.subheader("📆 Monatsverlauf – Brutto / Netto / MwSt")

    monat_agg = (
        df_jahr.groupby("monat")[["betrag_brutto", "betrag_netto", "mwst_betrag"]]
        .sum()
        .reset_index()
        .sort_values("monat")
    )
    monat_agg["Monat"] = monat_agg["monat"].astype(str)
    monat_agg = monat_agg.set_index("Monat")

    st.line_chart(monat_agg)

    # Top-Kategorien
    st.subheader("🏷️ Top-Kategorien (Brutto)")

    if "kategorie" in df_jahr.columns:
        top_kat = (
            df_jahr.groupby("kategorie")["betrag_brutto"]
            .sum()
            .reset_index()
            .sort_values("betrag_brutto", ascending=False)
            .head(15)
        )
        top_kat.columns = ["Kategorie", "Brutto (€)"]
        st.bar_chart(top_kat.set_index("Kategorie"))
    else:
        st.info("Keine Kategorien in den Haushaltsdaten vorhanden.")

    # Detailtabelle
    st.subheader("📋 Detailtabelle – gefilterte Haushaltsdaten")
    st.dataframe(df_jahr.sort_values("datum", ascending=False), use_container_width=True)

    st.caption(
        "Diese Analyse zeigt Netto, Brutto und MwSt nach Jahr, Monat und Kategorie. "
        "Filter links anpassen, um gezielt Bereiche zu untersuchen."
    )
