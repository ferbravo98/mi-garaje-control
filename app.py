import streamlit as st
import pandas as pd
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

#inject_global_styles()
create_tables()

language = st.sidebar.selectbox("Idioma / Language", ["es", "en"])
t = TEXTS[language]

st.markdown(
    f"""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="margin-bottom: 0.25rem;">🚗 {t["app_title"]}</h1>
        <p style="color: #64748B; margin: 0; font-size: 1rem;">{t["app_description"]}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("---")
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
