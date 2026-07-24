import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.tickets import router as tickets_router
from app.api.ai import router as ai_router
from app.core.config import settings
from app.core.database import engine, Base, get_db
from app.core.exceptions import ClosedTicketError, TicketNotFoundError


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    lifespan=lifespan,
)


# ----- Routes -----


@app.get("/")
def home():
    return {"message": settings.APP_NAME}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
async def ready(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready", "database": "disconnected"},
        )


# Include routers
app.include_router(tickets_router)
app.include_router(ai_router)