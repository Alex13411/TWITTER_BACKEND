# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import TwitterException
from app.api.v1.users import router as users_router
from app.api.v1.tweets import router as tweets_router
from app.api.v1.medias import router as medias_router
from fastapi.staticfiles import StaticFiles
app = FastAPI(
    title="Twitter Корпоративный Бэкенд",
    version="1.0.0",
    docs_url="/api/docs",  # Swagger документация будет тут
    redoc_url=None
)
app.include_router(users_router, prefix="/api", tags=["Users"])
app.include_router(tweets_router, prefix="/api", tags=["Tweets"])
app.include_router(medias_router, prefix="/api", tags=["Medias"])
app.mount("/static", StaticFiles(directory="static"), name="static")
# Глобальный обработчик для наших кастомных ошибок (формат по ТЗ)
@app.exception_handler(TwitterException)
async def twitter_exception_handler(request: Request, exc: TwitterException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "result": False,
            "error_type": exc.error_type,
            "error_message": exc.error_message
        }
    )

# Глобальный обработчик для всех остальных непредвиденных ошибок Python
@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "result": False,
            "error_type": "ServerError",
            "error_message": f"Внутренняя ошибка сервера: {str(exc)}"
        }
    )

# Тестовый эндпоинт проверки работоспособности
@app.get("/api/health")
async def health_check():
    return {"status": "working", "result": True}