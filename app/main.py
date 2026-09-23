from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="OpenBlueprint", version="0.2.0",
              description="Local-first AI engineering and design platform.")
app.include_router(router)
