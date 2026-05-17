import streamlit as st
import pandas as pd

from database import (
    add_vehicle,
    get_vehicles,
    update_vehicle,
    delete_vehicle,
)


def render_vehiculos(language):
    st.header("Vehículos" if language == "es" else "Vehicles")

    with st.form("vehicle_form"):
        marca = st.text_input("Marca" if language == "es" else "Brand")
        modelo = st.text_input("Modelo" if language == "es" else "Model")
        anio = st.number_input(
            "Año" if language == "es" else "Year",
            min_value=1900,
            max_value=2100,
            step=1,
        )
        tipo = st.selectbox(
            "Tipo" if language == "es" else "Type",
            ["Auto", "Moto"] if language == "es" else ["Car", "Motorcycle"],
        )
        patente = st.text_input("Patente" if language == "es" else "License plate")
        kilometraje_actual = st.number_input(
            "Kilometraje actual" if language == "es" else "Current mileage",
            min_value=0,
            step=100,
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
                kilometraje_actual,
            )

            st.success(
                "Vehículo guardado correctamente."
                if language == "es"
                else "Vehicle saved successfully."
            )

    st.subheader(
        "Vehículos registrados" if language == "es" else "Registered vehicles"
    )

    vehicles = get_vehicles()

    if vehicles:
        df = pd.DataFrame(
            vehicles,
            columns=[
                "ID",
                "Marca" if language == "es" else "Brand",
                "Modelo" if language == "es" else "Model",
                "Año" if language == "es" else "Year",
                "Tipo" if language == "es" else "Type",
                "Patente" if language == "es" else "License plate",
                "Kilometraje" if language == "es" else "Mileage",
                "Fecha creación" if language == "es" else "Created at",
            ],
        )
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader(
            "Editar vehículo"
            if language == "es"
            else "Edit vehicle"
        )

        vehicle_options = {
            f"{v[1]} {v[2]} ({v[5]})": v[0]
            for v in vehicles
        }

        selected_vehicle_label = st.selectbox(
            "Seleccionar vehículo"
            if language == "es"
            else "Select vehicle",
            list(vehicle_options.keys()),
        )

        selected_vehicle_id = vehicle_options[selected_vehicle_label]
        selected_vehicle = next(
            v for v in vehicles if v[0] == selected_vehicle_id
        )

        tipo_options = (
            ["Auto", "Moto"]
            if language == "es"
            else ["Car", "Motorcycle"]
        )
        tipo_index = (
            tipo_options.index(selected_vehicle[4])
            if selected_vehicle[4] in tipo_options
            else 0
        )

        with st.form("vehicle_edit_form"):
            edit_marca = st.text_input(
                "Marca" if language == "es" else "Brand",
                value=selected_vehicle[1],
            )
            edit_modelo = st.text_input(
                "Modelo" if language == "es" else "Model",
                value=selected_vehicle[2],
            )
            edit_anio = st.number_input(
                "Año" if language == "es" else "Year",
                min_value=1900,
                max_value=2100,
                step=1,
                value=int(selected_vehicle[3]),
            )
            edit_tipo = st.selectbox(
                "Tipo" if language == "es" else "Type",
                tipo_options,
                index=tipo_index,
            )
            edit_patente = st.text_input(
                "Patente" if language == "es" else "License plate",
                value=selected_vehicle[5] or "",
            )
            edit_kilometraje = st.number_input(
                "Kilometraje actual"
                if language == "es"
                else "Current mileage",
                min_value=0,
                step=100,
                value=int(selected_vehicle[6]),
            )

            update_submitted = st.form_submit_button(
                "Guardar cambios"
                if language == "es"
                else "Save changes"
            )

        if update_submitted:
            edit_marca = edit_marca.strip()
            edit_modelo = edit_modelo.strip()
            edit_patente = edit_patente.strip()

            errores_edicion = []

            if not edit_marca:
                errores_edicion.append(
                    "La marca es obligatoria."
                    if language == "es"
                    else "Brand is required."
                )

            if not edit_modelo:
                errores_edicion.append(
                    "El modelo es obligatorio."
                    if language == "es"
                    else "Model is required."
                )

            if edit_kilometraje < 1:
                errores_edicion.append(
                    "El kilometraje debe ser mayor a 0."
                    if language == "es"
                    else "Mileage must be greater than 0."
                )

            if errores_edicion:
                for error in errores_edicion:
                    st.error(error)
            else:
                update_vehicle(
                    selected_vehicle_id,
                    edit_marca,
                    edit_modelo,
                    edit_anio,
                    edit_tipo,
                    edit_patente,
                    edit_kilometraje,
                )

                st.success(
                    "Vehículo actualizado correctamente."
                    if language == "es"
                    else "Vehicle updated successfully."
                )
                st.rerun()

        st.warning(
            "Al eliminar un vehículo también se borran sus mantenimientos asociados."
            if language == "es"
            else "Deleting a vehicle also removes its associated maintenance records."
        )

        if st.button(
            "Eliminar vehículo"
            if language == "es"
            else "Delete vehicle",
            type="primary",
        ):
            delete_vehicle(selected_vehicle_id)

            st.success(
                "Vehículo eliminado correctamente."
                if language == "es"
                else "Vehicle deleted successfully."
            )
            st.rerun()

    else:
        st.info(
            "Todavía no hay vehículos registrados."
            if language == "es"
            else "No vehicles registered yet."
        )
