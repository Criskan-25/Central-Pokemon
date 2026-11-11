from fastapi import APIRouter

router = APIRouter()


@router.get("/api/pokemon")
def obtener_pokemon():
    return {
        "success": True,
        "data": {
            "results": []
        }
    }
