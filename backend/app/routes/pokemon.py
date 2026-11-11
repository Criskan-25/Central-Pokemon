from fastapi import APIRouter

from app.schemas.pokemon import PokemonListResponse

router = APIRouter()


@router.get("/api/pokemon", response_model=PokemonListResponse)
def obtener_pokemon():
    return {
        "success": True,
        "data": {
            "count": 0,
            "results": [] 
            }
    }
