# Casos de prueba manuales – Pokémon Explorer

Casos diseñados según el [plan de pruebas](test-plan.md). Los datos de prueba y el contrato de errores están en sus secciones 5 y 6.

**Cómo registrar la ejecución**

- **Resultado obtenido:** describir lo que se observó, aunque coincida con lo esperado.
- **Estado:** `Pass` si coincide con lo esperado, `Fail` si no coincide (y abrir un reporte en [bug-reports.md](bug-reports.md)), `Blocked` si no se pudo ejecutar (indicar la causa).
- **Evidencia:** guardar la captura en `screenshots/` con el nombre indicado.
- **Precondición base (PB):** backend en http://localhost:8000 y frontend en http://localhost:5173 en ejecución; Google Chrome con DevTools.

## Resumen

| ID | Título | Área | Prioridad | Estado |
| --- | --- | --- | --- | --- |
| TC-001 | Carga inicial del catálogo | UI | Alta | No ejecutado |
| TC-002 | Buscar Pokémon por nombre | UI | Alta | No ejecutado |
| TC-003 | Búsqueda con mayúsculas y espacios | UI | Media | No ejecutado |
| TC-004 | Búsqueda sin resultados | UI | Alta | No ejecutado |
| TC-005 | Búsqueda vacía o solo con espacios | UI + API | Media | No ejecutado |
| TC-006 | Búsqueda con caracteres especiales | UI + API | Media | No ejecutado |
| TC-007 | Búsqueda con texto muy largo | UI + API | Baja | No ejecutado |
| TC-008 | Búsqueda con números | UI | Baja | No ejecutado |
| TC-009 | Filtrar por tipo | UI | Alta | No ejecutado |
| TC-010 | Cambios rápidos de filtro | UI | Media | No ejecutado |
| TC-011 | Navegar entre páginas | UI | Alta | No ejecutado |
| TC-012 | Límites de la paginación | UI | Media | No ejecutado |
| TC-013 | Ver detalle de un Pokémon | UI | Alta | No ejecutado |
| TC-014 | Imagen faltante | UI | Media | No ejecutado |
| TC-015 | Backend no disponible | UI | Alta | No ejecutado |
| TC-016 | Red lenta | UI | Media | No ejecutado |
| TC-017 | Recargar la aplicación | UI | Media | No ejecutado |
| TC-018 | Vista móvil | UI | Media | No ejecutado |
| TC-019 | Validación de la paginación | API | Alta | No ejecutado |
| TC-020 | Recursos y endpoints inexistentes | API | Alta | No ejecutado |
| TC-021 | PokéAPI no disponible | API + UI | Alta | No ejecutado |
| TC-022 | Documentación Swagger | API | Media | No ejecutado |

**Totales:** 22 casos · Pass: 0 · Fail: 0 · Blocked: 0 · No ejecutado: 22

---

## TC-001 – Carga inicial del catálogo

