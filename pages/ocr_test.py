import streamlit as st
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes

def show():
    st.title("🖼️ OCR Test – Bild & PDF")

    st.write("Wähle ein Bild oder PDF aus, um die Texterkennung (OCR) zu testen.")

    uploaded_file = st.file_uploader("Datei auswählen", type=["png", "jpg", "jpeg", "pdf"])

    if uploaded_file:
        file_type = uploaded_file.type

        if file_type == "application/pdf":
            st.info("PDF erkannt – konvertiere Seiten…")
            pages = convert_from_bytes(uploaded_file.read())
            text_total = ""

            for i, page in enumerate(pages):
                st.image(page, caption=f"PDF Seite {i+1}", use_column_width=True)
                text = pytesseract.image_to_string(page, lang="deu")
                text_total += f"\n\n--- Seite {i+1} ---\n{text}"

            st.subheader("🔍 OCR Ergebnis (PDF)")
            st.text_area("Erkannter Text", text_total, height=400)

        else:
            image = Image.open(uploaded_file)
            st.image(image, caption="Ausgewähltes Bild", use_column_width=True)

            st.subheader("🔍 OCR Ergebnis (Bild)")
            text = pytesseract.image_to_string(image, lang="deu")
            st.text_area("Erkannter Text", text, height=300)
