import time

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

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
)

# ----- CORS Middleware -----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins - change this in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# ----- Middleware: X-Response-Time -----


@app.middleware("http")
async def add_response_time_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = int((time.perf_counter() - start) * 1000)
    response.headers["X-Response-Time"] = f"{elapsed_ms}ms"
    return response


# ----- Exception handlers -----


@app.exception_handler(TicketNotFoundError)
async def ticket_not_found_handler(request: Request, exc: TicketNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": "ticket_not_found", "id": exc.ticket_id},
    )


@app.exception_handler(ClosedTicketError)
async def closed_ticket_handler(request: Request, exc: ClosedTicketError):
    return JSONResponse(
        status_code=409,
        content={"error": "closed_ticket", "id": exc.ticket_id},
    )


# ----- Startup -----


@app.on_event("startup")
async def startup_event() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


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