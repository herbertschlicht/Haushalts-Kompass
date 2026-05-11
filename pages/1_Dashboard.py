import streamlit as st
import pandas as pd
from datetime import date

from services.data_service_haushalt import load_entries_haushalt
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


def _year_progress():
    today = date.today()
    start = date(today.year, 1, 1)
    end = date(today.year, 12, 31)
    days_total = (end - start).days + 1
    days_passed = (today - start).days + 1
    return today.year, days_passed / days_total * 100


def show():
    st.title("📊 Haushalts-Kompass – Dashboard")

    st.write(
        "Übersicht über **Haushalt** und **Gesundheit** mit "
        "Steuerfokus, Jahresfortschritt und wichtigsten Kennzahlen."
    )

    # Daten laden
    haushalt_raw = load_entries_haushalt()
    gesundheit_raw = load_entries_gesundheit()

    haushalt = _safe_df(haushalt_raw)
    gesundheit = _safe_df(gesundheit_raw)

    aktuelles_jahr = date.today().year

    # Filter auf aktuelles Jahr
    if len(haushalt) > 0:
        haushalt_jahr = haushalt[haushalt["jahr"] == aktuelles_jahr]
    else:
        haushalt_jahr = haushalt

    if len(gesundheit) > 0:
        gesundheit_jahr = gesundheit[gesundheit["jahr"] == aktuelles_jahr]
    else:
        gesundheit_jahr = gesundheit

    # -----------------------------
    # Jahresfortschritt
    # -----------------------------
    jahr, progress = _year_progress()
    st.subheader(f"📅 Jahresfortschritt {jahr}")
    st.progress(min(1.0, progress / 100.0))
    st.caption(f"{progress:.1f} % des Jahres sind bereits vergangen.")

    # -----------------------------
    # Kennzahlen – Haushalt & Gesundheit
    # -----------------------------
    st.subheader("📌 Zentrale Kennzahlen")

    # Haushalt-KPIs
    if len(haushalt_jahr) > 0:
        sum_brutto_h = haushalt_jahr["betrag_brutto"].sum()
        sum_netto_h = haushalt_jahr["betrag_netto"].sum()
        sum_mwst_h = haushalt_jahr["mwst_betrag"].sum()
    else:
        sum_brutto_h = sum_netto_h = sum_mwst_h = 0.0

    # Gesundheit-KPIs
    if len(gesundheit_jahr) > 0:
        sum_gesundheit = gesundheit_jahr["betrag"].sum()
        sum_eigenanteil = gesundheit_jahr["eigenanteil"].sum()
        sum_nicht_erstattet = gesundheit_jahr[
            gesundheit_jahr["erstattet"] == "Nein"
        ]["betrag"].sum()
    else:
        sum_gesundheit = sum_eigenanteil = sum_nicht_erstattet = 0.0

    # Steuerlich absetzbar (vereinfachte Sicht)
    steuerlich_absetzbar = sum_eigenanteil + (sum_gesundheit - sum_eigenanteil)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💶 Haushalt – Brutto gesamt", f"{sum_brutto_h:,.2f} €".replace(",", " "))
        st.metric("🧾 MwSt gesamt", f"{sum_mwst_h:,.2f} €".replace(",", " "))
    with col2:
        st.metric("🩺 Gesundheitskosten gesamt", f"{sum_gesundheit:,.2f} €".replace(",", " "))
        st.metric("💊 Eigenanteile gesamt", f"{sum_eigenanteil:,.2f} €".replace(",", " "))
    with col3:
        st.metric("⚖️ Steuerlich absetzbar (vereinfacht)", f"{steuerlich_absetzbar:,.2f} €".replace(",", " "))
        st.metric("🚫 Nicht erstattete Kosten", f"{sum_nicht_erstattet:,.2f} €".replace(",", " "))

    # -----------------------------
    # Monatsübersichten – Haushalt & Gesundheit
    # -----------------------------
    st.subheader("📆 Monatsübersichten")

    col_h, col_g = st.columns(2)

    with col_h:
        st.markdown("**Haushalt – Monatsausgaben (Brutto)**")
        if len(haushalt_jahr) > 0:
            monat_h = (
                haushalt_jahr.groupby("monat")["betrag_brutto"]
                .sum()
                .reset_index()
                .sort_values("monat")
            )
            monat_h["Monat"] = monat_h["monat"].astype(str)
            monat_h = monat_h[["Monat", "betrag_brutto"]]
            monat_h.columns = ["Monat", "Brutto (€)"]
            st.bar_chart(monat_h.set_index("Monat"))
        else:
            st.info("Keine Haushaltsdaten für das aktuelle Jahr.")

    with col_g:
        st.markdown("**Gesundheit – Monatsausgaben**")
        if len(gesundheit_jahr) > 0:
            monat_g = (
                gesundheit_jahr.groupby("monat")["betrag"]
                .sum()
                .reset_index()
                .sort_values("monat")
            )
            monat_g["Monat"] = monat_g["monat"].astype(str)
            monat_g = monat_g[["Monat", "betrag"]]
            monat_g.columns = ["Monat", "Gesundheitskosten (€)"]
            st.bar_chart(monat_g.set_index("Monat"))
        else:
            st.info("Keine Gesundheitsdaten für das aktuelle Jahr.")

    # -----------------------------
    # Top-Kategorien
    # -----------------------------
    st.subheader("🏷️ Top-Kategorien")

    col_h2, col_g2 = st.columns(2)

    with col_h2:
        st.markdown("**Haushalt – Top-Kategorien (Brutto)**")
        if len(haushalt_jahr) > 0 and "kategorie" in haushalt_jahr.columns:
            top_h = (
                haushalt_jahr.groupby("kategorie")["betrag_brutto"]
                .sum()
                .reset_index()
                .sort_values("betrag_brutto", ascending=False)
                .head(10)
            )
            top_h.columns = ["Kategorie", "Brutto (€)"]
            st.bar_chart(top_h.set_index("Kategorie"))
        else:
            st.info("Keine Haushaltskategorien verfügbar.")

    with col_g2:
        st.markdown("**Gesundheit – Top-Kategorien**")
        if len(gesundheit_jahr) > 0 and "kategorie" in gesundheit_jahr.columns:
            top_g = (
                gesundheit_jahr.groupby("kategorie")["betrag"]
                .sum()
                .reset_index()
                .sort_values("betrag", ascending=False)
                .head(10)
            )
            top_g.columns = ["Kategorie", "Gesundheitskosten (€)"]
            st.bar_chart(top_g.set_index("Kategorie"))
        else:
            st.info("Keine Gesundheitskategorien verfügbar.")

    # -----------------------------
    # Schnellzugriffe
    # -----------------------------
    st.subheader("⚡ Schnellzugriffe")

    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.page_link("pages/2_Belege.py", label="🧾 Belege – Übersicht", icon="📂")
    with col_b:
        st.page_link("pages/haushalt_belege.py", label="🏠 Haushalt – Belege", icon="🧾")
    with col_c:
        st.page_link("pages/gesundheit_belege.py", label="🩺 Gesundheit – Belege", icon="🧾")
    with col_d:
        st.page_link("pages/steuer_auswertung.py", label="📘 Steuer-Auswertung", icon="📊")

    st.caption(
        "Dieses Dashboard fasst die wichtigsten Kennzahlen zusammen und bietet "
        "direkte Einstiege in alle relevanten Bereiche."
    )
