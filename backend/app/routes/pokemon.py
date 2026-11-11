"""Endpoints REST relacionados con Pokémon."""

from fastapi import APIRouter

from app.schemas.pokemon import PokemonListResponse

# Agrupa las rutas de Pokémon; se registra en main.py con include_router().
router = APIRouter()


@router.get("/api/pokemon", response_model=PokemonListResponse)
def obtener_pokemon():
    """Devuelve la lista de Pokémon.

    Respuesta provisional: aún no consulta PokéAPI.
    """
    # response_model valida esta respuesta: si falta un campo
    # obligatorio (como count), FastAPI responde 500.
    return {
        "success": True,
        "data": {
            "count": 0,
            "results": []
        }
    }
