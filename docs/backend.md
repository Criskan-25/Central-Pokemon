# Backend – Documentación técnica

API REST en FastAPI que consulta [PokéAPI](https://pokeapi.co/docs/v2) y entrega los datos al cliente React con un formato propio, validado y consistente. El frontend nunca llama a PokéAPI: todo pasa por este backend.

> Este documento describe el diseño del backend. Si la implementación cambia, actualizar también el [plan de pruebas](test-plan.md).

## Índice

1. [Tecnologías](#1-tecnologías)
2. [Estructura](#2-estructura)
3. [Arquitectura](#3-arquitectura)
4. [Configuración](#4-configuración)
5. [Endpoints](#5-endpoints)
6. [Formato de respuesta](#6-formato-de-respuesta)
7. [Validación de entradas](#7-validación-de-entradas)
8. [Manejo de errores](#8-manejo-de-errores)
9. [Caché](#9-caché)
10. [Pruebas](#10-pruebas)
11. [Comandos](#11-comandos)
12. [Decisiones técnicas](#12-decisiones-técnicas)

---

## 1. Tecnologías

| Paquete | Versión | Uso |
| --- | --- | --- |
| Python | 3.11+ | Lenguaje |
| FastAPI | 0.162 | Framework web, validación y Swagger |
| Uvicorn | 0.54 | Servidor ASGI |
| HTTPX | 0.28 | Cliente HTTP asíncrono para PokéAPI |
| Pydantic | 2.14 | Modelos de respuesta (se instala con FastAPI) |
| Pytest | 9.2 | Pruebas |
| respx | 0.23 | Simulación (mock) de las llamadas HTTPX a PokéAPI |
| pytest-html | 4.2 | Reporte HTML de las pruebas |

`requirements.txt`:

```text
fastapi
uvicorn[standard]
httpx
pytest
respx
pytest-html
```

Fijar las versiones exactas (`pip freeze`) antes de entregar, para que el evaluador instale lo mismo que se probó.

## 2. Estructura

```
backend/
├── app/
│   ├── main.py              # Crea la app, CORS, manejadores de errores, ciclo de vida
│   ├── routes/pokemon.py    # Endpoints, validación de parámetros
│   ├── services/pokeapi.py  # Cliente de PokéAPI, conversión de datos, caché
│   ├── schemas/pokemon.py   # Modelos Pydantic de respuesta
│   └── core/
│       ├── config.py        # Configuración desde variables de entorno
│       └── errors.py        # Excepción ApiError y códigos de error
├── tests/
│   ├── conftest.py          # Cliente de pruebas y mock de PokéAPI
│   ├── fixtures/            # Respuestas reales de PokéAPI recortadas (JSON)
│   ├── test_pokemon.py      # Casos exitosos
│   └── test_errors.py       # Validación y fallas
├── reports/                 # Reporte HTML generado (no se sube a git)
└── requirements.txt
```

`core/errors.py` se agrega a la estructura sugerida en la prueba para que las rutas y el servicio lancen el mismo tipo de error sin depender de `main.py`.

## 3. Arquitectura

```
React ──HTTP──▶ routes/pokemon.py ──▶ services/pokeapi.py ──HTTPX──▶ PokéAPI
                  │ valida entradas         │ caché, timeout,
                  │                         │ convierte datos y errores
                  ▼                         ▼
              schemas/pokemon.py      core/errors.py (ApiError)
                  │                         │
                  └──────▶ main.py ◀────────┘
                     respuesta { success, data | error }
```

| Capa | Responsabilidad | No debe |
| --- | --- | --- |
| `routes` | Declarar endpoints, validar `path` y `query`, llamar al servicio, envolver en `{success, data}` | Llamar a HTTPX directamente |
| `services` | Llamar a PokéAPI, aplicar timeout y caché, convertir la respuesta al formato propio, traducir fallas a `ApiError` | Conocer detalles de HTTP del cliente (status de FastAPI, CORS) |
| `schemas` | Definir y documentar la forma de cada respuesta | Contener lógica |
| `main.py` | Crear la app, configurar CORS, registrar manejadores de error, abrir y cerrar el cliente HTTPX | Contener endpoints |

Se usa **un solo `httpx.AsyncClient`**, creado al iniciar la app (`lifespan`) y cerrado al apagarla. Reutiliza conexiones y centraliza el timeout.

## 4. Configuración

Todo se lee de variables de entorno con valores por defecto, así que no hace falta ningún archivo `.env` para ejecutar en local. No hay credenciales: PokéAPI es pública.

| Variable | Por defecto | Uso |
| --- | --- | --- |
| `POKEAPI_BASE_URL` | `https://pokeapi.co/api/v2` | URL base de PokéAPI |
| `POKEAPI_TIMEOUT_SECONDS` | `5` | Tiempo máximo de espera por petición a PokéAPI |
| `CACHE_TTL_SECONDS` | `300` | Tiempo que se guarda una respuesta en caché (`0` la desactiva) |
| `CORS_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | Orígenes permitidos, separados por comas |

`POKEAPI_BASE_URL` también sirve para probar fallas a mano: apuntarlo a una dirección que no responde (por ejemplo `http://10.255.255.1`) provoca un timeout.

## 5. Endpoints

| Método | Ruta | Parámetros | Respuesta (`data`) |
| --- | --- | --- | --- |
| GET | `/api/pokemon` | `limit` (1–100, por defecto 20), `offset` (≥ 0, por defecto 0) | Página de Pokémon |
| GET | `/api/pokemon/search` | `name` (obligatorio), `limit`, `offset` | Página de Pokémon |
| GET | `/api/pokemon/type/{type}` | `type`, `limit`, `offset` | Página de Pokémon |
| GET | `/api/pokemon/{id}` | `id` (entero ≥ 1) | Detalle de un Pokémon |
| GET | `/api/types` | — | Lista de nombres de tipos |

Las rutas `/search` y `/type/{type}` se declaran **antes** que `/{id}`. Si no, FastAPI intentaría interpretar `search` como un ID y respondería 422.

### GET /api/pokemon

Pasa `limit` y `offset` a `GET {POKEAPI_BASE_URL}/pokemon`. PokéAPI solo devuelve `name` y `url` de cada Pokémon. El `id` se extrae de la URL y la `image` se construye con el ID (`.../sprites/pokemon/other/official-artwork/{id}.png`), así no hace falta una llamada extra por Pokémon.

```json
{
  "success": true,
  "data": {
    "count": 1351,
    "limit": 20,
    "offset": 0,
    "results": [
      { "id": 1, "name": "bulbasaur", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png" }
    ]
  }
}
```

- `count` incluye las formas alternativas (IDs 10001 en adelante); por eso son 1351 y no 1025.
- Un `offset` mayor que `count` devuelve `200` con `results: []`.
- Algunas formas alternativas no tienen imagen oficial. La URL construida responde 404 y el frontend muestra la imagen de respaldo.

### GET /api/pokemon/{id}

Llama a `GET /pokemon/{id}` y reduce la respuesta (más de 20 campos) a lo que usa el frontend.

```json
{
  "success": true,
  "data": {
    "id": 25,
    "name": "pikachu",
    "height": 4,
    "weight": 60,
    "types": ["electric"],
    "abilities": ["static", "lightning-rod"],
    "stats": [
      { "name": "hp", "value": 35 },
      { "name": "attack", "value": 55 },
      { "name": "defense", "value": 40 },
      { "name": "special-attack", "value": 50 },
      { "name": "special-defense", "value": 50 },
      { "name": "speed", "value": 90 }
    ],
    "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png"
  }
}
```

| Campo | Origen en PokéAPI | Notas |
| --- | --- | --- |
| `height` | `height` | En decímetros, sin convertir |
| `weight` | `weight` | En hectogramos, sin convertir |
| `types` | `types[].type.name`, ordenado por `slot` | Todos los tipos, no solo el primero |
| `abilities` | `abilities[].ability.name`, ordenado por `slot` | Incluye las habilidades ocultas |
| `stats` | `stats[].stat.name` y `stats[].base_stat` | Se agrega al formato del enunciado porque el detalle debe mostrar estadísticas base |
| `image` | `sprites.other["official-artwork"].front_default`, y si es `null`, `sprites.front_default` | `null` si no hay ninguna |

### GET /api/pokemon/search?name=pikachu

PokéAPI no permite buscar por parte del nombre. El backend descarga una vez el índice completo de nombres (`GET /pokemon?limit=100000`, unos 93 KB), lo guarda en caché y filtra en memoria.

1. Se normaliza `name` (ver [validación](#7-validación-de-entradas)).
2. Se eligen los nombres que **contienen** el término.
3. Se ordenan: primero la coincidencia exacta, luego los que empiezan por el término y al final los que lo contienen en otra posición; en cada grupo, por ID.
4. Se pagina con `limit` y `offset`.

La respuesta tiene la misma forma que `GET /api/pokemon`. Buscar `pikachu` devuelve 17 resultados: `pikachu` primero y después formas como `pikachu-rock-star` o `pikachu-gmax`. Sin coincidencias: `200` con `count: 0` y `results: []`.

### GET /api/types

Llama a `GET /type` y devuelve solo los nombres. Se excluyen `stellar`, `unknown` y `shadow`, porque en PokéAPI existen pero no tienen ningún Pokémon y mostrarlos en el filtro llevaría siempre a una lista vacía.

```json
{ "success": true, "data": ["normal", "fighting", "flying", "poison", "ground", "rock", "bug", "ghost", "steel", "fire", "water", "grass", "electric", "psychic", "ice", "dragon", "dark", "fairy"] }
```

### GET /api/pokemon/type/{type}

Llama a `GET /type/{type}`. PokéAPI devuelve todos los Pokémon del tipo de una vez (por ejemplo, 114 para `electric`), así que el backend pagina en memoria con `limit` y `offset`. La respuesta tiene la misma forma que `GET /api/pokemon`. Pedir directamente `stellar` devuelve `200` con `results: []`.

## 6. Formato de respuesta

Todas las respuestas, incluidos los errores de FastAPI y las rutas inexistentes, usan el mismo formato.

```json
{ "success": true, "data": { } }
```

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "El parámetro 'limit' debe ser mayor o igual a 1.",
    "details": [{ "field": "limit", "message": "Input should be greater than or equal to 1" }]
  }
}
```

- `code`: constante en inglés para que el frontend y las pruebas decidan qué hacer.
- `message`: texto en español que se puede mostrar al usuario.
- `details`: solo en `VALIDATION_ERROR`; lista de parámetros inválidos.

Los modelos están en `schemas/pokemon.py` (`PokemonSummary`, `PokemonPage`, `PokemonDetail`, `Stat`, `ErrorResponse` y el genérico `ApiResponse[T]`). Cada endpoint declara su `response_model` y sus respuestas de error (`responses={404: ..., 422: ...}`), de modo que Swagger documenta los dos formatos.

## 7. Validación de entradas

| Parámetro | Regla | Si no se cumple |
| --- | --- | --- |
| `limit` | Entero, 1 a 100 | 422 |
| `offset` | Entero, ≥ 0 | 422 |
| `id` | Entero, ≥ 1 | 422 |
| `name` | Obligatorio; 1 a 50 caracteres después de quitar espacios de los extremos; solo letras, números, espacios, guiones, `.` y `'` | 422 |
| `type` | Solo letras y guiones, máximo 20 caracteres | 422 |
| `type` válido pero inexistente | — | 404 `TYPE_NOT_FOUND` |

**Normalización de `name`** (antes de validar el patrón): quitar los espacios de los extremos, pasar a minúsculas, quitar `.` y `'`, y reemplazar los espacios internos por `-`. Así `"  Mr. Mime "` se convierte en `mr-mime` y `"Farfetch'd"` en `farfetchd`, que son los nombres de PokéAPI.

`limit`, `offset` e `id` se validan con `Query`/`Path` de FastAPI. `name` se valida a mano en la ruta, porque `min_length=1` acepta `"   "`. Las entradas inválidas se rechazan **antes** de llamar a PokéAPI.

## 8. Manejo de errores

Las rutas y el servicio lanzan `ApiError(status_code, code, message)`. `main.py` registra manejadores que convierten cualquier error al formato de la sección 6.

| Situación | Se detecta con | HTTP | `code` |
| --- | --- | --- | --- |
| Parámetro inválido | `RequestValidationError` de FastAPI o validación manual | 422 | `VALIDATION_ERROR` |
| ID inexistente | PokéAPI responde 404 en `/pokemon/{id}` | 404 | `POKEMON_NOT_FOUND` |
| Tipo inexistente | PokéAPI responde 404 en `/type/{type}` | 404 | `TYPE_NOT_FOUND` |
| Ruta inexistente | `StarletteHTTPException` 404 | 404 | `NOT_FOUND` |
| Método no permitido | `StarletteHTTPException` 405 | 405 | `METHOD_NOT_ALLOWED` |
| PokéAPI tarda demasiado | `httpx.TimeoutException` | 504 | `EXTERNAL_API_TIMEOUT` |
| PokéAPI no responde | `httpx.RequestError` (conexión rechazada, DNS) | 503 | `EXTERNAL_API_UNAVAILABLE` |
| PokéAPI responde 5xx | Código de estado ≥ 500 | 503 | `EXTERNAL_API_UNAVAILABLE` |
| Respuesta de PokéAPI malformada | JSON inválido, campos faltantes o tipos incorrectos | 502 | `EXTERNAL_API_BAD_RESPONSE` |
| Cualquier otro error | Manejador genérico de `Exception` | 500 | `INTERNAL_ERROR` |

- Los errores 5xx se registran en el log del servidor (`logging`) con la causa; la respuesta al cliente nunca incluye trazas ni la respuesta original de PokéAPI.
- Los errores no se guardan en caché.

## 9. Caché

Caché en memoria con tiempo de vida (`CACHE_TTL_SECONDS`), con la URL de PokéAPI como clave. Se aplica a todas las respuestas correctas de PokéAPI y sobre todo al índice de nombres de la búsqueda.

- Es por proceso: se pierde al reiniciar el backend y no se comparte entre varias instancias.
- Cada `TestClient` crea su propia caché (se crea en el `lifespan`), así que una prueba no afecta a otra.
- Para probar fallas a mano (TC-021), consultar un Pokémon que no se haya pedido antes o reiniciar el backend.

## 10. Pruebas

Comando: `pytest -v`. Ninguna prueba llama a PokéAPI de verdad: `respx` intercepta las peticiones de HTTPX y devuelve respuestas fijas guardadas en `tests/fixtures/`. Esas respuestas se copiaron de PokéAPI y se recortaron a los campos que usa el backend.

```python
# Ejemplo: API-12, timeout de PokéAPI
def test_timeout_devuelve_504(client, pokeapi):
    pokeapi.get("/pokemon/25").mock(side_effect=httpx.ReadTimeout("timeout"))

    response = client.get("/api/pokemon/25")

    assert response.status_code == 504
    assert response.json() == {
        "success": False,
        "error": {"code": "EXTERNAL_API_TIMEOUT", "message": ANY},
    }
```

| Archivo | Escenarios |
| --- | --- |
| `test_pokemon.py` | API-01, API-02, API-03, API-07, API-09, API-10, API-14 |
| `test_errors.py` | API-04, API-05, API-06, API-08, API-11, API-12, API-13, API-15 |

Además de los 15 escenarios del [plan de pruebas](test-plan.md#7-pruebas-automatizadas-de-api), conviene cubrir: respuesta 5xx de PokéAPI, respuesta malformada (502), `limit=0` y `limit=101`, `id=0` e `id=abc`, normalización de `name` (`" Mr. Mime "`), orden de los resultados de búsqueda, exclusión de tipos vacíos en `/api/types`, cabeceras CORS y que la segunda petición igual use la caché (PokéAPI recibe una sola llamada).

Las pruebas que validan entradas también verifican que **no** hubo llamada a PokéAPI (`pokeapi.calls.call_count == 0`).

## 11. Comandos

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000          # ejecutar
pytest -v                                          # pruebas
pytest --html=reports/api-report.html --self-contained-html   # reporte HTML
```

| URL | Contenido |
| --- | --- |
| http://localhost:8000/docs | Swagger UI |
| http://localhost:8000/redoc | ReDoc |
| http://localhost:8000/openapi.json | Especificación OpenAPI |

Ejemplos rápidos:

```bash
curl "http://localhost:8000/api/pokemon?limit=5"
curl "http://localhost:8000/api/pokemon/25"
curl "http://localhost:8000/api/pokemon/search?name=pikachu"
curl "http://localhost:8000/api/types"
curl "http://localhost:8000/api/pokemon/type/electric?limit=5"
curl -i "http://localhost:8000/api/pokemon/99999"   # 404
```

## 12. Decisiones técnicas

| Decisión | Motivo | Alternativa descartada |
| --- | --- | --- |
| Búsqueda parcial con un índice de nombres en caché | PokéAPI solo busca por nombre exacto; el índice pesa unos 93 KB y se descarga una vez | Búsqueda exacta: `pika` no encontraría a Pikachu |
| Imagen de la lista construida a partir del ID | Evita 20 llamadas extra a PokéAPI por página | Pedir el detalle de cada Pokémon de la página |
| Página fuera de rango responde 200 con lista vacía | No es un error del cliente: la colección existe, solo no tiene más elementos | 404 |
| Ocultar `stellar`, `unknown` y `shadow` | No tienen Pokémon; elegirlos siempre daría una lista vacía | Mostrarlos todos |
| 503 para PokéAPI caído y 504 para timeout | Indica al cliente que el problema es externo y temporal, no del backend | 500 para todo |
| 502 para respuestas malformadas | PokéAPI respondió, pero con datos inutilizables | 500 |
| Mock con `respx` en las pruebas | Pruebas rápidas, estables y sin internet; permite simular timeouts y caídas | Llamar a PokéAPI real |
| `height` y `weight` sin convertir | Se mantienen las unidades de PokéAPI; el frontend convierte a metros y kilogramos | Convertir en el backend |
