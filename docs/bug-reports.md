# Reportes de bugs – Pokémon Explorer

Este documento registra los defectos encontrados al ejecutar el [plan de pruebas](test-plan.md). Cada reporte indica su **origen**:

- **Real:** defecto encontrado durante el desarrollo o las pruebas.
- **Intencional:** defecto introducido a propósito para demostrar que las pruebas lo detectan. Se introduce en una rama aparte, se ejecutan las pruebas, se guarda la evidencia y se revierte el cambio. El reporte indica el commit que lo introduce y el que lo revierte.

## Clasificación

La **severidad** mide el impacto técnico del defecto. La **prioridad** mide qué tan pronto hay que corregirlo. No siempre coinciden: una imagen rota en la tarjeta de Pikachu, el primer ejemplo que verá el evaluador, tiene severidad Baja pero prioridad Alta.

| Severidad | Significado en esta aplicación |
| --- | --- |
| Crítica | La aplicación o el backend no arrancan, o un flujo principal queda inutilizable para todos |
| Alta | Una función principal (búsqueda, filtro, paginación, detalle) da resultados incorrectos o falla |
| Media | La función sirve, pero con datos incorrectos en algunos casos o con un manejo de errores inadecuado |
| Baja | Problemas visuales, de texto o de usabilidad que no impiden usar la aplicación |

| Prioridad | Significado |
| --- | --- |
| Alta | Corregir antes de la entrega |
| Media | Corregir si hay tiempo; si no, documentarlo en el README |
| Baja | Documentarlo como limitación conocida |

## Resumen

| ID | Título | Origen | Severidad | Prioridad | Estado | Detectado por |
| --- | --- | --- | --- | --- | --- | --- |
| BUG-001 | La página 2 repite el último Pokémon de la página 1 | Intencional | Media | Alta | _completar_ | API-09, TC-011 |
| BUG-002 | El detalle de un Pokémon con dos tipos muestra solo uno | Intencional | Media | Alta | _completar_ | API-14, TC-013 |
| BUG-003 | Un ID inexistente devuelve 500 en lugar de 404 | Intencional | Media | Alta | _completar_ | API-04, TC-020 |
| BUG-004 | _Título del primer defecto real_ | Real | _completar_ | _completar_ | _completar_ | _completar_ |

---

## Defectos intencionales

### BUG-001 – La página 2 repite el último Pokémon de la página 1

