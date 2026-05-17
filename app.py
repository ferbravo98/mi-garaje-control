import streamlit as st

from translations import TEXTS
from database import create_tables
from pages_app import (
    render_dashboard,
    render_vehiculos,
    render_mantenimientos,
    render_reportes,
)


st.set_page_config(
    page_title="Mi Garaje Control",
    page_icon="🚗",
    layout="wide",
)

create_tables()

language = st.sidebar.selectbox("Idioma / Language", ["es", "en"])
t = TEXTS[language]

st.title(t["app_title"])
st.write(t["app_description"])

st.sidebar.title(t["menu"])
section = st.sidebar.radio(
    "Sección" if language == "es" else "Section",
    [
        "Dashboard",
        "Vehículos",
        "Mantenimientos",
        "Reportes",
    ],
)

if section == "Dashboard":
    render_dashboard(language)
elif section == "Vehículos":
    render_vehiculos(language)
elif section == "Mantenimientos":
    render_mantenimientos(language)
elif section == "Reportes":
    render_reportes(language)
