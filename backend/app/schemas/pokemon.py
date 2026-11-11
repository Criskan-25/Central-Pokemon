from pydantic import BaseModel


class PokemonListItem(BaseModel):
    id: int
    name: str
    image: str | None = None


class PokemonListData(BaseModel):
    count: int
    results: list[PokemonListItem]


class PokemonListResponse(BaseModel):
    success: bool = True
    data: PokemonListData
    