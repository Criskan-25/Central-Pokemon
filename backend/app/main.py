from fastapi import FastAPI

from app.routes.pokemon import router as pokemon_router

app = FastAPI()

app.include_router(pokemon_router)
