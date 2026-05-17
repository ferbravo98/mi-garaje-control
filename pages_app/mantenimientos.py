import streamlit as st
import pandas as pd

from database import (
    add_maintenance,
    get_vehicles,
    get_maintenance_by_vehicle,
)


def render_mantenimientos(language):
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
            list(vehicle_options.keys()),
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
                    "Otro",
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
                    "Otro",
                ]

            tipo_mantenimiento = st.selectbox(
                "Tipo de mantenimiento"
                if language == "es"
                else "Maintenance type",
                maintenance_options,
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
                step=100.0,
            )

            kilometraje = st.number_input(
                "Kilometraje"
                if language == "es"
                else "Mileage",
                min_value=1,
                step=100,
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
                        kilometraje,
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
                    "Fecha" if language == "es" else "Date",
                    "Tipo" if language == "es" else "Type",
                    "Descripción" if language == "es" else "Description",
                    "Costo" if language == "es" else "Cost",
                    "Kilometraje" if language == "es" else "Mileage",
                    "Fecha creación" if language == "es" else "Created at",
                ],
            )

            st.dataframe(df_maintenances, use_container_width=True, hide_index=True)

        else:
            st.info(
                "Todavía no hay mantenimientos registrados."
                if language == "es"
                else "No maintenance records yet."
            )
