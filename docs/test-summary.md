# Resumen de ejecución de pruebas – Pokémon Explorer

> Completar después de ejecutar todas las pruebas. Los campos en _cursiva_ son marcadores pendientes. Las cifras deben salir de las salidas reales de `pytest`, de Playwright y de [manual-test-cases.md](manual-test-cases.md).

## 1. Información de la ejecución

| Campo | Valor |
| --- | --- |
| Fecha | _completar_ |
| Versión probada (commit) | _completar_ |
| Ejecutado por | Miguel Pineda |
| Sistema operativo | _completar_ |
| Python / Node.js | _completar_ / _completar_ |
| Navegador manual | _completar_ |
| Navegador automatizado | Chromium (Playwright _versión_) |

## 2. Resultado general

| Tipo de prueba | Total | Pass | Fail | Blocked | No ejecutado | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| API automatizadas | _n_ | _n_ | _n_ | — | — | `backend/reports/api-report.html` |
| UI automatizadas | _n_ | _n_ | _n_ | — | — | `frontend/playwright-report/` |
| Manuales | 22 | _n_ | _n_ | _n_ | _n_ | [manual-test-cases.md](manual-test-cases.md) |
| **Total** | _n_ | _n_ | _n_ | _n_ | _n_ | |

**Bugs:** _n_ encontrados (_n_ reales, 3 intencionales) · _n_ resueltos · _n_ abiertos. Detalle en [bug-reports.md](bug-reports.md).

## 3. Pruebas automatizadas de API

```bash
cd backend
pytest -v --html=reports/api-report.html --self-contained-html
```

Resultado de la ejecución: _pegar la última línea de pytest, por ejemplo `15 passed in 0.84s`_

| ID | Escenario | Resultado | Notas |
| --- | --- | --- | --- |
| API-01 | Lista de Pokémon | _Pass / Fail_ | |
| API-02 | Pokémon por ID válido | _Pass / Fail_ | |
| API-03 | Buscar Pikachu | _Pass / Fail_ | |
| API-04 | Pokémon inexistente | _Pass / Fail_ | |
| API-05 | Nombre vacío | _Pass / Fail_ | |
| API-06 | Caracteres especiales | _Pass / Fail_ | |
| API-07 | Filtro por tipo válido | _Pass / Fail_ | |
| API-08 | Filtro por tipo inválido | _Pass / Fail_ | |
| API-09 | Primera página | _Pass / Fail_ | |
| API-10 | Página fuera de rango | _Pass / Fail_ | |
| API-11 | Paginación negativa | _Pass / Fail_ | |
| API-12 | Timeout de PokéAPI | _Pass / Fail_ | |
| API-13 | PokéAPI no disponible | _Pass / Fail_ | |
| API-14 | Estructura de la respuesta | _Pass / Fail_ | |
| API-15 | Endpoint inexistente | _Pass / Fail_ | |

Pruebas adicionales: _listar las que se agregaron además de las 15 (respuesta malformada, `limit=0`, CORS, etc.)_

## 4. Pruebas automatizadas de UI

```bash
cd frontend
npx playwright test
npx playwright show-report
```

Resultado de la ejecución: _pegar el resumen de Playwright, por ejemplo `10 passed (12.3s)`_

| ID | Escenario | Resultado | Notas |
| --- | --- | --- | --- |
| UI-01 | Abrir la aplicación | _Pass / Fail_ | |
| UI-02 | Buscar Pikachu | _Pass / Fail_ | |
| UI-03 | Buscar Pokémon inexistente | _Pass / Fail_ | |
| UI-04 | Filtrar por Electric | _Pass / Fail_ | |
| UI-05 | Ver detalle | _Pass / Fail_ | |
| UI-06 | Paginación | _Pass / Fail_ | |
| UI-07 | Falla del backend | _Pass / Fail_ | |
| UI-08 | Recargar la aplicación | _Pass / Fail_ | |
| UI-09 | Imágenes | _Pass / Fail_ | |
| UI-10 | Vista móvil | _Pass / Fail_ | |

## 5. Pruebas manuales

Resultado por caso: ver la tabla de resumen de [manual-test-cases.md](manual-test-cases.md).

Casos con estado Fail o Blocked:

| ID | Estado | Motivo | Bug relacionado |
| --- | --- | --- | --- |
| _TC-xxx_ | _Fail / Blocked_ | _…_ | _BUG-xxx_ |

## 6. Pruebas negativas y de borde

Hallazgos principales de los casos de la [sección 9 del plan de pruebas](test-plan.md#9-pruebas-negativas-y-de-borde):

| Área | Qué se probó | Qué se observó |
| --- | --- | --- |
| Entradas de búsqueda | Vacía, espacios, 300 caracteres, números, HTML y caracteres especiales | _completar_ |
| Paginación | Negativa, `0`, mayor de 100, fuera de rango, texto | _completar_ |
| Red | Red lenta, backend detenido, PokéAPI sin conexión | _completar_ |
| Datos | Imágenes bloqueadas, tipos sin Pokémon | _completar_ |
| Concurrencia | Cambios rápidos de filtro, búsquedas repetidas | _completar_ |

## 7. Tiempos de respuesta (opcional)

| Endpoint | Primera llamada (ms) | Llamadas siguientes (ms) | Notas |
| --- | --- | --- | --- |
| `GET /api/pokemon` | _n_ | _n_ | |
| `GET /api/pokemon/25` | _n_ | _n_ | |
| `GET /api/pokemon/search?name=pikachu` | _n_ | _n_ | |
| `GET /api/pokemon/type/electric` | _n_ | _n_ | |

Medición: _herramienta y número de llamadas, por ejemplo `curl -w "%{time_total}"` 10 veces por endpoint_

## 8. Criterios de aceptación

### Backend

- [ ] El servidor FastAPI arranca correctamente.
- [ ] Los cinco endpoints requeridos están implementados.
- [ ] Los datos vienen de PokéAPI.
- [ ] La paginación y la búsqueda funcionan.
- [ ] La validación de entradas funciona.
- [ ] Las respuestas de error son consistentes.
- [ ] Swagger UI está disponible.

### Frontend

- [ ] La aplicación React arranca correctamente.
- [ ] El catálogo muestra datos de Pokémon.
- [ ] La búsqueda, el filtro por tipo y la paginación funcionan.
- [ ] La vista de detalle muestra la información del Pokémon.
- [ ] Los estados de carga, vacío y error están implementados.
- [ ] El diseño responsivo funciona.

### QA

- [ ] Al menos 15 casos de prueba manuales documentados.
- [ ] Al menos 15 pruebas automatizadas de API.
- [ ] Al menos 8 pruebas automatizadas de UI.
- [ ] Al menos 3 reportes de bugs.
- [ ] Pruebas negativas y de borde realizadas.
- [ ] Evidencia de ejecución incluida.
- [ ] Resumen final de pruebas incluido.

## 9. Limitaciones y riesgos pendientes

- _Bugs abiertos, con su ID y por qué no se corrigieron._
- _Casos no cubiertos o bloqueados, y por qué._
- _Dependencias externas, por ejemplo: "los conteos de PokéAPI cambian con el tiempo"._

## 10. Conclusión

_Una o dos frases: si la aplicación cumple los criterios de aceptación, qué riesgo queda abierto y qué se probaría a continuación con más tiempo._
