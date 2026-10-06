from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import STATIC_DIR, settings
from .routes import router


app = FastAPI(
    title="ComicCraft AI",
    description="AI Comic Story Creator",
    version=settings.app_version,
)


app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)


app.include_router(router)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
    }