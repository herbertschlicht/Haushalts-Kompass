import streamlit as st
from PIL import Image
import pytesseract

def show():
    st.title("🖼️ OCR Test – Bild zu Text")

    st.write("Wähle ein Bild aus, um die Texterkennung (OCR) zu testen.")

    uploaded_file = st.file_uploader("Bild auswählen", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Ausgewähltes Bild", use_column_width=True)

        st.subheader("🔍 OCR Ergebnis")
        text = pytesseract.image_to_string(image, lang="deu")
        st.text_area("Erkannter Text", text, height=300)
