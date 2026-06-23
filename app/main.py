# app/main.py
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.medias import router as medias_router
from app.api.v1.tweets import router as tweets_router
from app.api.v1.users import router as users_router
from app.core.exceptions import TwitterException

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app = FastAPI(
    title="Twitter Корпоративный Бэкенд",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url=None,
)

app.include_router(users_router, prefix="/api", tags=["Users"])
app.include_router(tweets_router, prefix="/api", tags=["Tweets"])
app.include_router(medias_router, prefix="/api", tags=["Medias"])


@app.exception_handler(TwitterException)
async def twitter_exception_handler(request: Request, exc: TwitterException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "result": False,
            "error_type": exc.error_type,
            "error_message": exc.error_message,
        },
    )


@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "result": False,
            "error_type": "ServerError",
            "error_message": f"Внутренняя ошибка сервера: {str(exc)}",
        },
    )


@app.get("/api/health")
async def health_check():
    return {"status": "working", "result": True}


# Загруженные картинки: /static/uploads/...
app.mount("/static", StaticFiles(directory="static"), name="uploads")

# Vue SPA: /login, /profile/... и все маршруты → index.html
if FRONTEND_DIR.is_dir():

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_frontend(full_path: str = ""):
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404)

        if full_path:
            asset = FRONTEND_DIR / full_path
            if asset.is_file():
                return FileResponse(asset)

        index = FRONTEND_DIR / "index.html"
        if not index.is_file():
            raise HTTPException(status_code=404, detail="Frontend not found")
        return FileResponse(index)
