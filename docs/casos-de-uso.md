# Casos de Uso

## Actores

### Usuario
Persona que utiliza la aplicación para gestionar el mantenimiento de sus vehículos.

## Casos de uso principales

| Código | Caso de uso | Descripción |
|---|---|---|
| CU01 | Registrar vehículo | El usuario carga los datos básicos de un vehículo. |
| CU02 | Ver vehículos | El usuario consulta los vehículos registrados. |
| CU03 | Registrar mantenimiento | El usuario registra un arreglo, service o control realizado. |
| CU04 | Ver historial | El usuario consulta mantenimientos anteriores. |
| CU05 | Ver próximos mantenimientos | El usuario visualiza services pendientes o próximos. |
| CU06 | Cambiar idioma | El usuario cambia entre español e inglés. |

## CU01 - Registrar vehículo

### Objetivo
Permitir que el usuario cargue un nuevo vehículo.

### Flujo principal
1. El usuario ingresa a la sección Vehículos.
2. El sistema muestra un formulario.
3. El usuario completa marca, modelo, año, tipo, patente y kilometraje.
4. El usuario confirma el registro.
5. El sistema guarda el vehículo.
6. El sistema muestra mensaje de confirmación.

### Flujo alternativo
- Si faltan datos obligatorios, el sistema muestra un mensaje de error.

## CU03 - Registrar mantenimiento

### Objetivo
Permitir registrar un mantenimiento realizado sobre un vehículo.

### Flujo principal
1. El usuario selecciona un vehículo.
2. El usuario ingresa fecha, kilometraje, tipo de mantenimiento, costo y observaciones.
3. El usuario confirma la carga.
4. El sistema guarda el mantenimiento.
5. El sistema actualiza el historial del vehículo.