| Campo | Detalle |
| --- | --- |
| Origen | Intencional |
| Severidad / Prioridad | Media / Alta. La paginación sigue funcionando, pero el usuario ve un Pokémon repetido en cada página; es un flujo principal que el evaluador revisa. |
| Componente | Backend, cálculo del `offset` que se envía a PokéAPI |
| Cómo se introduce | Restar 1 al `offset` antes de llamar a PokéAPI |
| Rama y commits | Rama `bug/offset-off-by-one` · introduce: _hash_ · revierte: _hash_ |
| Entorno | OS: _completar_ · Navegador: _completar_ · Versión (commit): _completar_ |
| Pasos para reproducir | 1. `curl "http://localhost:8000/api/pokemon?limit=20&offset=0"` y anotar el último resultado.<br>2. `curl "http://localhost:8000/api/pokemon?limit=20&offset=20"` y anotar el primero.<br>3. En la UI, pulsar Siguiente en el catálogo. |
| Resultado esperado | La página 2 empieza en Spearow (#21) y no repite ningún Pokémon de la página 1. |
| Resultado obtenido | _completar con lo observado_ |
| Evidencia | Salida de `pytest -v` con API-09 fallando · `screenshots/BUG-001-pagina-repetida.png` |
| Estado | _Abierto / En progreso / Resuelto_ |
| Prevención de regresión | API-09 verifica que a PokéAPI se le pide exactamente el `offset` recibido |

### BUG-002 – El detalle de un Pokémon con dos tipos muestra solo uno

| Campo | Detalle |
| --- | --- |
| Origen | Intencional (basado en el ejercicio sugerido en el apéndice de la prueba) |
| Severidad / Prioridad | Media / Alta. Muestra información incorrecta de forma silenciosa y afecta a cientos de Pokémon con dos tipos. |
| Componente | Backend, conversión de la respuesta de PokéAPI al formato propio |
| Cómo se introduce | Devolver solo el primer elemento de la lista de tipos |
| Rama y commits | Rama `bug/missing-second-type` · introduce: _hash_ · revierte: _hash_ |
| Entorno | OS: _completar_ · Navegador: _completar_ · Versión (commit): _completar_ |
| Pasos para reproducir | 1. `curl http://localhost:8000/api/pokemon/1`<br>2. Revisar el campo `types`.<br>3. En la UI, abrir el detalle de Bulbasaur. |
| Resultado esperado | `types: ["grass", "poison"]`, y el detalle muestra las dos insignias de tipo. |
| Resultado obtenido | _completar con lo observado_ |
| Evidencia | Salida de `pytest -v` con API-14 fallando · `screenshots/BUG-002-tipo-faltante.png` |
| Estado | _Abierto / En progreso / Resuelto_ |
| Prevención de regresión | API-14 usa a Bulbasaur (dos tipos) en lugar de Pikachu (un tipo), que no detectaría este defecto |

### BUG-003 – Un ID inexistente devuelve 500 en lugar de 404

| Campo | Detalle |
| --- | --- |
| Origen | Intencional |
| Severidad / Prioridad | Media / Alta. El usuario ve un error genérico en lugar de "Pokémon no encontrado", y el 500 hace parecer que el servidor falló. |
| Componente | Backend, manejo de la respuesta 404 de PokéAPI |
| Cómo se introduce | Quitar el caso que convierte el 404 de PokéAPI en `POKEMON_NOT_FOUND`, para que llegue al manejador de errores genérico |
| Rama y commits | Rama `bug/404-as-500` · introduce: _hash_ · revierte: _hash_ |
| Entorno | OS: _completar_ · Navegador: _completar_ · Versión (commit): _completar_ |
| Pasos para reproducir | 1. `curl -i http://localhost:8000/api/pokemon/99999`<br>2. En la UI, abrir http://localhost:5173/pokemon/99999. |
| Resultado esperado | `404` con `{"success": false, "error": {"code": "POKEMON_NOT_FOUND", ...}}`, y en la UI un mensaje de "Pokémon no encontrado". |
| Resultado obtenido | _completar con lo observado_ |
| Evidencia | Salida de `pytest -v` con API-04 fallando · salida de `curl -i` |
| Estado | _Abierto / En progreso / Resuelto_ |
| Prevención de regresión | API-04 verifica el código HTTP y también `error.code` |

---

## Defectos reales

Registrar aquí cada defecto real encontrado al ejecutar los casos manuales y las pruebas automatizadas. Copiar la plantilla para cada uno (BUG-005, BUG-006, …). Los defectos que queden abiertos deben aparecer también en la sección "Limitaciones y bugs conocidos" del README.

### BUG-004 – _Título breve y concreto_

| Campo | Detalle |
| --- | --- |
| Origen | Real |
| Severidad / Prioridad | _Crítica / Alta / Media / Baja_ · _Alta / Media / Baja_. _Explicar por qué._ |
| Componente | _Backend / Frontend · archivo o pantalla_ |
| Entorno | OS: _completar_ · Navegador: _completar_ · Versión (commit): _completar_ |
| Pasos para reproducir | 1. _…_<br>2. _…_ |
| Resultado esperado | _…_ |
| Resultado obtenido | _…_ |
| Evidencia | _Captura, video o log_ |
| Detectado por | _ID del caso o de la prueba_ |
| Estado | _Abierto / En progreso / Resuelto_ |
| Causa y corrección | _Qué lo causaba y qué commit lo corrige (si está resuelto)_ |