| Campo | Detalle |
| --- | --- |
| Área / prioridad | UI · Alta |
| Precondiciones | PB. |
| Pasos | 1. Abrir DevTools → pestaña Network.<br>2. Abrir http://localhost:5173.<br>3. Esperar a que termine la carga. |
| Resultado esperado | Se muestra un indicador de carga y después una cuadrícula de tarjetas, cada una con imagen y nombre. La primera tarjeta es Bulbasaur (#1). En Network, todas las peticiones de datos van a `localhost:8000` y ninguna a `pokeapi.co`. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-001-catalogo.png`, `screenshots/TC-001-network.png` |

## TC-002 – Buscar Pokémon por nombre

| Campo | Detalle |
| --- | --- |
| Área / prioridad | UI · Alta |
| Precondiciones | PB. Catálogo visible. |
| Pasos | 1. Escribir `pikachu` en el campo de búsqueda.<br>2. Pulsar Buscar (o Enter). |
| Resultado esperado | Aparece Pikachu (#25) con su imagen y nombre. No aparecen Pokémon cuyo nombre no contenga `pikachu`. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-002-busqueda-pikachu.png` |

## TC-003 – Búsqueda con mayúsculas y espacios

| Campo | Detalle |
| --- | --- |
| Área / prioridad | UI · Media |
| Precondiciones | PB. |
| Pasos | 1. Escribir `  PiKaChU  ` (con dos espacios antes y después).<br>2. Pulsar Buscar. |
| Resultado esperado | Mismo resultado que en TC-002. La búsqueda no distingue mayúsculas y no tiene en cuenta los espacios de los extremos. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-003-mayusculas.png` |

## TC-004 – Búsqueda sin resultados

| Campo | Detalle |
| --- | --- |
| Área / prioridad | UI · Alta |
| Precondiciones | PB. |
| Pasos | 1. Buscar `noexiste`.<br>2. Después, buscar `pikachu`. |
| Resultado esperado | Paso 1: se muestra un mensaje claro de que no hay resultados, sin tarjetas, sin mensaje de error y sin controles de paginación activos. Paso 2: la búsqueda funciona con normalidad. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-004-estado-vacio.png` |

## TC-005 – Búsqueda vacía o solo con espacios

| Campo | Detalle |
| --- | --- |
| Área / prioridad | UI + API · Media |
| Precondiciones | PB. |
| Pasos | 1. Con el campo vacío, pulsar Buscar.<br>2. Escribir tres espacios y pulsar Buscar.<br>3. En una terminal: `curl -i "http://localhost:8000/api/pokemon/search?name="`<br>4. `curl -i "http://localhost:8000/api/pokemon/search?name=%20%20%20"` |
| Resultado esperado | Pasos 1 y 2: se muestra un mensaje de validación que pide escribir un nombre; la página no queda en blanco ni muestra un error técnico. Pasos 3 y 4: `422` con `success: false` y `error.code: "VALIDATION_ERROR"`. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-005-busqueda-vacia.png`, salida de `curl` |

## TC-006 – Búsqueda con caracteres especiales

| Campo | Detalle |
| --- | --- |
| Área / prioridad | UI + API · Media |
| Precondiciones | PB. |
| Pasos | 1. Buscar, uno por uno: `<script>alert(1)</script>`, `' OR 1=1 --`, `%`, `pikachu!`.<br>2. `curl -i "http://localhost:8000/api/pokemon/search?name=%3Cscript%3E"` |
| Resultado esperado | Paso 1: no se abre ningún cuadro de alerta; si el texto aparece en pantalla, se muestra como texto plano. Se muestra un mensaje de validación comprensible y la aplicación sigue respondiendo. Paso 2: `422` con `VALIDATION_ERROR`. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-006-caracteres-especiales.png` |

## TC-007 – Búsqueda con texto muy largo

| Campo | Detalle |
| --- | --- |
| Área / prioridad | UI + API · Baja |
| Precondiciones | PB. Generar el texto con `python3 -c "print('a' * 300)"`. |
| Pasos | 1. Pegar los 300 caracteres en el campo de búsqueda.<br>2. Pulsar Buscar.<br>3. `curl -i "http://localhost:8000/api/pokemon/search?name=$(python3 -c "print('a' * 300)")"` |
| Resultado esperado | Paso 2: mensaje de validación; el diseño no se deforma y no aparece scroll horizontal. Paso 3: `422` con `VALIDATION_ERROR`. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-007-texto-largo.png` |

## TC-008 – Búsqueda con números

| Campo | Detalle |
| --- | --- |
| Área / prioridad | UI · Baja |
| Precondiciones | PB. |
| Pasos | 1. Buscar `25`. |
| Resultado esperado | Se muestra el estado vacío, porque ningún Pokémon se llama `25`. No aparece un mensaje de error. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-008-numeros.png` |

## TC-009 – Filtrar por tipo

| Campo | Detalle |
| --- | --- |
| Área / prioridad | UI · Alta |
| Precondiciones | PB. |
| Pasos | 1. Abrir el selector de tipo y revisar las opciones.<br>2. Seleccionar `electric`.<br>3. Abrir el detalle de tres tarjetas al azar.<br>4. Abrir http://localhost:5173/?type=stellar. |
| Resultado esperado | Paso 1: aparecen los 18 tipos de Pokémon (normal, fire, water, electric, etc.) y no aparecen `stellar`, `unknown` ni `shadow`. Paso 2: Pikachu y Raichu están entre los resultados. Paso 3: el detalle de cada tarjeta incluye el tipo `electric`. Paso 4: estado vacío claro, no un error (este tipo no tiene Pokémon en PokéAPI). |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-009-filtro-electric.png` |

## TC-010 – Cambios rápidos de filtro

| Campo | Detalle |
| --- | --- |
| Área / prioridad | UI · Media |
| Precondiciones | PB. DevTools → Network → limitación de red "Slow 4G". |
| Pasos | 1. Seleccionar `fire`, luego `water` y luego `grass`, todo en menos de 2 segundos.<br>2. Esperar a que termine la carga.<br>3. Abrir una tarjeta. |
| Resultado esperado | Al final se muestran solo resultados de `grass`, el último tipo elegido (por ejemplo, Bulbasaur). Los resultados no cambian a `fire` o `water` después de mostrarse los de `grass`. La tarjeta abierta tiene el tipo `grass`. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-010-filtros-rapidos.png` o video |

## TC-011 – Navegar entre páginas

| Campo | Detalle |
| --- | --- |
| Área / prioridad | UI · Alta |
| Precondiciones | PB. Catálogo en la página 1. |
| Pasos | 1. Anotar el primer y el último Pokémon de la página 1.<br>2. Pulsar Siguiente.<br>3. Pulsar Anterior. |
| Resultado esperado | Paso 2: la página 2 empieza en Spearow (#21), ningún Pokémon se repite con la página 1 y el indicador de página se actualiza. Paso 3: se vuelve a la página 1 con los mismos Pokémon del paso 1. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-011-pagina-2.png` |

## TC-012 – Límites de la paginación

| Campo | Detalle |
| --- | --- |
| Área / prioridad | UI · Media |
| Precondiciones | PB. |
| Pasos | 1. En la página 1, revisar el botón Anterior.<br>2. Filtrar por `electric` (114 Pokémon, unas 6 páginas de 20).<br>3. Pulsar Siguiente hasta llegar a la última página. |
| Resultado esperado | Paso 1: Anterior está deshabilitado. Paso 3: la última página muestra los Pokémon restantes (menos de 20), Siguiente está deshabilitado y el indicador de página no supera el total. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-012-ultima-pagina.png` |

## TC-013 – Ver detalle de un Pokémon

| Campo | Detalle |
| --- | --- |
| Área / prioridad | UI · Alta |
| Precondiciones | PB. |
| Pasos | 1. Buscar `pikachu` y abrir su tarjeta.<br>2. Revisar los datos mostrados.<br>3. Volver al catálogo.<br>4. Abrir el detalle de Bulbasaur (#1). |
| Resultado esperado | Paso 2: nombre Pikachu, #25, imagen, tipo `electric`, habilidades `static` y `lightning-rod`, estadísticas base hp 35, attack 55, defense 40, special-attack 50, special-defense 50, speed 90. Paso 3: se vuelve al catálogo sin pantalla en blanco. Paso 4: muestra dos tipos, `grass` y `poison`. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-013-detalle-pikachu.png`, `screenshots/TC-013-detalle-bulbasaur.png` |

## TC-014 – Imagen faltante

| Campo | Detalle |
| --- | --- |
| Área / prioridad | UI · Media |
| Precondiciones | PB. |
| Pasos | 1. DevTools → menú ⋮ → More tools → Network request blocking.<br>2. Agregar el patrón `*raw.githubusercontent.com*` y activarlo.<br>3. Recargar el catálogo y abrir un detalle.<br>4. Quitar el bloqueo al terminar. |
| Resultado esperado | Cada tarjeta y el detalle muestran la imagen de respaldo en lugar del icono de imagen rota; el nombre sigue visible y el diseño no se deforma. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-014-imagen-respaldo.png` |

## TC-015 – Backend no disponible

| Campo | Detalle |
| --- | --- |
| Área / prioridad | UI · Alta |
| Precondiciones | PB. Catálogo cargado. |
| Pasos | 1. Detener el backend (Ctrl+C en su terminal).<br>2. Buscar `pikachu` o pulsar Siguiente.<br>3. Volver a iniciar el backend y repetir la acción. |
| Resultado esperado | Paso 2: un mensaje comprensible indica que no se pudo conectar con el servidor. No aparece una pantalla en blanco ni texto técnico como `TypeError: Failed to fetch`. Paso 3: la acción funciona sin recargar la página. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-015-backend-caido.png` |

## TC-016 – Red lenta

| Campo | Detalle |
| --- | --- |
| Área / prioridad | UI · Media |
| Precondiciones | PB. DevTools → Network → limitación de red "Slow 3G". |
| Pasos | 1. Recargar la página.<br>2. Buscar `pikachu` y pulsar Buscar varias veces seguidas.<br>3. Quitar la limitación de red. |
| Resultado esperado | Se muestra un indicador de carga durante cada petición y desaparece al terminar. Pulsar Buscar varias veces no duplica las tarjetas ni deja el indicador visible para siempre. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-016-cargando.png` |

## TC-017 – Recargar la aplicación

| Campo | Detalle |
| --- | --- |
| Área / prioridad | UI · Media |
| Precondiciones | PB. |
| Pasos | 1. Filtrar por `electric`, ir a la página 2 y recargar (F5).<br>2. Abrir el detalle de un Pokémon y recargar (F5). |
| Resultado esperado | Paso 1: la aplicación vuelve a cargar en la página 2 del tipo `electric`. Paso 2: se muestra el mismo Pokémon. En ambos casos no hay pantalla en blanco ni error 404 y todos los controles responden. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-017-recarga.png` |

## TC-018 – Vista móvil

| Campo | Detalle |
| --- | --- |
| Área / prioridad | UI · Media |
| Precondiciones | PB. DevTools → Toggle device toolbar → iPhone SE (375×667). |
| Pasos | 1. Recorrer el catálogo.<br>2. Buscar, filtrar por tipo y cambiar de página.<br>3. Abrir un detalle y volver. |
| Resultado esperado | No hay scroll horizontal. Las tarjetas se acomodan en una o dos columnas. Los botones y el selector se pueden pulsar sin solaparse y el texto se lee sin hacer zoom. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-018-movil-catalogo.png`, `screenshots/TC-018-movil-detalle.png` |

## TC-019 – Validación de la paginación

| Campo | Detalle |
| --- | --- |
| Área / prioridad | API · Alta |
| Precondiciones | Backend en ejecución. |
| Pasos | Ejecutar con `curl -i`:<br>1. `"http://localhost:8000/api/pokemon?limit=20&offset=0"`<br>2. `"...?offset=99999"`<br>3. `"...?limit=-1"`<br>4. `"...?offset=-5"`<br>5. `"...?limit=0"` y `"...?limit=101"`<br>6. `"...?limit=abc"` |
| Resultado esperado | 1: `200`, 20 resultados, el primero `bulbasaur`. 2: `200` con `results: []`. 3 a 6: `422` con `success: false` y `error.code: "VALIDATION_ERROR"`; el mensaje indica qué parámetro es inválido. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | Salida de `curl` guardada en `screenshots/TC-019-paginacion.txt` |

## TC-020 – Recursos y endpoints inexistentes

| Campo | Detalle |
| --- | --- |
| Área / prioridad | API · Alta |
| Precondiciones | Backend en ejecución. |
| Pasos | Ejecutar con `curl -i`:<br>1. `http://localhost:8000/api/pokemon/99999`<br>2. `http://localhost:8000/api/pokemon/type/faketype`<br>3. `http://localhost:8000/api/pokemon/abc`<br>4. `http://localhost:8000/api/pokemon/0`<br>5. `http://localhost:8000/api/noexiste` |
| Resultado esperado | 1: `404`, `POKEMON_NOT_FOUND`. 2: `404`, `TYPE_NOT_FOUND`. 3 y 4: `422`, `VALIDATION_ERROR`. 5: `404`, `NOT_FOUND`. Todas las respuestas siguen el formato de error estándar y ninguna muestra trazas de error. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | Salida de `curl` guardada en `screenshots/TC-020-inexistentes.txt` |

## TC-021 – PokéAPI no disponible

| Campo | Detalle |
| --- | --- |
| Área / prioridad | API + UI · Alta |
| Precondiciones | PB. Elegir un Pokémon que no se haya consultado antes en esta sesión del backend (por ejemplo, el ID 150), para que no se use una respuesta guardada en caché. |
| Pasos | 1. Desconectar la red del equipo (apagar el Wi-Fi o desconectar el cable).<br>2. `curl -i http://localhost:8000/api/pokemon/150`<br>3. En la aplicación, buscar `mewtwo` o abrir su detalle.<br>4. Volver a conectar la red y repetir el paso 2. |
| Resultado esperado | Paso 2: `503` con `EXTERNAL_API_UNAVAILABLE` (o `504` con `EXTERNAL_API_TIMEOUT` si la conexión se queda esperando hasta el tiempo límite). Paso 3: mensaje de error comprensible en la aplicación. Paso 4: `200` con los datos de Mewtwo. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-021-pokeapi-caido.png`, salida de `curl` |

## TC-022 – Documentación Swagger

| Campo | Detalle |
| --- | --- |
| Área / prioridad | API · Media |
| Precondiciones | Backend en ejecución. |
| Pasos | 1. Abrir http://localhost:8000/docs.<br>2. Revisar los endpoints listados y sus parámetros.<br>3. En `GET /api/pokemon/{id}`, pulsar Try it out, escribir `25` y ejecutar. |
| Resultado esperado | Paso 2: aparecen los 5 endpoints con sus parámetros (`limit`, `offset`, `id`, `name`, `type`) y las respuestas de error documentadas. Paso 3: `200` con los datos de Pikachu en el formato documentado. |
| Resultado obtenido | _Pendiente de ejecución_ |
| Estado | No ejecutado |
| Evidencia | `screenshots/TC-022-swagger.png` |
