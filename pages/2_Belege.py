import streamlit as st
import pandas as pd
from pathlib import Path
from services.data_service import load_entries, save_entries

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="Belege – Haushalts-Kompass", page_icon="📄", layout="wide")

st.title("📄 Belege")

st.subheader("Neuen Beleg erfassen")

col1, col2 = st.columns(2)
with col1:
    betrag = st.number_input("Betrag (€)", min_value=0.0, step=0.01)
    kategorie = st.text_input("Kategorie", value="Lebensmittel")
    art = st.selectbox("Art", ["Allgemein", "Arzt", "Fahrt", "Sonstiges"])
with col2:
    datum = st.date_input("Datum")
    kommentar = st.text_input("Kommentar", value="")

uploaded_file = st.file_uploader("Beleg-Datei hochladen (optional)", type=["jpg", "jpeg", "png", "pdf"])

if st.button("Beleg speichern"):
    entries = load_entries()
    file_path_str = None

    if uploaded_file is not None:
        file_path = UPLOAD_DIR / uploaded_file.name
        with file_path.open("wb") as f:
            f.write(uploaded_file.getbuffer())
        file_path_str = str(file_path)

    new_entry = {
        "betrag": float(betrag),
        "kategorie": kategorie,
        "art": art,
        "datum": str(datum),
        "kommentar": kommentar,
        "datei": file_path_str,
    }
    entries.append(new_entry)
    save_entries(entries)
    st.success("Beleg gespeichert.")

st.subheader("Erfasste Belege")

entries = load_entries()
if entries:
    df = pd.DataFrame(entries)
    st.dataframe(df, use_container_width=True)

    st.subheader("Auswertung nach Kategorie")
    agg = df.groupby("kategorie")["betrag"].sum().reset_index()
    st.bar_chart(agg, x="kategorie", y="betrag")

    st.subheader("Filter")
    sel_art = st.multiselect("Art filtern", options=df["art"].unique(), default=list(df["art"].unique()))
    df_filt = df[df["art"].isin(sel_art)]
    st.dataframe(df_filt, use_container_width=True)
else:
    st.info("Noch keine Belege erfasst.")
