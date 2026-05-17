import streamlit as st
import pandas as pd

from database import (
    get_total_vehicles,
    get_total_maintenances,
    get_total_maintenance_cost,
    get_last_maintenances,
    get_oil_change_alerts,
)


def render_dashboard(language):
    st.header("Dashboard")

    total_vehicles = get_total_vehicles()
    total_maintenances = get_total_maintenances()
    total_cost = get_total_maintenance_cost()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Vehículos registrados"
            if language == "es"
            else "Registered vehicles",
            total_vehicles,
        )

    with col2:
        st.metric(
            "Mantenimientos registrados"
            if language == "es"
            else "Registered maintenances",
            total_maintenances,
        )

    with col3:
        st.metric(
            "Costo total acumulado"
            if language == "es"
            else "Total accumulated cost",
            f"${total_cost:,.2f}",
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
                "Vehículo" if language == "es" else "Vehicle",
                "Tipo" if language == "es" else "Type",
                "Fecha" if language == "es" else "Date",
                "Kilometraje" if language == "es" else "Mileage",
                "Costo" if language == "es" else "Cost",
            ],
        )

        st.dataframe(df_latest, use_container_width=True, hide_index=True)

    else:
        st.info(
            "Todavía no hay mantenimientos registrados."
            if language == "es"
            else "No maintenances registered yet."
        )

    st.subheader(
        "Alertas de cambio de aceite"
        if language == "es"
        else "Oil change alerts"
    )

    oil_alerts = get_oil_change_alerts()

    if oil_alerts:
        alert_rows = []
        for alert in oil_alerts:
            km_restantes = alert["km_restantes"]
            if km_restantes > 0:
                estado = (
                    f"Faltan {km_restantes:,} km"
                    if language == "es"
                    else f"{km_restantes:,} km remaining"
                )
            elif km_restantes == 0:
                estado = (
                    "Cambio de aceite al día"
                    if language == "es"
                    else "Oil change due now"
                )
            else:
                estado = (
                    f"Vencido por {abs(km_restantes):,} km"
                    if language == "es"
                    else f"Overdue by {abs(km_restantes):,} km"
                )

            alert_rows.append({
                "Vehículo" if language == "es" else "Vehicle": alert["vehiculo"],
                "Km actual" if language == "es" else "Current km": alert["km_actual"],
                "Último cambio (km)"
                if language == "es"
                else "Last change (km)": alert["ultimo_aceite_km"],
                "Próximo cambio (km)"
                if language == "es"
                else "Next change (km)": alert["proximo_km"],
                "Estado" if language == "es" else "Status": estado,
            })

        st.dataframe(
            pd.DataFrame(alert_rows),
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            "Estimación: próximo cambio de aceite cada 5.000 km desde el último registrado."
            if language == "es"
            else "Estimate: next oil change every 5,000 km from the last recorded one."
        )

    else:
        st.info(
            "No hay vehículos con cambio de aceite registrado."
            if language == "es"
            else "No vehicles with a registered oil change."
        )
