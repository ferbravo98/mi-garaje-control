import streamlit as st


def render_reportes(language):
    st.header("Reportes" if language == "es" else "Reports")
    st.info(
        "Esta sección se desarrollará más adelante."
        if language == "es"
        else "This section will be developed later."
    )
