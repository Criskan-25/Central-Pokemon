# Plan de pruebas – Pokémon Explorer

| Campo | Valor |
| --- | --- |
| Proyecto | Pokémon Explorer (Central Pokemon) |
| Versión del documento | 1.0 |
| Fecha | 2026-10-30 |
| Autor | Miguel Pineda |
| Documentos relacionados | [Backend](backend.md) · [Frontend](frontend.md) · [Casos de prueba manuales](manual-test-cases.md) · [Reportes de bugs](bug-reports.md) · [Resumen de pruebas](test-summary.md) |

---

## 1. Objetivo

Verificar que Pokémon Explorer (backend FastAPI + cliente React) cumple los requisitos funcionales de la prueba técnica y que se comporta de forma correcta y predecible ante:

- entradas válidas,
- entradas inválidas o inesperadas,
- fallas del backend o de PokéAPI.

## 2. Alcance

### Dentro del alcance

| Componente | Qué se prueba |
| --- | --- |
| Backend FastAPI | Los 5 endpoints, validación de parámetros, paginación, formato de respuesta, manejo de errores (404, 422, 500, 503, 504), CORS y Swagger UI |
| Frontend React | Catálogo, búsqueda, filtro por tipo, paginación, detalle, estados de carga, vacío y error, imágenes de respaldo y diseño responsivo |
| Integración | El frontend solo llama al backend y el backend es el único que llama a PokéAPI |

### Fuera del alcance

- Pruebas de carga o estrés a gran escala (solo se miden tiempos de respuesta básicos).
- Pruebas de seguridad formales (solo se verifica que las entradas maliciosas no rompan la aplicación ni se ejecuten).
- Exactitud de los datos de PokéAPI, que se considera la fuente de verdad.
- Navegadores distintos de Chromium en las pruebas automatizadas.

## 3. Estrategia

