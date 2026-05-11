import streamlit as st
import pandas as pd

from translations import TEXTS
from database import (
    create_tables,
    add_vehicle,
    get_vehicles,
    add_maintenance,
    get_maintenance_by_vehicle,
    get_total_vehicles,
    get_total_maintenances,
    get_last_maintenances
)


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
    [
    "Dashboard",
    "Vehículos",
    "Mantenimientos",
    "Reportes"
]
)

if section == "Dashboard":

    st.header(
        "Dashboard"
        if language == "es"
        else "Dashboard"
    )

    total_vehicles = get_total_vehicles()
    total_maintenances = get_total_maintenances()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Vehículos registrados"
            if language == "es"
            else "Registered vehicles",
            total_vehicles
        )

    with col2:
        st.metric(
            "Mantenimientos registrados"
            if language == "es"
            else "Registered maintenances",
            total_maintenances
        )

    st.subheader(
        "Últimos mantenimientos"
        if language == "es"
        else "Latest maintenances"
    )

    latest_maintenances = get_last_maintenances()

    if latest_maintenances:

        df_latest = pd.DataFrame(
            latest_maintenances,
            columns=[
                "Marca",
                "Modelo",
                "Tipo",
                "Fecha",
                "Kilometraje"
            ]
        )

        st.dataframe(df_latest, use_container_width=True)

    else:

        st.info(
            "Todavía no hay mantenimientos registrados."
            if language == "es"
            else "No maintenances registered yet."
        )
    

elif section == "Vehículos":
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

    st.header(
        "Mantenimientos"
        if language == "es"
        else "Maintenance"
    )

    vehicles = get_vehicles()

    if not vehicles:
        st.warning(
            "Primero debés registrar un vehículo."
            if language == "es"
            else "You must register a vehicle first."
        )

    else:

        vehicle_options = {
            f"{v[1]} {v[2]} ({v[5]})": v[0]
            for v in vehicles
        }

        selected_vehicle = st.selectbox(
            "Seleccionar vehículo"
            if language == "es"
            else "Select vehicle",
            list(vehicle_options.keys())
        )

        selected_vehicle_id = vehicle_options[selected_vehicle]

        selected_vehicle_data = next(
        v for v in vehicles if v[0] == selected_vehicle_id
        )
        vehicle_type = selected_vehicle_data[4]

        st.subheader(
            "Registrar mantenimiento"
            if language == "es"
            else "Register maintenance"
        )

        with st.form("maintenance_form"):

            fecha = st.date_input(
                "Fecha"
                if language == "es"
                else "Date"
            )

            if vehicle_type == "Moto":
                maintenance_options = [
                    "Cambio de aceite",
                    "Cadena",
                    "Transmisión",  
                    "Frenos",
                    "Cubiertas",
                    "Batería",
                    "Service general",
                    "Otro"
                ]

            else:
                maintenance_options = [
                    "Cambio de aceite",
                    "Distribución",
                    "Alineado y balanceo",
                    "Amortiguadores",
                    "Frenos",
                    "Cubiertas",
                    "Batería",
                    "Embrague",
                    "Tren delantero",
                    "Service general",
                    "Otro"
                ]

            tipo_mantenimiento = st.selectbox(
                "Tipo de mantenimiento"
                if language == "es"
                else "Maintenance type",
                maintenance_options
            )

            descripcion = st.text_area(
                "Descripción"
                if language == "es"
                else "Description"
            )

            costo = st.number_input(
                "Costo"
                if language == "es"
                else "Cost",
                min_value=0.0,
                step=100.0
            )

            kilometraje = st.number_input(
                "Kilometraje"
                if language == "es"
                else "Mileage",
                min_value=1,
                step=100
            )

            maintenance_submitted = st.form_submit_button(
                "Guardar mantenimiento"
                if language == "es"
                else "Save maintenance"
            )

            if maintenance_submitted:

                errores = []

                if kilometraje < 1:
                    errores.append(
                        "El kilometraje debe ser mayor a 0."
                        if language == "es"
                        else "Mileage must be greater than 0."
                    )

                if errores:
                    for error in errores:
                        st.error(error)

                else:

                    add_maintenance(
                        selected_vehicle_id,
                        str(fecha),
                        tipo_mantenimiento,
                        descripcion,
                        costo,
                        kilometraje
                    )

                    st.success(
                        "Mantenimiento registrado correctamente."
                        if language == "es"
                        else "Maintenance registered successfully."
                    )

        st.subheader(
            "Historial de mantenimientos"
            if language == "es"
            else "Maintenance history"
        )

        maintenances = get_maintenance_by_vehicle(selected_vehicle_id)

        if maintenances:

            df_maintenances = pd.DataFrame(
                maintenances,
                columns=[
                    "ID",
                    "Fecha",
                    "Tipo",
                    "Descripción",
                    "Costo",
                    "Kilometraje",
                    "Fecha creación"
                ]
            )

            st.dataframe(df_maintenances, use_container_width=True)

        else:

            st.info(
                "Todavía no hay mantenimientos registrados."
                if language == "es"
                else "No maintenance records yet."
            )

elif section == "Reportes":
    st.header("Reportes" if language == "es" else "Reports")
    st.info("Esta sección se desarrollará más adelante.")