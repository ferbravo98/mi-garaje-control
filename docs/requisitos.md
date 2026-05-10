# Requisitos del Sistema

## Requerimientos funcionales

### RF01 - Registrar vehículo
El sistema debe permitir registrar un vehículo con marca, modelo, año, tipo, patente y kilometraje actual.

### RF02 - Consultar vehículos
El sistema debe permitir visualizar el listado de vehículos registrados.

### RF03 - Registrar mantenimiento
El sistema debe permitir registrar mantenimientos asociados a un vehículo.

### RF04 - Consultar historial
El sistema debe permitir consultar el historial de mantenimientos de cada vehículo.

### RF05 - Calcular próximo mantenimiento
El sistema debe permitir estimar el próximo mantenimiento según kilometraje o fecha.

### RF06 - Cambiar idioma
El sistema debe permitir cambiar entre español e inglés.

## Requerimientos no funcionales

### RNF01 - Responsive
La aplicación debe poder utilizarse correctamente desde celulares.

### RNF02 - Persistencia local
La información debe almacenarse en una base de datos SQLite.

### RNF03 - Usabilidad
La interfaz debe ser simple, clara y orientada a usuarios no técnicos.

### RNF04 - Rendimiento
Las operaciones principales deben responder en menos de 2 segundos.

### RNF05 - Mantenibilidad
El código debe estar separado en módulos para facilitar futuras mejoras.