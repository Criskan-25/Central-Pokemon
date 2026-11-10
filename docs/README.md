# Central Pokemon

```text
                                  ,'\
    _.----.        ____         ,'  _\   ___    ___     ____
_,-'       `.     |    |  /`.   \,-'    |   \  /   |   |    \  |`.
\      __    \    '-.  | /   `.  ___    |    \/    |   '-.   \ |  |
 \.    \ \   |  __  |  |/    ,','_  `.  |          | __  |    \|  |
   \    \/   /,' _`.|      ,' / / / /   |          ,' _`.|     |  |
    \     ,-'/  /   \    ,'   | \/ / ,`.|         /  /   \  |     |
     \    \ |   \_/  |   `-.  \    `'  /|  |    ||   \_/  | |\    |
      \    \ \      /       `-.`.___,-' |  |\  /| \      /  | |   |
       \    \ `.__,'|  |`-._    `|      |__| \/ |  `.__,'|  | |   |
        \_.-'       |__|    `-._ |              '-.|     '-.| |   |
                                `'                            '-._|

```

Aplicación web que consulta información de Pokémon desde la [PokéAPI](https://pokeapi.co/docs/v2) a través de un backend propio en **FastAPI** y la muestra en un cliente de Javascrip usando el framework **React**. Es una prueba técnica orientada a QA: además de construir la aplicación, se demuestra que funciona correctamente ante entradas válidas, inválidas y fallas inesperadas.

> El cliente React se comunica **solo** con el backend FastAPI. Nunca llama a PokéAPI directamente.

---

## Índice

1. [Tecnologías](#tecnologías)
2. [Requisitos previos](#requisitos-previos)
3. [Estructura del repositorio](#estructura-del-repositorio)
4. [Instalación](#instalación)
5. [Ejecutar la aplicación](#ejecutar-la-aplicación)
6. [Ejecutar las pruebas](#ejecutar-las-pruebas)
7. [API: endpoints y formato de respuesta](#api-endpoints-y-formato-de-respuesta)
8. [Documentación](#documentación)
9. [Decisiones técnicas y supuestos](#decisiones-técnicas-y-supuestos)
10. [Limitaciones y bugs conocidos](#limitaciones-y-bugs-conocidos)
11. [Git y GitHub: cómo bajar y subir el proyecto](#git-y-github-cómo-bajar-y-subir-el-proyecto)

---

## Tecnologías

| Área | Herramienta |
| --- | --- |
| Backend | Python 3.11+, FastAPI, Uvicorn |
| Cliente HTTP | HTTPX |
| Frontend | React + Vite |
| Pruebas de API | Pytest + FastAPI TestClient |
| Pruebas de UI | Playwright |
| Documentación de API | Swagger / OpenAPI |
| Control de versiones | Git / GitHub |

## Requisitos previos

- **Python** 3.11 o superior → `python --version`
- **Node.js** 20.19 o superior (o 22.12 o superior) y **npm** → `node --version`. Vite 8 no funciona con versiones anteriores.
- **Git** → `git --version`
- Una cuenta en **GitHub**
- Conexión a internet (para PokéAPI e instalar dependencias)

## Estructura del repositorio

```
pokemon-explorer/
├── backend/
│   ├── app/
│   │   ├── main.py              # Punto de entrada, CORS y manejo de errores
│   │   ├── routes/pokemon.py    # Endpoints REST
│   │   ├── services/pokeapi.py  # Cliente de PokéAPI
│   │   ├── schemas/pokemon.py   # Modelos de respuesta
│   │   └── core/config.py       # Configuración
│   ├── tests/                   # Pruebas automatizadas de API
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/pokemonService.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── tests/                   # Pruebas automatizadas de UI (Playwright)
│   └── package.json
├── docs/
│   ├── backend.md               # Documentación técnica del backend
│   ├── frontend.md              # Documentación técnica del frontend
│   ├── test-plan.md
│   ├── manual-test-cases.md
│   ├── bug-reports.md
│   └── test-summary.md
├── screenshots/                 # Evidencias de las pruebas
└── README.md
```

## Instalación

### Backend

```bash
cd backend
python -m venv venv

# Activar el entorno virtual
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
# macOS / Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
npx playwright install chromium   # navegador para las pruebas de UI
```

## Ejecutar la aplicación

Se necesitan **dos terminales**, una para cada parte.

**Terminal 1 – Backend**

```bash
cd backend
# (activar el entorno virtual si no está activo)
uvicorn app.main:app --reload --port 8000
```

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

**Terminal 2 – Frontend**

```bash
cd frontend
npm run dev
```

- Aplicación: http://localhost:5173

Si el backend corre en otra dirección, crea `frontend/.env` con:

```
VITE_API_URL=http://localhost:8000
```

## Ejecutar las pruebas

### Pruebas de API (Pytest)

```bash
cd backend
pytest                                                   # todas las pruebas
pytest -v                                                # detalle de cada prueba
pytest --html=reports/api-report.html --self-contained-html   # reporte HTML
```

Las respuestas de PokéAPI se simulan (mock), así que las pruebas no dependen de internet ni de que PokéAPI esté disponible.

### Pruebas de UI (Playwright)

```bash
cd frontend
npx playwright test            # inicia el frontend automáticamente y ejecuta las pruebas (no hace falta el backend: sus respuestas se simulan)
npx playwright test --headed   # ver el navegador mientras corren
npx playwright show-report     # abrir el reporte HTML
```

Si una prueba falla, Playwright guarda una captura de pantalla en `frontend/test-results/`.

## API: endpoints y formato de respuesta

| Método | Endpoint | Descripción |
| --- | --- | --- |
| GET | `/api/pokemon?limit=20&offset=0` | Lista paginada de Pokémon |
| GET | `/api/pokemon/{id}` | Detalle de un Pokémon por ID |
| GET | `/api/pokemon/search?name=pikachu` | Búsqueda por nombre |
| GET | `/api/types` | Tipos de Pokémon disponibles |
| GET | `/api/pokemon/type/{type}` | Pokémon filtrados por tipo |

**Respuesta exitosa**

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
    "image": "https://..."
  }
}
```

**Respuesta de error**

```json
{
  "success": false,
  "error": {
    "code": "POKEMON_NOT_FOUND",
    "message": "Pokémon no encontrado"
  }
}
```

**Códigos de estado usados**

| Código | `error.code` | Cuándo |
| --- | --- | --- |
| 200 | — | Petición correcta (incluye búsquedas o páginas sin resultados, que devuelven `results: []`) |
| 404 | `POKEMON_NOT_FOUND`, `TYPE_NOT_FOUND`, `NOT_FOUND` | Pokémon, tipo o endpoint inexistente |
| 422 | `VALIDATION_ERROR` | Parámetros inválidos (nombre vacío, caracteres especiales, paginación negativa) |
| 500 | `INTERNAL_ERROR` | Error interno no esperado |
| 502 | `EXTERNAL_API_BAD_RESPONSE` | PokéAPI respondió con datos malformados |
| 503 | `EXTERNAL_API_UNAVAILABLE` | PokéAPI no disponible |
| 504 | `EXTERNAL_API_TIMEOUT` | PokéAPI tardó demasiado en responder (timeout) |

Detalle de cada endpoint, sus parámetros y sus respuestas en [`docs/backend.md`](docs/backend.md).

## Documentación

| Documento | Contenido |
| --- | --- |
| [`docs/backend.md`](docs/backend.md) | Arquitectura, endpoints, validación, manejo de errores, caché y pruebas del backend |
| [`docs/frontend.md`](docs/frontend.md) | Estructura, rutas, componentes, estados de la interfaz y pruebas del frontend |
| [`docs/test-plan.md`](docs/test-plan.md) | Alcance, estrategia, datos de prueba, escenarios, trazabilidad y criterios de aceptación |
| [`docs/manual-test-cases.md`](docs/manual-test-cases.md) | 22 casos de prueba manuales |
| [`docs/bug-reports.md`](docs/bug-reports.md) | Reportes de bugs, indicando cuáles son reales y cuáles introducidos a propósito |
| [`docs/test-summary.md`](docs/test-summary.md) | Resumen final de la ejecución y resultados |
| [`screenshots/`](screenshots/) | Evidencias |

## Decisiones técnicas y supuestos

- El frontend consume únicamente el backend; el backend centraliza validación, errores y la llamada a PokéAPI.
- Todas las respuestas siguen el mismo formato (`success` + `data` o `error`).
- Una página fuera de rango devuelve **200 con lista vacía**, no un error.
- Las pruebas de API simulan PokéAPI para ser rápidas y estables.
- Las pruebas de UI simulan el backend; la integración con el backend real se verifica en los casos manuales.
- La búsqueda encuentra los nombres que contienen el texto (`pika` → Pikachu), usando un índice de nombres guardado en caché.
- La búsqueda y el filtro por tipo no se combinan: usar uno quita el otro.
- `/api/types` no incluye `stellar`, `unknown` ni `shadow`, porque no tienen Pokémon.
- Más decisiones en [`docs/backend.md`](docs/backend.md#12-decisiones-técnicas) y [`docs/frontend.md`](docs/frontend.md#12-decisiones-técnicas).
- *(Agrega aquí tus propias decisiones, preguntas y supuestos.)*

## Limitaciones y bugs conocidos

- PokéAPI solo busca por nombre exacto. Para permitir búsquedas parciales, el backend descarga una vez el índice completo de nombres y filtra en memoria; la primera búsqueda hace esa llamada extra a PokéAPI.
- El total de PokéAPI (1351) incluye formas alternativas, como `pikachu-gmax`, que aparecen en las últimas páginas del catálogo y en las búsquedas.
- Algunas formas alternativas de Pokémon no tienen imagen oficial; se muestra una imagen de respaldo.
- *(Lista aquí los bugs que sigan abiertos, con referencia a `docs/bug-reports.md`.)*

> No se incluyen contraseñas, claves de API ni otros datos sensibles en el repositorio.

---

## Git y GitHub: cómo bajar y subir el proyecto

Esta sección explica cómo subir el proyecto a GitHub por primera vez, cómo bajarlo en otra computadora y cómo seguir trabajando sobre **el mismo repositorio**.

### 0. Configurar Git (solo la primera vez en cada computadora)

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo@ejemplo.com"
```

### 1. Crear el repositorio en GitHub

1. Entra a https://github.com y haz clic en **New** (o **+ → New repository**).
2. Nombre: `pokemon-explorer`.
3. Elige **Public** (para que el evaluador pueda verlo).
4. **No** marques "Add a README", ".gitignore" ni "license" (ya los tienes en local; si los marcas, el primer `push` puede ser rechazado).
5. Clic en **Create repository** y copia la URL, por ejemplo:
   `https://github.com/TU_USUARIO/pokemon-explorer.git`

### 2. Crear el archivo `.gitignore`

En la raíz del proyecto, crea `.gitignore` para no subir dependencias ni archivos generados:

```gitignore
# Python
venv/
__pycache__/
*.pyc
.pytest_cache/
backend/reports/

# Node
node_modules/
dist/

# Playwright
frontend/test-results/
frontend/playwright-report/

# Variables de entorno y sistema
.env
.DS_Store
Thumbs.db
```

### 3. Subir el proyecto por primera vez

Desde la carpeta raíz `pokemon-explorer/`:

```bash
git init                         # inicia el repositorio local
git add .                        # prepara todos los archivos
git commit -m "Primer commit: Pokémon Explorer"
git branch -M main               # nombra la rama principal "main"
git remote add origin https://github.com/TU_USUARIO/pokemon-explorer.git
git push -u origin main          # sube el código a GitHub
```

Recarga la página del repositorio en GitHub: ya deberías ver tus archivos.

### 4. Bajar (clonar) el repositorio en otra computadora

```bash
git clone https://github.com/TU_USUARIO/pokemon-explorer.git
cd pokemon-explorer
```

Después sigue los pasos de [Instalación](#instalación) (las carpetas `venv/` y `node_modules/` no se suben, se crean de nuevo).

### 5. Trabajar en el mismo repositorio (flujo diario)

Siempre en este orden: **bajar cambios → trabajar → guardar → subir**.

```bash
git pull                         # 1. baja lo último del repositorio
# ... editas archivos ...
git status                       # 2. revisa qué cambió
git add .                        # 3. prepara los cambios
git commit -m "Agrega pruebas de paginación"   # 4. guarda con un mensaje claro
git push                         # 5. sube los cambios al mismo repositorio
```

Haz `git pull` al empezar a trabajar, sobre todo si usas más de una computadora o editaste algo directamente en GitHub.

### 6. Trabajar con ramas (recomendado)

```bash
git checkout -b feature/filtro-por-tipo   # crea una rama y te cambia a ella
# ... cambios, add y commit ...
git push -u origin feature/filtro-por-tipo
```

En GitHub aparecerá el botón **Compare & pull request**: crea el Pull Request y haz **Merge** a `main`. Luego, en local:

```bash
git checkout main
git pull
```

### 7. Autenticación en GitHub

GitHub ya no acepta tu contraseña normal al hacer `push` por HTTPS. Usa una de estas opciones:

- **Token personal (HTTPS):** GitHub → *Settings → Developer settings → Personal access tokens* → genera un token con permiso de repositorio. Cuando Git pida contraseña, pega el token.
- **GitHub CLI:** instala `gh` y ejecuta `gh auth login`.
- **SSH:** genera una llave con `ssh-keygen -t ed25519 -C "tu-correo@ejemplo.com"`, agrégala en *Settings → SSH and GPG keys* y usa la URL `git@github.com:TU_USUARIO/pokemon-explorer.git`.

### 8. Problemas comunes

| Mensaje | Causa | Solución |
| --- | --- | --- |
| `rejected ... (fetch first)` | GitHub tiene cambios que tú no tienes | `git pull --rebase` y luego `git push` |
| `remote origin already exists` | Ya configuraste el remoto | `git remote set-url origin URL_CORRECTA` |
| `Authentication failed` | Usaste tu contraseña normal | Usa un token, `gh auth login` o SSH |
| Conflicto en un archivo tras `git pull` | Se editó la misma línea en dos lugares | Abre el archivo, elige el contenido correcto, borra las marcas `<<<<<<<`, `=======`, `>>>>>>>`, y luego `git add .` y `git commit` |
| Se subió `node_modules/` por error | Faltaba el `.gitignore` | Agrega el `.gitignore`, luego `git rm -r --cached node_modules` y haz commit |

### 9. Comandos útiles

```bash
git log --oneline        # historial de commits
git diff                 # ver cambios aún no preparados
git remote -v            # ver a qué repositorio está conectado
git restore archivo.txt  # descartar cambios de un archivo (sin commit)
```

### 10. Entrega

Cuando todo esté subido, comparte la URL del repositorio:

```
https://github.com/TU_USUARIO/pokemon-explorer
```

Antes de entregarla, abre el enlace en una ventana privada para confirmar que el repositorio es público y que se ve el README.
