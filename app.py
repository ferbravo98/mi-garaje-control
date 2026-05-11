import streamlit as st
import pandas as pd

from translations import TEXTS
from database import create_tables, add_vehicle, get_vehicles


st.set_page_config(
    page_title="Mi Garaje Control",
    page_icon="🚗",
    layout="wide"
)

create_tables()

language = st.sidebar.selectbox("Idioma / Language", ["es", "en"])
t = TEXTS[language]

st.title(t["app_title"])
st.write(t["app_description"])

st.sidebar.title(t["menu"])
section = st.sidebar.radio(
    "Sección" if language == "es" else "Section",
    ["Vehículos", "Mantenimientos", "Reportes"]
)

if section == "Vehículos":
    st.header("Vehículos" if language == "es" else "Vehicles")

    with st.form("vehicle_form"):
        marca = st.text_input("Marca" if language == "es" else "Brand")
        modelo = st.text_input("Modelo" if language == "es" else "Model")
        anio = st.number_input(
            "Año" if language == "es" else "Year",
            min_value=1900,
            max_value=2100,
            step=1
        )
        tipo = st.selectbox(
            "Tipo" if language == "es" else "Type",
            ["Auto", "Moto"] if language == "es" else ["Car", "Motorcycle"]
        )
        patente = st.text_input("Patente" if language == "es" else "License plate")
        kilometraje_actual = st.number_input(
            "Kilometraje actual" if language == "es" else "Current mileage",
            min_value=0,
            step=100
        )

        submitted = st.form_submit_button(
            "Guardar vehículo" if language == "es" else "Save vehicle"
        )

    if submitted:

        marca = marca.strip()
        modelo = modelo.strip()
        patente = patente.strip()

        errores = []

        if not marca:
            errores.append(
                "La marca es obligatoria."
                if language == "es"
                else "Brand is required."
            )

        if not modelo:
            errores.append(
                "El modelo es obligatorio."
                if language == "es"
                else "Model is required."
            )

        if kilometraje_actual < 1:
            errores.append(
                "El kilometraje debe ser mayor a 0."
                if language == "es"
                else "Mileage must be greater than 0."
            )

        if errores:
            for error in errores:
                st.error(error)

        else:
            add_vehicle(
                marca,
                modelo,
                anio,
                tipo,
                patente,
                kilometraje_actual
            )

            st.success(
                "Vehículo guardado correctamente."
                if language == "es"
                else "Vehicle saved successfully."
            )

    st.subheader("Vehículos registrados" if language == "es" else "Registered vehicles")

    vehicles = get_vehicles()

    if vehicles:
        df = pd.DataFrame(
            vehicles,
            columns=[
                "ID",
                "Marca",
                "Modelo",
                "Año",
                "Tipo",
                "Patente",
                "Kilometraje",
                "Fecha creación"
            ]
        )
        st.dataframe(df, use_container_width=True)
    else:
        st.info(
            "Todavía no hay vehículos registrados."
            if language == "es"
            else "No vehicles registered yet."
        )

elif section == "Mantenimientos":
    st.header("Mantenimientos" if language == "es" else "Maintenance")
    st.info("Esta sección se desarrollará en el próximo módulo.")

elif section == "Reportes":
    st.header("Reportes" if language == "es" else "Reports")
    st.info("Esta sección se desarrollará más adelante.")