| Nivel | Herramienta | Enfoque | Ubicación |
| --- | --- | --- | --- |
| API automatizada | Pytest + FastAPI TestClient | PokéAPI simulado (mock), para que las pruebas sean estables y no dependan de internet | `backend/tests/` |
| UI automatizada | Playwright (Chromium) | Flujos de usuario completos con las respuestas del backend simuladas (`page.route`) a partir de fixtures, incluidas las fallas; la integración con el backend real se cubre en las pruebas manuales | `frontend/tests/` |
| Manual | Navegador con DevTools, `curl` y Swagger UI | Casos documentados y exploración de casos límite | [manual-test-cases.md](manual-test-cases.md) |
| Negativas y de borde | Las tres anteriores | Entradas inválidas, red lenta, servicios caídos y respuestas inesperadas | [Sección 9](#9-pruebas-negativas-y-de-borde) |

Cada requisito se cubre en al menos un nivel automatizado y uno manual (ver [trazabilidad](#10-trazabilidad-requisitos--pruebas)).

## 4. Entorno de pruebas

| Elemento | Valor |
| --- | --- |
| Sistema operativo | Linux _(completar distribución y versión)_ |
| Python | 3.11 o superior (equipo de pruebas: 3.12.3) |
| Node.js | 20 o superior (equipo de pruebas: 20.20.1) |
| Navegador manual | Google Chrome _(completar versión)_ |
| Navegador automatizado | Chromium incluido en Playwright |
| Backend | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Frontend | http://localhost:5173 |

## 5. Datos de prueba

| Dato | Valor | Uso |
| --- | --- | --- |
| Pokémon de un tipo | `pikachu`: ID 25, tipo `electric`, habilidades `static` y `lightning-rod` | Búsqueda y detalle |
| Pokémon de dos tipos | `bulbasaur`: ID 1, tipos `grass` y `poison` | Verificar campos con varios valores |
| Primera página | IDs 1–20; la página 2 empieza en `spearow` (ID 21) | Paginación |
| ID inexistente | `99999` | 404 |
| IDs inválidos | `0`, `-1`, `abc`, `1.5` | 422 |
| Tipo válido | `electric` | Filtro |
| Tipo inexistente | `faketype` | 404 |
| Tipos sin Pokémon | `stellar`, `unknown`, `shadow` | Estado vacío |
| Nombre inexistente | `noexiste` | Estado vacío |
| Nombre vacío | `""` y `"   "` | 422 |
| Caracteres especiales | `<script>alert(1)</script>`, `' OR 1=1 --`, `%`, `pikachu!` | 422 |
| Texto muy largo | 300 veces la letra `a` | 422 |
| Solo números | `25` | Sin resultados |
| Paginación | `offset=99999`, `limit=-1`, `offset=-5`, `limit=0`, `limit=101`, `limit=abc` | 200 vacío o 422 |

**Datos verificados directamente en PokéAPI el 2026-10-30** (pueden cambiar con el tiempo):

- `GET /pokemon` informa `count: 1351`. Esa cifra incluye formas alternativas con IDs de 10001 en adelante, por lo que las últimas páginas muestran formas como `meowstic-female-mega` (ID 10326).
- El tipo `electric` tiene 114 Pokémon (incluidas las formas alternativas). Los primeros son `pikachu`, `raichu` y `magnemite`.
- Los tipos `stellar`, `unknown` y `shadow` existen, pero tienen 0 Pokémon.
- Un `offset` fuera de rango devuelve `200` con `results: []`.
- Un ID inexistente devuelve `404` con `{"status":404,"message":"Not Found"}`.
- PokéAPI no tiene búsqueda parcial por nombre. En el índice completo, 17 nombres contienen `pikachu` (por ejemplo, `pikachu-gmax` y `pikachu-original-cap`).
- Estadísticas base de Pikachu: hp 35, attack 55, defense 40, special-attack 50, special-defense 50, speed 90. Altura 4 (decímetros) y peso 60 (hectogramos).

**Supuestos de validación** (deben coincidir con la implementación del backend):

- `limit` entre 1 y 100 (por defecto 20) y `offset` ≥ 0.
- `name` de 1 a 50 caracteres después de quitar los espacios de los extremos. Solo se permiten letras, números, espacios y guiones, sin distinguir mayúsculas; `.` y `'` se aceptan y se eliminan al normalizar (`Mr. Mime` → `mr-mime`).
- `/api/types` no incluye `stellar`, `unknown` ni `shadow`.
- `id` entero ≥ 1.

## 6. Contrato de respuestas esperado

Toda respuesta exitosa tiene `success: true` y `data`. Toda respuesta de error tiene `success: false`, `error.code` y `error.message`, y nunca expone trazas de error ni la respuesta original de PokéAPI.

| HTTP | `error.code` | Cuándo |
| --- | --- | --- |
| 200 | — | Petición correcta, incluidas las búsquedas o páginas sin resultados (`results: []`) |
| 404 | `POKEMON_NOT_FOUND` | ID inexistente |
| 404 | `TYPE_NOT_FOUND` | Tipo inexistente |
| 404 | `NOT_FOUND` | Endpoint inexistente |
| 422 | `VALIDATION_ERROR` | Parámetros inválidos (nombre vacío, caracteres especiales, paginación negativa) |
| 500 | `INTERNAL_ERROR` | Error interno no esperado |
| 502 | `EXTERNAL_API_BAD_RESPONSE` | PokéAPI responde con datos malformados (JSON inválido o campos faltantes) |
| 503 | `EXTERNAL_API_UNAVAILABLE` | PokéAPI no responde o devuelve un error 5xx |
| 504 | `EXTERNAL_API_TIMEOUT` | PokéAPI tarda más que el tiempo límite configurado |

## 7. Pruebas automatizadas de API

Ubicación: `backend/tests/`. Comando: `pytest -v`. PokéAPI se simula en todas las pruebas.

| ID | Escenario | Petición | Simulación de PokéAPI | Resultado esperado |
| --- | --- | --- | --- | --- |
| API-01 | Lista de Pokémon | `GET /api/pokemon` | Lista con 3 Pokémon | 200, `success: true`, `data.results` no vacío |
| API-02 | Pokémon por ID válido | `GET /api/pokemon/25` | Datos de Pikachu | 200, `id: 25`, `name: "pikachu"`, `types: ["electric"]` |
| API-03 | Buscar Pikachu | `GET /api/pokemon/search?name=pikachu` | Índice de nombres | 200 y Pikachu en los resultados; ningún resultado sin `pikachu` en el nombre |
| API-04 | Pokémon inexistente | `GET /api/pokemon/99999` | 404 | 404, `POKEMON_NOT_FOUND` |
| API-05 | Nombre vacío | `?name=` y `?name=%20%20%20` | No se llama | 422, `VALIDATION_ERROR` |
| API-06 | Caracteres especiales | `?name=<script>alert(1)</script>` y `?name=%25` | No se llama | 422, `VALIDATION_ERROR`; se verifica que no hubo llamada a PokéAPI |
| API-07 | Filtro por tipo válido | `GET /api/pokemon/type/electric` | Tipo con 3 Pokémon | 200; los resultados son exactamente los Pokémon simulados |
| API-08 | Filtro por tipo inválido | `GET /api/pokemon/type/faketype` | 404 | 404, `TYPE_NOT_FOUND` |
| API-09 | Primera página | `?limit=20&offset=0` | Lista de 20 | 200, `limit: 20`, `offset: 0`, como máximo 20 resultados; a PokéAPI se le pide `limit=20&offset=0` |
| API-10 | Página fuera de rango | `?offset=99999` | `results: []` | 200, `results: []` |
| API-11 | Paginación negativa | `?limit=-1` y `?offset=-5` | No se llama | 422, `VALIDATION_ERROR` |
| API-12 | Timeout de PokéAPI | `GET /api/pokemon/25` | Lanza un timeout | 504, `EXTERNAL_API_TIMEOUT` |
| API-13 | PokéAPI no disponible | `GET /api/pokemon/25` | Error de conexión y respuesta 503 | 503, `EXTERNAL_API_UNAVAILABLE` |
| API-14 | Estructura de la respuesta | `GET /api/pokemon/1` | Datos de Bulbasaur | `id` int, `name` str, `height` int, `weight` int, `types` `["grass", "poison"]`, `abilities` lista de str, `image` str o null |
| API-15 | Endpoint inexistente | `GET /api/noexiste` | No se llama | 404, `NOT_FOUND`, con el formato de error estándar |

API-14 usa un Pokémon de dos tipos a propósito: con un Pokémon de un solo tipo no se detectaría un error que pierda el segundo tipo.

Pruebas adicionales recomendadas: respuesta 5xx de PokéAPI, respuesta de PokéAPI malformada (JSON inválido o campos faltantes), `limit=0`, `limit=101`, `id=0`, `id=abc`, `GET /api/types` y cabeceras CORS para `http://localhost:5173`.

## 8. Pruebas automatizadas de UI

Ubicación: `frontend/tests/`. Comando: `npx playwright test`. Se guardan capturas de pantalla de las pruebas que fallan.

| ID | Escenario | Pasos | Resultado esperado |
| --- | --- | --- | --- |
| UI-01 | Abrir la aplicación | Abrir `/` | Se muestra el catálogo con tarjetas que tienen imagen y nombre |
| UI-02 | Buscar Pikachu | Escribir `pikachu` y buscar | Aparece la tarjeta de Pikachu |
| UI-03 | Buscar Pokémon inexistente | Buscar `noexiste` | Aparece el estado vacío y no hay tarjetas |
| UI-04 | Filtrar por Electric | Seleccionar el tipo `electric` | Aparecen Pokémon eléctricos (Pikachu, Raichu) |
| UI-05 | Ver detalle | Abrir la tarjeta de Pikachu | Se ven el nombre, el ID 25, el tipo, las habilidades y las estadísticas base |
| UI-06 | Paginación | Pulsar Siguiente | Cambian los resultados y la primera tarjeta es Spearow |
| UI-07 | Falla del backend | Hacer que `/api/*` responda 500 o falle la conexión | Aparece un mensaje de error comprensible |
| UI-08 | Recargar la aplicación | Recargar después de filtrar | La aplicación sigue funcionando sin pantalla en blanco |
| UI-09 | Imágenes | Hacer que fallen las imágenes | Cada tarjeta muestra la imagen de respaldo |
| UI-10 | Vista móvil | Viewport de 375×667 | No hay scroll horizontal y los controles se pueden usar |

## 9. Pruebas negativas y de borde

| Categoría | Caso | Esperado | Cobertura |
| --- | --- | --- | --- |
| Búsqueda | Nombre vacío o solo espacios | Mensaje de validación / 422 | API-05, TC-005 |
| Búsqueda | Texto de 300 caracteres | Mensaje de validación / 422; el diseño no se rompe | TC-007 |
| Búsqueda | Solo números (`25`) | Estado vacío, sin error | TC-008 |
| Búsqueda | Caracteres especiales y HTML | 422; nada se ejecuta en el navegador | API-06, TC-006 |
| Búsqueda | Mayúsculas y espacios en los extremos | Mismo resultado que en minúsculas | TC-003 |
| IDs | `0`, `-1`, `abc`, `99999` | 422 o 404 según el caso | API-04, TC-020 |
| Paginación | Valores negativos, `0`, mayores de 100, fuera de rango | 422 o 200 con lista vacía | API-10, API-11, TC-019 |
| Red | Red lenta (Slow 3G) | Indicador de carga visible | TC-016 |
| Red | Backend detenido | Mensaje de error comprensible | UI-07, TC-015 |
| Red | PokéAPI no disponible o lento | 503 o 504 con formato de error | API-12, API-13, TC-021 |
| Datos | Respuesta de PokéAPI malformada | 502 `EXTERNAL_API_BAD_RESPONSE`, nunca un 500 con traza | Prueba adicional de API |
| Datos | Imagen faltante o URL rota | Imagen de respaldo | UI-09, TC-014 |
| Datos | Tipos sin Pokémon (`stellar`, `unknown`, `shadow`) | Estado vacío, no error | TC-009 |
| Concurrencia | Búsquedas repetidas y cambios rápidos de filtro | Se muestran solo los resultados de la última acción | TC-010 |

## 10. Trazabilidad requisitos → pruebas

| Requisito | API automatizada | UI automatizada | Manual |
| --- | --- | --- | --- |
| Lista paginada | API-01, API-09, API-10, API-11 | UI-01, UI-06 | TC-001, TC-011, TC-012, TC-019 |
| Pokémon por ID | API-02, API-04, API-14 | UI-05 | TC-013, TC-020 |
| Búsqueda por nombre | API-03, API-05, API-06 | UI-02, UI-03 | TC-002 a TC-008 |
| Tipos y filtro por tipo | API-07, API-08 | UI-04 | TC-009, TC-010 |
| Manejo de errores | API-04, API-08, API-12, API-13, API-15 | UI-07 | TC-015, TC-020, TC-021 |
| Formato consistente | API-14 y todas las pruebas de error | — | TC-019, TC-020 |
| Estados de carga, vacío y error | — | UI-03, UI-07 | TC-004, TC-015, TC-016 |
| Imágenes de respaldo | — | UI-09 | TC-014 |
| Diseño responsivo | — | UI-10 | TC-018 |
| Swagger UI | — | — | TC-022 |
| El frontend no llama a PokéAPI | — | UI-01 (la prueba revisa las peticiones) | TC-001 |

## 11. Criterios de entrada y salida

**Entrada**

- El backend y el frontend arrancan con las instrucciones del README.
- Las dependencias están instaladas y Swagger UI responde.

**Salida**

- Las 15 pruebas de API y al menos 8 pruebas de UI se ejecutaron y pasan.
- Todos los casos manuales tienen estado Pass, Fail o Blocked, con evidencia cuando aplica.
- No quedan bugs abiertos de severidad Crítica o Alta.
- Los bugs abiertos están documentados en [bug-reports.md](bug-reports.md) y en la sección de limitaciones del README.

## 12. Riesgos

| Riesgo | Impacto | Mitigación |
| --- | --- | --- |
| PokéAPI lento, caído o con límite de peticiones | Pruebas inestables y app sin datos | Mock en las pruebas de API, tiempo límite configurado en el backend, códigos 503/504 |
| El conteo de PokéAPI incluye formas alternativas | Las últimas páginas muestran nombres poco conocidos y algunas no tienen imagen | Imagen de respaldo; documentado como comportamiento esperado |
| Tipos sin Pokémon (`stellar`, `unknown`, `shadow`) | El usuario elige un tipo y no ve nada | Se ocultan en `/api/types`; si se piden por URL, se muestra un estado vacío claro |
| PokéAPI no tiene búsqueda parcial | Resultados distintos de lo que espera el usuario | El backend busca en un índice de nombres en caché; el comportamiento está documentado en el README |
| Respuestas que llegan desordenadas al cambiar rápido los filtros | Se muestran resultados de una acción anterior | Cancelar las peticiones anteriores; caso TC-010 |
| Los datos de PokéAPI cambian con el tiempo | Fallan las aserciones que usan conteos exactos | Las pruebas automatizadas usan datos simulados; los conteos de este plan llevan fecha |

## 13. Entregables

| Entregable | Ubicación |
| --- | --- |
| Documentación del backend | `docs/backend.md` |
| Documentación del frontend | `docs/frontend.md` |
| Plan de pruebas | `docs/test-plan.md` |
| Casos de prueba manuales | `docs/manual-test-cases.md` |
| Reportes de bugs | `docs/bug-reports.md` |
| Resumen de ejecución | `docs/test-summary.md` |
| Reporte HTML de API | `backend/reports/api-report.html` |
| Reporte HTML de UI | `frontend/playwright-report/` |
| Evidencias | `screenshots/` |
