
## 4. `docs/testing.md`

```markdown
# Plan de Testing

## Objetivo

Validar que las funcionalidades principales de Mi Garaje Control funcionen correctamente.

## Tipos de pruebas

### Testing funcional
Se validará que el usuario pueda:
- registrar vehículos
- listar vehículos
- registrar mantenimientos
- consultar historial
- cambiar idioma

### Testing de base de datos
Se validará:
- creación de tablas
- inserción de registros
- consulta de registros
- actualización de datos
- eliminación lógica o física

### Testing unitario
Se utilizará Pytest para probar funciones específicas del sistema.

Ejemplo:

```python
def test_calcular_proximo_service():
    km_actual = 10000
    intervalo = 5000
    resultado = km_actual + intervalo
    assert resultado == 15000