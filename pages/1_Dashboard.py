import streamlit as st
import pandas as pd
from services.data_service import load_entries

st.set_page_config(page_title="Dashboard – Haushalts-Kompass", page_icon="📊", layout="wide")

st.title("📊 Dashboard")

entries = load_entries()
if not entries:
    st.info("Noch keine Daten vorhanden. Erfasse zuerst Belege auf der Seite **Belege**.")
else:
    df = pd.DataFrame(entries)

    col1, col2, col3 = st.columns(3)
    with col1:
        gesamt = df["betrag"].sum()
        st.metric("Gesamtausgaben", f"{gesamt:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))
    with col2:
        anzahl = len(df)
        st.metric("Anzahl Belege", anzahl)
    with col3:
        kategorien = df["kategorie"].nunique()
        st.metric("Kategorien", kategorien)

    st.subheader("Ausgaben nach Kategorie")
    agg_cat = df.groupby("kategorie")["betrag"].sum().reset_index()
    st.bar_chart(agg_cat, x="kategorie", y="betrag")

    if "datum" in df.columns:
        st.subheader("Ausgaben über die Zeit")
        df["datum"] = pd.to_datetime(df["datum"], errors="coerce")
        df_time = df.dropna(subset=["datum"]).set_index("datum").resample("M")["betrag"].sum()
        st.line_chart(df_time)
