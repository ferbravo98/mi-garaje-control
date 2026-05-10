import streamlit as st
from translations import TEXTS

st.set_page_config(
    page_title="Mi Garaje Control",
    page_icon="🚗",
    layout="wide"
)

language = st.sidebar.selectbox("Idioma / Language", ["es", "en"])
t = TEXTS[language]

st.title(t["app_title"])
st.write(t["app_description"])

st.sidebar.title(t["menu"])
st.sidebar.info(t["version"])