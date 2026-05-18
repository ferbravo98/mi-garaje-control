import sqlite3
from pathlib import Path

DB_PATH = Path("data/mi_garaje_control.db")


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            anio INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            patente TEXT,
            kilometraje_actual INTEGER NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mantenimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehiculo_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            tipo_mantenimiento TEXT NOT NULL,
            descripcion TEXT,
            costo REAL DEFAULT 0,
            kilometraje INTEGER NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id)
        )
    """)

    conn.commit()
    conn.close()


def add_vehicle(marca, modelo, anio, tipo, patente, kilometraje_actual):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO vehiculos (
            marca,
            modelo,
            anio,
            tipo,
            patente,
            kilometraje_actual
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (marca, modelo, anio, tipo, patente, kilometraje_actual))

    conn.commit()
    conn.close()


def get_vehicles():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            id,
            marca,
            modelo,
            anio,
            tipo,
            patente,
            kilometraje_actual,
            fecha_creacion
        FROM vehiculos
        ORDER BY fecha_creacion DESC
    """)

    vehicles = cursor.fetchall()
    conn.close()

    return vehicles


def update_vehicle(id, marca, modelo, anio, tipo, patente, kilometraje_actual):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE vehiculos
        SET
            marca = ?,
            modelo = ?,
            anio = ?,
            tipo = ?,
            patente = ?,
            kilometraje_actual = ?
        WHERE id = ?
    """, (marca, modelo, anio, tipo, patente, kilometraje_actual, id))

    conn.commit()
    conn.close()


def delete_vehicle(id):
    conn = get_connection()
    cursor = conn.cursor()

    # Eliminación física simple. En una versión futura convendría
    # eliminación lógica (p. ej. campo activo) para conservar historial.
    cursor.execute("DELETE FROM mantenimientos WHERE vehiculo_id = ?", (id,))
    cursor.execute("DELETE FROM vehiculos WHERE id = ?", (id,))

    conn.commit()
    conn.close()


def add_maintenance(
    vehiculo_id,
    fecha,
    tipo_mantenimiento,
    descripcion,
    costo,
    kilometraje
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO mantenimientos (
            vehiculo_id,
            fecha,
            tipo_mantenimiento,
            descripcion,
            costo,
            kilometraje
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        vehiculo_id,
        fecha,
        tipo_mantenimiento,
        descripcion,
        costo,
        kilometraje
    ))

    conn.commit()
    conn.close()


def get_maintenance_by_vehicle(vehiculo_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            fecha,
            tipo_mantenimiento,
            descripcion,
            costo,
            kilometraje,
            fecha_creacion
        FROM mantenimientos
        WHERE vehiculo_id = ?
        ORDER BY fecha DESC
    """, (vehiculo_id,))

    maintenances = cursor.fetchall()
    conn.close()

    return maintenances

def get_total_vehicles():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM vehiculos")

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_total_maintenances():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM mantenimientos")

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_total_maintenance_cost():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(SUM(costo), 0) FROM mantenimientos")

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_last_maintenances(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            v.marca || ' ' || v.modelo AS vehiculo,
            m.tipo_mantenimiento,
            m.fecha,
            m.kilometraje,
            m.costo
        FROM mantenimientos m
        INNER JOIN vehiculos v
            ON m.vehiculo_id = v.id
        ORDER BY m.fecha DESC, m.id DESC
        LIMIT ?
    """, (limit,))

    maintenances = cursor.fetchall()

    conn.close()

    return maintenances


OIL_CHANGE_INTERVAL_KM = 5000
OIL_CHANGE_TYPE = "Cambio de aceite"


def get_oil_change_alerts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            v.id,
            v.marca,
            v.modelo,
            v.patente,
            v.kilometraje_actual,
            (
                SELECT m.kilometraje
                FROM mantenimientos m
                WHERE m.vehiculo_id = v.id
                  AND m.tipo_mantenimiento = ?
                ORDER BY m.fecha DESC, m.id DESC
                LIMIT 1
            ) AS ultimo_aceite_km
        FROM vehiculos v
        ORDER BY v.marca, v.modelo
    """, (OIL_CHANGE_TYPE,))

    rows = cursor.fetchall()
    conn.close()

    alerts = []
    for vehicle_id, marca, modelo, patente, km_actual, ultimo_aceite_km in rows:
        if ultimo_aceite_km is None:
            continue

        proximo_km = ultimo_aceite_km + OIL_CHANGE_INTERVAL_KM
        km_restantes = proximo_km - km_actual

        if patente:
            vehiculo = f"{marca} {modelo} ({patente})"
        else:
            vehiculo = f"{marca} {modelo}"

        alerts.append({
            "vehiculo": vehiculo,
            "km_actual": km_actual,
            "ultimo_aceite_km": ultimo_aceite_km,
            "proximo_km": proximo_km,
            "km_restantes": km_restantes,
        })

    return alerts

def get_costs_by_vehicle():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            v.marca || ' ' || v.modelo AS vehiculo,
            SUM(m.costo) AS costo_total
        FROM mantenimientos m
        INNER JOIN vehiculos v ON m.vehiculo_id = v.id
        GROUP BY v.id
        ORDER BY costo_total DESC
    """)

    results = cursor.fetchall()
    conn.close()
    return results
