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