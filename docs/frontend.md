# Frontend – Documentación técnica

Cliente React (Vite) para explorar Pokémon: catálogo, búsqueda, filtro por tipo, paginación y detalle. Solo se comunica con el [backend](backend.md); nunca llama a PokéAPI.

> Este documento describe el diseño del frontend. Si la implementación cambia, actualizar también el [plan de pruebas](test-plan.md).

## Índice

1. [Tecnologías](#1-tecnologías)
2. [Estructura](#2-estructura)
3. [Rutas y estado en la URL](#3-rutas-y-estado-en-la-url)
4. [Comunicación con el backend](#4-comunicación-con-el-backend)
5. [Hooks](#5-hooks)
6. [Componentes](#6-componentes)
7. [Estados de la interfaz](#7-estados-de-la-interfaz)
8. [Imágenes](#8-imágenes)
9. [Diseño responsivo y accesibilidad](#9-diseño-responsivo-y-accesibilidad)
10. [Pruebas con Playwright](#10-pruebas-con-playwright)
11. [Comandos](#11-comandos)
12. [Decisiones técnicas](#12-decisiones-técnicas)

---

## 1. Tecnologías

| Paquete | Versión | Uso |
| --- | --- | --- |
| Node.js | 20.19+ o 22.12+ | Requisito de Vite 8 |
| React | 19 | Interfaz |
| Vite | 8 | Servidor de desarrollo y build |
| React Router | 7 | Rutas del catálogo y del detalle |
| CSS propio (variables CSS) | — | Estilos, sin librería de componentes |
| Playwright | 1.64 | Pruebas de UI |

No se usa Tailwind ni Material UI: la interfaz es pequeña y el CSS propio evita dependencias que habría que explicar.

## 2. Estructura

```
frontend/
├── public/
│   └── pokemon-placeholder.svg   # Imagen de respaldo
├── src/
│   ├── components/
│   │   ├── SearchBar.jsx
│   │   ├── TypeFilter.jsx
│   │   ├── PokemonGrid.jsx
│   │   ├── PokemonCard.jsx
│   │   ├── PokemonImage.jsx
│   │   ├── Pagination.jsx
│   │   ├── TypeBadge.jsx
│   │   ├── StatBar.jsx
│   │   ├── Loader.jsx
│   │   ├── EmptyState.jsx
│   │   └── ErrorMessage.jsx
│   ├── pages/
│   │   ├── CatalogPage.jsx
│   │   ├── PokemonDetailPage.jsx
│   │   └── NotFoundPage.jsx
│   ├── hooks/
│   │   ├── usePokemonList.js
│   │   ├── usePokemon.js
│   │   └── useTypes.js
│   ├── services/pokemonService.js
│   ├── utils/
│   │   ├── validation.js         # Reglas de búsqueda (iguales a las del backend)
│   │   └── format.js             # Unidades y nombres
│   ├── styles.css
│   ├── App.jsx                   # Rutas
│   └── main.jsx                  # Punto de entrada
├── tests/
│   ├── fixtures/                 # Respuestas del backend (JSON)
│   ├── helpers/mockApi.js        # Intercepta /api/* con page.route
│   ├── catalog.spec.js
│   ├── search.spec.js
│   ├── filter.spec.js
│   ├── detail.spec.js
│   ├── errors.spec.js
│   └── responsive.spec.js
├── playwright.config.js
├── vite.config.js
└── package.json
```

## 3. Rutas y estado en la URL

| Ruta | Página | Ejemplo |
| --- | --- | --- |
| `/` | Catálogo | `/?type=electric&page=2` |
| `/pokemon/:id` | Detalle | `/pokemon/25` |
| `*` | No encontrada | `/xyz` |

El estado del catálogo vive en los parámetros de la URL, no solo en el estado de React:

| Parámetro | Valores | Por defecto |
| --- | --- | --- |
| `q` | Texto de búsqueda | — |
| `type` | Nombre de un tipo | — |
| `page` | Entero ≥ 1 | `1` |

Así, recargar la página (UI-08, TC-017) conserva la búsqueda, el filtro y la página; el botón Atrás del navegador funciona; y un resultado se puede compartir con un enlace.

Reglas:

- **Búsqueda y filtro por tipo son excluyentes.** El backend no tiene un endpoint que combine los dos, así que buscar quita el filtro de tipo y elegir un tipo borra la búsqueda.
- Cambiar la búsqueda o el tipo vuelve a la página 1.
- `page` inválido en la URL (`abc`, `0`, `-3`) se trata como `1`. Una página mayor que la última muestra el estado vacío con un botón para volver a la primera.
- El detalle tiene un enlace "Volver" que regresa al catálogo con los mismos parámetros que tenía antes; si se abrió el detalle directamente por URL, vuelve a `/`.
- `/pokemon/abc` o `/pokemon/0` muestran "Pokémon no encontrado" sin llamar al backend.

## 4. Comunicación con el backend

Toda llamada pasa por `services/pokemonService.js`; los componentes nunca usan `fetch` directamente.

| Función | Endpoint |
| --- | --- |
| `getPokemonList({ limit, offset, signal })` | `GET /api/pokemon` |
| `searchPokemon({ name, limit, offset, signal })` | `GET /api/pokemon/search` |
| `getPokemonByType({ type, limit, offset, signal })` | `GET /api/pokemon/type/{type}` |
| `getPokemon({ id, signal })` | `GET /api/pokemon/{id}` |
| `getTypes({ signal })` | `GET /api/types` |

- **URL base:** `import.meta.env.VITE_API_URL`, o `http://localhost:8000` si no está definida.
- **Formato:** cada función devuelve `data` cuando `success` es `true`. Si es `false`, lanza un `ApiError` con `status`, `code` y `message`.
- **Tiempo límite:** 15 segundos por petición (`AbortController`). Si se supera, se lanza `ApiError` con `code: "REQUEST_TIMEOUT"`.
- **Sin conexión:** si `fetch` falla (backend detenido, CORS, sin red), se lanza `ApiError` con `code: "NETWORK_ERROR"`.
- **Respuesta inesperada:** si la respuesta no es JSON o no tiene `success`, se lanza `ApiError` con `code: "INVALID_RESPONSE"`.
- **Cancelación:** cada función acepta un `signal`; una petición cancelada a propósito no se muestra como error.

Mensajes que ve el usuario según el `code`:

| `code` | Mensaje |
| --- | --- |
| `NETWORK_ERROR` | No se pudo conectar con el servidor. Revisa que el backend esté en ejecución e inténtalo de nuevo. |
| `REQUEST_TIMEOUT` | El servidor tardó demasiado en responder. Inténtalo de nuevo. |
| `POKEMON_NOT_FOUND` | Pokémon no encontrado. |
| `TYPE_NOT_FOUND` | Ese tipo de Pokémon no existe. |
| `VALIDATION_ERROR` | El `message` que envía el backend |
| `EXTERNAL_API_UNAVAILABLE`, `EXTERNAL_API_TIMEOUT`, `EXTERNAL_API_BAD_RESPONSE` | El servicio de Pokémon no está disponible en este momento. Inténtalo más tarde. |
| Cualquier otro | Ocurrió un error inesperado. Inténtalo de nuevo. |

El mensaje técnico (`status`, `code`, URL) se escribe en la consola del navegador para depurar, nunca en la pantalla.

## 5. Hooks

Cada hook devuelve `{ data, loading, error, retry }`.

| Hook | Uso | Se vuelve a ejecutar cuando cambia |
| --- | --- | --- |
| `usePokemonList({ q, type, page })` | Elige el endpoint: búsqueda si hay `q`, tipo si hay `type`, lista si no hay ninguno | `q`, `type`, `page` |
| `usePokemon(id)` | Detalle | `id` |
| `useTypes()` | Opciones del filtro (una vez) | — |

Cada ejecución crea un `AbortController` y la limpieza del efecto cancela la petición anterior. Si el usuario cambia de tipo tres veces seguidas (TC-010), solo se muestran los resultados del último, aunque las respuestas lleguen desordenadas.

## 6. Componentes

| Componente | Qué hace |
| --- | --- |
| `SearchBar` | Campo y botón Buscar. Busca al pulsar el botón o Enter, no mientras se escribe. Valida antes de enviar (ver abajo) y muestra el mensaje debajo del campo. Incluye un botón para limpiar la búsqueda. |
| `TypeFilter` | `<select>` con "Todos los tipos" y los tipos de `useTypes`. Si los tipos no cargan, se deshabilita sin bloquear el resto de la página. |
| `PokemonGrid` | Cuadrícula de `PokemonCard`. |
| `PokemonCard` | Imagen, nombre y número (`#025`). Toda la tarjeta es un enlace a `/pokemon/:id`. |
| `PokemonImage` | `<img>` con imagen de respaldo (ver [Imágenes](#8-imágenes)). |
| `Pagination` | Anterior, "Página X de Y" y Siguiente. Anterior se deshabilita en la página 1 y Siguiente en la última. Se oculta si todo cabe en una página. |
| `TypeBadge` | Insignia de color por tipo. |
| `StatBar` | Nombre, valor y barra proporcional (máximo 255). |
| `Loader`, `EmptyState`, `ErrorMessage` | Estados de la interfaz (sección 7). |

**Validación de la búsqueda en el cliente** (`utils/validation.js`), con las mismas reglas que el [backend](backend.md#7-validación-de-entradas): no vacío ni solo espacios, máximo 50 caracteres, solo letras, números, espacios, guiones, `.` y `'`. Así el usuario ve el mensaje sin esperar al servidor. Si el backend responde 422 de todos modos, se muestra su `message`.

**Detalle (`PokemonDetailPage`):** imagen grande, nombre, número, tipos, habilidades, estadísticas base, altura en metros (`height / 10`) y peso en kilogramos (`weight / 10`). Los nombres de PokéAPI se muestran con formato: `lightning-rod` → "Lightning Rod".

**Tamaño de página:** 20 Pokémon (constante `PAGE_SIZE`). Total de páginas = `Math.ceil(count / 20)`.

## 7. Estados de la interfaz

| Estado | Cuándo | Qué se muestra |
| --- | --- | --- |
| Cargando | Mientras hay una petición en curso | Indicador "Cargando Pokémon…" en el lugar de la cuadrícula (`role="status"`). Los controles siguen activos: una nueva búsqueda cancela la anterior. |
| Vacío | `results` es una lista vacía | "No se encontraron Pokémon" con el término o tipo buscado y un botón "Ver todos" |
| Error | La petición lanzó `ApiError` | Mensaje de la sección 4 y botón "Reintentar" (`role="alert"`). La búsqueda y el filtro siguen visibles. |
| No encontrado | Detalle con ID inexistente o ruta desconocida | "Pokémon no encontrado" / "Página no encontrada" con enlace al catálogo |

Ningún estado deja la página en blanco: el encabezado, la búsqueda y el filtro se muestran siempre.

## 8. Imágenes

`PokemonImage` muestra `public/pokemon-placeholder.svg` cuando:

- `image` es `null`, o
- la imagen no carga (evento `onError`), por ejemplo en formas alternativas sin imagen oficial o con `raw.githubusercontent.com` bloqueado (TC-014).

Otros detalles:

- `alt` con el nombre del Pokémon; la imagen de respaldo usa `alt="Imagen no disponible de <nombre>"`.
- `loading="lazy"` en las tarjetas.
- Ancho y alto fijos para que la cuadrícula no salte mientras cargan las imágenes.
- El `onError` se desactiva después de usar el respaldo, para evitar un bucle si el SVG también fallara.

## 9. Diseño responsivo y accesibilidad

- Cuadrícula con `grid-template-columns: repeat(auto-fill, minmax(150px, 1fr))`: 2 columnas en un teléfono de 375 px y 5 o 6 en escritorio.
- Margen lateral de 16 px en móvil; ancho máximo del contenido de 1200 px.
- Búsqueda y filtro uno debajo del otro en móvil y en la misma fila en escritorio.
- Botones e inputs de al menos 44 px de alto para tocarlos con el dedo.
- Sin scroll horizontal a 375 px (UI-10, TC-018); los nombres largos (`pikachu-original-cap`) se cortan con `…`.
- Todos los campos tienen `<label>` (puede ser visualmente oculto); los botones son `<button>`; el foco del teclado es visible.
- Los colores de los tipos tienen contraste suficiente con el texto de la insignia.

## 10. Pruebas con Playwright

Comando: `npx playwright test`. Playwright arranca el frontend (`npm run dev`) con `webServer`; **no hace falta tener el backend en ejecución**.

Las pruebas interceptan todas las peticiones a `/api/*` con `page.route` y responden con fixtures en `tests/fixtures/`, copiadas de respuestas reales del backend. Así las pruebas son rápidas, dan siempre el mismo resultado y pueden simular fallas que serían difíciles de provocar a mano. La integración con el backend real se comprueba en los casos manuales.

```js
// Ejemplo: UI-07, falla del backend
test('muestra un mensaje si el backend no responde', async ({ page }) => {
  await page.route('**/api/**', (route) => route.abort('connectionrefused'));

  await page.goto('/');

  await expect(page.getByRole('alert')).toContainText('No se pudo conectar con el servidor');
  await expect(page.getByRole('button', { name: 'Reintentar' })).toBeVisible();
});
```

| Archivo | Escenarios |
| --- | --- |
| `catalog.spec.js` | UI-01, UI-06, UI-08 |
| `search.spec.js` | UI-02, UI-03 |
| `filter.spec.js` | UI-04 |
| `detail.spec.js` | UI-05, UI-09 |
| `errors.spec.js` | UI-07 |
| `responsive.spec.js` | UI-10 |

UI-01 también registra todas las peticiones de la página y verifica que ninguna va a `pokeapi.co`.

**Localizadores.** Se prefieren los accesibles (`getByRole`, `getByLabel`, `getByText`). Para lo que no tiene un rol claro se usan estos `data-testid`:

| `data-testid` | Elemento |
| --- | --- |
| `pokemon-card` | Cada tarjeta del catálogo |
| `pokemon-image` | Imagen de una tarjeta o del detalle |
| `page-indicator` | Texto "Página X de Y" |
| `empty-state` | Estado vacío |
| `pokemon-detail` | Contenedor del detalle |
| `stat-<nombre>` | Barra de una estadística, por ejemplo `stat-hp` |

**Configuración (`playwright.config.js`):**

| Opción | Valor | Motivo |
| --- | --- | --- |
| `baseURL` | `http://localhost:5173` | Rutas cortas en `page.goto` |
| `webServer` | `npm run dev`, reutiliza el servidor si ya está corriendo | Arranque automático |
| `screenshot` | `only-on-failure` | Evidencia en `test-results/` |
| `trace` | `retain-on-failure` | Ver paso a paso por qué falló |
| `retries` | `0` en local, `1` en CI | Que los fallos intermitentes se noten en local |
| `reporter` | `html` y `list` | Reporte en `playwright-report/` |
| `projects` | Chromium de escritorio; UI-10 cambia el viewport a 375×667 | Un solo navegador instalado |

## 11. Comandos

```bash
cd frontend
npm install
npx playwright install chromium   # solo la primera vez

npm run dev                       # http://localhost:5173
npm run build                     # build de producción en dist/
npm run preview                   # sirve el build

npx playwright test               # pruebas de UI
npx playwright test --headed      # viendo el navegador
npx playwright test --ui          # modo interactivo
npx playwright show-report        # reporte HTML
```

Si el backend corre en otra dirección, crear `frontend/.env`:

```
VITE_API_URL=http://localhost:8000
```

## 12. Decisiones técnicas

| Decisión | Motivo | Alternativa descartada |
| --- | --- | --- |
| Estado del catálogo en la URL | Recargar y el botón Atrás funcionan; los resultados se pueden compartir | Solo `useState`: al recargar se pierde todo |
| Búsqueda y filtro excluyentes | El backend no combina búsqueda y tipo | Filtrar en el cliente la página actual, que daría resultados incompletos |
| Buscar al pulsar Buscar, no al escribir | Menos peticiones y un comportamiento fácil de probar | Búsqueda en vivo con espera (debounce) |
| Cancelar la petición anterior con `AbortController` | Evita que una respuesta lenta pise a la más reciente | Ignorar el problema o deshabilitar los controles |
| Validar la búsqueda también en el cliente | El usuario ve el error al instante; el backend sigue validando por seguridad | Validar solo en el backend |
| Página de detalle con ruta propia en vez de un modal | Se puede recargar y enlazar; más fácil de probar | Modal sobre el catálogo |
| Backend simulado en las pruebas de UI | Pruebas estables sin depender del backend ni de PokéAPI | Pruebas contra el backend real, más lentas e inestables |
| CSS propio | Pocas pantallas; sin dependencias extra | Tailwind o Material UI |
