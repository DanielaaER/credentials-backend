
# Casos de Prueba - Sistema de Gestión Escolar

Este documento describe los casos de prueba implementados para verificar el correcto funcionamiento del sistema.

## 🔐 Pruebas de Tokens QR

| Caso                      | Entrada                             | Resultado Esperado            |
|---------------------------|--------------------------------------|-------------------------------|
| Token válido              | Usuario ID: 1, tipo: 'docente'       | `valido: True`                |
| Token expirado            | Usuario ID: 2, esperar 31 segundos   | `valido: False`, razón: 'expirado' |
| Token inválido            | Cadena corrupta o firmada mal        | `valido: False`, razón: 'token inválido' |

## 🕒 Pruebas de Traslape de Horarios

| Caso                            | Entrada                                          | Resultado Esperado |
|---------------------------------|--------------------------------------------------|---------------------|
| Clase se traslapa en aula       | Día: lunes, 10:00–11:00, mismo aula              | `True`              |
| Clase con docente duplicado     | Día: lunes, 10:00–11:00, mismo docente           | `True`              |
| Clase válida (sin traslape)     | Día: martes, 12:00–13:00, aula/docente distintos | `False`             |

## 📉 Pruebas de Rendimiento

Utiliza `pytest-benchmark` para medir el tiempo de generación/validación de QR y detección de traslapes.

## 🧪 Comando para ejecutar pruebas

```bash
pytest tests/ --benchmark-only
```
