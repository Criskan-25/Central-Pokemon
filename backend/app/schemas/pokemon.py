"""Modelos Pydantic que definen el formato de las respuestas de la API."""

from pydantic import BaseModel


class PokemonListItem(BaseModel):
    """Un Pokémon dentro de la lista."""

    id: int
    name: str
    # Opcional: algunas formas alternativas no tienen imagen oficial.
    image: str | None = None


class PokemonListData(BaseModel):
    """Contenido de 'data' en la respuesta de la lista."""

    count: int  # Total de Pokémon disponibles, no solo los de esta página.
    results: list[PokemonListItem]


class PokemonListResponse(BaseModel):
    """Respuesta completa de GET /api/pokemon."""

    success: bool = True
    data: PokemonListData
