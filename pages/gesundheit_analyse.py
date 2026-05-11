import streamlit as st
import pandas as pd
from datetime import date

from services.data_service_gesundheit import load_entries_gesundheit


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
    st.title("🩺 Gesundheit – Analyse (Premium)")

    st.write(
        "Detaillierte Auswertung der Gesundheitskosten mit Fokus auf "
        "Eigenanteile, Erstattungen, Kategorien und zeitliche Entwicklung."
    )

    data = load_entries_gesundheit()
    df = _safe_df(data)

    if len(df) == 0:
        st.info("Noch keine Gesundheitsdaten vorhanden.")
        return

    aktuelles_jahr = date.today().year

    # Filterbereich
    st.sidebar.header("Filter – Gesundheit")
    jahre = sorted(df["jahr"].unique())
    jahr_auswahl = st.sidebar.selectbox("Jahr", jahre, index=jahre.index(aktuelles_jahr) if aktuelles_jahr in jahre else 0)

    df_jahr = df[df["jahr"] == jahr_auswahl]

    kategorien = sorted(df_jahr["kategorie"].dropna().unique()) if "kategorie" in df_jahr.columns else []
    kategorie_auswahl = st.sidebar.multiselect("Kategorien", kategorien, default=kategorien)

    if kategorie_auswahl:
        df_jahr = df_jahr[df_jahr["kategorie"].isin(kategorie_auswahl)]

    # KPIs
    st.subheader(f"📌 Kennzahlen {jahr_auswahl}")

    sum_gesamt = df_jahr["betrag"].sum()
    sum_eigenanteil = df_jahr["eigenanteil"].sum() if "eigenanteil" in df_jahr.columns else 0.0
    sum_nicht_erstattet = df_jahr[df_jahr.get("erstattet", "") == "Nein"]["betrag"].sum() if "erstattet" in df_jahr.columns else 0.0

    erstattete = df_jahr[df_jahr.get("erstattet", "") == "Ja"]["betrag"].sum() if "erstattet" in df_jahr.columns else 0.0
    erstattungsquote = (erstattete / sum_gesamt * 100) if sum_gesamt > 0 else 0.0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Gesundheitskosten gesamt", f"{sum_gesamt:,.2f} €".replace(",", " "))
    with col2:
        st.metric("Eigenanteile gesamt", f"{sum_eigenanteil:,.2f} €".replace(",", " "))
    with col3:
        st.metric("Nicht erstattete Kosten", f"{sum_nicht_erstattet:,.2f} €".replace(",", " "))

    col4, col5 = st.columns(2)
    with col4:
        st.metric("Erstattete Kosten", f"{erstattete:,.2f} €".replace(",", " "))
    with col5:
        st.metric("Erstattungsquote", f"{erstattungsquote:.1f} %")

    # Monatsverlauf
    st.subheader("📆 Monatsverlauf – Gesundheitskosten")

    monat_agg = (
        df_jahr.groupby("monat")[["betrag", "eigenanteil"]]
        .sum()
        .reset_index()
        .sort_values("monat")
    )
    monat_agg["Monat"] = monat_agg["monat"].astype(str)
    monat_agg = monat_agg.set_index("Monat")

    st.line_chart(monat_agg)

    # Kategorien – Heilbehandlungen vs. Medikamente vs. Rest
    st.subheader("🏷️ Kategorien – Struktur der Gesundheitskosten")

    heil_kategorien = ["Physiotherapie", "Ergotherapie", "Logopädie", "Akupunktur", "Osteopathie"]
    arzt_kategorien = [
        "Allgemeinmedizin", "Orthopädie", "Kardiologie", "Dermatologie", "Neurologie",
        "HNO", "Augenarzt", "Diabetologie", "Pneumologie", "Psychotherapie", "Krankenhaus", "Labor"
    ]
    medi_kategorien = ["Medikamente", "Hilfsmittel"]

    heil_summe = df_jahr[df_jahr["kategorie"].isin(heil_kategorien)]["betrag"].sum()
    arzt_summe = df_jahr[df_jahr["kategorie"].isin(arzt_kategorien)]["betrag"].sum()
    medi_summe = df_jahr[df_jahr["kategorie"].isin(medi_kategorien)]["betrag"].sum()
    rest_summe = sum_gesamt - (heil_summe + arzt_summe + medi_summe)

    kat_df = pd.DataFrame(
        {
            "Kategorie": ["Heilbehandlungen", "Arztkosten", "Medikamente & Hilfsmittel", "Sonstige"],
            "Betrag (€)": [heil_summe, arzt_summe, medi_summe, rest_summe],
        }
    ).set_index("Kategorie")

    st.bar_chart(kat_df)

    # Top-Kategorien
    st.subheader("🏷️ Top-Kategorien (Detail)")

    if "kategorie" in df_jahr.columns:
        top_kat = (
            df_jahr.groupby("kategorie")["betrag"]
            .sum()
            .reset_index()
            .sort_values("betrag", ascending=False)
            .head(15)
        )
        top_kat.columns = ["Kategorie", "Gesundheitskosten (€)"]
        st.bar_chart(top_kat.set_index("Kategorie"))
    else:
        st.info("Keine Kategorien in den Gesundheitsdaten vorhanden.")

    # Detailtabelle
    st.subheader("📋 Detailtabelle – gefilterte Gesundheitsdaten")
    st.dataframe(df_jahr.sort_values("datum", ascending=False), use_container_width=True)

    st.caption(
        "Diese Analyse zeigt Gesundheitskosten, Eigenanteile, Erstattungen und die Verteilung "
        "auf medizinische Kategorien. Filter links anpassen, um gezielt Bereiche zu untersuchen."
    )
