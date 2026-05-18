import streamlit as st
import pandas as pd
import plotly.express as px

from database import (
    get_total_vehicles,
    get_total_maintenances,
    get_total_maintenance_cost,
    get_last_maintenances,
    get_oil_change_alerts,
    get_costs_by_vehicle,
    get_maintenance_count_by_type,
    get_monthly_maintenance_costs,
    get_costs_by_maintenance_type,
)

def render_metric_card(title, value, icon):
    st.markdown(
        f"""
        <div style="
            background: #111827;
            border: 1px solid #1f2937;
            border-radius: 18px;
            padding: 24px;
            min-height: 150px;
        ">
            <div style="font-size: 28px; margin-bottom: 12px;">{icon}</div>
            <div style="
                color: #94a3b8;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 1px;
                text-transform: uppercase;
            ">
                {title}
            </div>
            <div style="
                color: #ffffff;
                font-size: 36px;
                font-weight: 900;
                margin-top: 12px;
            ">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_dashboard(language):
    st.header("Dashboard")

    total_vehicles = get_total_vehicles()
    total_maintenances = get_total_maintenances()
    total_cost = get_total_maintenance_cost()

    col1, col2, col3 = st.columns(3)

    with col1:
        render_metric_card(
            "Vehículos" if language == "es" else "Vehicles",
            total_vehicles,
            "🚗",
        )

    with col2:
        render_metric_card(
            "Mantenimientos" if language == "es" else "Maintenances",
            total_maintenances,
            "🔧",
        )

    with col3:
        render_metric_card(
            "Costo total" if language == "es" else "Total cost",
            f"${total_cost:,.2f}",
            "💰",
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
        st.subheader(
        "Costos acumulados por vehículo"
        if language == "es"
        else "Accumulated costs by vehicle"
    )
        st.subheader(
        "Análisis visual de mantenimientos"
        if language == "es"
        else "Maintenance visual analysis"
    )

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        maintenance_by_type = get_maintenance_count_by_type()

        if maintenance_by_type:
            df_type_count = pd.DataFrame(
                maintenance_by_type,
                columns=[
                    "Tipo" if language == "es" else "Type",
                    "Cantidad" if language == "es" else "Quantity",
                ],
            )

            fig_type_count = px.bar(
                df_type_count,
                x="Tipo" if language == "es" else "Type",
                y="Cantidad" if language == "es" else "Quantity",
                title=(
                    "Cantidad por tipo de mantenimiento"
                    if language == "es"
                    else "Quantity by maintenance type"
                ),
                text="Cantidad" if language == "es" else "Quantity",
            )

            st.plotly_chart(fig_type_count, use_container_width=True)

    with col_chart2:
        costs_by_type = get_costs_by_maintenance_type()

        if costs_by_type:
            df_costs_type = pd.DataFrame(
                costs_by_type,
                columns=[
                    "Tipo" if language == "es" else "Type",
                    "Costo total" if language == "es" else "Total cost",
                ],
            )

            fig_costs_type = px.pie(
                df_costs_type,
                names="Tipo" if language == "es" else "Type",
                values="Costo total" if language == "es" else "Total cost",
                title=(
                    "Distribución de costos por tipo"
                    if language == "es"
                    else "Cost distribution by type"
                ),
                hole=0.45,
            )

            st.plotly_chart(fig_costs_type, use_container_width=True)

    monthly_costs = get_monthly_maintenance_costs()

    if monthly_costs:
        df_monthly = pd.DataFrame(
            monthly_costs,
            columns=[
                "Mes" if language == "es" else "Month",
                "Costo total" if language == "es" else "Total cost",
            ],
        )

        fig_monthly = px.bar(
            df_monthly,
            x="Mes" if language == "es" else "Month",
            y="Costo total" if language == "es" else "Total cost",
            text="Costo total" if language == "es" else "Total cost",
            title=(
                "Evolución mensual de gastos"
                if language == "es"
                else "Monthly expense trend"
            ),
        )

        fig_monthly.update_layout(
            xaxis_title=None,
            yaxis_title=None,
        )

        st.plotly_chart(fig_monthly, use_container_width=True)
        

    costs_by_vehicle = get_costs_by_vehicle()

    if costs_by_vehicle:
        df_costs = pd.DataFrame(
            costs_by_vehicle,
            columns=[
                "Vehículo" if language == "es" else "Vehicle",
                "Costo total" if language == "es" else "Total cost",
            ],
        )

        fig = px.bar(
            df_costs,
            x="Vehículo" if language == "es" else "Vehicle",
            y="Costo total" if language == "es" else "Total cost",
            text="Costo total" if language == "es" else "Total cost",
            title=(
                "Gasto total por vehículo"
                if language == "es"
                else "Total expenses by vehicle"
            ),
        )

        fig.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info(
            "Todavía no hay costos registrados."
            if language == "es"
            else "No costs registered yet."
        )
