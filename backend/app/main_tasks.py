from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.database import close_database
from app.routes.tasks import router as tasks_router
from app.utils.errors import register_exception_handlers


settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    await close_database()


app = FastAPI(title=f"{settings.app_name} - Tasks Service", lifespan=lifespan)
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def healthcheck():
    return {"status": "ok", "service": "tasks"}
